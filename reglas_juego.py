# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 10:40:41 2020

@author: ledicia.diaz
"""

import numpy.random as rd
import numpy as np

## 1. Definir el numero de bazas que se juegan durante una partida:
# Cada vez que se completa una baza un jugador gana una serie de puntos
def num_bazas(num_jugadores = 2, num_cartas = 40):
    return int(num_cartas/num_jugadores)


## 2. Definir el valor de las cartas:
def puntos(num_carta):
    puntos = {1: 11, 3: 10, 12: 4, 11: 3, 10: 2}
    try:
        puntos = puntos[num_carta]
    except:
        puntos = 0
    return puntos


## 3. Actualizar la mano de cada jugador:
def actualizar_mano(cartas_jugador, carta_jugada):
    try:
        cartas_jugador.remove(carta_jugada)
    except ValueError:
        pass
        # print('{} no se encuentra en la lista'.format(carta_jugada))
    return cartas_jugador


## REGLAS DEL JUEGO ##
#-----------------------------------------------------------------------------------------------------------------------
# Si se tiene un carta del palo de salida:
    # 1. Obligacion de montar
    # 2. Obligacion de asistir
# Si no se tiene pero se tiene una del palo del triunfo
    # Obligacion de fallar/jugarla (en funcion de como avance el juego sera mejor echar una u otra si se tienen varias)
# Si no se puede ni montar ni asisitir ni fallar:
    # Se puede jugar cualquier carta

# El ganador de la baza es el que abre el juego

# Canticos: Solo se pueden hacer cuando se gana la priemra baza y hay dos tipos:
    # Se tiene un caballo y un rey del mismo palo que no es el palo del triunfo: ganas 20 puntos
    # Se tiene un caballo y un rey del mismo palo que ademas son del palo del triunfo: ganas 40 puntos
#-----------------------------------------------------------------------------------------------------------------------

## 4. Montar/Asistir
# cartas_posibles_jugador: cartas del jugador que permiten montar o asistir
# carta_salida = (palo, numero): numero que tenemos que superara para montar o tirar una inferior para asistir
# cartas_jugadas_por_baza: se podria incluir para adaptar un algoritmo mas complejo en funcion del numero de jugadores
def montar_o_asistir(cartas_posibles_jugador, carta_salida):
    cartas_para_montar = [item for item in cartas_posibles_jugador if puntos(item[1]) > puntos(carta_salida[1])]
    if cartas_para_montar.__len__() != 0:
        print('El jugador monta')
        carta_jugada = max(cartas_posibles_jugador, key=lambda x: puntos(x[1]))
    else:
        print('El jugador asiste')
        # Actualizar el algoritmo en base al transcurso de la partida (numero de cartas jugadas) ya que e sposible que
        # si estoy al ppio el otro jugador tb tenga cartas del palo de salida y no pueda llevarse el triunfo
        # No obstante, si la partida esta avanzada, las probabilidades de que tenga carta del palo de salida se reducen
        # aumentando sus probabilidades de llevarse el triunfo
        carta_jugada = min(cartas_posibles_jugador, key=lambda x: puntos(x[1]))
    return carta_jugada


## 5. Fallar:
# Supongo que siempre quiero jugar el triunfo maximo para saber que me lo llevo seguro
# Para implementar mas de dos jugadores ademas deberia de pasarle a la funcion las cartas jugadas por los jugadores previos
# y las bazas que se han jugado para hacer una funcion probabilistica de decision
def fallar(cartas_posibles_jugador):
    print('El jugador falla')
    carta_jugada = max(cartas_posibles_jugador, key=lambda x: puntos(x[1]))
    return carta_jugada


## 6. Jugar cualquier carta
# cartas_posibles_jugador: todas las cartas de la baraja del jugador cuando este no tiene ni palo de salida ni palo de triunfo
def carta_aleatoria(cartas_posibles_jugador):
    print('El jugador no puede montar, ni asistir, ni fallar')
    carta_jugada = min(cartas_posibles_jugador, key=lambda x: puntos(x[1]))
    return carta_jugada


## 7. Accion que toma el jugador en funcion de sus cartas y de las cartas jugadas previamente (la de salida en este caso)
def accion_jugador(cartas_jugadas_por_baza, palo_triunfo, cartas_jugador):

    carta_salida = cartas_jugadas_por_baza[0]     # tupla (palo, numero)
    palo_salida = carta_salida[0]

    ## 1. Obligacion de montar/asistir
    cartas_montar_asistir = [item for item in cartas_jugador if item[0] == palo_salida]
    # En caso de que su longitud sea nula el jugador no puede ni montar ni asistir -> tiene que fallar
    if cartas_montar_asistir.__len__() != 0:
        carta_jugada = montar_o_asistir(cartas_montar_asistir, carta_salida)
        cartas_jugador = actualizar_mano(cartas_jugador, carta_jugada)

    ## 2. Obligacion de fallar
    else:
        cartas_fallar = [item for item in cartas_jugador if item[0] == palo_triunfo]
        # En caso de que su longitud sea nula el jugador no puede fallar -> tiene que jugar una carta cualqueira
        if cartas_fallar.__len__() != 0:
            carta_jugada = fallar(cartas_fallar)
            cartas_jugador = actualizar_mano(cartas_jugador, carta_jugada)

        ## 3. En caso de no poder ni montar ni asistir ni fallar se juega una carta aleatoria (la peor que se tenga)
        else:
            carta_jugada = carta_aleatoria(cartas_jugador)
            cartas_jugador = actualizar_mano(cartas_jugador, carta_jugada)

    return carta_jugada, cartas_jugador


## 8. Ganador de la baza:
## Gana el jugador que tira el triunfo más alto, o en caso de que no haya triunfo,
# la carta de más valor que sea del palo de salida (carta que haya salido el primer jugador en la ronda)
def ganador_baza(cartas_jugadas_por_baza, palo_salida, palo_triunfo):

    # ganador_baza: tupla que contiene el jugador ganador, las cartas que se lleva y un 1 (baza ganada)
    ganador_baza = None

    puntos_jugador1 = puntos(cartas_jugadas_por_baza[0][1])
    palo_jugador1 = cartas_jugadas_por_baza[0][0]
    puntos_jugador2 = puntos(cartas_jugadas_por_baza[1][1])
    palo_jugador2 = cartas_jugadas_por_baza[1][0]

    if palo_jugador1 == palo_salida and palo_jugador2 != palo_triunfo and puntos_jugador1 > puntos_jugador2:
        print('Gana el jugador 1')
        num_bazas_ganadas1 = 1
        ganador_baza = ('jugador1', cartas_jugadas_por_baza, num_bazas_ganadas1)
    elif palo_jugador2 == palo_salida and palo_jugador1 != palo_triunfo and puntos_jugador1 < puntos_jugador2:
        print('Gana el jugador 2')
        num_bazas_ganadas2 = 1
        ganador_baza = ('jugador2', cartas_jugadas_por_baza, num_bazas_ganadas2)
    elif palo_jugador1 == palo_triunfo and palo_jugador2 == palo_triunfo and puntos_jugador1 > puntos_jugador2:
        print('Gana el jugador 1')
        num_bazas_ganadas1 = 1
        ganador_baza = ('jugador1', cartas_jugadas_por_baza, num_bazas_ganadas1)
    elif palo_jugador1 == palo_triunfo and palo_jugador2 == palo_triunfo and puntos_jugador1 < puntos_jugador2:
        print('Gana el jugador 2')
        num_bazas_ganadas2 = 1
        ganador_baza = ('jugador2', cartas_jugadas_por_baza, num_bazas_ganadas2)
    else:
        if cartas_jugadas_por_baza[0][1] > cartas_jugadas_por_baza[1][1]:
            num_bazas_ganadas1 = 1
            ganador_baza = ('jugador1', cartas_jugadas_por_baza, num_bazas_ganadas1)
        else:
            num_bazas_ganadas2 = 1
            ganador_baza = ('jugador2', cartas_jugadas_por_baza, num_bazas_ganadas2)

    return ganador_baza

## 9. Canticos
# inf_bazas_ganadas = ganador_baza(cartas_jugadas_por_baza, palo_salida, palo_triunfo)
# ganador_bazas = inf_bazas_ganadas[0]
# num_bazas_ganadas = inf_bazas_ganadas[2]
def cantico(cartas_jugador, ganador_bazas, num_bazas_ganadas, palo_triunfo):

    # Booleanos para cantar
    palos_cantar_20 = ['oros', 'espadas', 'bastos', 'copas']
    palos_cantar_20.remove(palo_triunfo)
    cantar_20_list = []
    cantar_20_list.append((palos_cantar_20[0], 11) in cartas_jugador and (palos_cantar_20[0], 12) in cartas_jugador)
    cantar_20_list.append((palos_cantar_20[1], 11) in cartas_jugador and (palos_cantar_20[1], 12) in cartas_jugador)
    cantar_20_list.append((palos_cantar_20[2], 11) in cartas_jugador and (palos_cantar_20[2], 12) in cartas_jugador)
    cantar_20 = cantar_20_list[cantar_20_list == True]

    cantar_40 = (palo_triunfo, 11) in cartas_jugador and (palo_triunfo, 12) in cartas_jugador

    cantar_40_20 = False

    puntuacion = 0
    if num_bazas_ganadas == 1:
        if cantar_40 == True:
            puntuacion = 40
            cantar_40_20 = True
            print('El ' + str(ganador_bazas) + ' canta las 40')
        elif cantar_20 == True:
            puntuacion = 20
            print('El ' + str(ganador_bazas) + ' canta las 20')

    if num_bazas_ganadas == 2 and cantar_20 == True and cantar_40_20 == True:
        puntuacion = 20
        print('El ' + str(ganador_bazas) + ' canta las 20 ademas de haber cantado las 40')

    return puntuacion

## 8. Sumar los puntos de cada baza
# inf_bazas_ganadas = ganador_baza(cartas_jugadas_por_baza, palo_salida, palo_triunfo)
# ganador_bazas = inf_bazas_ganadas[0]
# cartas_ganadas = inf_bazas_ganadas[1]
def contar_puntos(ganador_baza, cartas_ganadas):

    puntos_jugador1 = 0; puntos_jugador2 = 0; inf_puntuacion_baza = None
    if ganador_baza == 'jugador1':
        for i in cartas_ganadas:
            puntos_jugador1 += puntos(i[1])
        inf_puntuacion_baza = (ganador_baza, puntos_jugador1)
    elif ganador_baza == 'jugador2':
        for i in cartas_ganadas:
            puntos_jugador2 += puntos(i[1])
        inf_puntuacion_baza = (ganador_baza, puntos_jugador2)

    return inf_puntuacion_baza  # Tupla con el jugador que ha ganado la baza y los puntos que ha obtenido

def ganador(puntuacion_jugador1, puntuacion_jugador2):
    total_puntos_j1 = sum(puntuacion_jugador1)
    total_puntos_j2 = sum(puntuacion_jugador2)
    if total_puntos_j1 > total_puntos_j2:
        print('El ganador es el jugador 1 con ' + str(total_puntos_j1) + ' frente a '+ str(total_puntos_j2) + ' puntos del jugador 2')
    elif total_puntos_j1 < total_puntos_j2:
        print('El ganador es el jugador 2 con ' + str(total_puntos_j2) + ' frente a '+ str(total_puntos_j1) + ' puntos del jugador 1')
    else:
        print('Los jugadores 1 y 2 han empatado')

