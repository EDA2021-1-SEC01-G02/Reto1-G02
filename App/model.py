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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.DataStructures.arraylist import addLast, defaultfunction, getElement
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort as sa
import pandas as pd
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():

    catalog = {
        "artworks" : None,
        "artists" : None,
    }
    catalog['artworks'] =  lt.newList()
    catalog['artists'] = lt.newList('ARRAY_LIST',
                                    cmpfunction=compareartists)
    return catalog

def artistsInfo():
    artists_info = lt.newList('ARRAY_LIST',
                cmpfunction=None)
    return artists_info

def newList(type, cmpfun):
    newList = lt.newList(type, cmpfunction=cmpfun)
    return newList

# Funciones para agregar informacion al catalogo

def addArtWork(catalog, artwork):
    lt.addLast(catalog['artworks'], artwork)
    artists = artwork['ConstituentID'].split(',')
    artworktitle = artwork['Title']

    for artist in artists:
        addArtWorkArtist(catalog, artist.strip() , artworktitle)
    

def addArtWorkArtist(catalog, artistname, artwork):

    artists = catalog['artists']
    posArtist = lt.isPresent(artists, artistname)
    if posArtist > 0:
        artist = lt.getElement(artists, posArtist)
    else:
        artist = newArtist(artistname)
        lt.addLast(artists, artist)
    artistname = artist['name']

    lt.addLast(artist['artworks'], artwork)

def addArtistsInfo(artists_info, info):
    var =  lt.isEmpty(artists_info)
    if var == True:
        lt.addFirst(artists_info, info)
    else:
        lt.addLast(artists_info, info)
    
def addConstituentID(consList, size, artworks):
    for ind in range(1,size):
        item = lt.getElement(artworks, ind)
        constituentID = item['ConstituentID'].split(',')
        for i in constituentID:
            i = i.strip('[').strip(']').strip()
            lt.addLast(consList, i)

# Funciones para creacion de datos

def newArtist(name):

    artist = {
        'name' : "",
        'artworks' : None,
        'info' : None,
            }
    artist['name'] = name
    artist['artworks'] = lt.newList('ARRAY_LIST')
    artist['info'] = 'x'
    return artist


# Funciones de consulta
def getNatInfo(artists_info, artistsInfo):
    natList = {

    }
    size = artists_info['size'] + 1
    for artist in artistsInfo:
        id =  artist 

        for pos in range(1,size):
            temp = lt.getElement(artists_info, pos)
            if id == temp['ConstituentID'].strip():
                nat = temp['Nationality'].lower()
                if nat == '' or nat == 'nationality unknown':
                    continue
                if nat not in natList:
                    natList[nat] = [1]
                    natList[nat].append([])
                    natList[nat][1].append(artist)
                else:
                    natList[nat][0] += 1
                    natList[nat][1].append(artist)
    return natList

def getArtworksbyArtists(artists, artworks, artists_info):
    artworksByAr = newList('ARRAY_LIST', None)

    for artist in artists:
        size = lt.size(artworks) + 1
        for pos in range(1,size):
            artwork = lt.getElement(artworks, pos)
            elements = artwork['ConstituentID'].split(',')
            codes = artwork['ConstituentID'].split(',')
            id = getArtistbyConID(codes, artists_info)
            for key in id:
                artistsNames = id[key] + ', '
            info = [artwork['ObjectID'],artwork['Title'],artistsNames,artwork['Date'],artwork['Medium'],artwork['Dimensions']]
            if lt.isPresent(artworksByAr,info):
                continue
            for item in elements:
                elem = item.strip().strip('[').strip(']')
                if artist == elem:
                    if lt.isPresent(artworksByAr, info) == 0:
                        lt.addLast(artworksByAr,info)
                        break
                            
    a = pd.DataFrame(artworksByAr['elements'], columns=['ObjectId', 'Title','Artists', 'Date', 'Medium', 'Dimensions'])
    print(a)


def getArtistbyConID(codes, artists_info):
    names = {

    }
    size = 1 + lt.size(artists_info)
    for code in codes:
        code2 =  code.strip().strip('[').strip(']')
        if code2 not in names:
            for pos in range(1,size):
                data = lt.getElement(artists_info,pos)
                code3 = data['ConstituentID'].strip().strip('[').strip(']')
                if code2 == code3 and code3 not in names:
                    names[code2] = data['DisplayName']
                    break
    return names
                    



# Funciones utilizadas para comparar elementos dentro de una lista

def compareartists(artistname1, artist):
    if (artistname1.lower() in artist['name'].lower()):
        return 0
    return -1
    return None

def compareCont(item1, item2):
    if item1[0] > item2[0]:
        return True
    else:
        return False

# Funciones de ordenamiento
def sortNat(consIDs):
    natSort = newList('ARRAY_LIST', None)

    for id in consIDs:
        cont = consIDs[id][0]
        nationality = id
        newValue = [cont, nationality]
        lt.addLast(natSort, newValue)
    
    quickSort(natSort, compareCont)
    lessEl = lt.subList(natSort,1,10)
    print('Nationality' + '       '+ 'Artworks')
    for nat in lessEl['elements']:
        space = 25 - len(nat[1]) - len(str(nat[0]))
        print(nat[1].capitalize(), space * " " , nat[0])
    great = lt.firstElement(lessEl)
    print('La nacionalidad con mas obras es %s con %s obras.' %(great[1].capitalize(),great[0]))
    return great[1]

def partition(lst, lo, hi, lessequalfunction):
    follower = leader = lo
    while leader < hi:
        if(lessequalfunction( lt.getElement(lst, leader), lt.getElement(lst, hi))):
            lt.exchange(lst,follower,leader)
            follower += 1
        leader += 1
    lt.exchange(lst, follower, hi)
    return follower

def sort( lst, lo, hi, lessequalfunction):
    if (lo >= hi ) :
        return
    pivot = partition(lst,lo, hi, lessequalfunction)
    sort(lst, lo, pivot-1, lessequalfunction)
    sort(lst, pivot+1, hi, lessequalfunction)

def quickSort(lst, lessequalfunction):
    sort(lst,1,lt.size(lst), lessequalfunction)