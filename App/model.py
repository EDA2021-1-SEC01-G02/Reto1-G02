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
from DISClib.DataStructures.arraylist import addLast, defaultfunction, firstElement, getElement, subList
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
def getYearRange(artists_info, year1, year2):
    size = lt.size(artists_info) +1
    for pos in range(1, size):
        temp =  lt.getElement(artists_info, pos)['BeginDate']
        if cmpArtistByDate(temp, year1) == False:
            firstPos = pos 
            break
    for pos in range(firstPos, size):
        temp =  lt.getElement(artists_info, pos)['BeginDate']
        if cmpArtistByDate(temp, year2) == False:
            secondPos = pos
            if int(temp)> int(year2):
                break

    len = secondPos - firstPos
    rangeList = lt.subList(artists_info,firstPos, len)
    sizeRange = lt.size(rangeList)
    lista = newList('ARRAY_LIST', None)
    print('Entre los años %s y %s esuvieron activos %s artistas' %(year1, year2, sizeRange))
    for pos in range(1, 4):
        lt.addLast( lista,(lt.getElement(rangeList,pos)))

    for pos in range(sizeRange-2, sizeRange+1):
        lt.addLast( lista,(lt.getElement(rangeList,pos)))

    print(pd.DataFrame(lista['elements']))
    
    

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
            nat = 'unknown'
        if nat not in natList:
            natList[nat] = [1]
            natList[nat].append([])
            natList[nat][1].append(temp)
        else:
            natList[nat][0] += 1
            natList[nat][1].append(temp)
    return natList

def getArtworksbyArtists(artists, artworks, artists_info, firstEl):
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
    sixEl = newList('ARRAY_LIST', None)
    sizeSub = lt.size(artworksByAr)
    for pos in range(1,4):
        temp = lt.getElement(artworksByAr,pos)
        lt.addLast(sixEl, temp)
    for pos in range(sizeSub-4,sizeSub):
        temp = lt.getElement(artworksByAr,pos)
        lt.addLast(sixEl, temp)
    print('La nacionalidad con mas obras es %s con %s obras.' %(firstEl.capitalize(),lt.size(artworksByAr)))
    a = pd.DataFrame(sixEl['elements'], columns=['ObjectId', 'Title','Artists', 'Date', 'Medium', 'Dimensions'])
    print(a)

