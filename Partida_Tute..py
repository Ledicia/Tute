# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 10:40:41 2020

@author: ledicia.diaz
"""

import reglas_juego as rj
from Clases_Tute.Baraja import Baraja
from Clases_Tute.Jugadores import jugador_maquina


def repartir_algunas_cartas(jugador1, jugador2, baraja, num_cartas):
    for i in range(num_cartas):
        jugador1.coger_carta(baraja.coger_carta())
        jugador2.coger_carta(baraja.coger_carta())
    return

def ganador(total_puntos_j1, total_puntos_j2):
    if total_puntos_j1 > total_puntos_j2:
        print('El ganador es el jugador 1 con ' + str(total_puntos_j1) + ' frente a '+ str(total_puntos_j2) + ' puntos del jugador 2')
    elif total_puntos_j1 < total_puntos_j2:
        print('El ganador es el jugador 2 con ' + str(total_puntos_j2) + ' frente a '+ str(total_puntos_j1) + ' puntos del jugador 1')
    else:
        print('Los jugadores 1 y 2 han empatado')


## JUEGO ##
if __name__ == '__main__':

    ## 1. Creacion de la baraja de cartas
    Baraja = Baraja()

    ## 2. Reparto de las cartas a cada jugador
    inf_cartas = Baraja.repartir_todas_las_cartas(jugadores = 2)
    palo_triunfo = inf_cartas['palo_triunfo'][0][0]
    cartas_jugador1 = inf_cartas['cartas_jugador1']
    cartas_jugador2 = inf_cartas['cartas_jugador2']

    ## 3. Creacion de las instancias de la clase jugador, una instancia por cada jugador
    # Repartimos todas las cartas:
    jugador1 = jugador_maquina('jugador1', cartas_jugador1)
    jugador2 = jugador_maquina('jugador2', cartas_jugador2)

    ## Repartir algunas cartas:
    # jugador1 = jugador_maquina('jugador1')
    # jugador2 = jugador_maquina('jugador2')
    # repartir_algunas_cartas(jugador1, jugador2, Baraja, 10)

    ## 4. Contadores para los ganadores de las bazas
    num_bazas_ganadas1 = 0
    num_bazas_ganadas2 = 0

    ## 5. Booleano para saber que jugador empieza
    empieza_jugador1 = True

    bazas_jugadas = 0
    while jugador1.tengo_cartas():
        # Lista que contiene las cartas jugadas por baza
        cartas_jugadas_por_baza = []
        if empieza_jugador1 == True:
            if bazas_jugadas == 0:
                print('Empieza el jugador 1')
            else:
                print('Empieza el jugador 1 porque ha ganado la baza anterior')

            carta_salida = jugador1.jugada(cartas_jugadas_por_baza, palo_triunfo)
            palo_salida = carta_salida[0]
            cartas_jugadas_por_baza.append(carta_salida)

            carta_jugador2 = jugador2.jugada(cartas_jugadas_por_baza, palo_triunfo)
            cartas_jugadas_por_baza.append(carta_jugador2)

            inf_ganador_baza = rj.ganador_baza(cartas_jugadas_por_baza, palo_salida, palo_triunfo)
            ganador_baza = inf_ganador_baza[0]
            cartas_ganadas = inf_ganador_baza[1]

            if ganador_baza == 'jugador1':
                empieza_jugador1 = True
                jugador1.actualizar_num_bazas_ganadas()
                jugador1.sumar_puntos(cartas_ganadas, palo_triunfo)
                print('El jugador 1 gana la baza numero ' + str(jugador1.num_bazas_ganadas))
            elif ganador_baza == 'jugador2':
                empieza_jugador1 = False
                jugador2.actualizar_num_bazas_ganadas()
                jugador2.sumar_puntos(cartas_ganadas, palo_triunfo)
                print('El jugador 2 gana la baza numero ' + str(jugador2.num_bazas_ganadas))

            print('El jugador ' + str(ganador_baza) + ' gana la baza con las cartas ' + str(cartas_ganadas))

            bazas_jugadas += 1            # Se actualizan las bazas jugadas
            cartas_jugadas_por_baza = []  # Se resetean las cartas cuando se termina la primera baza

        else:
            print('Empieza el jugador 2 porque ha ganado la baza anterior')

            carta_salida = jugador2.jugada(cartas_jugadas_por_baza, palo_triunfo)
            palo_salida = carta_salida[0]
            cartas_jugadas_por_baza.append(carta_salida)

            carta_jugador1 = jugador1.jugada(cartas_jugadas_por_baza, palo_triunfo)
            cartas_jugadas_por_baza.append(carta_jugador1)

            inf_ganador_baza = rj.ganador_baza(cartas_jugadas_por_baza, palo_salida, palo_triunfo)
            ganador_baza = inf_ganador_baza[0]
            cartas_ganadas = inf_ganador_baza[1]

            if ganador_baza == 'jugador1':
                empieza_jugador1 = True
                jugador1.actualizar_num_bazas_ganadas()
                jugador1.sumar_puntos(cartas_ganadas, palo_triunfo)
                print('El jugador 1 gana la baza numero ' + str(jugador1.num_bazas_ganadas))
            elif ganador_baza == 'jugador2':
                empieza_jugador1 = False
                jugador2.actualizar_num_bazas_ganadas()
                jugador2.sumar_puntos(cartas_ganadas, palo_triunfo)
                print('El jugador 2 gana la baza numero ' + str(jugador2.num_bazas_ganadas))

            print('El jugador ' + str(ganador_baza) + ' gana la baza con las cartas ' + str(cartas_ganadas))

            bazas_jugadas += 1  # Se actualizan las bazas jugadas
            cartas_jugadas_por_baza = []  # Se resetean las cartas cuando se termina la primera baza

    ganador(jugador1.puntos, jugador2.puntos)


