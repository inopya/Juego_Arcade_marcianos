#!/usr/bin/env python
#-*- coding: UTF-8 -*-

#         _\|/_
#         (O-O)             A ver, que tenemos por aqui....
# -----oOO-(_)-OOo----------------------------------------------------


#######################################################################
# ******************************************************************* #
# *                       Mi Primer ARCADE PyGame                   * #
# *                    Autor: Eulogio López Cayuela                 * #
# *                                                                 * #
# *                  Versión 1.2    Fecha: 09/11/2014               * #
# *                                                                 * #
# ******************************************************************* #
#######################################################################



import pygame, random, sys
from pygame.locals import *

# ---------------------------------------------
# INICIO DEL BLOQUE DE DEFINICIÓN DE CONSTANTES
# ---------------------------------------------

# Definición de algunas 'CONSTANTES' que podemos modificar.
# En comentarios su explicación y sus valores de referrencia

''' Los datos de cada nivel de juego pueden ser modificados en la lista
de diccionarios 'NIVELES'.
Aconsejable hacer puebas sólo sobre el nivel 0 antes de modificar el
resto de niveles'''

#----------------------------------------------------------------------
# Numero de vidas con las que cuenta el jugador para la partida
MAX_VIDAS = 3

# Máximo numero de enemigos en pantalla simultaneamente
numeroEnemigosActivos = 40 #40

# El usuario puede decrementar (o 'recuperar') la velocidad de los
# enemigos mediante las teclas 'a' y 'z' que modificaran a esta variable
# (Mejor hacerlo durante el juego)
# No se puede aumentar la velocidad maxima definida para un nivel. 
frenoVelocidadEnemigo = 0 #0

# Establecer velocidad constante o variable para las naves Jefe
velocidadConstante = False # False, las naves JEFE tiene velociadad variable
velocidadJefe = 4 #4 Valor que se aplica si velocidadConstante = 'True'

# 'pausaEnemigos' Establece cada cuantos ciclos de programa se mueve al
# enemigo. Ha de ser un numero mayor de 0 o se produce division por
# cero. Valor 1, funcionamiento normal. Valores mayores sólo para
# ralentizar los enemigos en 'modo Debug' ya que se pueden producir
# pequeños saltos en la visualización
pausaEnemigos = 1 #1

# Numero de frames por segundo del juego. 40 es un valor óptimo para que
# las animaciones sean fluidas. Valores menores se pueden usar para
# frenar el juego, aunque no es aconsejable bajar demasiado si no se
# quiere perder la fluidez y 'naturalidad' de los movimientos.
FPS = 40 # 40 Número de frames por segundo del juego

# Evitar ser destruido por los enemigos. (Usar sólo con crios pequeños)
invencible = False #False  'True' evita ser destruido. Es bastante aburrido :-(

# Activar imagen de fondo, o por el contrario usar un color.
#E l valor color de fondo, 'BACKGROUND_COLOR' se define tras el bloque de
# definicion de colores (como es obvio)
fondoActivo = True # True
#----------------------------------------------------------------------

fondox = 0
fondoy = -3800
contadorMovimientoFondo = 0
pasoMovimientoFondo = 3

# DEFINICIÓN DE CONSTANTES PARA EL JUEGO

# Lleva el conteo de ciclos pausados si se utiliza pausaEnemigos.
#(NO modificar).
contadorPausaEnemigos = 0 

ANCHO_PANTALLA = 600
ALTO_PANTALLA = 700
# Bloque de definicion de colores con nombres para facilitar su uso.
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_ROJO = (255, 0, 0)
COLOR_VERDE = (0, 255, 0)
COLOR_AZUL = (0, 0, 255)
COLOR_AZUL_OSCURO = (0, 0, 100)
COLOR_AMARILLO = (255,255,0)
COLOR_BLANCO_SUCIO = (250, 250, 250) # Color Blanco sucio.
COLOR_NEGRO_SUCIO = (35, 25, 35) # Color Gris oscuro casi negro.
COLOR_ROSA = (255,0,210) # Color Rosa vivo.
COLOR_AZUL_CIELO = (45, 180, 235)

COLOR_BALA = COLOR_ROJO
BACKGROUND_COLOR = COLOR_NEGRO


# le indica al cargador de datos que está en el inicio de juego, carga
# todos los valores iniciales y posteriormente se establece en el
# valor 0 para iniciar juego por dicho nivel.
nivel = -1 

# Tipo de municion inicial
tipoMunicion = 'SIMPLE'

# Contadores para almacenar la cantidad de municion extra (si la hay)
municionExtraDoble = 0
municionExtraTriple = 0

# Reset inicial de los contadores de puntuacion y vidas
puntuacion_Max = 0
puntuacion_nivel = 0
PUNTUACION_DE_NIVEL = 0
puntuacionJuego = 0

# Numero de vidas con las que cuenta el jugador para la partida
NUMERO_VIDAS = 3

# lista para almacenar las balas y calcular colisiones
balas = [] 
# lista para almacenar los enemigos y los JEFES
enemigos = [] 
# lista para almacenar los enemigos destruidos y aimar sus explosiones
enemigos_destruidos = []
# reset de las condiciones de movimiento
moveLeft = moveRight = moveUp = moveDown = False
# Lleva la cuenta de ciclos de reloj entre la creacion de dos enemigos
contadorNuevoEnemigo = 0
# indica si exite vida para poder jugar
finDeVida = 0 #0 Existe vida

