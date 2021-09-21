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


from DISClib.ADT.stack import top
from DISClib.ADT.orderedmap import keys
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
    #Sirve para recolectar los ID de los artistas de las obras de arte, sin tomar en cuenta si estan repetidos o no
    #  (Habran repetidos, pues servira para contar las nacionalidades)

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


def getArtworksByDate(artworks, date1, date2):
    size = lt.size(artworks) + 1
    contPur =  0
    artistas = newList('ARRAY_LIST', None)
    for pos in range(1, size):
        temp = lt.getElement(artworks, pos)['DateAcquired']
        if cmpDateAdquired(temp,date1) == False:
            firstPos =  pos 
            break
    for pos in range(firstPos, size):
        temp = lt.getElement(artworks, pos)['DateAcquired']
        temp2 = lt.getElement(artworks, pos)['ConstituentID']
        temp3 =  temp2.split(',')
        for code in temp3:
            lt.addLast(artistas,code.strip().strip('[').strip(']')) 
        if cmpDateAdquired(temp, date2) == False:
            secondPos =  pos 
            break
    len =  secondPos - firstPos
    artworksbyDate = lt.subList(artworks, firstPos, len)
    size =  lt.size(artworksbyDate)

    for pos in range(1,size+1):
        item =  lt.getElement(artworksbyDate,pos)
        str = item['CreditLine'].lower()
        if 'purchase' in str:
            contPur += 1
    artsize =  lt.size(artistas) -1

    print('Entre las fechas %s y %s se adquirieron %s obras unicas y %s fueron compradas.\n Y con un total de %s artistas' %(date1, date2,size, contPur,artsize))
    return((artworksbyDate))

def getSixArtworks(lst, artists_info):
    list = newList('ARRAY_LIST', None)
    size =  lt.size(lst)+1
    size2 = size-3
    for pos in range (1, 4):
        item = lt.getElement(lst, pos)
        consID = item['ConstituentID'].split(',')
        names = getArtistbyConID(consID, artists_info)
        string = ''
        for name in names:
            string += names[name] + ', '
        item['ConstituentID'] = string
        lt.addLast(list,item)
    
    for pos in range(size2,size):
        item = lt.getElement(lst, pos)
        consID = item['ConstituentID'].split(',')
        names = getArtistbyConID(consID, artists_info)
        string = ''
        for name in names:
            string += names[name] + ', '
        item['ConstituentID'] = string
        lt.addLast(list, item)
    printArtworks(list)

def printArtworks(lst):
    size = 1 + lt.size(lst)
    lista =  []
    for pos in range(1,size):
        lista.append(lt.getElement(lst,pos))
    a = pd.DataFrame(lista)
    print(a[['Title','ConstituentID', 'DateAcquired']])



