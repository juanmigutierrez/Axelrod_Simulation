
#-*- coding: utf-8 -*-
from random import uniform
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import scipy as sp

random.seed(time.time())

# *******************************************************************
# DEFINICIONES DE OBJETOS Y FUNCIONES
# *******************************************************************

class Jugadores():
    # Se define un objeto jugadores con tres propiedades
    def __init__(self, S, B, V):
        self.Score = S
        self.Boldness = B
        self.Vengefulness = V

def Imprimir_Jugador(j, Personas):
    print("Score: " + str(Personas[j].Score))
    print("Boldness: " + str(Personas[j].Boldness))
    print("Vengefulness: " + str(Personas[j].Vengefulness))

def Iteracion(Poblacion):
    Corrompe_norma=[]
    for u in range(len(Poblacion)):
        #Le damos a cada habitante 4 oportunidades para no cumplir la norma
        for k in range(0,4):
            s = uniform(0,1)
            b = Poblacion[u].Boldness
            if s < b:
                Poblacion[u].Score +=3
                Corrompe_norma.append(0)
                for y in range(len(Poblacion)):
                    if y!=u:
                        Poblacion[y].Score += -1
                        if s < Poblacion[y].Vengefulness:
                            Poblacion[u].Score += -9
                            Poblacion[y].Score += -2
            else:
                Corrompe_norma.append(1)
    return Poblacion, Corrompe_norma

def Experimento():
    # Inicializamos las variables
    Personas = []
    Scores =[]
    Boldness_1 =[]
    Vengefulness_1 = []
    Corrompe_norma_1 = []

    # Creamos la poblacion inicial donde cada habitante tiene un nivel aleatorio de boldness y vengefulness
    for i in range(0,20):
        Bold = randint(0,7)
        Prob_Bold= Bold/7 #int(round(x)) redondea el numero decimal al entero mas cercano 

        Veng = randint(0,7)
        Prob_Veng = Veng/7

        Personas.append(Jugadores(0, Prob_Bold, Prob_Veng))

    #Creamos un bucle para iterar 100 nuevas generaciones
    print("Corriendo iteraciones...")
    for y in range(0,NumGeneraciones):

        Personas, aux = Iteracion(Personas)

        Scores.append([u.Score for u in Personas])
        # print "i: " + str(y) + " Scores: ", Scores
        Boldness_1.append([u.Boldness for u in Personas])
        Vengefulness_1.append([u.Vengefulness for u in Personas])
        Corrompe_norma_1.append(aux)

        # Halla el promedio del Score y su desvacion estándar
        M = np.mean(Scores)
        # print "El promedio de scores es: " + str(M)
        std_deviation = np.std(Scores)
        # print "La desv. est. de scores es: " + str(std_deviation)

        # M = np.mean(Boldness_1)
        # print "El promedio de boldness es: " + str(M)
        #
        # M = np.mean(Vengefulness_1)
        # print "El promedio de vengefulness es: " + str(M)


        # Identifica a los buenos y a los regulares
        Personas_nuevas =[]

        for i in range(len(Personas)):
            x = (Personas[i].Score-M)/std_deviation
            if Personas[i].Score >= M + 1*std_deviation: 
                Personas_nuevas.append(Jugadores(0, Personas[i].Boldness, Personas[i].Vengefulness))
                Personas_nuevas.append(Jugadores(0, Personas[i].Boldness, Personas[i].Vengefulness))
            elif Personas[i].Score >= M and Personas[i].Score < M + 1*std_deviation:
                Personas_nuevas.append(Jugadores(0, Personas[i].Boldness, Personas[i].Vengefulness))


        # print "Lista de buenos (tamano " + str(len(indices_buenos)) + ")"
        # print indices_buenos
        # print "Lista de regulares (tamano " + str(len(indices_regulares)) + ")"
        # print indices_regulares

        # Se crea una nueva lista dependiendo de la descendencia de los buenos y los 			regulares

        # print "Tamano de los nuevos regulares: " + str(len(Personas_nuevas))

        if len(Personas_nuevas)<=20:
            Personas = Personas_nuevas
            x = 20 - len(Personas)
            for i in range(x):
                Bold = randint(0,7)
                Prob_Bold= Bold/7 #int(round(x)) redondea el numero decimal al entero mas cercano 
                
                Veng = randint(0,7)
                Prob_Veng = Veng/7

                Personas.append(Jugadores(0, Prob_Bold, Prob_Veng))
        else:
            Personas = Personas_nuevas[:20]


        #Mutación
        for i in range(len(Personas)):
            mutation = uniform(0,101)
            if mutation <1:
                Bold = randint(0,7)
                Prob_Bold= Bold/7 #int(round(x)) redondea el numero decimal al entero mas cercano 
                
                Veng = randint(0,7)
                Prob_Veng = Veng/7

                Personas[i].Boldness = Prob_Bold
                Personas[i].Vengefulness = Prob_Veng


    return Scores,Boldness_1,Vengefulness_1,Corrompe_norma_1