def getArtworksByArtistsTechnique(artistName,artistID,artworks):
    """
    Recibe el ID del artista, extrae los artworks y los ordena por tecnica ademas de obtener
    el numero de obras hechas con cierta tecnica

    Mostrara al usuario la tecnica mas usada (junto con las otras 5 mas usadas) y 
    algunas obras hechas con esta tecnica

    Recibe:
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

                if tempArtwork["Medium"] not in conteo.keys(): #Añadir tecnica / medio si no existia en el registro
                    conteo[tempArtwork["Medium"]] = 0
                conteo[tempArtwork["Medium"]] += 1 #Contar uno mas en la tecnica / el medio

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
        print(pd.DataFrame(topConteo["elements"],columns=["Medio / Tecnica","Conteo"])) #TODO: Solo imprime una de las 5 y tiene que imprimir las 5 menquepaso

        print("Tres ejemplos de "+str(topMedium[0])+"de la coleccion son: ")
        print(resultadoTabla)

def getDepArtworks (artworks,dep):
    """
    Recibe los datos de las obras y el nombre del departamento

    Buscara todas las obras correspondientes al departamento y las retornara en una nueva lista

    Recibe:
    artworks - Obras registradas
    dep - Nombre del departamento a buscar

    Retorna:
    Lista con las obras correspondientes al departamento
    """

    resultado = lt.newList('ARRAY_LIST', None) #Crea la lista que contendra los registros filtrados
    size = lt.size(artworks)

    for i in range(0,size+1):
        artwork = lt.getElement(artworks,i)
        if artwork["Department"].lower() == dep.lower():
            lt.addLast(resultado,artwork)
    
    return resultado

def calculatePrice(artworks,artists):
    resultado = None
    size = lt.size(artworks) 
    if size != 0: #Revisa si encontro el departamento antes de continuar
        
        resultado = lt.newList('ARRAY_LIST', None) #Crea la lista donde se guardaran los datos junto con su precio
        resultWeight = 0.0
        resultCost = 0.0

        for i in range(1,size+1): #Recorre registro por registro
            artwork = lt.getElement(artworks,i)
            
            artworkWeight = artwork["Weight (kg)"] #Extrae el peso de la obra
            if artworkWeight != "": #Si tiene valores, continuara
                artworkWeight = float(artworkWeight)
                if artworkWeight != 0: #Para evitar dividir entre 0
                    resultWeight += artworkWeight #Añade el peso de la obra al contador
                    artworkWeightCost = 72 * artworkWeight #Multiplica por la tarifa
                    weight = True
                else:
                    artworkWeightCost = 0
                    weight = False
            else: 
                artworkWeightCost = 0
                weight = False

            artworkHeigh = artwork["Height (cm)"]
            artworkWidth = artwork["Width (cm)"]
            if artworkHeigh != "" and artworkWidth != "": #Si tiene valores, continuara
                artworkHeigh = float(artworkHeigh)
                artworkWidth = float(artworkWidth)
                if (artworkHeigh != 0) and (artworkWidth != 0): #Para evitar dividir entre cero
                    artwork2dSize = artworkHeigh * artworkWidth
                    artwork2dCost = 72 * (artwork2dSize/10000) #Convierte a metros cuadrados y saca el precio
                    size2d = True

                    artworkDepth = artwork["Depth (cm)"]
                    if artworkDepth != "": #Si existen tres dimensiones
                        artworkDepth = float(artworkDepth)
                        if artworkDepth != 0: #Para evitar dividir entre cero
                            artwork3dSize = artwork2dSize * artworkDepth
                            size3d = True
                            artwork3dCost = 72 * (artwork3dSize/1000000) #Convierte a metros cubicos y saca el precio
                        else: #Si son solo dos dimensiones
                            artwork3dCost = 0
                            size3d = False
                    else: 
                        artwork3dCost = 0
                        size3d = False
                else:
                    artwork2dCost = 0
                    size2d = False
                    artwork3dCost = 0
                    size3d = False
            else:
                artwork2dCost = 0
                size2d = False
                artwork3dCost = 0
                size3d = False
            
            if (size2d or size3d or weight) and ((artwork2dCost > 0) or (artwork3dCost > 0) or (artworkWeightCost > 0)): #Si hay informacion para calcular la tarifa
                if (artwork2dCost >= artworkWeightCost) and (artwork2dCost >= artwork3dCost): #Buscara cual es la tarifa mas costosa
                    artworkCost = artwork2dCost
                elif (artwork3dCost >= artwork2dCost) and (artwork3dCost >= artworkWeightCost):
                    artworkCost = artwork3dCost
                else:
                    artworkCost = artworkWeightCost
            else: #Si no hay informacion para calcular, se aplicara la regla por defecto (48 USD por obra)
                artworkCost = 48
            resultCost += artworkCost

            codes = artwork['ConstituentID'].split(',')
            info = [artwork["ObjectID"],artwork["Title"],getArtistbyConID(codes,artists),artwork["Medium"],artwork["Date"],artwork["Dimensions"],artwork["Classification"],artworkCost,artwork["URL"]]
            lt.addLast(resultado,info)
        
    return (resultado,resultWeight,resultCost)

def showPrice(artworks,weight,cost,dep):

    if artworks == None:
        print("Departamento no encontrado. Intente nuevamente")

    else:
        size = lt.size(artworks)
        artworksByDate = me.sort(artworks,cmpArtworkByDate)

        olderList = lt.newList('ARRAY_LIST', None)
        for pos in range (1,size+1):
            artwork = lt.getElement(artworksByDate,pos)

            if artwork[4] != '':
                lt.addLast(olderList,artwork)
        minolderList = subList(olderList,1,6)
        minolderList = pd.DataFrame(minolderList["elements"],columns=["ID","Titulo","Artistas","Medio / Tecnica","Fecha","Dimensiones","Clasificacion","Costo de transporte (USD)","URL"])

        artworksByDate = me.sort(artworks, cmpArtworkByCost)

        expensiveList = lt.newList('ARRAY_LIST', None)
        for pos in range(1,6):
            artwork = lt.getElement(artworksByDate,pos)
            lt.addLast(expensiveList,artwork)
            
            
        expensiveList = pd.DataFrame(expensiveList["elements"],columns=["ID","Titulo","Artistas","Medio / Tecnica","Fecha","Dimensiones","Clasificacion","Costo de transporte (USD)","URL"])

        
        print ("El MoMa transportara "+str(size)+" obras del departamento de "+dep+".")
        print("RECUERDE!!!, NO TODOS los datos del MoMa estan completos!!!... Esto es solo un aproximado al valor real.")
        print("Peso estimado de carga: "+str(weight))
        print("Costo estimado de carga: "+str(cost))

        print("El TOP 5 de los elementos mas costosos de transportar es:")
        print(expensiveList)
        print("El TOP 5 de los elementos mas viejos a transportar es:")
        print(minolderList)

def cmpArtworkByCost(artwork1,artwork2):
    cost1 = artwork1[7]
    cost2 = artwork2[7]
    if cost1 == '':
        cost1 =  0
    if cost2 == '':
        cost2 = 0
    if float(cost1) > float(cost2):
        return True
    else:
        return False

    pass

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
    if artwork1[1].lower() < artwork2[1].lower():
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

def cmpArtworkByDate(artwork1,artwork2):
    """
    Compara la fecha de dos obras, donde devuelve True si el primero es mas viejo
    """

    date1 = artwork1[4]
    date2 = artwork2[4]
    if date1 == '':
        date1 =  0
    if date2 == '':
        date2 = 0
    if int(date1) < int(date2):
        return True
    else:
        return False

def compareCont(item1, item2):
    #Compara cual de los dos conteos es mayor (Se utiliza para ordenar las nacionalidades)
    if item1[0] > item2[0]:
        return True
    else:
        return False

def cmpArtistByDate(artist1, artist2):
    if type(artist1) != int and type(artist1) != str:
        date1 = int(artist1['BeginDate'])
    else:
        date1= int(artist1)
    
    if type(artist2) != int and type(artist2) != str:
        date2 = int(artist2['BeginDate'])
    else:
        date2 = int(artist2)

    if date1 < (date2):
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
    return great[1]


def sortByDate(artworks):
    me.sort(artworks,cmpArtworkByDateAdquired)

def sortArtistByDate(artists_info):
    artList = newList('ARRAY_LIST',None)
    dict =  lt.firstElement(artists_info)
    for artist in dict:
        lt.addLast(artList,dict[artist])
    me.sort(artList,cmpArtistByDate)
    return artList

