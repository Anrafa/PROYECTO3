import random
import time
import os
import re
import pathlib
import operator

RED = '\033[1;31m'
BLUE = '\033[1;34m'
AMARILLO = '\033[1;33m'
NOCOLOR = '\033[0;0m'
BLACK = '\033[30m'
GREEN = '\033[32m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'


def inicia_juego():
    print("       [1] Jugar partida nueva")
    print("   ================================")
    print("       ")
    print("       ")

    nombre1 = input("       Ingresa el nombre del jugador n° 1: ")
    nombre2 = input("       Ingresa el nombre del jugador n° 2: ")

    nombresDict = {}
    nombresDict['X'] = nombre1
    nombresDict['O'] = nombre2

    ficha = ""
    ''' Se define quien juega primero: X / O / aleatorio'''
    while ficha != "O" and ficha != "X" and ficha != "A":
        ficha = input("       ¿Quién empieza? Ingresar (X)=" + nombresDict['X'] + " / (O)=" + nombresDict[
            'O'] + " ) o (A)leatorio: ").upper()

    if ficha == "O":
        jugador1 = "O"
        jugador2 = "X"
    elif ficha == "X":
        jugador1 = "X"
        jugador2 = "O"
    else:
        aleatorio = ("X", "O")
        primero = aleatorio[random.randint(0, 1)]
        if primero == "O":
            jugador1 = "O"
            jugador2 = "X"
        else:
            jugador1 = "X"
            jugador2 = "O"
    return jugador1, jugador2, nombresDict


def inicia_juego_computador():
    print("       [6] Juega contra el ordenador")
    print("   ================================")
    print("       ")
    print("       La ficha O juega primero")
    print("       ")
    ficha = ""
    dificultad = ""

    nombre1 = input("       Ingresa tu nombre: ")

    ''' Define tu ficha: X / O  / aleatorio'''
    while ficha != "O" and ficha != "X" and ficha != "A":
        ficha = input("       ¿Qué ficha eliges? Ingresar (X/O) o (A)leatorio: ").upper()

    ''' Define nivel de dificultad'''
    while dificultad != "F" and dificultad != "D":
        dificultad = input("       ¿En qué dificultad quieres jugar? (F)ácil o (D)ifícil: ").upper()

    nombresDict = {}

    if ficha == "O":
        jugador = "O"
        computador = "X"
        nombresDict["O"] = nombre1
        nombresDict["X"] = "El ordenador"
    elif ficha == "X":
        jugador = "X"
        computador = "O"
        nombresDict["X"] = nombre1
        nombresDict["O"] = "El ordenador"
    else:
        aleatorio = ("X", "O")
        primero = aleatorio[random.randint(0, 1)]
        if primero == "O":
            jugador = "O"
            computador = "X"
            nombresDict["O"] = nombre1
            nombresDict["X"] = "El ordenador"
        else:
            jugador = "X"
            computador = "O"
            nombresDict["X"] = nombre1
            nombresDict["O"] = "El ordenador"
    return jugador, computador, dificultad, nombresDict


def color_ficha(ficha):
    # color del tablero y ficha de jugadores
    fichacolor = AMARILLO
    if ficha == "O":
        fichacolor = BLUE + ficha + AMARILLO
    elif ficha == "X":
        fichacolor = RED + ficha + AMARILLO
    else:
        fichacolor = ficha + AMARILLO
    return fichacolor


def mostrar_tablero(tablero):
    ''' dibuja el tablero '''

    print(AMARILLO)
    print("     -------------------------")
    print("     |1      |2      |3      |")
    print("     |   {}   |   {}   |   {}".format(color_ficha(tablero[0]), color_ficha(tablero[1]),
                                                 color_ficha(tablero[2])), "  |")
    print("     |       |       |       |")
    print("     --------+-------+--------")
    print("     |4      |5      |6      |")
    print("     |   {}   |   {}   |   {}".format(color_ficha(tablero[3]), color_ficha(tablero[4]),
                                                 color_ficha(tablero[5])), "  |")
    print("     |       |       |       |")
    print("     --------+-------+--------")
    print("     |7      |8      |9      |")
    print("     |   {}   |   {}   |   {}".format(color_ficha(tablero[6]), color_ficha(tablero[7]),
                                                 color_ficha(tablero[8])), "  |")
    print("     |       |       |       |")
    print("     -------------------------")
    print(NOCOLOR)


