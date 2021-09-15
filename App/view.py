"""
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
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar los top x ")
    print("3- Consultar los top x ")
    print("4- Consultar los top x ")
    print("5- Clasificar las obras por la nacionalidad de sus creadores")

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
        num_artists = lt.size(artists_info)
        print('Artworks cargados: ' + str(num_artworks))
        print('Artistas cargados: ' + str(num_artists))
        print("Ultimos Artworks cargados:")
        for i in range(0,3):
            print(i+1,". ",(lt.getElement(catalog["artworks"],num_artworks-i)["Title"]))
        print("--------------------------------------------------------------")
        print("Ultimos artistas cargados: ")
        for i in range(0,3):
            print(i+1,". ",lt.getElement(artists_info,num_artists-i)["DisplayName"])


    elif int(inputs[0]) == 2:
        print(lt.firstElement(artists_info))

        

    elif int(inputs[0]) == 3:
        pass
    elif int(inputs[0]) == 4:
        pass
    elif int(inputs[0]) == 5:
        artworks = catalog['artworks']
        controller.ObrasPorNacionalidad(artworks, artists_info)
        
        pass

    else:
        sys.exit(0)
sys.exit(0)