# Definir unos niveles de juego
# Valores de los niveles
NIVELES = [
    {'NIVEL': 0, #'NIVEL DE PRUEBAS'
     'PUNTUACION_DE_NIVEL': 100,#100 Puntos necesarios para superar nivel
     'ENEMIGO_MinSIZE': 35, #40 Tamaño mínimo de las naves enemigas
     'ENEMIGO_MaxSIZE': 40, #40 Tamaño máximo de las naves enemigas
     'ENEMIGO_MinSPEED': 1,#2 Velocidad mínima de las naves enemigas
     'ENEMIGO_MaxSPEED': 2,#2 Velocidad máxima de las naves enemigas
     'ESPERA_CREACION_ENEMIGOS': FPS,#30 Pausa para crear nuevos enemigos (en FPS)
     'VELOCIDAD_JUGADOR': 5,#10 Velocidad en pixeles del jugador si se usa teclado
     'NUMERO_JEFES': 100,# 100 Número maximo de jefes para el nivel
     'VALOR_NAVE_JEFE': 20, # puntos que obtenemos con las naves JEFE
    },

    {'NIVEL': 1,
     'PUNTUACION_DE_NIVEL': 250,
     'ENEMIGO_MinSIZE': 30,
     'ENEMIGO_MaxSIZE': 40,
     'ENEMIGO_MinSPEED': 4,
     'ENEMIGO_MaxSPEED': 6,
     'ESPERA_CREACION_ENEMIGOS': FPS-5,
     'VELOCIDAD_JUGADOR': 10,
     'NUMERO_JEFES': 20,
     'VALOR_NAVE_JEFE': 30,
    },
    {'NIVEL': 2,
     'PUNTUACION_DE_NIVEL': 350,
     'ENEMIGO_MinSIZE': 30,
     'ENEMIGO_MaxSIZE': 35,
     'ENEMIGO_MinSPEED': 6,
     'ENEMIGO_MaxSPEED': 8,
     'ESPERA_CREACION_ENEMIGOS': FPS-10,
     'VELOCIDAD_JUGADOR': 10,
     'NUMERO_JEFES': 15,
     'VALOR_NAVE_JEFE': 40,
    },
    {'NIVEL': 3,
     'PUNTUACION_DE_NIVEL': 350,
     'ENEMIGO_MinSIZE': 25,
     'ENEMIGO_MaxSIZE': 35,
     'ENEMIGO_MinSPEED': 6,
     'ENEMIGO_MaxSPEED': 10,
     'ESPERA_CREACION_ENEMIGOS': FPS-15,
     'VELOCIDAD_JUGADOR': 10,
     'NUMERO_JEFES': 13,
     'VALOR_NAVE_JEFE': 50,
    },
    {'NIVEL': 4,
     'PUNTUACION_DE_NIVEL': 450,
     'ENEMIGO_MinSIZE': 20,
     'ENEMIGO_MaxSIZE': 30,
     'ENEMIGO_MinSPEED': 8,
     'ENEMIGO_MaxSPEED': 12,
     'ESPERA_CREACION_ENEMIGOS': FPS-20,
     'VELOCIDAD_JUGADOR': 10,
     'NUMERO_JEFES': 10,
     'VALOR_NAVE_JEFE': 60,
    },
    {'NIVEL': 5,
     'PUNTUACION_DE_NIVEL': 750,
     'ENEMIGO_MinSIZE': 20,
     'ENEMIGO_MaxSIZE': 25,
     'ENEMIGO_MinSPEED': 10,
     'ENEMIGO_MaxSPEED': 14,
     'ESPERA_CREACION_ENEMIGOS': FPS-25,
     'VELOCIDAD_JUGADOR': 10,
     'NUMERO_JEFES': 10,
     'VALOR_NAVE_JEFE': 70,
    },]
# --------------------------------------------
# FIN DEL BLOQUE DE DEFINICIÓN DE CONSTANTES
# --------------------------------------------


# --------------------------------------------
# INICIO DEL BLOQUE DE DEFINICIÓN DE FUNCIONES
# --------------------------------------------

def fin_juego():
    guardar_records()
    pygame.quit()
    sys.exit()
# --------------------------------------------
def cargar_records():
    global RECORD
    f = open('records.txt', 'r')
    RECORD = f.read()
    f.close() 
# --------------------------------------------
def comprobar_y_mostrar_records():
    global RECORD
    RECORD = RECORD[:-1]
    # Recorremos 'RECORD' para encontrar los 'records' que están separadas por '\n'
    # y almacenamos dichas 'palabras' en la 'lista'
    listaRecords = []
    for dato in RECORD.split('\n'):
        listaRecords.append(dato)

    i = 0
    preguntar = True
    listaScore = []
    while i < len(listaRecords):
        registro = listaRecords[i]
        nombre = registro.split('***')[0]
        numero = registro.split('***')[-1]
        if preguntar == True and MaxPlayerScore >= int(numero):
            preguntar = False
            nombreNuevo = preguntar_nombre()
            recordNuevo = MaxPlayerScore
            listaScore.append([nombreNuevo, recordNuevo])
        listaScore.append([nombre, numero])
        i += 1

    if len (listaScore) > 6:
        listaScore = listaScore[:6]
    SCREEN.fill(BACKGROUND_COLOR)
    dibujar_Textos('PUNTUCIONES MÁXIMAS', font50, COLOR_ROJO, SCREEN, 0, (100),1)
    dibujar_Textos('Pulsa una tecla para continuar', font35, COLOR_VERDE,
                   SCREEN, 0, (ALTO_PANTALLA - 40),1)
    i = 0
    RECORD = ''
    # alternar colores para diferenciar las lineas entre usuarios
    colores = [COLOR_BLANCO, COLOR_AMARILLO]
    margenPantallaIz = (ANCHO_PANTALLA -300)/2
    margenPantallaDr = ANCHO_PANTALLA - margenPantallaIz
    while i < len (listaScore):
        jugador = str(listaScore[i][0])
        puntos = str(listaScore[i][1])
        separador = '          '
        puntosFormat = '%7.7s' % (puntos)
        color = colores[i%2]
        dibujar_Textos(jugador, font25, color, SCREEN, margenPantallaIz, (190+(i*30)),0)
        dibujar_Textos(puntosFormat, font25, color, SCREEN, margenPantallaDr, (190+(i*30)),2)
    
        RECORD += jugador + '***' + puntos + '\n'
        i += 1
    if preguntar == True:
        puntosFormat = '%7.7s' % (MaxPlayerScore)
        dibujar_Textos('Tu resultado', font25, COLOR_ROJO, SCREEN, margenPantallaIz, (190+(i*30)),0)
        dibujar_Textos(puntosFormat, font25, COLOR_ROJO, SCREEN, margenPantallaDr, (190+(i*30)),2)
        
    pygame.display.update()
    return