def contar_jugadas(tablero):
    # cuenta jugadas de los 2 jugadores
    contador = 0
    for i in range(0, 9):
        if tablero[i] != ' ':
            contador = contador + 1
    return str(contador)


def contar_jugadas_jugador(tablero, jugador):
    # cuenta jugadas de un jugador
    contador = 0
    for i in range(0, 9):
        if tablero[i] == jugador:
            contador = contador + 1
    return str(contador)


def busca_ganador(tablero, jugador):  # validacion de movimientos ganadores
    for i in range(0, 7, 3):
        if (tablero[i] == jugador and tablero[i + 1] == jugador and tablero[i + 2] == jugador):
            return True, "FILA"
    for i in range(0, 3):
        if (tablero[i] == jugador and tablero[i + 3] == jugador and tablero[i + 6] == jugador):
            return True, "COLUMNA"
    if (tablero[0] == jugador and tablero[4] == jugador and tablero[8] == jugador):
        return True, "DIAGONAL"
    if (tablero[2] == jugador and tablero[4] == jugador and tablero[6] == jugador):
        return True, "DIAGONAL"
    return False, " "


def busca_perdedor(tablero, jugador):
    if (jugador == "X"):
        oponente = "O"
    else:
        oponente = "X"
    ganador, tipo = busca_ganador(tablero, oponente)
    if (ganador):
        return True
    return False


def tablero_lleno(tablero):
    ''' valida si el tablero se encuentra lleno o no '''
    for i in tablero:
        if i == " ":
            return False
    else:
        return True


def movimiento_computador_easy(tablero):
    vacios = []
    for i in range(9):
        if tablero[i] == ' ':
            # se identifica las casillas vacias
            vacios.append(i)
    # se retorna aleatorio de entre las casillas vacias
    return random.choice(vacios)


def movimiento_computador_hard(tablero, siguienteMovimiento, computador):
    ganador, tipo = busca_ganador(tablero, computador)
    if (ganador):
        return (-1, 10)  # 10 es el score que representa jugada ganadora
    elif (busca_perdedor(tablero, computador)):
        return (-1, -10)  # 10 es el score que representa jugada perdedora
    elif (tablero_lleno(tablero)):
        return (-1, 0)  # 0 es el score que representa jugada empate

    moves = []

    for i in range(len(tablero)):
        if (tablero[i] == " "):
            tablero[i] = siguienteMovimiento
            # obtiene el score de la jugada, se generan las "n" jugadas posibles
            score = movimiento_computador_hard(tablero, ("X" if siguienteMovimiento == "O" else "O"), computador)[1]
            moves.append((i, score))
            tablero[i] = " "

    if siguienteMovimiento == computador:
        maxScore = moves[0][1]
        bestMove = moves[0]
        for move in moves:  # se busca la mejor juagada, es decir, la ganadora
            if (move[1] > maxScore):
                bestMove = move
                maxScore = move[1]
        return bestMove
    else:
        minScore = moves[0][1]
        worstMove = moves[0]
        for move in moves:  # se busca la peor jugada
            if (move[1] < minScore):
                worstMove = move
                minScore = move[1]
        return worstMove


def casilla_libre(tablero, casilla):
    ''' valida si la casilla está libre '''
    return tablero[casilla] == " "


def movimiento_jugador(tablero, jugador, nombreDict):
    ''' devuelve la casilla que el jugador X / O ha elegido '''
    posiciones = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "G"]
    posicion = None
    while True:
        if posicion not in posiciones:  # valida que la respuesta ingresada sea alguno de 'posiciones'
            posicion = input(
                "  {}({})-> Ingresa posicion (1 al 9) o (G)uardar: ".format(nombreDict[jugador], jugador)).upper()
        else:
            if posicion == "G":
                # guardar partida pendiente a fichero, colocando un nombre
                guardar_partida(tablero, jugador, nombreDict)
                return 100
            else:
                posicion = int(posicion)
                if not casilla_libre(tablero, posicion - 1):
                    print("   posicion está marcada")
                else:
                    return posicion - 1


