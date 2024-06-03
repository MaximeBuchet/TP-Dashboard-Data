from django.urls import path
from .views import home_view, login_view, logout_view, upload_file_fiew,add_sales_view, performance_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('upload', upload_file_fiew, name='upload_file' ),
    path('addsales',add_sales_view, name='add_sales'),
    path('performance', performance_view, name="performance")
]

