from bs4 import BeautifulSoup
import re
import globales
import collections
from collections import Counter
import math

#Esta funcion realizar la impresion de un menu.
def Menu():
    #Imprime la opciones del menu
    print("MENU:"+"\n"+"1)Configurar datos")
    #.\\reut2-001.sgm
    print("2)Salir")
    
    opcion=""
    opcion= input("Escribe una opcion: ")

    if opcion=="1":
        configurarDatos()
    elif opcion=="2":
        Salir()     
    else:
        print("Ingrese opciones validas.")
        Menu()
        
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Por medio de esta funcion el usuario ingresa datos para la realizacion del diseno
def configurarDatos():
    print("------------1) CONFIGURAR DATOS------------")
    
    globales.ruta= input("Ingrese la ruta del archivo: ")

    globales.numMejores= input("Ingrese la cantidad de mejores términos que serán escogidos (numMejores): ")

    globales.minNc= input("Ingrese cantidad mínima de documentos por clase (minNc): ")

    globales.minNi= input("Ingrese cantidad mínima de documentos por término (minNi): ")

    globales.prefijo= input("Ingrese un prefijo para usar en los nombres de los archivos generados: ")

    globales.ruta=str(globales.ruta)
    globales.numMejores=int(globales.numMejores)
    globales.minNc=int(globales.minNc)
    globales.minNi=int(globales.minNi)
    globales.prefijo=str(globales.prefijo)
    crearArchivos(globales.ruta,globales.minNc,globales.minNi,globales.prefijo,globales.numMejores)
    calculos(globales.prefijo,globales.numMejores) 
    print("-------------------------------------------")
    iraMenu()

    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Esta funcion te da la opcion de ir al menu
def imprimirDatos():
    print("------------DATOS DE CONFIGURACION------------")
    print("Ruta : "+str(globales.ruta))
    print("numMejores : "+str(globales.numMejores))
    print("minNc : "+str(globales.minNc))
    print("minNi : "+str(globales.minNi))
    print("prefijo : "+str(globales.prefijo))
    print("----------------------------------------------")
    iraMenu()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Esta funcion te da la opcion de ir al menu
def iraMenu():
    IraM = input("Desea ir al menu: ")
    if IraM =="si":
        Menu()
    elif IraM =="no":
        iraMenu()
    else:
        print("Digite si o no")
        iraMenu()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def Salir():
    salir= input("Desea salir del programa: ")
    if salir=="si":
        exit()
    elif salir=="no":
        Menu()
    else:
        print("Digite si o no")
        Salir()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
stopwords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself"]