def menu_principal():
    os.system('cls')
    print("         MENU ")
    print("-----------------------")
    print(" [1] Jugar partida nueva")
    print(" [2] Jugar una partida guardada")
    print(" [3] Ver partidas por #jugadas")
    print(" [4] Mostrar todos los tableros de jugadas pasadas")
    print(" [5] Ranking partidas ganadas por nombre jugador")
    print(" [6] Juega contra el ordenador")
    print(" [7] Salir")
    return input("  Escoge una opción-> ")


def jugar_tres_raya():
    # partida del juego
    # se inicializa las 9 casillas en blanco
    tablero = [" "] * 9

    os.system('cls')
    jugador1, jugador2, nombresDict = inicia_juego()

    turno = jugador1

    partida = True

    while partida:

        mostrar_tablero(tablero)

        if tablero_lleno(tablero):
            print(" ¡Hubo un empate!")
            partida = False
            print()
            input("  Presiona enter tecla para continuar... ")
        elif turno == jugador1:
            casilla = movimiento_jugador(tablero, jugador1, nombresDict)
            if casilla == 100:
                break
            tablero[casilla] = jugador1
            turno = jugador2
            flag, tipo = busca_ganador(tablero, jugador1)
            if flag:
                mostrar_tablero(tablero)
                # print("Jugador ",jugador1,"--> ¡¡¡HAS GANADO EN UNA ",tipo," !!!")
                print("Felicidades ", nombresDict[jugador1], " --> Colocaste 3 fichas en una ", tipo, " ¡Ganaste!")
                graba_partidas_completadas(tablero, nombresDict)
                guardar_ganadores(nombresDict[jugador1])
                print()
                input("  Presiona enter para continuar... ")
                partida = False
        elif turno == jugador2:
            casilla = movimiento_jugador(tablero, jugador2, nombresDict)
            if casilla == 100:
                break
            tablero[casilla] = jugador2
            turno = jugador1
            flag, tipo = busca_ganador(tablero, jugador2)
            if flag:
                mostrar_tablero(tablero)
                # print("Jugador ",jugador2,"--> ¡¡¡HAS GANADO EN UNA ",tipo," !!!")
                print("Felicidades ", nombresDict[jugador2], " --> Colocaste 3 fichas en una ", tipo, " ¡Ganaste!")
                graba_partidas_completadas(tablero, nombresDict)
                guardar_ganadores(nombresDict[jugador2])
                print()
                input("  Presiona enter para continuar... ")
                partida = False


def jugar_tres_raya_computador():
    # partida del juego
    # se inicializa las 9 casillas en blanco
    tablero = [" "] * 9

    os.system('cls')

    jugador, computador, nivel_dificultad, nombresDict = inicia_juego_computador()

    turno = ""
    if jugador == "O":  # juega primero
        turno = jugador
    else:
        turno = computador

    partida = True

    while partida:

        mostrar_tablero(tablero)

        if tablero_lleno(tablero):
            print("Rayos", nombresDict[jugador], "--> No venciste al ordenador. ¡Empate!")
            partida = False
            print()
            input("  Presiona enter para continuar... ")
        elif turno == jugador:
            casilla = movimiento_jugador(tablero, jugador, nombresDict)
            if casilla == 100:
                break
            tablero[casilla] = jugador
            turno = computador
            flag, tipo = busca_ganador(tablero, jugador)
            if flag:
                mostrar_tablero(tablero)
                print("Excelente ", nombresDict[jugador], "--> Venciste al ordenador formando una ", tipo,
                      " ¡Tú ganas!")
                graba_partidas_completadas(tablero, nombresDict)
                guardar_ganadores(nombresDict[jugador])
                print()
                input("  Presiona enter para continuar... ")
                partida = False
        elif turno == computador:
            casilla = ""
            print("    El ordenador está pensando....")

            if nivel_dificultad == "F":
                casilla = movimiento_computador_easy(tablero)
                time.sleep(0.5)

            if nivel_dificultad == "D":
                casilla = int(movimiento_computador_hard(tablero, computador, computador)[0])
                time.sleep(0.7)

            tablero[casilla] = computador
            turno = jugador
            flag, tipo = busca_ganador(tablero, computador)
            if flag:
                mostrar_tablero(tablero)
                print("Rayos", nombresDict[jugador], ". El ordenador te venció formando una", tipo, "¡No te rindas!")
                graba_partidas_completadas(tablero, nombresDict)
                guardar_ganadores("Ordenador")
                print()
                input("  Presiona enter para continuar... ")
                partida = False


