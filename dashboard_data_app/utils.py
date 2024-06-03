import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import pandas as pd
import seaborn as sns 
from io import BytesIO 
import base64 

def get_image(): 
    # create a bytes buffer for the image to save 
    buffer = BytesIO() 
    # create the plot with the use of BytesIO object as its 'file' 
    plt.savefig(buffer, format='png') 
    # set the cursor the begining of the stream 
    buffer.seek(0) 
    # retreive the entire content of the 'file' 
    image_png = buffer.getvalue() 

    graph = base64.b64encode(image_png) 
    graph = graph.decode('utf-8') 

    # free the memory of the buffer  
    buffer.close() 
    return graph


def barplot(df):
    plt.clf()

    df['date'] = pd.to_datetime(df['date']).dt.date

    # Agréger les données pour obtenir le prix total par jour
    df = df.groupby('date').agg({'total_price': 'sum'}).reset_index()

    # Tracer le graphique à l'aide de Seaborn
    # plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='date', y='total_price')
    plt.title('Total Price per Day (bar)')
    plt.xticks(rotation=45,ha='right')
    plt.tight_layout()

    return get_image()

def lineplot(df):
    plt.clf()

    df['date'] = pd.to_datetime(df['date']).dt.date

    # Agréger les données pour obtenir le prix total par jour
    df = df.groupby('date').agg({'total_price': 'sum'}).reset_index()

    # Tracer le graphique à l'aide de Seaborn
    # plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='date', y='total_price')
    plt.title('Total Price per Day (line)')
    plt.xticks(rotation=45,ha='right')
    plt.tight_layout()

    return get_image()

def countplot(df):
    plt.clf()

    # df = pd.DataFrame(df["product"])
    sns.countplot(df,x="product")
    plt.title('Product count')
    plt.xticks(rotation=45,ha='right')
    plt.tight_layout()

    return get_image()