# --------------------------------------------
def preguntar_nombre():
    def formatear_cadena(nombre):
        '''crea una cadena de longitud 10, completando con espacios si es necesario'''
        cadenaFormateada = nombre[:-1] + "          "
        nombre = cadenaFormateada[:10]
        return(nombre)
    
    nombre = ''
    cursor = '_'
    pulsacion = ''
    nombre += cursor
    contador_parpadeo = 0
    pygame.event.set_allowed([KEYDOWN, KEYUP])
    devolverNombre = False
    while not devolverNombre:
        contador_parpadeo += 1
        if contador_parpadeo <= 150:
            cursor = ' '
        if contador_parpadeo > 150:
            cursor = '_'
        if contador_parpadeo >= 300:
            contador_parpadeo = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                nombre = formatear_cadena(nombre)
                return(nombre)
            if event.type is KEYDOWN:
                sonidoLaser.play()
                if event.key == K_SPACE: # pulsar 'barra espaciadora' para terminar
                    nombre = formatear_cadena(nombre)
                    return(nombre)
                if event.key == K_DELETE:
                    nombre = nombre[:-2] + cursor

                pulsacion = str(event.unicode)
                nombre = nombre[:-1] + pulsacion + cursor
        nombre = nombre[:-1] + cursor


        SCREEN.fill(COLOR_AZUL_OSCURO)
        dibujar_Textos(nombre, font40, COLOR_ROJO, SCREEN, 0, (ALTO_PANTALLA / 2),1)
        dibujar_Textos('NUEVO RECORD', font50, COLOR_BLANCO, SCREEN, 0, (ALTO_PANTALLA / 4),1)
        dibujar_Textos('Escribe tu nombre', font25, COLOR_BLANCO, SCREEN, 0, ((ALTO_PANTALLA / 4) + 30),1)
        dibujar_Textos('Pulsa ESPACIO para terminar', font20, COLOR_VERDE, SCREEN, 0, (ALTO_PANTALLA - 30),1)
        pygame.display.update()
    return(nombre)
# --------------------------------------------
def guardar_records():
    global RECORD
    f = open('records.txt', 'w') # Abrimos el fichero para escribir en el
    f.write(RECORD) # Variable para almacenar todo el contenido del fichero TXT
    f.close()           # Cerramos el fichero tras su lectura
    
    pygame.display.update()
    return
# --------------------------------------------
def mostrar_game_over():
    global NUMERO_VIDAS
    SCREEN.fill(BACKGROUND_COLOR)
    sonidoGameOver.play()
    dibujar_Textos('GAME OVER', font65, COLOR_ROJO, SCREEN, 0, (ALTO_PANTALLA / 3),1)
    dibujar_Textos('Pulsa una tecla si deseas continuar', font35, COLOR_VERDE,
                   SCREEN, 0, ((ALTO_PANTALLA / 3) + 50),1)
    pygame.display.update()
    return
# --------------------------------------------
def mostrar_marcadores():
    dibujar_Textos('NIVEL: %s     VIDAS: %s' % (nivel, NUMERO_VIDAS),
                   font25, COLOR_AMARILLO, SCREEN, 10, 5)
    dibujar_Textos('PUNTUACIÓN: %s' % (puntuacionJuego), font25, COLOR_BLANCO, SCREEN, 250, 5)
    dibujar_Textos('Freno: %s' % (frenoVelocidadEnemigo),
                   font25, COLOR_BLANCO, SCREEN, (ANCHO_PANTALLA-10), 5,2)

    dibujar_Textos('Puntos para cambiar de nivel: %s' % ((PUNTUACION_DE_NIVEL - puntuacion_nivel)),
                   font25, COLOR_ROJO, SCREEN, 10, 30)
    if tipoMunicion != 'SIMPLE':
        dibujar_Textos('Disparo Extra >>  Dobles: %s // Triples: %s'
                       % (municionExtraDoble, municionExtraTriple),
                       font25, COLOR_BLANCO, SCREEN, 10, 55)
    return 
# --------------------------------------------
def esperarPulsacionTeclado():
    pygame.event.set_allowed([KEYDOWN, KEYUP])
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                fin_juego()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pulsar 'escape' para terminar
                    fin_juego()
                return

# --------------------------------------------
def PausarJuego():
    global pausarPartida
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_p:
                    return