def guardar_partida(tablero, jugador, nombreDict):
    # guarda partida antes de haber terminado
    # ejemplo contenido de linea:  partidaGuardada* | |X|O| | | | | |*X*nombreDeX*nombreDeO
    file = pathlib.Path("guardadas_tres_raya.txt")
    nombre = input(" Ingresa nombre de la partida : ")
    if file.exists():
        f = open("guardadas_tres_raya.txt", "r")  # apertura de arcuhivos
        lines = len(f.readlines())
        f.close()

        g = open("guardadas_tres_raya.txt", "a")  # apertura de arcuhivos
        marcas = ''
        for elemento in tablero:
            marcas = marcas + elemento + '|'
        g.write(nombre + '*' + marcas + '*' + jugador + '*' + nombreDict['X'] + '*' + nombreDict[
            'O'] + '\n')  # escritura en un archivo
        g.close()
    else:
        g = open("guardadas_tres_raya.txt", "w")
        marcas = ''
        for elemento in tablero:
            marcas = marcas + elemento + '|'
        g.write(nombre + '*' + marcas + '*' + jugador + '*' + nombreDict['X'] + '*' + nombreDict['O'] + '\n')
        g.close()
    input("Tu partida fue guardada. Presione enter para continuar ... ")


def graba_partidas_completadas(tablero, nombreDict):
    # ejemplo:   partida #2* |X|O|X|O|X|O| | |*6*JugadorX*JugadorO
    file = pathlib.Path("historico_tres_raya.txt")

    marcas = ''
    for elemento in tablero:
        marcas = marcas + elemento + '|'

    if file.exists():
        f = open("historico_tres_raya.txt", "r")
        lines = len(f.readlines())
        f.close()

        g = open("historico_tres_raya.txt", "a")
        g.write(
            'partida #' + str(lines + 1) + '*' + marcas + '*' + contar_jugadas(tablero) + '*' + nombreDict['X'] + '*' +
            nombreDict['O'] + '\n')

        g.close()
    else:
        g = open("historico_tres_raya.txt", "w")
        g.write('partida #1*' + marcas + '*' + contar_jugadas(tablero) + '*' + nombreDict['X'] + '*' + nombreDict[
            'O'] + '\n')
        g.close()


def listar_partidas_guardadas():
    os.system('cls')
    print("       [2] Jugar una partida guardada")
    print("   =======================================")
    print("       ")
    print("Nombre de Partidas:")
    print("--------------------------")

    file = pathlib.Path("guardadas_tres_raya.txt")
    if file.exists():
        f = open("guardadas_tres_raya.txt", "r")
        for partida in f:
            item = partida.split("*")
            print(item[0])
        f.close()
        nombre = input("       Ingrese el nombre de una partida: ")
        accion = ""
        while accion != "A" and accion != "E":
            accion = input("       Desea (A)brir o (E)liminar? ->").upper()

        if accion == 'E':
            eliminar_partida_guardada(nombre)
            print("       ¡¡¡Partida eliminada!!! ")
        if accion == 'A':
            abrir_partida_guardada(nombre)
    else:
        print(" ¡¡¡¡NO HAY PARTIDAS GUARDADAS!!!")


