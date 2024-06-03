import csv
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
import pandas as pd
from .forms import LoginForm, UploadFileForm, AddSalesForm, PerformanceForm
from .models import Product, Sale
from .utils import barplot, countplot, lineplot

# Create your views here.

def home_view(request):
    return render(request,'home.html',{})

def login_view(request):

    if (request.method == "POST"):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def upload_file_fiew(request):
    file_uploaded = False

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']

            # Lire le fichier CSV et remplir la table SQLite
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file, delimiter=";")
            for row in reader:
                product = row[0]
                if not Product.objects.filter(name=product).exists():
                    product = Product(name = product)
                    product.save()

                sale = Sale(
                    product = Product.objects.get(name=product),
                    price = int(row[2]),
                    quantity = int(row[1]),
                    seller = request.user,
                    date = row[4],
                )
                sale.save()
                # Créer une nouvelle instance du modèle et la sauvegarder
            file_uploaded = True
    else:
        form = UploadFileForm()

    return render(request, 'upload_file.html', {'form': form, 'file_uploaded' : file_uploaded})


def add_sales_view(request):
    sales_added = False

    if request.method == 'POST':
        form = AddSalesForm(request.POST)
        if form.is_valid():
            sale = Sale(
                product = form.cleaned_data["product"],
                price = int(form.cleaned_data["price"]),
                quantity = int(form.cleaned_data["quantity"]),
                seller = request.user,
                date = datetime.now()
            )
            sale.save()
            sales_added = True
    else:
        form = AddSalesForm()

    return render(request, 'add_sales.html', {'form': form, 'sales_added' : sales_added})


def performance_view(request):
    if request.method == 'POST':
        form = PerformanceForm(request.POST)
        if form.is_valid():
            chart_type = form.cleaned_data['chart_type']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            
            if date_from is not None and date_to is not None:
                sales = Sale.objects.filter(date__gte=date_from).filter(date__lte = date_to)
            else:
                sales = Sale.objects.all()

            df = pd.DataFrame(
                [{
                    'product' : sale.product,
                    'price': sale.price,
                    'quantity': sale.quantity,
                    'total_price': sale.total_price,
                    'date': sale.date
                }for sale in sales]
            )

            if request.POST.get('action') == 'Show_chart':
                if chart_type == "bar":
                    graph = barplot(df)
                elif chart_type == "line":
                    graph = lineplot(df)
                elif chart_type == "count":
                    graph = countplot(df)
                return render(request, 'performance.html', {'form': form, 'graph': graph})
            
            elif request.POST.get('action') == 'summary':
                stats = {
                    "count" : df['price'].count(),
                    "mean" : df['price'].mean(),
                    "median" : df['price'].median(),
                    "min" : df['price'].min(),
                    "max" : df['price'].max(),
                    "std_dev" : df['price'].std()
                }
                return render(request, 'performance.html', {'form': form,'stats': stats})

    form = PerformanceForm()

    return render(request, 'performance.html', {'form': form})

