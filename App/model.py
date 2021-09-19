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


from App.controller import artistsTecnique
from DISClib.DataStructures.arraylist import addLast, defaultfunction, firstElement, getElement
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import mergesort as me
from DISClib.Algorithms.Sorting import quicksort as qu
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
    catalog['artworks'] =  lt.newList('ARRAY_LIST', None)
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
        dict ={ info['ConstituentID'] :info

        }
        lt.addFirst(artists_info, dict)

    else:
        data = lt.getElement(artists_info, 1)
        data[info['ConstituentID']] = info
     
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

def sublist(lst,pos,numelement):
    return lt.sublist(lst,pos,numelement)


def subListByDate(lst,date1,date2):
    size = 1 + lt.size(lst)
    dateStart = {'DateAcquired' : date1}
    dateEnd = {'DateAcquired' : date2}
    for i in range(1, size):
        if cmpArtworkByDateAdquired(dateStart, lt.getElement(lst,i)) == True:
            pos1 = i - 1
           
            break
    for i in range(pos1, size):
        if cmpArtworkByDateAdquired(dateEnd, lt.getElement(lst,i)) == True:
            pos2 = i - 1
           
            break
    numelement = pos2 - pos1
    
    a= lt.subList(lst, pos1, numelement)




# Funciones de consulta
def getNatInfo(artists_info, artistsInfo):
    natList = {

    }
    size = lt.size(artistsInfo) +1
    dict = lt.firstElement(artists_info)
    for pos in range(1,size):
        temp = lt.getElement(artistsInfo,pos)
        dict = lt.firstElement(artists_info)
        data = dict[temp]
        nat = data['Nationality'].lower()
        if nat == '' or nat == 'nationality unknown':
            continue
        if nat not in natList:
            natList[nat] = [1]
            natList[nat].append([])
            natList[nat][1].append(temp)
        else:
            natList[nat][0] += 1
            natList[nat][1].append(temp)
    return natList

def getArtworksbyArtists(artists, artworks, artists_info):
    artworksByAr = newList('ARRAY_LIST', None)

    for artist in artists:
        size = lt.size(artworks) + 1
        for pos in range(1,size):
            artwork = lt.getElement(artworks, pos)
            codes = artwork['ConstituentID'].split(',')
            if contOrNot(artist,codes) == True:
                continue
            id = getArtistbyConID(codes, artists_info)
            artistsNames = ''
            for key in id:
                artistsNames += str(id[key] + ', ')
            info = [artwork['ObjectID'],artwork['Title'],artistsNames,artwork['Date'],artwork['Medium'],artwork['Dimensions']]
            if lt.isPresent(artworksByAr,info) != 0:
                continue
            for item in codes:
                elem = item.strip().strip('[').strip(']')
                if artist == elem:
                    
                    lt.addLast(artworksByAr,info)
                    break
    me.sort(artworksByAr,compareTitle)
    a = pd.DataFrame(artworksByAr['elements'], columns=['ObjectId', 'Title','Artists', 'Date', 'Medium', 'Dimensions'])
    print(a)

def getArtworksByArtistsTechnique(artistName,artistID,artworks):
    """
    Recibe el ID del artista, extrae los artworks y los ordena por tecnica ademas de retornar
    el numero de obras hechas con cierta tecnica

    artistID - Id del artista
    artworks - Datos de obras

    Retorna en lista:

    sortedArtworks - Obras ordenadas y seleccionadas
    count - Diccionario usando tecnicas por llaves y numeros de obras por valor
    """
    #TODO Acabar
    resultado = newList('ARRAY_LIST', None)
    conteo = {}
    for artwork in artworks:

        codes = artwork["ConstituentID"].split(",")
        if contOrNot (artistID,codes) == True:
            continue
        if artistID == artwork["ConstituentID"]:
            lt.addLast(resultado,artwork)

    #print(resultado)
    
    #me.sort(resultado,compareMedium)

    for artwork in resultado:
        if artwork["Medium"] not in conteo.keys():
            conteo[artwork["Medium"]] = 0
        conteo[artwork["Medium"]] += 1

    resultado = pd.DataFrame(resultado["elements"], colums=["Title","Date","Medium","Dimensions"])

    print(artistName+" con id de MoMa "+str(artistID)+" tiene "+str(len(resultado))+" obras a su nombre en el museo.")
    print("Hay "+str(len(conteo))+" diferentes medios / tecnicas en su trabajo")
    print("Su top 5 de medios / tecnicas son:")
    print(pd.DataFrame(conteo[:5]))

    print("Tres ejemplos de "+conteo.keys()[0]+"de la coleccion son: ")
    

def contOrNot(artist,codes):
    for i in codes:
        code = i.strip().strip('[').strip(']')
        if code == artist:
            return False
    return True

def getArtistID(name,artists_info):
    """Recibe por parametro el nombre del artista junto con el info de los artistas y devuelve su ID"""
    result = 0
    size = lt.size(artists_info)
    complete = False
    artist = 1
    while artist <= size and not complete:
        #TODO Averiguar por que esta cosa no toma un registro en especifico
        temp = lt.getElement(artists_info,artist)
        Dict = lt.firstElement(artists_info)
        print(Dict)
        data = Dict[temp]
        print(temp)
        if temp["DisplayName"].lower == name.lower():
            result = temp["ConstituentID"]
            complete = True
        artist += 1
    print(result)
    return result



def getArtistbyConID(codes, artists_info):
    names = {}

    for code in codes:
        code2 =  code.strip().strip('[').strip(']')
        if code2 not in names:
            dict = lt.firstElement(artists_info)
            info = dict[code2]['DisplayName']
            names[code2]  = info
    return names




# Funciones utilizadas para comparar elementos dentro de una lista

def compareartists(artistname1, artist):
    if (artistname1.lower() in artist['name'].lower()):
        return 0
    return -1

def compareTitle(artwork1, artwork2):
    if artwork1[1].lower() > artwork2[1].lower():
        return True
    return False

def compareTechnique(technique,artistTecniques):
    if technique in artistsTecnique:
        return True
    return False
    


def cmpArtworkByDateAdquired(artwork1,artwork2):
    date1 = artwork1["DateAcquired"].split("-")
    date2 = artwork2["DateAcquired"].split("-")
    if len(date1)!= 3:
        return True
    if len(date2) != 3:
        return False

    if int(date1[0]) < int(date2[0]):
        return True
    elif int( date1[0]) == int(date2[0]):
        if date1[1] < date2[1]:
            return True
        elif int(date1[1]) == int(date2[1]):
            if int(date1[2]) < int(date2[2]):
                return True  
    else:
        return False

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
    me.sort(natSort, compareCont)
    lessEl = lt.subList(natSort,1,10)
    print('Nationality' + '       '+ 'Artworks')
    for nat in lessEl['elements']:
        space = 25 - len(nat[1]) - len(str(nat[0]))
        print(nat[1].capitalize(), space * " " , nat[0])
    great = lt.firstElement(lessEl)
    print('La nacionalidad con mas obras es %s con %s obras.' %(great[1].capitalize(),great[0]))
    return great[1]


def sortByDate(lst, sortType):

    if sortType == 1:
        a = ins.sort(lst, cmpArtworkByDateAdquired)
        print(a)
    elif sortType == 2:
        sa.sort(lst,cmpArtworkByDateAdquired)
    elif sortType == 3:
        me.sort(lst,cmpArtworkByDateAdquired)
    elif sortType == 4:
        qu.sort(lst,cmpArtworkByDateAdquired)
    