# *******************************************************************
# PARAMETROS DEL MODELO
# *******************************************************************

NumExp = 10
NumGeneraciones = 100

# *******************************************************************

X = []
Y = []
Z = []
U = []
Boldness_Av = []
Vengefulness_Av = []

# Esto dentro de un bucle
for i in range(NumExp):
    print("Comenzando experimento " + str(i) + "esimo")
    Scores,Boldness_1,Vengefulness_1,Corrompe_norma_1 = Experimento()
    Boldness_Av.append(Boldness_1[len(Boldness_1)-1])
    Vengefulness_Av.append(Vengefulness_1[len(Vengefulness_1)-1])
    # for i in range(len(x)):
    #     print "i: " + str(i) + " x: " + str(x[i])
    x = [np.mean(u) for u in Scores]
    y = [np.mean(u) for u in Boldness_1]
    z = [np.mean(u) for u in Vengefulness_1]
    u = [np.mean(u) for u in Corrompe_norma_1]
    X.append(x)
    Y.append(y)
    Z.append(z)
    U.append(u)



# Grafica Axelrod Básica

plt.xlabel("Boldness")
plt.ylabel("Vengefullness")
plt.title('Norms Game Dynamics')
plt.ylim([0.0, 1.0])
plt.xlim([0.0, 1.0])
plt.plot([np.mean(u) for u in Vengefulness_Av],[np.mean(u) for u in Boldness_Av],'D',color = 'grey')
plt.savefig("Norms_Game_Dynamics.png")
plt.show()

# Hallamos los promedios por experimento
x = []
for i in range(NumGeneraciones):
    gen = [e[i] for e in X]
    x.append(np.mean(gen))

y = []
for i in range(NumGeneraciones):
    gen = [e[i] for e in Y]
    y.append(np.mean(gen))

z = []
for i in range(NumGeneraciones):
    gen = [e[i] for e in Z]
    z.append(np.mean(gen))

u = []
for i in range(NumGeneraciones):
    gen = [e[i] for e in U]
    u.append(np.mean(gen))


#Graficar Vengefullnes Y Boldness Unico // Solo estamos graficando el ultimo experimento ojo ! 
fig, ax = plt.subplots()

ax.plot(z,color = 'grey',label = "Boldness")
ax.plot(y,color = 'black' , linestyle = '--',label = "Vengefulness")

plt.xlabel("Time")
plt.ylabel("Value")
plt.legend()
plt.ylim([0.0, 1.0])
plt.yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
plt.xlim([0.0, NumGeneraciones])
plt.savefig("Experimento.png")
plt.show()

# print Corrompe_norma_1
# print "Listo!"

print("Dibujando...")
# f, axarr = plt.subplots(4, sharex=True)
f, axarr = plt.subplots(4)


axarr[0].set_ylabel('Score')
axarr[1].set_ylabel('Boldness')
axarr[1].set_ylim(-0.1, 1.1)
axarr[2].set_ylabel('Vengefulness')
axarr[2].set_ylim(-0.1, 1.1)
axarr[3].set_ylabel('Norma')
axarr[3].set_ylim(-0.1, 1.1)
axarr[3].set_xlabel('Generation')

axarr[0].plot(x)
axarr[1].plot(y)
axarr[2].plot(z)
axarr[3].plot(u)
# axarr[1].plot( y, 'y--', linewidth = 1)
# axarr[2].plot( z, 'r-.', linewidth = 1)
#axarr[0].set_title('Boldness =' + str(Boldness_inicial) + ' Vengefulness =' + str(Vengefulness_inicial))

# axarr[1].scatter(x, y)
plt.savefig("Multiple.png")
plt.show()

# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# #ax1.set_title("Temperatura del panal vs. tiempo")
# # ax1.set_xlabel('t (time)')
# # ax1.set_ylabel('T (temperature)')
# # ax1.set_ylim([29, 33])
# ax1.plot([np.mean(u) for u in Scores], marker="v", ls='-') # , 'x', c = 'black', linewidth=4)
# ax1.plot([np.mean(u) for u in Boldness_1], marker="o",ls='-') # , 'x', c = 'black', linewidth=4)
# plt.show()
# #ax1.plot(Tp, c='black')