# --------------------------------------------
def mostrarPantallaInicial():
    global ANCHO_PANTALLA, ALTO_PANTALLA
    mostarTextosDeInicio()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                fin_juego()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    ANCHO_PANTALLA -=10
                if event.key == K_RIGHT:
                    ANCHO_PANTALLA +=10
                if event.key == K_UP:
                    ALTO_PANTALLA -= 10
                if event.key == K_DOWN:
                    ALTO_PANTALLA += 10
                if event.key == K_ESCAPE: # pulsar 'escape' para terminar
                    fin_juego()
                if event.key == K_SPACE:  # pulsar 'espacio' para continuar
                    return
                mostarTextosDeInicio()
# --------------------------------------------
def mostarTextosDeInicio():
    global ANCHO_PANTALLA, ALTO_PANTALLA, SCREEN
    SCREEN.fill(BACKGROUND_COLOR)
    q = 6
    # Mostrar pantalla de inicio
    SCREEN = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), 0, 32)
    dibujar_Textos('MARCIANITOS', font48, COLOR_VERDE, SCREEN, 0, (ALTO_PANTALLA / q),1)
    dibujar_Textos('Usa las flechas de cursor si deseas',
                   font25, COLOR_BLANCO_SUCIO, SCREEN, 0, (ALTO_PANTALLA / q) + 60,1)
    dibujar_Textos('modificar el tamaño de la ventana ahora',
                   font25, COLOR_BLANCO_SUCIO, SCREEN, 0, (ALTO_PANTALLA / q) + 80,1)

    dibujar_Textos('TECLAS DE JUEGO',
                   font25, COLOR_AZUL_CIELO, SCREEN, 0, (ALTO_PANTALLA / q) + 130,1)
    offset = dibujar_Textos('\'RATON:\'  Usa el ratón para desplazar al jugador',
                   font25, COLOR_AZUL_CIELO, SCREEN, 0, (ALTO_PANTALLA / q) + 160,3)
    x = int(ANCHO_PANTALLA - offset)/2
    dibujar_Textos('(Tambien puedes usar las flechas)',
                   font20, COLOR_AZUL_CIELO, SCREEN, x, (ALTO_PANTALLA / q) + 170,0)

    dibujar_Textos('\'A:\' Acelerar Enemigos (si han sido frenados)',
                   font25, COLOR_AZUL_CIELO, SCREEN, x, (ALTO_PANTALLA / q) + 190,0)
    dibujar_Textos('\'Z:\'  Frenar Enemigos',
                   font25, COLOR_AZUL_CIELO, SCREEN, x, (ALTO_PANTALLA / q) + 210,0)
    dibujar_Textos('(los cambios de velocidad afectan a todos los niveles',
                   font20, COLOR_ROJO, SCREEN, x, (ALTO_PANTALLA / q) + 230,0)
    dibujar_Textos('pero no evita los incrementos de velocidad de cada nivel)',
                   font20, COLOR_ROJO, SCREEN, x, (ALTO_PANTALLA / q) + 245,0)
    dibujar_Textos('\'BARRA ESPACIADORA:\'  Disparar',
                   font25, COLOR_AZUL_CIELO, SCREEN, x, (ALTO_PANTALLA / q) + 265,0)
    dibujar_Textos('\'ESC:\'  Salir del juego',
                   font25, COLOR_BLANCO_SUCIO, SCREEN, x, (ALTO_PANTALLA / q) + 285,0)


    dibujar_Textos('Pulsa la tecla DISPARO para comenzar',
                   font25, COLOR_AMARILLO, SCREEN, 0, (ALTO_PANTALLA / q) + 345,1)

    pygame.display.update()
    return
# --------------------------------------------
def jugador_Colision_Enemigo(jugadorRect, enemigos):
    dummyRect = Rect(0,0,10,16)
    for enemigo in enemigos:
        dummyRect.centerx = enemigo['rect'].centerx
        dummyRect.centery = enemigo['rect'].centery
##        if jugadorRect.colliderect(enemigo['rect']):
        # disponer de un poco mas de margen en las colisiones
        if jugadorRect.colliderect(dummyRect): 
            return True
    return False
# --------------------------------------------
def bala_Toca_Enemigo(enemigoRect, balas):
    for bala in balas:
        if enemigoRect.colliderect(bala['rect']):
            balas.remove(bala)
            return True
    return False
# --------------------------------------------
def dibujar_Textos(text, size, color, surface, x, y, posicion = 0):
    textobj = size.render(text, 1, color)
    textrect = textobj.get_rect()
##    print (textrect.right)
    if posicion == 1: # centrado respecto de (y)
        textrect.centerx = SCREEN.get_rect().centerx
        textrect.centery = y
    if posicion == 2: # alineacion Derecha respecto de (x,y)
        textrect.topright = (x, y)
    if posicion == 0: # alineacion Izquierda respecto de (x,y)
        textrect.topleft = (x, y)
    if posicion == 3: # alineacion centro y devuelve espacio lateral
        textrect.centerx = SCREEN.get_rect().centerx
        textrect.centery = y
        surface.blit(textobj, textrect)
        return (textrect.width)
    surface.blit(textobj, textrect)

# --------------------------------------------
def explosion_Nave_Jugador():
    """ Animar los sprites que componen la explosion """
    intervalo = 50
    for i in range(0,11):
        SCREEN.blit(imagenExplosion[i], (jugadorRect.x-10,jugadorRect.y-10))
        pygame.time.wait(intervalo)
        pygame.display.update()
# --------------------------------------------
def proyectil():
    ''' creaccion de las balas simples'''
    rect = imagenBala.get_rect()
    rect.centerx = jugadorRect.centerx
    rect.centery = jugadorRect.y
    nuevaBala = {'rect': rect, 'lateral': 0, 'speed': -35, 'surface':imagenBala,}

    balas.append(nuevaBala)
    return ()
