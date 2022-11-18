#Dado un CSV con un listado de URL de imágenes, devuelve su peso, ancho y alto
import streamlit as st
import time 
from PIL import Image
import pandas as pd
from urllib.request import Request, urlopen
from io import BytesIO
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

#Devuelve el peso en KB
def getPesoKB(bytes):
    pesoKB=0
    pesoKB=round(len(bytes)/1024,2)
    return pesoKB

st.set_page_config(
   page_title="Obtener peso, alto y ancho de un listado de URL de imágenes",
   layout="wide"
)
st.title("Obtener peso, alto y ancho de un listado de URL de imágenes")
st.text("Dado un CSV con un listado de URL de imágenes, devuelve su peso (KB), ancho y alto")
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
            nombre=getNombreImagen(url) 
            request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            #Leemos la URL pero asignamos un timeout para que no se quede procesando demasiado tiempo.
            #Hay dominios como https://eimv3-statics.yves-rocher.com/ que dejan la petición corriendo sin límite
            bytes = urlopen(request_site,timeout=6).read()
            im = Image.open(BytesIO(bytes))  
            #Obtenemos el ancho y el alto
            width, height = im.size
            #Obtenemos su peso
            peso=getPesoKB(bytes)
            im.close()
            st.success("Imagen procesada: "+url)
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
            if e.args is not None:
                st.warning(str(e)+" - "+url)           
        time.sleep(0.5)
    df = pd.DataFrame(dct_arr)
    st.write(df)
    st.download_button(
        label="Descargar como CSV",
        data=df.to_csv(index=False, decimal=",",quotechar='"').encode('utf-8'),
        file_name='imagenes.csv',
        mime='text/csv'
        )
        