def abrir_partida_guardada(nombre):
    f = open("guardadas_tres_raya.txt", "r")
    # Creamos una lista con cada una de sus lineas
    lineas = f.readlines()
    # cerramos el archivo
    f.close()
    tablero = []
    turno = ''
    jugadorX = ''
    jugadorO = ''
    # recorremos todas las lineas para armar el 'tablero' con juegos pendientes
    # ejemplo contenido de linea:  partidaGuardada* | |X|O| | | | | |*X*nombreDeX*nombreDeO
    for linea in lineas:
        item = linea.split("*")
        # se extrae las jugadas del archivo representada por ejemplo: * | |X|O| | | | | |*
        # y se guarda cada jugada guardada en 'tablero'
        if item[0] == nombre:
            tablero = list(item[1].split('|'))
            tablero.pop(9)
            turno = item[2].rstrip()
            jugadorX = item[3].rstrip()
            jugadorO = item[4].rstrip()

    if turno == 'X':
        jugador1 = 'X'
        jugador2 = 'O'

    if turno == 'O':
        jugador1 = 'O'
        jugador2 = 'X'

    ## LEER NOMBRE DE JUGADORES Y  ASIGNAR DICCIONARIO
    nombresDict = {}
    nombresDict["X"] = jugadorX
    nombresDict["O"] = jugadorO

    partida = True

    while partida:

        mostrar_tablero(tablero)

        if tablero_lleno(tablero):
            print(" La partida ha terminado. ¡Empate!")
            partida = False
            print()
            input("  Presiona enter para continuar... ")
        elif turno == jugador1:
            casilla = movimiento_jugador(tablero, jugador1, nombresDict)
            # el valor 100 indica que se elige la opción Guardar partida y se interrumpe el juego
            if casilla == 100:
                break
            tablero[casilla] = jugador1
            turno = jugador2
            flag, tipo = busca_ganador(tablero, jugador1)
            if flag:
                mostrar_tablero(tablero)
                print("Bien hecho", nombresDict[jugador1], " --> Formaste una ", tipo, ". ¡Tú ganas!")
                graba_partidas_completadas(tablero, nombresDict)
                guardar_ganadores(nombresDict[jugador1])
                print()
                input("  Presiona enter para continuar... ")
                partida = False
        elif turno == jugador2:
            casilla = movimiento_jugador(tablero, jugador2, nombresDict)
            # el valor 100 indica que se elige la opción Guardar partida y se interrumpe el juego
            if casilla == 100:
                break
            tablero[casilla] = jugador2
            turno = jugador1
            flag, tipo = busca_ganador(tablero, jugador2)
            if flag:
                mostrar_tablero(tablero)
                print("Felicidades ", nombresDict[jugador2], "--> Formaste una ", tipo, ". ¡Tú ganas!")
                graba_partidas_completadas(tablero, nombresDict)
                guardar_ganadores(nombresDict[jugador2])
                print()
                input("  Presiona enter para continuar... ")
                partida = False


def eliminar_partida_guardada(nombre):
    # abrimos el archivo solo de lectura
    f = open("guardadas_tres_raya.txt", "r")
    # Creamos una lista con cada una de sus lineas
    lineas = f.readlines()
    # cerramos el archivo
    f.close()
    # abrimos el archivo pero vacio
    f = open("guardadas_tres_raya.txt", "w")
    # ejemplo contenido de linea:  partidaGuardada* | |X|O| | | | | |*X

    # recorremos todas las lineas
    for linea in lineas:
        item = linea.split("*")
        # se copia todas las lineas excepto la que se ingresa para eliminar.
        if item[0] != nombre:
            # Si no es la linea que queremos eliminar, guardamos la linea en el archivo
            f.write(linea)
    # cerramos el archivo
    f.close()
    input("Presione enter para continuar ... ")


def ver_partidas_nro_jugadas():
    os.system('cls')
    print("       [3] Ver partidas por #jugadas")
    print("   =======================================")
    print("       ")
    print("Lista de Partidas terminadas:")
    print("--------------------------")
    file = pathlib.Path("historico_tres_raya.txt")
    # valida si existe archivo
    if file.exists():
        f = open("historico_tres_raya.txt", "r")
        # ejemplo contenido de linea:  partida #2* |X|O|X|O|X|O| | |*6*jugadorX*jugadorO
        lineas = f.readlines()
        f.close()

        # recorremos todas las lineas
        # se guarda las partidas en diccionario 'partidas': {'partida #2':6}
        lpartidas = []
        for linea in lineas:
            item = linea.split("*")
            # partidas[item[0]] = item[2].rstrip()
            lpartidas.append(Partida(item[0], item[1], int(item[2]), item[3], item[4].rstrip()))

            # ordena quicksort
        orden = ""
        while orden != "A" and orden != "D":
            orden = input("       Ingrese ordenar (A)scendente o (D)escendente ->").upper()

        n = len(lpartidas)
        quicksort(lpartidas, 0, n - 1, orden)

        for part in lpartidas:
            tablero = []
            tablero = list(part.jugadas.split('|'))
            tablero.pop(9)  # esta linea elimina el elemento 10 que sobra.
            print(part.nombre, '\tJugadas Totales: ', part.total, '\tjugadores-> ', part.jugadorX, ": ",
                  contar_jugadas_jugador(tablero, "X"), " movimientos vs ", part.jugadorO, ": ",
                  contar_jugadas_jugador(tablero, "O"), " movimientos")

    input("  Presiona cualquier tecla para continuar... ")


