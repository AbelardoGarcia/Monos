#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pilasengine
import random

fin_de_juego = False

pilas = pilasengine.iniciar()

pilas.fondos.Espacio()
puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.rojo)
puntos.magnitud = 40
pilas.actores.Sonido()

# Variables y Constantes
balas_simples = pilas.actores.Bala
monos = []

# Funciones
def mono_destruido(disparo, enemigo):
    enemigo.eliminar()
    disparo.eliminar()
    del monos[monos.index(enemigo)]
    puntos.escala=[1, 0, 5, 1], .1
    puntos.aumentar(1)

def perder_fin(torreta, enemigo):
    global fin_de_juego
    enemigo.sonreir()
    enemigo.decir("Easy")
    torreta.eliminar()
    torreta.aprender(pilas.habilidades.PuedeExplotar)
    fin_de_juego=True
    pilas.avisar("Llegaste a %d puntos"%(puntos.obtener()))
    pilas.actores.Texto("GAME OVER")
    #Cuando finaliza el juego los monos sonrien y dicen "Easy" y la torreta se elimina  y provoca una explosion
def crear_mono():
    enemigo = pilas.actores.Mono()
    eh = random.uniform(.25, .75)
    enemigo.escala=[1, eh], .1
    enemigo.radio_de_colision = eh*50
    # El enemigo explota al ser impactado por una bala
    enemigo.aprender(pilas.habilidades.PuedeExplotar)
    # Aparece en una posicion al azar, alejado del jugador
    x = random.randrange(-340, 340)
    y = random.randrange(-240, 240)
    if x >= 0 and x <= 100:
        x = 180
    elif x <= 0 and x >= -100:
        x = -180
    if y >= 0 and y <= 100:
        y = 180
    elif y <= 0 and y >= -100:
        y = -180
    enemigo.x = x
    enemigo.y = y
    # El enemigo obtiene movimientos irregulares más impredecibles
    duracion = 1 +random.random()*4
    
    pilas.utils.interpolar(enemigo, 'x', 0, duracion)
    pilas.utils.interpolar(enemigo, 'y', 0, duracion)
    
    # Añadirlo a la lista de enemigos
    monos.append(enemigo)

    if  random.randrange(0,20)>15:
        if torreta.municion!=pilasengine.actores.Bomba:
            estrella=pilas.actores.Estrella(x, y)
            estrella.escala=[3,0,.3],.3
            pilas.colisiones.agregar(estrella,torreta.habilidades.DispararConClick.proyectiles,asignar_arma_mejorada)
            pilas.tareas.agregar(3, eliminar_estrella, estrella)

    # Se crean enemigos mientras el juego esté en activo
    if fin_de_juego:
        return False
    else:
        return True


def asignar_arma_simple():
    # Asignar la munición sencilla
    torreta.municion=pilasengine.actores.Bala

def asignar_arma_mejorada(estrella, proyectil):
    global torreta
    torreta.municion=pilasengine.actores.Misil
    estrella.eliminar()
    pilas.tareas.agregar(10, asignar_arma_simple)
    pilas.avisar("Mejora Activada")
    #Cuando colisiona una bala con la estrella se mejora el arma, comienza a disparar misiles y manda un mensaje en la esquina 
    #inferior izquierda avisando de que se mejoro el arma.
def eliminar_estrella(estrella):
    estrella.eliminar()
    #Se elimina la estrella cundo se pone en contacto con la bala.
# Añade la torreta del jugador
torreta = pilas.actores.Torreta(enemigos=monos, municion_bala_simple="bala", cuando_elimina_enemigo=mono_destruido)
torreta.municion=pilasengine.actores.Bala
pilas.tareas.agregar(1, crear_mono)
pilas.colisiones.agregar(torreta, monos, perder_fin)
# Inicia el juego
pilas.ejecutar()
