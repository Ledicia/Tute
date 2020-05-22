# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 10:40:41 2020

@author: ledicia.diaz
"""

import numpy as np
import random

class Carta:
    # Constructor del objeto carta
    def __init__(self, palo, numero):
        if not 0. < numero < 13.:
            raise TypeError('Número de carta incorrecto')
        if not palo in ['oros', 'bastos', 'espadas', 'copas']:
            raise TypeError('Nombre de palo incorrecto')
        self.palo = str(palo)
        self.numero = int(numero)

    # Funciones de la clase
    def puntos(self):
        puntos = {1: 11, 3: 10, 12: 4, 11: 3, 10: 2}
        if self.numero in puntos:
            puntos = puntos[self.numero]
        else:
            puntos = 0
        return puntos



class Baraja:
    # Constuctor del objeto baraja ya barajado
    def __init__(self):
        self.cartas = []
        palos = ['oros', 'bastos', 'espadas', 'copas']
        numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
        for i in palos:
            for j in numeros:
                self.cartas.append((i, j))
        random.shuffle(self.cartas)                 # Barajar/desordenar la baraja antes de repartir las cartas

    # Funciones de la clase:
    def repartir_todas_las_cartas(self, jugadores):
        if jugadores == 2:
            cartas_jugador1 = []; cartas_jugador2 = []
            while self.cartas:
                cartas_jugador1.append(self.cartas.pop())
                cartas_jugador2.append(self.cartas.pop())
            palo_triunfo = cartas_jugador2[-1:]  # La ultima carta es la que marca el triunfo
            d = {'palo_triunfo': palo_triunfo, 'cartas_jugador1': cartas_jugador1, 'cartas_jugador2': cartas_jugador2}
            return d
        if jugadores == 3:
            cartas_jugador1 = []; cartas_jugador2 = []; cartas_jugador3 = []
            cartas_a_repatir = int(self.cartas.__len__() / jugadores)*jugadores
            cartas_a_eliminar = self.cartas.__len__() - cartas_a_repatir
            for i in range(cartas_a_eliminar):
                self.cartas.pop()  # Para eliminar las cartas que no se pueden repartir
            while self.cartas:
                cartas_jugador1.append(self.cartas.pop())
                cartas_jugador2.append(self.cartas.pop())
                cartas_jugador3.append(self.cartas.pop())
            palo_triunfo = cartas_jugador3[-1:]  # La ultima carta es la que marca el triunfo
            d = {'palo_triunfo': palo_triunfo, 'cartas_jugador1': cartas_jugador1,
                 'cartas_jugador2': cartas_jugador2, 'cartas_jugador3': cartas_jugador3}
            return d
        if jugadores == 4:
            cartas_jugador1 = []; cartas_jugador2 = []; cartas_jugador3 = []; cartas_jugador4 = []
            while self.cartas:
                cartas_jugador1.append(self.cartas.pop())
                cartas_jugador2.append(self.cartas.pop())
                cartas_jugador3.append(self.cartas.pop())
                cartas_jugador4.append(self.cartas.pop())
            palo_triunfo = cartas_jugador4[-1:]  # La ultima carta es la que marca el triunfo
            d = {'palo_triunfo': palo_triunfo, 'cartas_jugador1': cartas_jugador1, 'cartas_jugador2': cartas_jugador2,
                 'cartas_jugador3': cartas_jugador3, 'cartas_jugador4': cartas_jugador4}
            return d

    # Para coger cartas de una en una si no se quieren repartir todas
    def coger_carta(self):
        carta_nueva = self.cartas.pop()
        # carta_nueva = self.cartas[0]
        # self.cartas = self.cartas[1:]
        return carta_nueva

    def quedan_cartas(self):
        return len(self.cartas) > 0

    def dar_palo(self):
        carta_nueva = self.cartas[0]
        self.cartas = self.cartas[1:]
        self.cartas.append(carta_nueva)
        return carta_nueva.palo