def partition(A, low, high, orden):
    i = low
    # /** Elegimos el primer elemento del array como pivot */
    pivot = A[low].total
    for j in range(low + 1, high + 1):

        if orden == "D":  # orden descendente
            if A[j].total >= pivot:
                i = i + 1
                if i != j:
                    A[i], A[j] = A[j], A[i]

        if orden == "A":  # orden ascendente
            if A[j].total <= pivot:
                i = i + 1
                if i != j:
                    A[i], A[j] = A[j], A[i]

    A[i], A[low] = A[low], A[i]
    w = i
    return w


def quicksort(A, low, high, sort):
    if low < high:
        w = partition(A, low, high, sort)
        quicksort(A, low, w - 1, sort)
        quicksort(A, w + 1, high, sort)


def mostrar_todos_tableros():
    os.system('cls')
    print("       [4] Mostrar todos los tableros de jugadas pasadas")
    print("   ==========================================================")
    print("       ")
    print("Partidas de jugadas pasadas:")
    print("--------------------------")
    file = pathlib.Path("historico_tres_raya.txt")
    # valida existencia del archivo
    if file.exists():
        f = open("historico_tres_raya.txt", "r")
        # ejemplo contenido de linea:  partida #2* |X|O|X|O|X|O| | |*6*jugadorX*jugadorO
        lineas = f.readlines()
        f.close()

        # recorremos todas las lineas para listar las partidas
        # cada elemento del archivo está separado por el caracter '*'
        i = 1
        for linea in lineas:
            item = linea.split("*")
            print('(', i, ') ', item[0], "\t", item[3], " vs ", item[4].rstrip())
            i += 1

        nroPartida = input("       Ingrese el número de partida ->")

        # se extrae las jugadas del archivo representada por ejemplo: * | |X|O| | | | | |*
        # y se guarda cada jugada guardada en 'tablero'
        for linea in lineas:
            item = linea.split("*")
            if item[0] == 'partida #' + nroPartida:
                tablero = list(item[1].split('|'))
                tablero.pop(9)  # esta linea elimina el elemento 10 que sobra.
                mostrar_tablero(tablero)
                print(item[3], "(X) vs ", item[4].rstrip(), "(O)")

                flag, tipo = busca_ganador(tablero, "X")
                if flag:
                    print("¡¡¡Ganador ", item[3].rstrip(), " en una ", tipo)

                flag, tipo = busca_ganador(tablero, "O")
                if flag:
                    print("¡¡¡Ganador ", item[4].rstrip(), " en una ", tipo)
    print()
    input("  Presiona cualquier tecla para continuar... ")


def guardar_ganadores(nombre):
    # guarda partida antes de haber terminado
    # ejemplo contenido de linea:  NombreGanador1
    file = pathlib.Path("historico_ganadores.txt")
    if file.exists():
        f = open("historico_ganadores.txt", "r")
        lines = len(f.readlines())
        f.close()

        g = open("historico_ganadores.txt", "a")
        g.write(nombre + '\n')
        g.close()
    else:
        g = open("historico_ganadores.txt", "w")
        g.write(nombre + '\n')
        g.close()


def submenu_ganadores():
    os.system('cls')
    print("       [5] Ranking partidas ganadas por nombre jugador")
    print("   ==========================================================")
    print("       ")
    print("Partidas de jugadas pasadas:")
    print("--------------------------")

    print(" (1) Numero de partidas ganadas ascendente")
    print(" (2) Numero de partidas ganadas descendente")
    print(" (3) Numero de jugadores ascendente")
    print(" (4) Numero de jugadores descendente")
    print(" (5) Salir")

    return input("  Escoge una opción-> ")


def orderna_nombres_insertion_sort(lista, orden):
    # ordenamiento por orden
    for i in range(1, len(lista)):
        h = i
        if orden == "D":  # orden descendente
            while h > 0 and lista[h][0].upper() > lista[h - 1][
                0].upper():  # lista[X][0] contiene nombre del diccionario
                aux = lista[h]
                lista[h] = lista[h - 1]
                lista[h - 1] = aux
                h = h - 1
        if orden == "A":  # orden descendente
            while h > 0 and lista[h][0].upper() < lista[h - 1][
                0].upper():  # lista[X][0] contiene nombre del diccionario
                aux = lista[h]
                lista[h] = lista[h - 1]
                lista[h - 1] = aux
                h = h - 1


