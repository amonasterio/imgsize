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
import logging
logging.basicConfig(filename='test.log')

MAX_URL=1000

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

def eliminaDuplicadosLista(lista):
    if len(lista)>0:
        lista=list(dict.fromkeys(lista))
    return lista

st.set_page_config(
   page_title="Obtener peso, alto y ancho de un listado de URL de imágenes",
   layout="wide"
)
st.title("Obtener peso, alto y ancho de un listado de URL de imágenes")
st.markdown("Dada una lista de URL de URL de imágenes, devuelve su peso (KB), ancho y alto. **Máximo "+str(MAX_URL)+" imágenes**", unsafe_allow_html=False)
lista_url=st.text_area("Introduzca las URL de imágenes que desea analizar o cárguelas en un CSV",'')
csv=st.file_uploader('CSV con imágenes a analizar', type='csv')
addresses=[]

#Si no hay CSV miramos el textArea
if csv is  None:
    if len(lista_url)>0:
        addresses=lista_url.split('\n')
else: 
    df_entrada=pd.read_csv(csv,header=None)
    st.write(df_entrada)
    addresses = df_entrada[0].tolist()
if len(addresses)>0:
    dict={}
    dct_arr=[]
    #Eliminamos posibles duplicados
    lista_img=eliminaDuplicadosLista(addresses)
    total_count=0
    bar = st.progress(0.0)
    longitud=len(lista_img)
    if longitud <= MAX_URL:
        for row in lista_img:
            url=row
            try:
                total_count+=1
                percent_complete=total_count/longitud
                bar.progress(percent_complete)
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
                logging.info(str(total_count)+": Imagen procesada: "+url)
                dict["url"]=url
                dict["nombre"]=nombre
                dict["pesoKB"]=peso
                dict["width"]=width
                dict["height"]=height
                dct_arr.append(dict)
            except  Exception as e:
                logging.error(str(total_count)+": Error procesando imagen: "+url)  
                dict={}
                dict["url"]=url 
                dct_arr.append(dict)
                if e.args is not None:
                    st.warning(str(e)+" - "+url)  
                    logging.error(str(e)+" - "+url)         
            time.sleep(0.2)
        df = pd.DataFrame(dct_arr)
        st.write(df)
        st.download_button(
            label="Descargar como CSV",
            data=df.to_csv(index=False, decimal=",",quotechar='"').encode('utf-8'),
            file_name='imagenes.csv',
            mime='text/csv'
            )
    #Hay más de MAX_URL URL
    else:
        st.warning("Hay "+str(longitud)+ " URL únicas. El número máximo de URL a procesar son "+str(MAX_URL))
else:
    st.warning("No ha introducido ninguna URL")      
