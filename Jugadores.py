# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 10:40:41 2020

@author: ledicia.diaz
"""

import numpy as np
import baraja as Baraja
import reglas_juego as rj
import numpy.random as rd

class jugador_maquina:
    # Constructor de un jugador: el jugador tiene una mano, unos puntos, y un numero de bazas ganadas
    def __init__(self, name, cartas = None):
        self.puntos = 0
        self.num_bazas_ganadas = 0
        self.jugador = name
        # Si se reparten todas las cartas
        if cartas != None:
            self.mano = cartas
        # Si solo se reparten x cartas
        else:
            self.mano = []

    # Repartir un numero de cartas determinado
    def coger_carta(self, carta):
        self.mano.append(carta)

    # Si al jugador le quedan cartas puede seguir jugando
    def tengo_cartas(self):
        return self.mano.__len__() > 0

    # Accion que toma el jugador en funcion de las cartas que han sido jugadas
    def jugada(self, cartas_jugadas_por_baza, palo_triunfo):
        if cartas_jugadas_por_baza.__len__() != 0:

            carta_salida = cartas_jugadas_por_baza[0]  # tupla (palo, numero)
            palo_salida = carta_salida[0]

            ## 1. Obligacion de montar/asistir
            cartas_montar_asistir = [item for item in self.mano if item[0] == palo_salida]
            # En caso de que su longitud sea nula el jugador no puede ni montar ni asistir -> tiene que fallar
            if cartas_montar_asistir.__len__() != 0:
                carta_jugada = rj.montar_o_asistir(cartas_montar_asistir, carta_salida)
                rj.actualizar_mano(self.mano, carta_jugada)  # Elimina la carta_jugada de self.mano

            ## 2. Obligacion de fallar
            else:
                cartas_fallar = [item for item in self.mano if item[0] == palo_triunfo]
                # En caso de que su longitud sea nula el jugador no puede fallar -> tiene que jugar una carta cualqueira
                if cartas_fallar.__len__() != 0:
                    carta_jugada = rj.fallar(cartas_fallar)
                    rj.actualizar_mano(self.mano, carta_jugada)

                ## 3. En caso de no poder ni montar ni asistir ni fallar se juega una carta aleatoria (la peor que se tenga)
                else:
                    carta_jugada = rj.carta_aleatoria(self.mano)
                    rj.actualizar_mano(self.mano, carta_jugada)
            return carta_jugada
        else:
            numero_random = int(rd.random() * len(self.mano))
            carta_salida = self.mano.pop(
                numero_random)  # Al hacer un pop() no hace falta actualizar la mano porque se actualiza sola
            return carta_salida

    # Actualizar el numero de bazas ganadas: asi se puede determinar si se puede cantar
    def actualizar_num_bazas_ganadas(self):
        self.num_bazas_ganadas += 1
        print(self.num_bazas_ganadas)

    def cantar(self, palo_triunfo):

        # Booleanos para cantar
        palos_cantar_20 = ['oros', 'espadas', 'bastos', 'copas']
        palos_cantar_20.remove(palo_triunfo)
        cantar_20_list = []
        cantar_20_list.append((palos_cantar_20[0], 11) in self.mano and (palos_cantar_20[0], 12) in self.mano)
        cantar_20_list.append((palos_cantar_20[1], 11) in self.mano and (palos_cantar_20[1], 12) in self.mano)
        cantar_20_list.append((palos_cantar_20[2], 11) in self.mano and (palos_cantar_20[2], 12) in self.mano)
        cantar_20 = cantar_20_list[cantar_20_list == True]

        cantar_40 = (palo_triunfo, 11) in self.mano and (palo_triunfo, 12) in self.mano

        cantar_40_20 = False

        puntuacion = 0
        if self.num_bazas_ganadas == 1:
            if cantar_40 == True:
                puntuacion = 40
                cantar_40_20 = True
                print('El ' + str(self.jugador) + ' canta las 40')
            elif cantar_20 == True:
                puntuacion = 20
                print('El ' + str(self.jugador) + ' canta las 20')

        if self.num_bazas_ganadas == 2 and cantar_20 == True and cantar_40_20 == True:
            puntuacion = 20
            print('El ' + str(self.jugador) + ' canta las 20 ademas de haber cantado las 40')

        return puntuacion

    # Puntos que va acumulando el jugador
    def sumar_puntos(self, cartas_ganadas, palo_triunfo):
        self.puntos += self.cantar(palo_triunfo)
        for i in cartas_ganadas:
            self.puntos += rj.puntos(i[1])


class jugador_humano:
    # Constructor de un jugador: el jugador tiene una mano, unos puntos, y un numero de bazas ganadas
    def __init__(self, name, cartas = None):
        self.puntos = 0
        self.num_bazas_ganadas = 0
        self.jugador = name
        # Si se reparten todas las cartas
        if cartas != None:
            self.mano = cartas
        # Si solo se reparten x cartas
        else:
            self.mano = []

    # Repartir un numero de cartas determinado
    def coger_carta(self, carta):
        self.mano.append(carta)

    # Si al jugador le quedan cartas puede seguir jugando
    def tengo_cartas(self):
        return self.mano.__len__() > 0

    def coger_carta(self, carta):
        self.mano.append(carta)

    def sumar_puntos(self, puntos):
        self.puntos += puntos

    def jugar_carta(self, palo=None, numero=None, palo_partida=None):
        print('Tu mano actual es: ')
        print(self.print_mano())
        carta = input('Introduce la carta que quieres jugar como una tupla (str(palo), numero)')
        return self.mano.pop(self.mano(carta))

    def print_mano(self):
        lista = []
        for i in self.mano:
            lista.append(str(i))
        return lista

