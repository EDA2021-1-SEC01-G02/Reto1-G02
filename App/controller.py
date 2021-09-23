"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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

from DISClib.DataStructures.arraylist import defaultfunction, firstElement
import config as cf
from DISClib.ADT import list as lt
import model
import csv
import time #TODO BORRAR


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    catalog = model.newCatalog()
    return catalog

def artistsInfo():
    artists_info = model.artistsInfo()
    return artists_info

# Funciones para la carga de datos
def loadData(catalog, artists_info):
    loadArtistsinfo(artists_info)
    loadArtWorks(catalog)
   

def loadArtWorks(catalog):
    artworksfile = cf.data_dir + 'MoMA/Artworks-utf8-small.csv'
    input_file = csv.DictReader(open(artworksfile, encoding = 'utf-8'))
    for artwork in input_file:
        model.addArtWork(catalog, artwork)

def loadArtistsinfo(artists_info):
    artistsfile = cf.data_dir + 'MoMA/Artists-utf8-small.csv'
    input_file =  csv.DictReader(open(artistsfile, encoding= 'utf-8'))
    
    for info in input_file:
        model.addArtistsInfo(artists_info, info)
    


# Funciones de ordenamiento

def sortArtistByDate(artists_info, year1, year2):
    start_time = time.process_time()

    sortedArtists = (model.sortArtistByDate(artists_info))
    model.getYearRange(sortedArtists, year1, year2)

    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print(elapsed_time_mseg)

def sortByDate(artworks, date1, date2, artists_info):
    start_time = time.process_time()

    model.sortByDate(artworks)
    range = lt.lastElement(artworks)['DateAcquired']
    while model.cmpDateAdquired(date1,range) == False :
        if date1 <= range:
            break
        print('Ingrese una fecha de inicio valida en el formato aaaa-mm-dd (Menor a %s)' %(range))
        date1 = input('--  ').strip()

    while model.cmpDateAdquired(date2,range) == False :
        if date2 <= range:
            break
        print('Ingrese una fecha final valida en el formato aaaa-mm-dd (Menor a %s)' %(range))
        date2 = input('--  ').strip()
    

    artworksByDate = model.getArtworksByDate(artworks,date1,date2)

    model.getSixArtworks(artworksByDate, artists_info)    

    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print(elapsed_time_mseg)
    

# Funciones de consulta sobre el catálogo
def artistsTecnique (artworks,artist_info,artist):
    start_time = time.process_time()

    artistID = int(model.getArtistID(artist,artist_info))
    model.getArtworksByArtistsTechnique(artist,artistID,artworks)

    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print(elapsed_time_mseg)
    

def ObrasPorNacionalidad(artworks, artist_info):
    start_time = time.process_time()

    consIDs =  model.newList('ARRAY_LIST', None)
    size = artworks['size'] + 1

    model.addConstituentID(consIDs, size, artworks)
    natList = model.getNatInfo(artist_info, consIDs)
    firstEl = model.sortNat(natList)
    model.getArtworksbyArtists(natList[firstEl][1], artworks, artist_info, firstEl)

    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print(elapsed_time_mseg)

def precioTransporte(artworks,artists,dep):
    start_time = time.process_time()

    depArtworks = model.getDepArtworks(artworks,dep)
    prices = model.calculatePrice(depArtworks,artists)
    model.showPrice(prices[0],prices[1],prices[2],dep)

    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print(elapsed_time_mseg)