# Funciones de consulta
def getNatInfo(artists_info, artistsInfo):
    """Se encarga de agarrar los ID de los artistas y devolver un dict con los datos de las nacionalidades (conteo de obras y artistas)"""
    
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
    """Con IDs de artistas, busca sus obras y las muestra en pantalla organizandolas por titulo"""

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
    Recibe el ID del artista, extrae los artworks y los ordena por tecnica ademas de obtener
    el numero de obras hechas con cierta tecnica

    Mostrara al usuario la tecnica mas usada (junto con las otras 5 mas usadas) y 
    algunas obras hechas con esta tecnica

    artistName - Nombre del artista en str (Dado por el usuario en view)
    artistID - Id del artista (Dado por getArtistID)
    artworks - Datos de obras
    """

    if artistID == 0: #Si no encontro un ID con la funcion getArtistID, no realizara el proceso
        print("No se encontro el artista en los registros.")
    else:
        resultado = newList('ARRAY_LIST', None)
        conteo = {}
        sizeArtworks = lt.size(artworks)
        #Extraccion de obras que coincidan con el ID del artista
        for artwork in range(0,sizeArtworks+1):
            tempArtwork = lt.getElement(artworks,artwork) #Seleccionar registro
            codes = tempArtwork["ConstituentID"].split(",") #Obtener IDs de autores
            for i in range(len(codes)):
                codes[i] = int(codes[i].strip("[").strip("]")) #Eliminar los [ ] y convertir a numero

            if artistID in codes: #Revisa si el codigo del artista esta en los codigos de los autores de la obra
                info = [tempArtwork["Title"],tempArtwork["Date"],tempArtwork["Medium"],tempArtwork["Dimensions"]] #Añadir a lista que tiene los datos filtrados
                lt.addFirst(resultado,info)

                #TODO preguntar si este tipo de lista esta bien o si toca con las funciones
                if tempArtwork["Medium"] not in conteo.keys(): #Añadir tecnica / medio si no existia en el registro
                    conteo[tempArtwork["Medium"]] = 0
                conteo[tempArtwork["Medium"]] += 1 #Contar uno mas en la tecnica / el medio
    
        #TODO implementar merge para organizar y mostrar los resultados asi como lo pide el enunciado
        #me.sort(resultado,compareMedium)

        sortedConteo = {}
        sortedMediums = sorted(conteo,key=conteo.get,reverse=True)
        for medium in sortedMediums:
            sortedConteo[medium] = conteo[medium]

        topConteo = lt.newList('ARRAY_LIST', None)
        for i in range(0,5):
            info = [list(sortedConteo.keys())[i],list(sortedConteo.values())[i]]
            lt.addLast(topConteo,info)
        topMedium = lt.getElement(topConteo,1)

        resultadoTabla = pd.DataFrame(resultado["elements"], columns=["Title","Date","Medium","Dimensions"]) #Aplicar para mostrar los tres ejemplos mas abajo
        resultadoTabla = resultadoTabla[resultadoTabla["Medium"]==str(topMedium[0])]

        print(artistName+" con id de MoMa "+str(artistID)+" tiene "+str(lt.size(resultado))+" obras a su nombre en el museo.")
        print("Hay "+str(len(conteo))+" diferentes medios / tecnicas en su trabajo")
        print("Su top 5 de medios / tecnicas son:")
        print(pd.DataFrame(topConteo["elements"],columns=["Medio / Tecnica","Conteo"]))

        print("Tres ejemplos de "+str(topMedium[0])+"de la coleccion son: ")
        print(resultadoTabla)
    

def contOrNot(artist,codes):
    for i in codes:
        code = i.strip().strip('[').strip(']')
        if code == artist:
            return False
    return True

def getArtistID(name,artists_info):
    """Recibe por parametro el nombre del artista junto con el info de los artistas y devuelve su ID"""
    result = 0 #ID del artista. Se mantendra en 0 si no lo encuentra
    temp = lt.getElement(artists_info,1) #Accede a los registros
    
    for i in temp: #Recorre
        if temp[i]["DisplayName"].lower() == name.lower(): #Compara nombre
            result = temp[i]["ConstituentID"] #Toma el ID
            break #Rompe el for
    return result



def getArtistbyConID(codes, artists_info):
    #Dados unos Cons ID (lista), devuelve los nombres del artista en un Dict
    names = {}

    for code in codes:
        code2 =  code.strip().strip('[').strip(']')
        if code2 not in names:
            dict = lt.firstElement(artists_info)
            info = dict[code2]['DisplayName']
            names[code2]  = info
    return names




# Funciones utilizadas para comparar elementos dentro de una lista
def cmpDateAdquired(date1,date2):
    date1 = date1.split("-")
    date2 = date2.split("-")
    if len(date1)!= 3:
        return True
    if len(date2) != 3:
        return True

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
        else:
            return False
    else:
        return False

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
    # Compara el dia de adquisicion de una obra, devolviendo True si el primero es menor

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
    #Compara cual de los dos conteos es mayor (Se utiliza para ordenar las nacionalidades)
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


def sortByDate(artworks):
    me.sort(artworks,cmpArtworkByDateAdquired)
    
    