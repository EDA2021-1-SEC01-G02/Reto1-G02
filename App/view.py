﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido:")
    print("1- Cargar información en el catálogo.")
    print("2- listar cronológicamente los artistas.")
    print("3- Listar cronológicamente las adquisiciones.")
    print("4- Consultar artista por medio / tecnica.")
    print("5- Clasificar las obras por la nacionalidad de sus creadores.")
    print("6- Consultar costo para transportar obras de un departamento.")

def initCatalog():

    return controller.initCatalog()

def loadData(catalog, artists_info):
    
    controller.loadData(catalog, artists_info)
    
def printArtistData(artist):
    print('Artista encontrado: ' + artist['name'])

def artistsInfo():
    return controller.artistsInfo()

catalog = None
artists_info = None
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        artists_info = artistsInfo()
        loadData(catalog, artists_info)
        num_artworks = lt.size(catalog['artworks'])
        num_artists = len(lt.getElement(artists_info,1))
        print('Artworks cargados: ' + str(num_artworks))
        print('Artistas cargados: ' + str(num_artists))
        print("Ultimos Artworks cargados:")

    elif int(inputs[0]) == 2:
        year1 = int(input("Digite el AÑO INICIAL: "))
        year2 = int(input("Ahora digite el AÑO FINAL: "))
        controller.sortArtistByDate(artists_info, year1, year2)

    elif int(inputs[0]) == 3:
        print('Ingrese la fecha de inicio en el formato aaaa-mm-dd')
        date1 = input('--  ').strip()
        print('Ingrese la fecha final en el formato aaaa-mm-dd' )
        date2 = input( '--  ').strip()  
        data_artists = lt.firstElement(artists_info)
        controller.sortByDate(catalog['artworks'], date1,date2, artists_info)

    elif int(inputs[0]) == 4:
        print("Importante!!! - Se recomienda que disminuya el zoom en la consola para que se puedan ver todos los datos")
        name = input("Digite el nombre del artista a buscar: ")
        controller.artistsTecnique(catalog["artworks"],artists_info,name)
        
    elif int(inputs[0]) == 5:
        artworks = catalog['artworks']
        controller.ObrasPorNacionalidad(artworks, artists_info)

    elif int(inputs[0]) == 6:
        dep = input("Digite el departamento al cual se realizara la consulta: ")
        controller.precioTransporte(catalog["artworks"],artists_info,dep)

    else:
        sys.exit(0)
sys.exit(0)