def orderna_partidas_insertion_sort(lista, orden):
    # ordenamiento por orden
    for i in range(1, len(lista)):
        h = i
        if orden == "D":  # orden descendente
            while h > 0 and lista[h][1] > lista[h - 1][1]:  # lista[X][1] contiene valor del diccionario
                aux = lista[h]
                lista[h] = lista[h - 1]
                lista[h - 1] = aux
                h = h - 1
        if orden == "A":  # orden descendente
            while h > 0 and lista[h][1] < lista[h - 1][1]:  # lista[X][1] contiene valor del diccionario
                aux = lista[h]
                lista[h] = lista[h - 1]
                lista[h - 1] = aux
                h = h - 1


def lista_ganadores(lista):
    print("")
    for i in range(0, len(lista)):
        print(lista[i][0], " -> ", lista[i][1], " juagadas")
    print("")


def mostrar_nombres_ganadores():
    op = 0

    file = pathlib.Path("historico_ganadores.txt")
    ranking_ganadores = {}
    # valida existencia del archivo
    if file.exists():
        f = open("historico_ganadores.txt", "r")
        # ejemplo contenido de linea:  jugador1
        lineas = f.readlines()
        f.close()

        # recorremos todas las lineas para listar las partidas
        # cada elemento del archivo está separado por el caracter '*'
        i = 1

        for linea in lineas:  # se contruye conteo de ganadas por jugador
            item = linea.rstrip()
            if item not in ranking_ganadores:
                ranking_ganadores[item] = 1
            else:
                i = ranking_ganadores[item]
                i += 1
                ranking_ganadores[item] = i

    while op != 5:
        op = submenu_ganadores()
        if op == '1':
            # diccionario se pasa a lista
            lista = list(ranking_ganadores.items())
            orderna_partidas_insertion_sort(lista, "A")
            lista_ganadores(lista)
            input("  Presiona cualquier tecla para contianuar....")
        elif op == '2':
            # diccionario se pasa a lista
            lista = list(ranking_ganadores.items())
            orderna_partidas_insertion_sort(lista, "D")
            lista_ganadores(lista)
            input("  Presiona cualquier tecla para contianuar....")
        elif op == '3':
            # diccionario se pasa a lista
            lista = list(ranking_ganadores.items())
            orderna_nombres_insertion_sort(lista, "A")
            lista_ganadores(lista)
            input("  Presiona cualquier tecla para contianuar....")
        elif op == '4':
            # diccionario se pasa a lista
            lista = list(ranking_ganadores.items())
            orderna_nombres_insertion_sort(lista, "D")
            lista_ganadores(lista)
            input("  Presiona cualquier tecla para contianuar....")
        elif opcion == '5':
            break


###############PROGRAMA PRINCIPAL###############
# SE CREA EL ARCHIVO historico_tres_raya.txt PARA ALMACENAR LAS JUAGADAS GANADORAS
# ESTAN SEPARADO POR * : NOMBRE_PARTIDA*TABLERO*CANTIDAD_JUGADAS
# ejemplo:   partida #2* |X|O|X|O|X|O| | |*6

# SE CREA EL ARCHIVO guardadas_tres_raya.txt PARA ALMACENAR LAS JUAGADAS QUE SE GUARDAN SIN TERMINAR,
# ESTAN SEPARADO POR * : NOMBRE_PARTIDA*TABLERO*JUGADOR_QUE_LE_TOCA
# ejemplo:   partidaGuardada* | |X|O| | | | | |*X

opcion = 0
while opcion != 7:
    opcion = menu_principal()
    if opcion == '1':
        jugar_tres_raya()
    elif opcion == '2':
        listar_partidas_guardadas()
    elif opcion == '3':
        ver_partidas_nro_jugadas()
    elif opcion == '4':
        mostrar_todos_tableros()
    elif opcion == '5':
        mostrar_nombres_ganadores()
    elif opcion == '6':
        jugar_tres_raya_computador()
    elif opcion == '7':
        quit()