# --------------------------------------------
def proyectil_doble():
    ''' creaccion de las balas dobles '''
    global municionExtraDoble
    municionExtraDoble -= 1
       
    rect1 = imagenBalaI.get_rect()
    rect2 = imagenBalaD.get_rect()
    rect1.centerx = jugadorRect.centerx - 16
    rect1.centery = jugadorRect.y
    rect2.centerx = jugadorRect.centerx + 16
    rect2.centery = jugadorRect.y

    nuevaBalaI = {'rect': rect1, 'lateral': 0, 'speed': -30, 'surface':imagenBalaI,}
    nuevaBalaD = {'rect': rect2, 'lateral': 0, 'speed': -30, 'surface':imagenBalaD,}

    balas.append(nuevaBalaI)
    balas.append(nuevaBalaD)

    return()
# --------------------------------------------
def proyectil_triple():
    ''' creaccion de las balas triples'''
    global municionExtraTriple 
    municionExtraTriple -= 1
    
    rect1 = imagenBalaI.get_rect()
    rect2 = imagenBalaD.get_rect()
    rect3 = imagenBalaIC.get_rect()
    rect4 = imagenBalaDC.get_rect()
    
    rect1.centerx = jugadorRect.centerx - 16
    rect1.centery = jugadorRect.y
    rect2.centerx = jugadorRect.centerx + 16
    rect2.centery = jugadorRect.y
    rect3.centerx = jugadorRect.centerx
    rect3.centery = jugadorRect.centery
    rect4.centerx = jugadorRect.centerx
    rect4.centery = jugadorRect.centery

    nuevaBalaI = {'rect': rect1, 'lateral': 0, 'speed': -30, 'surface':imagenBalaI,}
    nuevaBalaD = {'rect': rect2, 'lateral': 0, 'speed': -30, 'surface':imagenBalaD,}

    nuevaBalaIC = {'rect': rect3, 'lateral': -8, 'speed': -20, 'surface':imagenBalaIC,}
    nuevaBalaDC = {'rect': rect4, 'lateral': 8, 'speed': -20, 'surface':imagenBalaDC,}
    balas.append(nuevaBalaI)
    balas.append(nuevaBalaD)
    balas.append(nuevaBalaIC)
    balas.append(nuevaBalaDC)
    return()
# --------------------------------------------
def CargarDatosNivel():
    PUNTUACION_DE_NIVEL = NIVELES[nivel]['PUNTUACION_DE_NIVEL']
    ENEMIGO_MinSIZE = NIVELES[nivel]['ENEMIGO_MinSIZE']
    ENEMIGO_MaxSIZE = NIVELES[nivel]['ENEMIGO_MaxSIZE']
    ENEMIGO_MinSPEED = NIVELES[nivel]['ENEMIGO_MinSPEED']
    ENEMIGO_MaxSPEED = NIVELES[nivel]['ENEMIGO_MaxSPEED']
    ESPERA_CREACION_ENEMIGOS = NIVELES[nivel]['ESPERA_CREACION_ENEMIGOS']
    NUMERO_JEFES = NIVELES[nivel]['NUMERO_JEFES']
    VALOR_NAVE_JEFE = NIVELES[nivel]['VALOR_NAVE_JEFE']
    VELOCIDAD_JUGADOR = NIVELES[nivel]['VELOCIDAD_JUGADOR']
    jefe_SIZE = int((ENEMIGO_MinSIZE + ENEMIGO_MaxSIZE)/2)
    velocidadJefe = 6
    lista_cosas_buenas = []
    i = 0
    while i < NUMERO_JEFES:
        
        if velocidadConstante == False:
            velocidadJefe = random.randint(ENEMIGO_MinSPEED, ENEMIGO_MaxSPEED)
        naveJefe = {'rect': pygame.Rect(random.randint
                            (0, ANCHO_PANTALLA-jefe_SIZE),0 - jefe_SIZE, jefe_SIZE, jefe_SIZE),
                        'speed': velocidadJefe, 'speed2': velocidadJefe, 'puntos': VALOR_NAVE_JEFE,
                        'surface': pygame.transform.scale(imagen_Enemigo_jefe,(jefe_SIZE, int(jefe_SIZE * proporcionEnemigo_jefe))),
                        'indice': 0, 'clase': random.randint(2,3),}
        lista_cosas_buenas.append(naveJefe)
        i += 1
        
    listaDatosNivel =[PUNTUACION_DE_NIVEL, ENEMIGO_MinSIZE,
                      ENEMIGO_MaxSIZE, ENEMIGO_MinSPEED,
                      ENEMIGO_MaxSPEED, ESPERA_CREACION_ENEMIGOS,
                      NUMERO_JEFES, VALOR_NAVE_JEFE,VELOCIDAD_JUGADOR,
                      lista_cosas_buenas]
    return (listaDatosNivel)
# --------------------------------------------
#  FIN DEL BLOQUE DE DEFINICIÓN DE FUNCIONES
# --------------------------------------------



# ********************************************
#           INICIO DEL PROGRAMA
# ********************************************


# Inicializar la ventana y el cursor
pygame.init()
mainClock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption(' - Marcianitos v1.2 - ')
pygame.mouse.set_visible(False)

# Definir tipos de letra
font20 = pygame.font.SysFont(None, 20)
font25 = pygame.font.SysFont(None, 25)
font30 = pygame.font.SysFont(None, 30)
font35 = pygame.font.SysFont(None, 35)
font40 = pygame.font.SysFont(None, 40)
font45 = pygame.font.SysFont(None, 45)
font48 = pygame.font.SysFont(None, 48)
font50 = pygame.font.SysFont(None, 50)
font65 = pygame.font.SysFont(None, 65)

