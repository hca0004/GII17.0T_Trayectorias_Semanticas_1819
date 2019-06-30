# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 18:54:01 2019

@author: Hector
"""

from load.LoadCSV import LoadCSV 
from time import time
from load.CrearTrayectoriaB import CrearTrayectoriaB
from load.ConfiguracionDeLectura import ConfiguracionDeLectura as CDL
from modelo.TrayectoriaConceptual import TrayectoriaConceptual
from modelo.TrayectoriaSemantica import TrayectoriasSemantica
from load.Contadores import idUsuario
from SQL import SQLInsert as si
from SQL import SQLSelect as ss
from SQL import SQLUpdate as su
from nominatim import peticion as pet
import numpy as np

start=time()
def cargarDeSQLConceptuales():
    l=ss.cargarTrayectoriasConceptuales()
    print(len(l))
    return l
def cargarDeSQLBrutas():
    l=ss.cargarTrayectoriasBrutas(Where="where public.trayectoria.id_usuario=1")
    print(len(l))
def cargarDatosCSV2SQL(x,y,t,ts,exten,lineaIni,dir):
    contaUsu=idUsuario()
    direccion="E:/TFG/Data"#"E:/TFG/Data GPX"
    exten='.plt'#'.csv'
    x=1 #Longitud
    y=0 #Latitud

    r=list()
    #cdl=CDL(x=3,y=2,t=[1],ts=["%Y-%m-%dT%H:%M:%SZ"],extension=".csv",lineaIni=1)
    cdl=CDL(x=x,y=y,t=[5,6],ts=["%Y-%m-%d","%H:%M:%S"],extension=exten,lineaIni=6)
    usuarios=list()
    conceptuales=list()
    conta=0
    
    #lectorCSV=LoadCSV(x,y,[(5,"%Y-%m-%d"),(6,"%H:%M:%S")],exten,'epsg:4326',6)
    lectorCSV=LoadCSV(cdl)
    for i in lectorCSV.rutasPorUsuario(direccion):
        usuario=contaUsu.cId()
        usuarios.append(usuario)
        procesar=CrearTrayectoriaB(args=[i,usuario,0,1,2,3])
        r.extend(procesar.run())
        for j in range(len(r)):
            conceptuales.append(TrayectoriaConceptual(r[j]))
        si.insertUsuarios(usuarios)
        si.insertTrayectoria(r)
        si.insertarTrayectoriaConceptual(conceptuales)
        print(conta)
        r=list()
        conceptuales=list()
        usuarios=list()
        conta+=1
def guardarIdOSM():    
    l=cargarDeSQLConceptuales()
    for i in l:
        l3=list()    
        for j in range(len(i.getGDF())):
            l3.append([j,i.getIdTrayectoria(),pet.getNominatimIdOSM(i.getGDF()["punto"].iloc[j].y,i.getGDF()["punto"].iloc[j].x)])
        su.updateIdOSM(l3)
def cargarRutas(From,Where):
    from prediccion import Conversor as con
    from prediccion import Probador as pro

    conversor=con.Conversor()
    ltc=ss.cargarTrayectoriasConceptuales(From=From, Where=Where)
    listasOSM=conversor.TStoIdOSM(conversor.TCtoTS(ltc))
    p=pro.Probador(listasOSM)
    fmeasure,precision,recall,aciertos,fallos=p.validacionCruzada("category",division=5,minSupport=0.1)
    print(fmeasure,precision,recall,aciertos,fallos)
cargarRutas("FROM public.parado ","Where trayectoria.id_usuario=17")


#from prediccion import Probador as pro
#from prediccion import Conversor as con
#from prediccion import ClusteringMatrices as CM
###153
##conversor=con.Conversor()
##clus=CM.ClusteringMatrices()
##for i in [3]:
#ltc=ss.cargarTrayectoriasConceptuales(From=" FROM public.parado ", Where="   where   EXTRACT(ISODOW FROM parado.instante_inicio) IN (1,2,3,4,5,6,7)  and trayectoria.id_usuario=1")
#print(len(ltc))
#    listasOSM=conversor.TStoIdOSM(conversor.TCtoTS(ltc))
#    p=pro.Probador(listasOSM)
#    for i in range(50):
#        p.validacionCruzada("category",division=5,minSupport=0.01*i)
#
#    print(p.getEstadisticos())
#    p.graficos()
#print(clus.Clustering(agrupar=3,ID_Usuario_ini=0,ID_Usuario_fin=20))



#aciertos=0
#fallos=0
#
#for i in range(0,6):
#    a,f=probarClasificador(u=i)
#    aciertos=aciertos+a
#    fallos=fallos+f
#print("Aciertos:",aciertos,"Fallos:",fallos)
#print("Porcentaje de aciertos:",100/(aciertos+fallos)*aciertos)
#guardarIdOSM()
#cargarDeSQLBrutas()
