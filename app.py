#Dado un CSV con un listado de URL de imágenes, devuelve su peso, ancho y alto
import streamlit as st
import time 
import os
from PIL import Image
import urllib.request
import pandas as pd
import os
import ssl
#Para que no haya problemas al descargar las imágenes
ssl._create_default_https_context = ssl._create_unverified_context

#Obtiene el nombre de la imagen de la URL
def getNombreImagen(url):
    nombre=url[url.rfind("/")+1:len(url)]
    index = nombre.find("?")
    if index >0:
        nombre=nombre[:index]
    return nombre

#Elimina el fichero pasado como parámetro
def eliminaFichero(myfile):
    if os.path.isfile(myfile):
        os.remove(myfile)

#Devuelve el peso en KB de las imagen
def getPesoKB(img_name):
    pesoKB=0
    file_size = os.path.getsize(img_name)
    if file_size:
        pesoKB=round(file_size/1024,2)
    return pesoKB


csv=st.file_uploader('CSV con imágenes a analizar', type='csv')
if csv is not None:
    dict={}
    df_entrada=pd.read_csv(csv,header=None)
    st.write(df_entrada)
    addresses = df_entrada[0].tolist()
    dct_arr=[]
    for row in addresses:
        url=row
        try:
            dict={}
            #Obtenemos la imagen
            data_headers ={"User-Agent":"Mozilla/5.0"}
            nombre=getNombreImagen(url) 
            urllib.request.urlretrieve(url,nombre)
            st.success("Imagen descargada: "+url)
            im=Image.open(nombre)
            #Obtenemos el ancho y el alto
            width, height = im.size
            #Obtenemos su peso
            peso=getPesoKB(nombre)
            im.close()
            #Eliminamos el fichero de la imagen
            eliminaFichero(nombre)
            dict["url"]=url
            dict["nombre"]=nombre
            dict["pesoKB"]=peso
            dict["width"]=width
            dict["height"]=height
            dct_arr.append(dict)
        except  Exception as e:
            dict={}
            dict["url"]=url 
            dct_arr.append(dict)
            st.warning("Error al procesar la imagen: "+url)
            
        time.sleep(0.5)
    df = pd.DataFrame(dct_arr)
    st.write(df)
    st.download_button(
        label="Descargar como CSV",
        data=df.to_csv(index=False, decimal=",",quotechar='"').encode('utf-8'),
        file_name='imagenes.csv',
        mime='text/csv'
        )
        
