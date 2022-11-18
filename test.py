

import time 
from PIL import Image
import pandas as pd
from urllib.request import Request, urlopen
from io import BytesIO
import ssl
#Para que no haya problemas al descargar las imágenes
ssl._create_default_https_context = ssl._create_unverified_context

f_entrada='lista.csv'
f_salida="salida.csv"

#Obtiene el nombre de la imagen de la URL
def getNombreImagen(url):
    nombre=url[url.rfind("/")+1:len(url)]
    index = nombre.find("?")
    if index >0:
        nombre=nombre[:index]
    return nombre

def getPesoKB(bytes):
    pesoKB=0
    pesoKB=round(len(bytes)/1024,2)
    return pesoKB

df=pd.read_csv(f_entrada,header=None)
addresses = df[0].tolist()
dct_arr=[]

for row in addresses:
    url=row
    try:
        dict={}
        #Obtenemos la imagen
        nombre=getNombreImagen(url) 
        request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        bytes = urlopen(request_site).read()
        im = Image.open(BytesIO(bytes))  
        #Obtenemos el ancho y el alto
        width, height = im.size
        #Obtenemos su peso
        peso=getPesoKB(bytes)
        im.close()
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
            print(str(e)+" - "+url)           
    time.sleep(0.5)
df = pd.DataFrame(dct_arr)
df.to_csv(f_salida, index=False, decimal=",",quotechar='"')
print("fin")