# Definir sonidos
sonidoGameOver = pygame.mixer.Sound('sonidos/Sonido_Fallo.wav')
sonidoLaser = pygame.mixer.Sound('sonidos/laser2.wav')
sonidoExplosion = pygame.mixer.Sound('sonidos/explosion.wav')

# Definir imagenes
imagenBala = pygame.image.load('imagenes/disparo3x15amarillo.png')
imagenBalaI = pygame.image.load('imagenes/disparo3x15rojo.png')
imagenBalaD = pygame.image.load('imagenes/disparo3x15rojo.png')
imagenBalaIC = pygame.image.load('imagenes/disparo5x5rojo.png')
imagenBalaDC = pygame.image.load('imagenes/disparo5x5rojo.png')

imagen_Jugador = pygame.image.load('imagenes/nave_jugador.png')
jugadorRect = imagen_Jugador.get_rect()
proporcionJugador = jugadorRect.height / jugadorRect.width

imagen_Enemigo = pygame.image.load('imagenes/nave_enemiga.png')
Enemigo_Rect = imagen_Enemigo.get_rect()
proporcionEnemigo = Enemigo_Rect.height / Enemigo_Rect.width

imagen_Enemigo_jefe = pygame.image.load('imagenes/nave_enemiga_jefe.png')
Enemigo_jefe_Rect = imagen_Enemigo_jefe.get_rect()
proporcionEnemigo_jefe = Enemigo_jefe_Rect.height / Enemigo_jefe_Rect.width

imagen_Fondo = pygame.image.load('imagenes/fondo.jpg').convert()

imagenExplosion = []
imagenExplosion.append(pygame.image.load('explosion1/explosion_01.png'))
imagenExplosion.append(pygame.image.load('explosion1/explosion_02.png'))
imagenExplosion.append(pygame.image.load('explosion1/explosion_03.png'))
imagenExplosion.append(pygame.image.load('explosion1/explosion_04.png'))
imagenExplosion.append(pygame.image.load('explosion1/explosion_05.png'))
imagenExplosion.append(pygame.image.load('explosion1/explosion_06.png'))
imagenExplosion.append(pygame.image.load('explosion1/explosion_07.png'))
imagenExplosion.append(pygame.image.load('explosion1/explosion_08.png'))
imagenExplosion.append(pygame.image.load('explosion1/explosion_09.png'))
imagenExplosion.append(pygame.image.load('explosion1/explosion_10.png'))
imagenExplosion.append(pygame.image.load('explosion1/explosion_11.png'))
imagenExplosion.append(pygame.image.load('explosion1/explosion_12.png'))
imagenExplosion.append(pygame.image.load('explosion1/explosion_13.png'))
imagenExplosion.append(pygame.image.load('explosion1/explosion_14.png'))
imagenExplosion.append(pygame.image.load('explosion1/explosion_15.png'))
imagenExplosion.append(pygame.image.load('explosion1/explosion_16.png'))
imagenExplosion.append(pygame.image.load('explosion1/explosion_17.png'))
imagenExplosion.append(pygame.image.load('explosion1/explosion_18.png'))

# obtener las dimensiones de la imagen del Jugador
ancho, alto = imagen_Jugador.get_rect().size

# Redimensionado de las fotogramas de la explosión a 1.2 veces el
# tamaño del Jugador al tiempo que se introducen en una lista para
# facilitar su uso posterior.
for i in range(0,18):
    imagenExplosion[i] = pygame.transform.scale(imagenExplosion[i], (int(ancho*1.2), int(alto*1.2)))

# Cargar el fichero con los datos de los records previos
cargar_records()

# Mostrar pantalla de inicio
mostrarPantallaInicial()


# ********************************************
# Bucle principal del programa
# ********************************************

# Definir posicion inicial del jugador al iniciar la partida
jugadorRect.center = (ANCHO_PANTALLA / 2, ALTO_PANTALLA - 100)

# Cargar sonido de fondo para el juego
pygame.mixer.music.load('sonidos/time_n.mp3')
# iniciar reproduccion con bucle infinito (-1)
pygame.mixer.music.play(-1, 0.0)
    
while True: # Bucle para el juego. Mientras la partida esté activa
    # comprobar si se superan los requisitos para cambio de nivel.
    if puntuacion_nivel >= PUNTUACION_DE_NIVEL or nivel == -1:
        nivel += 1
        puntuacion_nivel = 0
        fin_de_juego = 0
        if nivel >= len(NIVELES):
            fin_de_juego = 1
            nivel = 0
            FPS += 10
            # destruir enemigos si se superan todos los niveles.
            for enemigo in enemigos:        
                enemigos.remove(enemigo)
                enemigos_destruidos.append(enemigo)
                puntuacionJuego += 5 # Dar dos puntos extra por cada nave en pantalla
                puntuacion_nivel += 5
            
            #NUMERO_VIDAS += 1 #Descomentar si se desea dar vidas al superar los niveles
        # Cargar los datos del siguiente nivel    
        listaDatosNivel = CargarDatosNivel()
        
        PUNTUACION_DE_NIVEL = listaDatosNivel[0]
        ENEMIGO_MinSIZE = listaDatosNivel[1]
        ENEMIGO_MaxSIZE = listaDatosNivel[2]
        ENEMIGO_MinSPEED = listaDatosNivel[3]
        ENEMIGO_MaxSPEED = listaDatosNivel[4]
        ESPERA_CREACION_ENEMIGOS = listaDatosNivel[5]
        NUMERO_JEFES = listaDatosNivel[6]
        VALOR_NAVE_JEFE = listaDatosNivel[7]
        VELOCIDAD_JUGADOR = listaDatosNivel[8]
        lista_cosas_buenas = listaDatosNivel[9]

    
    # Atender eventos de teclado y raton
    for event in pygame.event.get():
        if event.type == QUIT:
            fin_juego()
            
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
##                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT:
##                moveLeft = False
                moveRight = True
            if event.key == K_UP:
