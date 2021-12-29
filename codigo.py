#### REQUIREMENTS: pip install hilbertcurve - colormap - pillow - math - pandas - numpy

D = 2 #Dimensión curva de hilbert
from hilbertcurve.hilbertcurve import HilbertCurve
from colormap import rgb2hex
from PIL import Image
from PIL import ImageColor
import math
import pandas as pd
import numpy as np

Lenna2 = Image.open("Lenna2.png") #1
Lenna4 = Image.open("Lenna4.png") #2
Lenna8 = Image.open("Lenna8.png") #3 
Lenna16 = Image.open("Lenna16.png") #4
Lenna32 = Image.open("Lenna32.png") #5
Lenna64 = Image.open("Lenna64.png") #6
Lenna128 = Image.open("Lenna128.png") #7
Lenna256 = Image.open("Lenna256.png") #8
Lenna512 = Image.open("Lenna512.png") #9
Lenna1024 = Image.open("Lenna1024.jpg") #10
#####Lenna2048 = Image.open("Lenna2048.jpg") #11
#####Lenna4096 = Image.open("Lenna4096.jpg") #12
Imagenes = {2:Lenna2, 4:Lenna4, 8:Lenna8, 16:Lenna16, 32:Lenna32, 64:Lenna64, 128:Lenna128, 
            256:Lenna256, 512:Lenna512, 1024:Lenna1024}

print("\n"*5)
tamanos = [f'{2**n}x{2**n}' for n in range(1,10+1)]

################################################################
def print_menu():
    print("Presione 1 para seleccionar el tamaño de la imagen")
    print("Presione 2 para decodificar un texto en su respectiva imagen")

def main():
    print_menu()
    Input  = int(input(""))
    if Input==1:
        print("Seleccione uno entre los siguientes: ")
        print(tamanos)
        tamano = input("")
        tamano = int(tamano.split("x")[0])
        n = int(math.log(tamano,2)) #Aproximación enesima de la curva de Hilbert
        Imagen = Imagenes[tamano]
        Imagen = Imagen.convert("RGB")

        hilbert_curve = HilbertCurve(n, D)
        distances = list(range(2**n * 2**n))
        points = hilbert_curve.points_from_distances(distances)
        listaDeColores = []
        for point, dist in zip(points, distances):
            rgb = Imagen.getpixel(tuple(point))
            hexa = rgb2hex(*rgb)
            listaDeColores.append((dist,point,hexa))
        listaFinal = []
        for i in listaDeColores:
            for _ in range(int(4**10/(2**n * 2**n))):
                listaFinal.append(i[2])

        
        textfile = open("imagenes.csv", "a")
        textfile.write(str(tamano)+"x"+str(tamano)+",")
        for element in listaFinal:
            textfile.write(element + ",")
        textfile.write("\n")
        textfile.close()

    elif Input==2: 
        n = 10
        hilbert_curve = HilbertCurve(n, D)
        distances = list(range(2**n * 2**n))
        points = hilbert_curve.points_from_distances(distances)

        matriz = [[0 for x in range(1024)] for y in range(1024)]

        print("Seleccione uno entre los siguientes: ")
        print(tamanos)
        tamano = input("")
        
        df = pd.read_csv("imagenesT.csv",dtype=str)
        saved_column = df[tamano]
        for point, dist, color in zip(points, distances, saved_column):
            matriz[point[1]][point[0]] = ImageColor.getcolor(color, "RGB")

        array = np.array(matriz, dtype=np.uint8)
        new_image = Image.fromarray(array)
        new_image.save("Lenna"+tamano.split("x")[0]+"D"+".png")

main()