def crearArchivos(path,minNc,minNi,prefijo,numMejores):
    file = open(path,"r")
    contents = file.read()
    listaDocs = contents.split("<R")[1:]
    for i in range(0,len(listaDocs)):
        listaDocs[i] = "<R" + listaDocs[i]

    #listar clases
    clases = {}
    for i in range(0,len(listaDocs)):
        soup = BeautifulSoup(listaDocs[i],'html.parser')
        topicTag = soup.find('topics')
        if(len(topicTag.text) > 0):
            topic = topicTag.find('d').text
            if(topic in clases):
                clases[topic] += 1
            else:
                clases[topic] = 1
    
    #listar docs
    docs = {}
    dicc = {}
    for i in range(0,len(listaDocs)):
        soup = BeautifulSoup(listaDocs[i],'html.parser')
        reuters = soup.find('reuters')
        if(reuters['topics'] == 'YES'):#topics = YES
            topicTag = soup.find('topics')
            if(len(topicTag.text) > 0): #tiene topic
                topic = topicTag.find('d').text
                if(clases[topic] >= minNc):#el topic es valido
                    docId = soup.find('reuters')['newid']
                    docs[docId] = topic #guardar newId
                    #listar terminos
                    if(docId in docs):
                        bodyTag = soup.find('body')
                        if(bodyTag != None):
                            terminosAnalizados = []
                            terminosValidos = sacarPalabrasNumeros(quitarStopWords(bodyTag.text.lower()))
                            for termino in terminosValidos:
                                if(not termino in terminosAnalizados):
                                    if(termino in dicc):
                                        if(topic in dicc[termino]):
                                            dicc[termino][topic] += 1
                                        else:
                                            dicc[termino][topic] = 1
                                    else:
                                        dicc[termino] = {}
                                        dicc[termino][topic] = 1
                                    terminosAnalizados.append(termino)

    #crear clases.txt
    clasesFile = open(prefijo+"clases.txt","w+")
    for key in clases:
        if(clases[key] >= minNc):
            clasesFile.write(key + "\t" + str(clases[key]) + "\n")
    clasesFile.close()

    #crear docs.txt
    docsFile = open(prefijo+"docs.txt","w+")
    for key in docs:
        docsFile.write(key + "\t" + docs[key] + "\n")
    docsFile.close()

    #crear dicc.txt
    diccFile = open(prefijo+"dicc.txt","w+")
    for key in dicc:
        ni = 0
        nik = []
        for clase in dicc[key]:
            ni += dicc[key][clase]
            nik.append((clase,str(dicc[key][clase])))
        if(ni >= minNi):
            diccFile.write(key + "\t" + str(ni) + "\t" + "")
            nikString = ""
            for pair in nik:
                nikString += "" + pair[0] + "," + pair[1] + "/"
            diccFile.write(nikString[:-1] + "\n")
    diccFile.close()
    #AQUI HACE LOS CALCULOS
    globales.minNc=minNc
    globales.minNi=minNi  
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------         
def sacarPalabrasNumeros(texto):
    patronPalabras = r'\b[a-z]+\b'
    patronNumeros = r'\b\d+,\d+,\d+\.\d+\b|\b\d+,\d+\.\d+\b|\b\d+\.\d+\b|\b\d+,\d+,\d+\b|\b\d+,\d+\b|\b\d+\b'
    soloPalabras = re.findall(patronPalabras,texto) 
    soloNumeros = re.findall(patronNumeros,texto)
    numerosSinComas = []
    for numero in soloNumeros:
        nuevoNumero = numero.replace(',','')
        numerosSinComas.append(nuevoNumero)
    return soloPalabras + numerosSinComas
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------       
def quitarStopWords(texto):
    textoSplit = texto.split()
    resultado = [palabra for palabra in textoSplit if not palabra in stopwords]
    temp = ""
    for palabra in resultado:
        temp += palabra + " "
    return temp[:-1]
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def calculos(prefijo,numMejores):
    #calculos("pref_",5)
    """
    E(C): Entropía de la colección con clases C.
    E(C,termi):	Entropía de que se obtiene al separar la colección con clases C usando el término i.
    GI(C,termi): ganancia de información que se obtiene al usar el término i.
    nik: número de documentos de clase k que contienen el término i
    nck: número de documentos en clase k
    ni:	número de documentos que contienen término i
    N: número total de documentos de la colección
    """
    globales.prefijo = prefijo
    listClases = leerArchivosSimples(str(prefijo)+"clases.txt")
    listDicc = leerArchivosComplejos(str(prefijo)+"dicc.txt")#"pref_dicc.txt"
    listDocs = leerArchivosSimples(str(prefijo)+"docs.txt")
    
    N = len(listDocs)   #número total de documentos de la colección
    
    listaEPorClase = E_C(listClases,N)
    listaEClaseTermino = E_C_T(listClases,listDicc,N)
    GI(listaEPorClase,listaEClaseTermino,prefijo,numMejores)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def E_C(listClases,N):
    listaEPorClase = []
    #----------CALCULO DE E(C)---------------------
    if(listClases != []):
        print("---------------------------------------------")
        print('-----CALCULOS DE ENTROPIA POR CLASE E(C)-----')
        print("---------------------------------------------")
        entropiaTotal = 0
        entropiaPorClase = 0
        #ECUACION 1 PARA E(C)
        for y in range(0,len(listClases)): #for key in clases:
            #print ("TOPICS: " +str(key))
            #print ("nck: "+ str(clases[key]))
            nck_N = int(listClases[y][1])/N
            if(( nck_N ) != 0):
                e_x_Clase = nck_N * (math.log(nck_N, 2))
            else:
                e_x_Clase = 0
            entropiaPorClase = e_x_Clase *-1
            #print ("TOPICS: " + str(listClases[y][0]) + " / nck: "+ str(listClases[y][1])+ " / E(C) por Clase: "+ str(entropiaPorClase))
            listaEPorClase += [[listClases[y][0],listClases[y][1],entropiaPorClase]]
            entropiaTotal += entropiaPorClase
            
        print ("E(C) TOTAL: "+ str(entropiaTotal))
        print("---------------------------------------------"+ "\n")
        #print(listaEPorClase)
    return listaEPorClase
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def E_C_T(listClases,listDicc,N):
    listaEClaseTermino = []
    #--------------CALCULO DE E(C,termi)---------------------       
    if(listDicc != []):
        print("-----------------------------------------------------------")
        print('----CALCULOS DE ENTROPIA POR CLASE Y TERMINO E(C,termi)----')
        print("-----------------------------------------------------------")
        ni = 0
        y=0
        entropiaTotal=0
        while( y < len(listClases)):
            Znikxlog2_nik = 0 #n_ik * log_2 ( n_ik )/ ZUMATORIA /(ROSA)
            Znck_nikxlog2_nck_nik= 0 #(nc_k-n_ik)log_2(nc_k-n_ik )/ZUMATORIA/(ROJO)
            clase = listClases[y][0] # Nombre de la clase
            nckClase = int(listClases[y][1])# nck
            x=0
            while( x < len(listDicc)):
                termino = listDicc[x][0] # Nombre del termino
                ni = int(listDicc[x][1]) # ni
                listaPares = listDicc[x][2] # Pares de clases
                i=0
                while( i < len(listaPares)):
                    claseXTerm = listaPares[i][0] # Nombre de la Clase X temino
                    nikXClaseXTerm = int(listaPares[i][1]) # nik de la Clase X temino
                    if( claseXTerm == clase):
                        Znikxlog2_nik +=  nikXClaseXTerm * (math.log(nikXClaseXTerm, 2))#n_ik * log_2 ( n_ik )/ ZUMATORIA /(ROSA)  
                        nck_nik = (nckClase - nikXClaseXTerm)# (nck - nik) resta de nck y nik
                        #print(str("clase:"+clase+"/"+"Termino:"+ termino )+" nck_nik : "+str(nck_nik))
                        if(nck_nik != 0):
                            Znck_nikxlog2_nck_nik += nck_nik * (math.log(nck_nik, 2))#(nc_k-n_ik)log_2(nc_k-n_ik )/ ZUMATORIA /(ROJO)
                    i += 1  
                x += 1
                nixlog2ni = ni * (math.log(ni, 2))#n_i*log_2 (n_i ) FINAL (AMARILLO)
                #print( "( "+str(N)+" - "+str(ni)+ ") * ( math.log( " + str(N)+" - "+str(ni)+", 2)")
                if(( N - ni ) != 0):
                    N_nixlog2N_ni = ( N - ni ) * ( math.log( N - ni, 2) )#(N-n_i )*log_2 (N-n_i ) FINAL (VERDE)
                else:
                    N_nixlog2N_ni=0
                #print( "( "+str(nixlog2ni) +" + "+str(N_nixlog2N_ni)+ " - " + str(Znikxlog2_nik) +" - "+ str(Znck_nikxlog2_nck_nik)+" ) "+" / "+str(N))
                entropiaPorClasePorTerm = ( nixlog2ni + N_nixlog2N_ni - Znikxlog2_nik - Znck_nikxlog2_nck_nik )/N
                #print ("TOPICS: " + str(clase) + " / Termino: "+ str(termino)+ " / E(C,termi): "+ str(entropiaPorClasePorTerm))
                listaEClaseTermino += [[clase,termino,entropiaPorClasePorTerm]]
                ni=0
                Znck_nikxlog2_nck_nik = 0
                Znikxlog2_nik = 0
                entropiaTotal += entropiaPorClasePorTerm
            y += 1
        print ("E(C,termi) TOTAL: "+ str(entropiaTotal))
        print("-----------------------------------------------------------"+ "\n")
        #print (listaEClaseTermino)
    return listaEClaseTermino
   
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def GI(listaEPorClase,listaEClaseTermino,prefijo,numMejores):
    print("-----------------------------------------------------------------------")
    print('----CALCULOS DE GANANCIA DE INFORMACION CLASE Y TERMINO GI(C,termi)----')
    print("-----------------------------------------------------------------------")
    x=0
    GI=0
    listGI=[]
    ListaResultadosFinales = []
    GITotal= 0
    entropiaTotal=0
    while( x < len(listaEPorClase)):
        clase = listaEPorClase[x][0] # Nombre de la clase
        nck = float(listaEPorClase[x][1]) # nck
        E_C = float(listaEPorClase[x][2]) # Entropia por clase
        i=0
        GI=0
        while( i < len(listaEClaseTermino)):
            claseXTerm = listaEClaseTermino[i][0] # Nombre de la Clase X temino
            termino = listaEClaseTermino[i][1] #Termino
            E_C_termi= float(listaEClaseTermino[i][2]) # nik de la Clase X temino
            if( clase == claseXTerm):
                GI = E_C - E_C_termi
                # listGI += [[termino,clase,GI]]
                # print("Termino: "+str(termino)+ "| Clase: " + str(clase)+ "| GI: " + str(GI)+ "| E(C,termi): " + str(E_C_termi))
                ListaResultadosFinales += [[termino,clase,GI,E_C_termi]]
                GITotal+= float(GI)
                entropiaTotal += E_C_termi
            i += 1
        x += 1
    print("GI(C,termi) TOTAL: "+str(GITotal))
    print("---------------------------------------------"+ "\n")
    #crear gi.txt
    clasesFile = open(prefijo+"gi.txt","w+")
    clasesFile.write("ENTROPIA TOTAL: "+str(entropiaTotal)+ "\n")
    ListaResultadosFinales.sort(key=lambda termino : termino[0], reverse=False)
    for y in range(0,len(ListaResultadosFinales)):
        termino_ = ListaResultadosFinales[y][0]
        clase_ = ListaResultadosFinales[y][1]
        GI_= ListaResultadosFinales[y][2]
        entropia_= ListaResultadosFinales[y][3]
        clasesFile.write("Term: "+str(termino_)+ "\t Clase: " + str(clase_)+ "\t GI: " + str(GI_)+ "\t E(C,termi): " + str(entropia_) + "\n")
    clasesFile.close()

    #crear mejores.txt
    clasesFile = open(prefijo+"mejores.txt","w+")
    ListaResultadosFinales.sort(key=lambda termino : termino[2], reverse=True)
    for y in range(0,numMejores):
        termino_ = ListaResultadosFinales[y][0]
        clase_ = ListaResultadosFinales[y][1]
        GI_= ListaResultadosFinales[y][2]
        entropia_= ListaResultadosFinales[y][3]
        clasesFile.write("Term: "+str(termino_)+ "\t Clase: " + str(clase_)+ "\t GI: " + str(GI_)+ "\t E(C,termi): " + str(entropia_) + "\n")
    clasesFile.close()
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def imprimirDatos(dicc, docs, clases):
    if(dicc != {}):
        print("---------------------------------------------")
        print('DICC CON DATOS')
        for word in dicc:
            globales.minNi
            print ("Termino: " +str(word))
            print ("nik: "+ str(dicc[word])) 
        print("---------------------------------------------")
    if(docs != {}):
        print("---------------------------------------------")
        print('DOCS CON DATOS')
        for doc in docs:
            print ("REUTERS: " +str(doc))
            print ("TOPICS: "+ str(docs[doc]))
        print("---------------------------------------------")    
    if(clases != {}):
        print("---------------------------------------------")
        print('CLASES CON DATOS')
        for key in clases:
            if(clases[key] >= globales.minNc):
                print ("TOPICS: " +str(key))
                print ("nck: "+ str(clases[key]))
        print("---------------------------------------------")
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def H(s):
    # s= 'Standard English text usually falls somewhere between 3.5 and 5'
    # s = ["Standard","English","text","usually","falls", "somewhere", "between", "3.5","and","5"]
    probabilities = [n_x/len(s) for x,n_x in collections.Counter(s).items()]
    e_x = [-p_x*math.log(p_x,2) for p_x in probabilities]
    print("N = " + str(sum(e_x)))
    return sum(e_x)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def H1(s):
    return sum([-p_x*math.log(p_x,2) for p_x in [n_x/len(s) for x,n_x in collections.Counter(s).items()]])
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def entropia(lista):
    N = len(lista)
    probs = (len(freq)/N  for freq in lista if len(freq)>0)
    return -sum(x * math.log(x, 2) for x in probs)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def E1(lista,term):
    N = len(lista)
    print("N = " + str(N))
    #list1 = ['x','y','z','x','x','x','y', 'z']
    #print(Counter(list1))
    probabilities = [nck/N for x,nck in collections.Counter(lista).items()]
    e_x = [-p_x*math.log(p_x,2) for p_x in probabilities]    
    print("RESULTADO PROB ENTRE N = " + str(probabilities))
    print("E(c) ENTRE N = " + str(sum(e_x)))
    
    probabilities = [nck for x,nck in collections.Counter(lista).items()]
    e_x = [-p_x*math.log(p_x,2) for p_x in probabilities]    
    print("RESULTADO PROB SIN N = " +str(probabilities))
    print("E(c) SIN N = " + str(sum(e_x)))
    
    probabilities = [nck/N for x,nck in collections.Counter(lista).items()if x == term]
    e_x = [-p_x*math.log(p_x,2) for p_x in probabilities]
    print("RESULTADO PROB CON TERMINO = " +str(sum(probabilities)))
    print("E(c) CON TERMINO "+ str(term) +" = " + str(sum(e_x)))
    
    return sum(e_x)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def estimate_shannon_entropy(dna_sequence):
    m = len(dna_sequence)
    bases = collections.Counter([tmp_base for tmp_base in dna_sequence])
    
    shannon_entropy_value = 0
    for base in bases:
        # number of residues
        n_i = bases[base]
        # n_i (# residues type i) / M (# residues in column)
        p_i = n_i / float(m)
        entropy_i = p_i * (math.log(p_i, 2))
        shannon_entropy_value += entropy_i
 
    return shannon_entropy_value * -1
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def leerArchivosComplejos(txt):
    #txt = "pref_dicc.txt"
    #leerArchivosComplejos("pref_dicc.txt")
    f = open(txt, "r")
    lista = []
    while(True):
        linea = f.readline()
        if not linea:
            break
        datos = linea.split()
        #print ("TOPICS: " +str(datos[0]))
        #print ("nik: "+ str(datos[1]))
        #print ("pares: "+ str(datos[2]))
        pares = datos[2].split("/")
        datoi = []
        for y in range(0,len(pares)):
            dato = pares[y].split(",")
            datoi += [dato]
            #print ("clase: "+ str(dato[0]))
            #print ("freq: "+ str(dato[1]))
        lista += [[datos[0],datos[1],datoi]]    
    #print(lista) 
    f.close()
    return lista
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def leerArchivosSimples(txt):
    #txt = "pref_clases.txt"
    f = open(txt, "r")
    lista = []
    while(True):
        linea = f.readline()
        if not linea:
            break
        datos = linea.split()
        lista += [datos]    
    #print(lista) 
    f.close()
    return lista
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#crearArchivos(".\\reut2-001.sgm",3,5,"pref_")