##                moveDown = False
                moveUp = True
            if event.key == K_DOWN:
##                moveUp = False
                moveDown = True
            # Hacer una pausa si se pulsa la tecla('P')
            if event.key == K_p:
                PausarJuego()
            if event.key == K_a:
                frenoVelocidadEnemigo += 1
                if frenoVelocidadEnemigo > 0:
                    frenoVelocidadEnemigo = 0
            if event.key == K_z:
                frenoVelocidadEnemigo -= 1
                if frenoVelocidadEnemigo < -(listaDatosNivel[4]-1):
                    frenoVelocidadEnemigo = -(listaDatosNivel[4]-1)
            if event.key == K_SPACE:
                # sonido del disparo
                sonidoLaser.play()
                # Disparar si se pulsa 'barra espaciadora'
                if tipoMunicion == 'DOBLE':
                    proyectil_doble()
                    break                        
                if tipoMunicion == 'TRIPLE':
                    proyectil_triple()
                    break
                else:
                    proyectil()

        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                    fin_juego()
            if event.key == K_LEFT:
                moveLeft = False
            if event.key == K_RIGHT:
                moveRight = False
            if event.key == K_UP:
                moveUp = False
            if event.key == K_DOWN:
                moveDown = False

        if event.type == MOUSEMOTION:
            # si el raton se mueve, el jugador se mueve a donde este el cursor
            jugadorRect.move_ip(event.pos[0] - jugadorRect.centerx, event.pos[1] - jugadorRect.centery)
    
    # añadir nuevos enemigos si se necesitan,
    # es decir, si se cumple el tiempo establecido para ello
    contadorNuevoEnemigo += 1
    if len(enemigos) < numeroEnemigosActivos and contadorNuevoEnemigo >= ESPERA_CREACION_ENEMIGOS:
        '''creacion de nuevos enemigos si se alcanza el tiempo de
        espera establecido o si la lista de enemigos ha quedado vacía '''
        contadorNuevoEnemigo = 0
        enemigo_SIZE = random.randint(ENEMIGO_MinSIZE, ENEMIGO_MaxSIZE)
        velocidad = random.randint(ENEMIGO_MinSPEED, ENEMIGO_MaxSPEED)
        nave_jefe = random.randint(0,100)
        if nave_jefe >= 95 and len(lista_cosas_buenas) > 0:
            nuevoEnemigo = lista_cosas_buenas.pop()
        else:
            nuevoEnemigo = {'rect': pygame.Rect(random.randint
                                (0, ANCHO_PANTALLA-enemigo_SIZE),0 - enemigo_SIZE, enemigo_SIZE, enemigo_SIZE),
                            'speed': velocidad,'speed2': velocidad, 'puntos': int(velocidad +(ENEMIGO_MaxSIZE-enemigo_SIZE)/5),
                            'surface': pygame.transform.scale(imagen_Enemigo,(enemigo_SIZE, int(enemigo_SIZE * proporcionEnemigo))),
                            'indice': 0,'clase': 0,}
        enemigos.append(nuevoEnemigo)
       
    # Mover el jugador
    if moveLeft and jugadorRect.left > 0:
        jugadorRect.move_ip(-1 * VELOCIDAD_JUGADOR, 0)
    if moveRight and jugadorRect.right < ANCHO_PANTALLA:
        jugadorRect.move_ip(VELOCIDAD_JUGADOR, 0)
    if moveUp and jugadorRect.top > 0:
        jugadorRect.move_ip(0, -1 * VELOCIDAD_JUGADOR)
    if moveDown and jugadorRect.bottom < ALTO_PANTALLA:
        jugadorRect.move_ip(0, VELOCIDAD_JUGADOR)

    # mover el puntero del ratón para coincidir con el jugador
    # si este se mueve con el teclado
    pygame.mouse.set_pos(jugadorRect.centerx, jugadorRect.centery)

    # movimiento de caida de los enemigos
    contadorPausaEnemigos += 1
    if contadorPausaEnemigos % pausaEnemigos == 0:
        contadorPausaEnemigos = 0
        for enemigo in enemigos:
            '''Evita ligeras incongruencias visuales (si estamos
            frenados en el ultimo nivel y completamos una vuelta de
            cicclo volviendo a niveles inferiores)'''
            if frenoVelocidadEnemigo < -(listaDatosNivel[4]-1):
                frenoVelocidadEnemigo = -(listaDatosNivel[4]-1)

            desplazamientoEnemigo = enemigo['speed2'] + frenoVelocidadEnemigo
            # Evitar que los enemigos se paren
            if desplazamientoEnemigo < 1: 
                desplazamientoEnemigo = 1
            # Evitar que superen su velocidad original
            if desplazamientoEnemigo > enemigo['speed']:
                desplazamientoEnemigo = enemigo['speed']
            enemigo['rect'].move_ip(0, desplazamientoEnemigo)


    # borrar los enemigos que se salen por la parte inferior
    for enemigo in enemigos:
        if enemigo['rect'].top > ALTO_PANTALLA:
            enemigos.remove(enemigo)
    # movimiento de las balas
    for bala in balas:
        bala['rect'].move_ip(bala['lateral'], bala['speed'])
        # borrar las balas que se salen por la parte superior
        if bala['rect'].top < -15:
            balas.remove(bala)

    # borrar la pantalla y
    # Establecer imagen (o un color) de fondo
    
    if fondoActivo == True:
        contadorMovimientoFondo += 1
        if contadorMovimientoFondo % pasoMovimientoFondo == 0:
            contadorMovimientoFondo = 0
            fondoy += 1
            if fondoy > 0:
                fondoy = -3800            
        SCREEN.blit(imagen_Fondo, (fondox, fondoy))
    else:
        SCREEN.fill(BACKGROUND_COLOR)

    # dibujar los enemigos
    for enemigo in enemigos:
        SCREEN.blit(enemigo['surface'], enemigo['rect'])

    # dibujar las balas
    for bala in balas:
        SCREEN.blit(bala['surface'], bala['rect'])
    
    # dibujar el jugador
    SCREEN.blit(imagen_Jugador, jugadorRect)
    
    # dibujar el marcador en la parte superior izquierda
    mostrar_marcadores()
                

    # comprobar si una bala toca las naves.
    for enemigo in enemigos:        
        if bala_Toca_Enemigo(enemigo['rect'], balas):
            enemigos.remove(enemigo)
            enemigos_destruidos.append(enemigo)
            puntuacionJuego += enemigo['puntos']
            puntuacion_nivel += enemigo['puntos']
            if enemigo['clase'] == 2:
                municionExtraDoble += 25
            if enemigo['clase'] == 3:
                municionExtraTriple += 20
    # Establecer el tipo de minición activa
    tipoMunicion = 'SIMPLE'
    if municionExtraDoble > 0:
        tipoMunicion = 'DOBLE'
    if municionExtraTriple > 0:
        tipoMunicion = 'TRIPLE'

    # Animar la explosión de los enemigos destruidos r.2
    '''Este método sí genera indices individuales para cada enemigo que ha
    sido abatido, produciendo por tanto animaciones independientes de principio a fin'''
    if len(enemigos_destruidos) > 0:
        '''Hacemos una pausa de (n) FPS para cada frame de la 
        animacion, por eso ejecutamos la animación sólo cuando 
        el indice es multiplo de (velocidad_animacion)'''        
        velocidad_animacion = 1

        for destruido in enemigos_destruidos:
            destruido['indice'] += 1#2, con valor 2 nos saltariamos 1 de cada 2 frame del sprite...etc
            if destruido['indice'] % velocidad_animacion == 0:
                indice = int((destruido['indice'])/velocidad_animacion - 2)
                exploSize = int(destruido['rect'].width * 1.2)
                # ajustamos el tamaño de la explosion al objeto que explota
                imagen_a_Escala = pygame.transform.scale(imagenExplosion[indice], (exploSize, exploSize))
                SCREEN.blit(imagen_a_Escala, destruido['rect'])
            if destruido['indice'] > (17 * velocidad_animacion):
                '''como la animación de la explosión tiene 18
                pasos, si el indice es mayor de (17*velocidad_animacion), eliminamos al
                enemigo de la lista de enemigos_destruidos'''
                enemigos_destruidos.remove(destruido)
                
    # comprobar si el jugador colisiona con los enemigos.
    if invencible == False:
        if jugador_Colision_Enemigo(jugadorRect, enemigos):
            # Sonido de la explosion
            sonidoExplosion.play()
            # animacion de la explosion
            explosion_Nave_Jugador()            
            finDeVida = 1

    pygame.display.update()

    # Pausar el juego y comprobar si acaba o si solo se pierde un crédito
    if finDeVida == 1:
        pygame.event.clear() # limpiar lista de eventos
        NUMERO_VIDAS -= 1
        if NUMERO_VIDAS > 0:
            dibujar_Textos('Pulsa una tecla para continuar', font35, COLOR_VERDE,
                           SCREEN, 0, ((ALTO_PANTALLA ) - 100),1)
            pygame.display.update()
            esperarPulsacionTeclado()
        # restablecer algunos valores del juego para reinicar nivel actual
        finDeVida = 0
        puntuacion_nivel = 0
        PUNTUACION_DE_NIVEL = listaDatosNivel[0]
        enemigos = []
        enemigos_destruidos = []
        # posicionar el jugardor en la parte baja de la pantalla
        jugadorRect.center = (int(ANCHO_PANTALLA / 2), ALTO_PANTALLA - 100)
        # mover el puntero del ratón para coincidir con el jugador al iniciar nueva vida
        pygame.mouse.set_pos(jugadorRect.centerx, jugadorRect.centery)
        # Resetear posibles movimientos activos
        moveLeft = moveRight = moveUp = moveDown = False
        # Reset del tiempo para crear nuevos enemigos
        contadorNuevoEnemigo = 0
        
        if NUMERO_VIDAS == 0:
            # restablecer algunos valores más del juego por si se inicia partida nueva
            finDeVida = 0
            NUMERO_VIDAS = MAX_VIDAS 
            nivel = 0
            FPS = 40
            puntuacion_nivel = 0
            MaxPlayerScore = puntuacionJuego
            puntuacionJuego = 0
            pygame.mixer.music.stop()
            mostrar_game_over()
            esperarPulsacionTeclado()
            comprobar_y_mostrar_records()
            frenoVelocidadEnemigo = 0
            esperarPulsacionTeclado()
            mostrarPantallaInicial()
            # Reiniciar musica de fondo
            pygame.mixer.music.play(-1, 0.0)
    # Control de tiempo del reloj del programa
    mainClock.tick(FPS)


