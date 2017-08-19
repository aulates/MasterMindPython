# coding=utf-8
import time
import random


# Clase Principal
class Principal:
    def __init__(self):
        self.registro = {}
        self.sesion_iniciada = ""

    # Registrar un nuevo usuario
    def nuevo_usuario(self, aprobar, registro, records):
        cedula = raw_input("Digite su ID: ")
        if cedula not in registro:  # Para veificar que el usuario no exista
            while True:  # Valida que en el nombre no se digiten números y sean solo letras
                nombre = raw_input("Digite su nombre completo: ")
                datos = ("".join([x for x in nombre if x.isdigit()]))  # se saca los números que se digiten en el nombre
                numerico = datos.isdigit()  # Si es True hay números si es False no hay números
                if not numerico:  # no hay numeros, puede seguir
                    break
                else:  # si hay numeros se pide nuevamente el nombre del usuario
                    print("Ingrese solo letras")
            while True:  # Valida que sean solo números y no letras
                try:  # Si se cumple puede seguir
                    edad = int(input("Digite su edad: "))
                    break
                except:  # Si no se cumple, se solicita nuevamente
                    print("Ingrese valor Numerico")
            while True:
                correo = raw_input("Digite su correo electronico: ")
                arroba = "@"
                if arroba in correo:
                    break
                else:
                    print("Digite nuevamente su correo")
            contrasena = raw_input("Digite la contraseña: ")
            while True:  # Tipos de usuarios
                tipo = raw_input("1. Administrador.\n2. Jugador\n\nSeleccione el tipo de usuario: ")
                if tipo.isdigit() and int(tipo) < 3:  # Si la variable tipo es 1 o 2
                    tipo = int(tipo)  # la variable va a ser un entero
                    break
            condicion = 0  # El campo "condicion" guarda 0 por defecto ya que debe esperar la aprobacion
            registro[cedula] = [cedula, nombre, edad, correo, contrasena, tipo, condicion]
            aprobar.append(cedula)  # El nuevo usuario se agrega a la lista de usuarios esperando aprobacion
            if tipo == 2:   # Si es de tipo jugador
                records[cedula] = []  # Se guarda el ID del usuario en el diccionario de records personales
            print("\nSe ha registrado exitosamente")
        else:  # Si el ID ya existe no se puede volver a guardar
            print("\nEl usuario ya existe!!")


# Clase jugador
class Jugador:
    def __init__(self):
        self.inscripciones = {}  # Torneos en los que se han inscrito los jugadores
        self.records = {}  # Records del usuario

    # Torneos disponibles
    def menu_torneos(self, torneos, inscripciones, sesion_iniciada):
        torneos_disponibles = {}
        menu = "\nTORNEOS DISPONIBLES\n\n"
        posicion = 1
        for i in torneos:  # Para crear el menú con los torneos disponibles para mostrarlos al usuario
            if torneos[i][4] < torneos[i][0]:  # Para verificar que el torneo aun no este lleno
                torneos_disponibles[posicion] = i
                menu += str(posicion) + ". " + i + ":\n"
                if torneos[i][3] == 1:
                    duplicados = "SI"  # Para agregar duplicados
                else:
                    duplicados = "NO"  # Para no agregar los duplicados
                menu += "Maximo de participantes: {}\n" \
                        "Nivel de dificultad: {}\n" \
                        "Máximo de intentos: {}\n" \
                        "Duplicados: {}\n".format(torneos[i][0], torneos[i][1], torneos[i][2], duplicados)
                menu += "\n"
                posicion += 1
        menu += "Ingrese el numero del torneo en el que desea participar: "
        while True:  # imprime el menú de torneos disponibles
            opcion = raw_input(menu)
            if opcion.isdigit():
                opcion = int(opcion)
            if opcion in torneos_disponibles:  # verificar que la opción digitada exista en torneos
                if not torneos_disponibles[opcion] in inscripciones[sesion_iniciada]:  # Verificar que no se haya inscrito en el torneo
                    nombre_torneo = torneos_disponibles[opcion]
                    torneos[nombre_torneo][4] += 1  # Aumentar el numero de jugadores inscritos
                    inscripciones[sesion_iniciada].append(nombre_torneo)  # agregar un participante al torneo
                    break
                else:
                    print("\nYa está inscrito en el torneo!!")
                    break
            else:  # La opcion no es válida
                print("\nLa opción no existe, intente de nuevo")

    def ver_records(self, sesion_iniciada):  # Records del usuario, según ID
        resultados = self.records[sesion_iniciada]  # records de la sesión iniciada
        dificultad = 1
        records = {}  # Diccionario de los record del usuario
        while dificultad <= 6:  # Mostrar el mejor tiempo en cada dificultad
            tiempo = 99999  # Tiempo máximo por defecto
            intentos = 50  # intentos máximos por defecto
            records[dificultad] = [" -- ", "-"] # Por defecto no hay ningun record
            for r in resultados:  # para recorrer los records del usuario
                if r[2] == dificultad:  # para ordenarlos por nivel de dificultad
                    if r[0] < tiempo:   # si es un mejor tiempo
                        tiempo = r[0]
                        intentos = r[1]
                        t = print_timer(tiempo)
                        records[dificultad] = [t, r[1]]
                    elif r[0] == tiempo:    # Si el tiempo es igual
                        if r[1] < intentos: # Si tiene menos intentos
                            tiempo = r[0]
                            intentos = r[1]
                            t = print_timer(tiempo)
                            records[dificultad] = [t, r[1]]
            dificultad += 1
        print("\n\nMEJOR TIEMPO EN CADA NIVEL DE DIFICULTAD\nDificultad\tTiempo\tIntentos")
        dificultad = 1
        for x in range(6):
            print("\t{}\t\t{}\t\t{}".format(dificultad, print_timer(records[dificultad][0]), records[dificultad][1]))
            dificultad += 1


# Clase administrador
class Administrador:
    def __init__(self):
        self.aprobar = []  # lista de usuarios que se registraron pero no han sido aprobados
        self.torneos = {}
        self.torneos_terminados = []
        self.records_torneos = {}

    # Funcion de aprobar o negar jugadores
    def aprobar_jugador(self, registro, aprobar, inscripciones):
        print("\nLista de jugadores esperando aprobación: ")
        cont = 1
        for x in aprobar:  # para ver los usuarios sin aprobar
            print(str(cont) + ". " + x)
            cont += 1
        num = int(input("Digite el número del jugador en la lista: "))
        id = aprobar[num - 1]
        if registro[id][5] == 1:  # tipo de usuario
            tipo = "Administrador"
        else:
            tipo = "Jugador"
        while True:
            print("\nInformación del jugador:\n\n"
                  "Nombre: {}\n"
                  "Edad: {}\n"
                  "Correo: {}\n"
                  "Tipo: {}\n".format(registro[id][1], registro[id][2], registro[id][3], tipo))
            opcion = int(input(menu_aprobar))
            if opcion == 1:
                registro[id][6] = 1
                inscripciones[id] = []  # Cuando se aprueba un jugador se le crea un campo para inscribirse en torneos
                break
            elif opcion == 2:
                registro[id][6] = 2
                break
            else:
                print("La opcion no existe, intente de nuevo")
        aprobar.remove(id)  # cuando aprueba o desaprueba un usuario se quita de la lista de espera llamada aprobar

    # Crear torneos
    def crear_torneos(self, torneos):
        nombre_torneo = raw_input("Digite el nombre del torneo:  ")
        cantidad_participantes = int(input("Cantidad mínima de participantes: "))
        nivel_dificultad = int(input("Nivel de dificultad: "))
        maximo_intentos = int(input("Cantidad máxima de intentos: "))
        while True:  # para saber si el torneo tiene duplicados o no
            print("\nDuplicados: \n1.Sí \n2.No")
            opcion = raw_input("Se permiten duplicados: ")
            # si la opción en un dígito y un entero menor a tres
            if opcion.isdigit() and int(opcion) < 3:
                opcion = int(opcion)
                break
            else:
                print("\nLa opción no existe, intente de nuevo\n")
        torneos[nombre_torneo] = [cantidad_participantes, nivel_dificultad, maximo_intentos, opcion, 0, 0]

    # Modificar los torneos
    def modificar_torneos(self, torneos):
        print("\nModificación de un torneo\n")
        nombre_torneo = raw_input("Digite el nombre del torneo:  ")
        if nombre_torneo in torneos:  # si el nombre del torneo esta en la lista de torneos
            cantidad_participantes = int(input("Cantidad de participantes: "))
            nivel_dificultad = int(input("Nivel de dificultad: "))
            maximo_intentos = int(input("Cantidad máxima de intentos: "))
            while True:  # para cambiarle los duplicados o no duplicados
                print("\nDuplicados: \n1.Sí \n2.No")
                opcion = raw_input("Se permiten duplicados: ")
                # si la opción en un dígito y un entero menor a tres
                if opcion.isdigit() and int(opcion) < 3:
                    opcion = int(opcion)
                    break
                else:
                    print("\nLa opción no existe, intente de nuevo\n")
            torneos[nombre_torneo] = [cantidad_participantes, nivel_dificultad, maximo_intentos, opcion, 0, 0]
        else:
            print("\nEl torneo no existe!!\n")

    # Eliminar los torneos
    def eliminar_torneos(self, torneos):
        nombre_torneo = raw_input("\nDigite el nombre del torneo:  ")
        if nombre_torneo in torneos:
            del torneos[nombre_torneo]  # elimina el torneo del diccionario de torneos
        else:
            print("\nEl torneo no existe!!")

    # Quitar de torneos y agregar a torneos finalizados
    def torneos_finalizados(self):
        terminados = []
        for i in self.torneos:
            if self.torneos[i][5] == self.torneos[i][0]:
                self.torneos_terminados.append(i)  # agrega el torneo que ya finalizo en la lista terminados
                terminados.append(i)
        for t in terminados:
            del self.torneos[t]  # elimina el torneo terminado de torneos

    # Funcion para ver el ganador de los torneos
    def ganador_torneo(self):
        menu = ""
        cont = 1
        # Para revisar los torneos terminados
        for x in self.torneos_terminados:
            menu += str(cont) + ". " + x + "\n"
            cont += 1
            print(menu)
        while True:
            opcion = int(input("Seleccione un torneo: "))
            if opcion <= len(self.torneos_terminados):
                nombre_torneo = self.torneos_terminados[opcion - 1]
                resultados = self.records_torneos[nombre_torneo]
                jugador = resultados[0][0]
                tiempo = resultados[0][1]
                intentos = resultados[0][2]
                # Para sacar el ganador de cada torneo
                for x in resultados:
                    if x[1] < tiempo:
                        jugador = x[0]
                        tiempo = x[1]
                        intentos = x[2]
                    elif x[1] == tiempo:
                        if x[2] < intentos:
                            jugador = x[0]
                            tiempo = x[1]
                            intentos = x[2]
                print("Torneo: {}\nId: {}\nNombre: {}\nTiempo: {}\n"
                      "Intentos: {}".format(nombre_torneo, jugador, p.registro[jugador][1], print_timer(tiempo),
                                            intentos))
                break

    # Diez mejores jugadores
    def diez_mejores(self, dificultad, records):
        records_nivel = []
        tiempos = []
        diez_mejores = []
        for x in records:
            for y in records[x]:
                if y[2] == dificultad:  # Saca el ganador por nivel de dificultad
                    records_nivel.append(y)
                    tiempos.append(y[0])
        tiempos.sort()
        if len(tiempos) > 10:
            tiempos = tiempos[:10]
        for t in tiempos:
            for r in records_nivel:
                if r[0] == t and r not in diez_mejores:  # Para revisar que el record no este ya en la lista
                    diez_mejores.append(r)  # agregar a la lista de mejores jugadores

        print("   Tiempo    Intentos")
        cont = 1  # Da el lugar de cada jugador, ya sea 1,2,3,4,5...
        for x in diez_mejores:
            print("{}.  {}     {}".format(cont, print_timer(x[0]), x[1]))
            cont += 1

    # Mejor jugador, el que haya ganado el juego mas dificil en el menor tiempo.
    def mejor_jugador(self, records):
        nivel = 1
        tiempo = 99999
        intentos = 50
        mejor = {}
        # Para ver los jugadores que ya estan guardados en records
        for j in records:
            for r in records[j]:
                if r[2] >= nivel:
                    if r[2] > nivel:
                        nivel = r[2]
                        tiempo = 99999
                        intentos = 50
                        if r[0] < tiempo:
                            tiempo = r[0]
                            intentos = r[1]
                            jugador = j
                            mejor[str(nivel)] = [tiempo, intentos, jugador]
                        elif r[0] == tiempo:
                            if r[1] < intentos:
                                tiempo = r[0]
                                intentos = r[1]
                                jugador = j
                                mejor[str(nivel)] = [tiempo, intentos, jugador]
        nivel = str(nivel)
        # El mejor jugador que esta guardado en records
        print("\nMEJOR JUGADOR\n>> {}\nDificultad: {}\nTiempo: {}\nIntentos: {}".format(mejor[nivel][2], nivel,
                                                                                        print_timer(mejor[nivel][0]),
                                                                                        mejor[nivel][1]))


# Clase Juego
class Juego:
    def __init__(self):
        self.jugador = ""
        self.dificiltad = 0
        self.duplicados = 0

    # Generar una lista de colores aleatoria
    def nuevo_juego(self, duplicados, dificultad):
        respuesta = []
        while len(respuesta) < dificultad:
            n = random.randint(41, 46)
            if not n in respuesta:  # El nuemro se agrega solo si no esta en la lista
                respuesta.append(n)
        if duplicados == 1:  # Si se permiten duplicados
            # Generar el duplicado reemplazando uno de los numeros por otro que ya exista en la lista
            p = random.randint(0, len(respuesta) - 1)  # La posicion que vamos a remplazar
            r = random.randint(0, len(respuesta) - 1)  # El numero por el que remplazamos
            while r == p:  # Para asegurarnos de que los dos numeros aleatorios sean diferentes
                r = random.randint(0, len(respuesta) - 1)
            respuesta[p] = respuesta[r]
        return respuesta

    # Para agregar al menu de juegos los torneos iniciados
    def torneos_iniciados(self, torneos, inscripciones, sesion_iniciada):
        mis_torneos = inscripciones[sesion_iniciada]  # Guardas las inscripciones del usuario iniciado
        t_iniciados = []
        for x in mis_torneos:
            if torneos[x][4] == torneos[x][0]:
                t_iniciados.append(x)  # Se agrega el torneo que ya se inicio
        menu = "0. Volver\n" \
               "1. Partida local\n\n"
        if len(t_iniciados) >= 1:
            cont = 2
            menu += "Torneos iniciados:\n"
            for x in t_iniciados:
                menu += str(cont) + ". " + x + "\n"
                cont += 1
            print(menu)
        else:
            print(menu)
        return t_iniciados

    # Diccionario de colores
    def contar_colores(self, lista):
        diccolores = {}  # Diccionario de los colores
        for x in lista:
            diccolores[x] = lista.count(x)
        return diccolores

    # Funcion para revisar la combinacion de colores que propone el jugador
    def revisar(self, respuesta, combinacion):
        correctas = 0
        coinciden = 0
        resp = self.contar_colores(respuesta)
        for x in range(len(respuesta)):  # Para comparar la opción propuesta por el usuario y la combinación correcta
            if combinacion[x] == respuesta[x]:
                if int(resp[combinacion[x]]) > 0:
                    correctas += 1
                    resp[combinacion[x]] -= 1
            elif combinacion[x] in respuesta:
                if int(resp[combinacion[x]]) > 0:
                    coinciden += 1
                    resp[combinacion[x]] -= 1
        cad_cod = ''
        pistas = ""
        pistas += (print_color("*", 1, 38, 40) + " ") * correctas
        pistas += (print_color("*", 1, 30, 47) + " ") * coinciden
        cad_cod += "        >> " + pistas
        return cad_cod

    # Juego
    def jugar(self, respuesta, max_intentos=49):
        start = time.time()  # inicia el tiempo para guardarlo en records, y al final imprimir cuanto tiempo duro jugando
        intentos = 0
        while True:  # Para comparar la cantidad inicial de intentos con la máxima de intentos
            if intentos < max_intentos:
                c = raw_input("\nDigite su propuesta: ")
                combinacion = c.split(",")
                valido = True
                try:
                    for x in range(len(combinacion)):
                        # Convertir cada dígito de la combinacion en su respectivo código de color
                        if int(combinacion[x]) > 6:
                            valido = False
                        combinacion[x] = int(combinacion[x]) + 40
                except ValueError:
                    valido = False
                if valido:
                    if len(combinacion) == len(respuesta):
                        cad_cod = ''
                        for color in combinacion:
                            fmto = ';'.join([str(1), str(30), str(color)])
                            cad_cod += "\033[" + fmto + "m " + "**" + " \033[0m" + " "
                        print("\t\t\t\t\t\t\t\t\t" + cad_cod + g.revisar(respuesta, combinacion))
                        intentos += 1
                    else:
                        print("Debe ingresar {} números".format(len(respuesta)))
                else:
                    print("Digite solo numeros entre 1 y 6 separados por comas!!")
                # Si la combinación es igual a respuesta
                if combinacion == respuesta:
                    end = time.time()  # termina el tiempo
                    timer = end - start  # Se saca cuanto duró jugando
                    gano = True
                    print("\nGANASTE\nTiempo: {} Intentos: {}".format(print_timer(timer), intentos))
                    break
            # Si agoto los intentos antes de terminar el juego
            else:
                print("Has agotado el número de intentos :(")
                end = time.time()  # detiene el tiempo
                timer = round(end - start)  # redondea lo que duró
                cad_cod = ''
                for color in respuesta:
                    fmto = ';'.join([str(1), str(30), str(color)])
                    cad_cod += "\033[" + fmto + "m " + "**" + " \033[0m" + " "
                print("\n\t\t\t\t\t\t\t\t" + cad_cod + "\nPERDISTE\nTiempo: {} Intentos: {}".format(print_timer(timer),
                                                                                                    intentos))
                gano = False
                break
                # retorna que perdió, el tiempo, y los intentos usados
        return [gano, round(end - start), intentos]
        # Agregar el resultado del usuario en records de la sesión iniciada

    def agregar_record(self, records, sesion_iniciada, resultado):
        records[sesion_iniciada].append(resultado)


"""Objetos"""
p = Principal()
a = Administrador()
j = Jugador()
g = Juego()

## Datos por defecto ##

# registro["ced"] = ["ced", "nombre", "edad", "correo", "contrasena", "tipo de usuario", "condicion"]
# La condicion puede ser = 0:esperando aprobacion, 1:aprobado, 2:rechazado
p.registro["207770677"] = ["207770677", "Carol Sandi", "19", "casandif@est.utn.ac.cr", "caroladrisf", 1, 1]
p.registro["201230123"] = ["201230123", "Ana Ulate", "18", "ana@est.utn.ac.cr", "anita2017", 1, 1]
p.registro["101110111"] = ["101110111", "Jimena M", "16", "vane@gmail.com", "jimena", 2, 1]
p.registro["202220222"] = ["202220222", "Pedro P", "28", "pepe@hotmail.com", "pepe", 2, 1]
p.registro["303330333"] = ["303330333", "Julia A", "14", "juliaa@gmail.com", "julita", 2, 1]
p.registro["404440444"] = ["404440444", "Raul F", "17", "raulf@gmail.com", "RAUL", 2, 1]
p.registro["505550555"] = ["505550555", "Edgar H", "21", "edgarh@gmail.com", "12345", 2, 0]
p.registro["606660666"] = ["606660666", "Sonia L", "34", "sonial33@gmail.com", "$oniA", 2, 0]
p.registro["707770777"] = ["707770777", "Rosa J", "25", "rosa@gmail.com", "rosita", 2, 0]

# records[id] = [tiempo, intentos, dificultad]
j.records["101110111"] = [[221, 4, 1], [357, 17, 3], [129, 5, 1], [229, 9, 4], [206, 14, 4], [302, 4, 1], [331, 14, 4],
                          [130, 5, 2], [229, 8, 4], [591, 22, 5], [392, 12, 6]]
j.records["202220222"] = [[218, 5, 4], [256, 17, 5], [123, 5, 1], [229, 9, 4], [206, 14, 4], [302, 4, 6], [331, 14, 4],
                          [130, 4, 4], [229, 8, 4], [529, 22, 4], [392, 12, 6]]
j.records["303330333"] = [[114, 3, 1]]
j.records["404440444"] = []
j.records["505550555"] = []
j.records["606660666"] = []
j.records["707770777"] = [[124, 7, 4], [256, 20, 4], [148, 4, 4], [229, 7, 4], [256, 14, 4], [392, 4, 6]]

# torneos["nombre"] = ["min participantes", "dificultad", "max intentos", "duplicados", "num participantes inscritos", "num participantes que ya jugaron"]
a.torneos["Gato"] = [3, 3, 5, 2, 3, 3]
a.torneos["Principiantes"] = [7, 1, 10, 2, 0, 0]
a.torneos["Campeones"] = [3, 5, 5, 1, 2, 0]
# ...
j.inscripciones["101110111"] = ["Campeones"]
j.inscripciones["202220222"] = ["Campeones"]
j.inscripciones["303330333"] = []
# ...
a.aprobar = ["404440444", "505550555", "606660666", "707770777"]
a.torneos_terminados = []
a.records_torneos["Gato"] = [["101110111", 120, 5], ["202220222", 160, 8], ["303330333", 118, 6]]
a.records_torneos["Principiantes"] = []
a.records_torneos["Campeones"] = []
## Menus ##

# Menu principal
menu_principal = ("MASTER MIND\n\n"
                  "1. Registrar\n"
                  "2. Iniciar sesión\n"
                  "3. Salir\n\n"
                  "Digite la opcion que desea realizar: ")

# Menu del administrador
menu_administrador = ("\nMENU DEL ADMINISTRADOR\n\n"
                      "1. Aprobar jugadores.\n"
                      "2. Torneos\n"
                      "3. Records\n"
                      "4. Cerrar sesión\n\n"
                      "Seleccione una opcion del menu de administrador: ")

# Menu de los jugadores que fueron aprobados por el administrador
menu_jugador_aprobado = ("\nMENU DEL JUGADOR\n\n"
                         "1. Jugar \n"
                         "2. Inscribirse en un torneo\n"
                         "3. Ver los records\n"
                         "4. Cerrar sesión\n\n"
                         "Seleccione la opción que desea realizar: ")

# Menu de los jugadores que aun no son aprobados
menu_jugador = ("\nMENU DEL JUGADOR\n\n"
                "1. Jugar partida local\n"
                "2. Ver los records\n"
                "3. Cerrar sesión\n\n"
                "Seleccione la opción que desea realizar: ")

# Menu de Torneos Administrador
menu_torneos = ("\nMENÚ TORNEOS\n\n"
                "1. Crear torneo\n"
                "2. Modificar Torneos\n"
                "3. Eliminar torneos\n"
                "4. Volver al menu de administrador\n\n"
                "Digite la opción que desea realizar: ")

# Menu para aprobar o rechazar los jugadores
menu_aprobar = "\n1.Aprobar\n" \
               "2.Rechazar\n\n" \
               "Seleccione una opción: "

# Menu de las categorias de juego
menu_categorias = "\nDIFICULTADES\n" \
                  "\nSin duplicados:\n" \
                  "1. Tres espacios\n" \
                  "2. Cuatro espacios\n" \
                  "3. Cinco espacios\n" \
                  "\nCon duplicados:\n" \
                  "4. Cuatro espacios\n" \
                  "5. Cinco espacios\n" \
                  "6. Seis espacios\n" \
                  "Seleccione una opcion: "

# Instrucciones del juego
instrucciones = "\nINSTRUCCIONES\n" \
                "\nDebe adivinar un código de {} colores {}.\n" \
                "{}\n\n" \
                "IMPORTANTE:\n" \
                "Escriba los números que corresponden a los colores SEPARADOS POR COMAS!!\n" \
                "Por ejemplo: 1,2,3\n" \
                "Por cada color en la posición correcta verá un >> {}\n" \
                "Por cada color que esté dentro del código pero en otra posición verá un >> {}"

# Menu de records del administrador
menu_record = ("\nMENU DE RECORD ADMINISTRADOR\n\n"
               "1. Ganador de un torneo\n"
               "2. Mejor Jugador\n"
               "3. Los mejores 10 jugadores\n"
               "4. Salir de este menú\n\n"
               "Seleccione una opcion del menu de records administrador:")


# imprimir el tiempo en minutos y segundos
def print_timer(tiempo):
    try:
        min = tiempo // 60
        seg = tiempo % 60
        if seg < 10:
            seg = "0" + str(seg)
        return "{}:{}".format(min, seg)
    except TypeError:
        return tiempo


# imprimir la linea de colores
def print_color(mensaje, estilo=0, colortexto=30, colorfondo=38, end="\n"):
    cad_cod = ''
    fmto = ';'.join([str(estilo), str(colortexto), str(colorfondo)])
    cad_cod += "\033[" + fmto + "m " + mensaje + " \033[0m"  # + end
    return cad_cod


# el menú de los colores que se muestran al usuario
def menu_colores():
    cad_cod = ''
    cont = 1
    for colorfondo in range(41, 47):
        fmto = ';'.join([str(0), str(30), str(colorfondo)])
        cad_cod += "\033[" + fmto + "m " + str(cont) + " \033[0m"
        cont += 1
    return cad_cod


# Opciones que se usan en el menú
def elegir_opcion(menu):
    opcion = raw_input(menu)
    return opcion


# Errores de alguna opción
def error_opcion():
    print("\nLa opcion no existe, intente nuevamente\n")


while True:
    opcion = elegir_opcion(menu_principal)  # Menu principal
    if opcion == "1":  # Registrar usuario
        p.nuevo_usuario(a.aprobar, p.registro, j.records)
    elif opcion == "2":  # Iniciar sesión
        usuario = raw_input("Digite su id: ")
        if usuario in p.registro:  # si el ID del usuario existe en registro
            datos = p.registro[usuario]
            contrasena = raw_input("Digite su contraseña: ")
            if contrasena == datos[4]:  # Verifica que la contraseña es válida
                p.sesion_iniciada = usuario
                if datos[5] == 1:  # Si el usuario es Administrador
                    while True:
                        opcion = elegir_opcion(menu_administrador)  # Menu administrador
                        if opcion == "1":  # Aprobar o negar jugadores
                            while True:
                                a.aprobar_jugador(p.registro, a.aprobar, j.inscripciones)
                                opcion = raw_input("1. Continuar\n2. Salir   ")
                                if opcion == "2":
                                    break
                        elif opcion == "2":  # Menu torneos
                            while True:
                                opcion = elegir_opcion(menu_torneos)
                                if opcion == "1":  # Crear torneos
                                    a.crear_torneos(a.torneos)
                                elif opcion == "2":  # Modificar torneos existentes
                                    a.modificar_torneos(a.torneos)
                                elif opcion == "3":  # Eliminar alguno de los torneos
                                    a.eliminar_torneos(a.torneos)
                                elif opcion == "4":  # Salir del menú
                                    break
                                else:  # Error el digito de la opción
                                    error_opcion()
                        elif opcion == "3":  # records de los torneos
                            a.torneos_finalizados()
                            while True:
                                opcion = (raw_input(menu_record))
                                if opcion == "1":
                                    a.ganador_torneo()
                                elif opcion == "2":
                                    a.mejor_jugador(j.records)
                                elif opcion == "3":
                                    dificultad = int(input(menu_categorias))
                                    a.diez_mejores(dificultad, j.records)
                                elif opcion == "4":
                                    break
                                else:
                                    error_opcion()
                        elif opcion == "4":  # Cerrar sesión
                            p.sesion_iniciada = ""  # Sale de la seción iniciada
                            break
                        else:
                            error_opcion()
                else:  # Jugador aprobado
                    if datos[6] == 1:  # Si el jugador esta aprobado
                        while True:
                            opcion = elegir_opcion(menu_jugador_aprobado)
                            if opcion == "1":  # Jugar
                                while True:
                                    t_iniciados = g.torneos_iniciados(a.torneos, j.inscripciones, p.sesion_iniciada)
                                    opcion = raw_input("Seleccione una opción: ")

                                    if opcion == "0":  # Salir
                                        break
                                    elif opcion == "1":  # Partida local
                                        while True:
                                            opcion = raw_input(menu_categorias)  # solicita la categoría  para jugar
                                            if opcion.isdigit():
                                                opcion = int(opcion)
                                                dificultad = opcion
                                                if opcion < 4:  # Sin los duplicados
                                                    du = 2
                                                    di = opcion + 2
                                                    x = "Sin duplicados"
                                                    break
                                                elif opcion < 7:  # Con los duplicados
                                                    du = 1
                                                    di = opcion
                                                    x = "Con duplicados"
                                                    break
                                        respuesta = g.nuevo_juego(du, di)
                                        # Imprime las instruciones del juego
                                        print(instrucciones.format(str(di), x, menu_colores(),
                                                                   print_color("*", 1, 38, 40),
                                                                   print_color("*", 1, 30, 47)))
                                        # Inicia el juego
                                        resultado = g.jugar(respuesta)  # pide la respuesta del juego
                                        if resultado[0]:
                                            resultado.append(dificultad)  # ....
                                            g.agregar_record(j.records, p.sesion_iniciada,
                                                             resultado)  # Agrega a records el resultado de la partida

                                    else:  # Jugar un torneo
                                        try:
                                            datos_torneo = a.torneos[t_iniciados[opcion - 2]]
                                            di = datos_torneo[1]  # Dificultad del juego
                                            du = datos_torneo[3]  # Duplicados
                                            respuesta = g.nuevo_juego(du, di)
                                            if datos_torneo[3] == 1:
                                                x = "Con duplicados"
                                            else:
                                                x = "Sin duplicados"
                                            print(instrucciones.format(str(di), x, menu_colores(),
                                                                       print_color("*", 1, 38, 40),
                                                                       print_color("*", 1, 30, 47)))

                                            # Inicia el juego
                                            resultado = g.jugar(respuesta, datos_torneo[2])
                                            datos_torneo[5] += 1  # Agregar que un jugador ya jugó el torneo
                                            a.torneos[t_iniciados[int(opcion) - 2]] = datos_torneo
                                            j.inscripciones[p.sesion_iniciada].remove(t_iniciados[
                                                                                          int(opcion) - 2])  # Una vez que jugó el torneo, este no se puede volver a jugar
                                            resultado.append(datos_torneo[1])
                                        except IndexError:  # Si elige una opcion que no está en el menu
                                            print("Opción inválida!")
                            elif opcion == "2":  # Inscribirse en un torneo
                                j.menu_torneos(a.torneos, j.inscripciones, p.sesion_iniciada)
                            elif opcion == "3":  # Ver records del jugador
                                j.ver_records(p.sesion_iniciada)
                            elif opcion == "4":  # Cerrar sesión
                                p.sesion_iniciada = ""
                                break
                            else:  # error en la opción digitada
                                error_opcion()
                    else:
                        while True:  # Menu jugador sin aprobar
                            opcion = elegir_opcion(menu_jugador)
                            if opcion == "1":
                                while True:
                                    opcion = raw_input(menu_categorias)  # solicita la categoría  para jugar
                                    if opcion.isdigit():
                                        opcion = int(opcion)
                                        dificultad = opcion
                                        if opcion < 4:  # Sin los duplicados
                                            du = 2
                                            di = opcion + 2 # A opción se le suma 2 porque en el menú esta de 1 a 3 y en las categorias son de 3 a 5 espacios
                                            x = "Sin duplicados"
                                            break
                                        elif opcion < 7:  # Elige la categoría de 4 a 6 espacios
                                            du = 1
                                            di = opcion
                                            x = "Con duplicados"
                                            break
                                respuesta = g.nuevo_juego(du, di)
                                print(instrucciones.format(str(di), x, menu_colores(), print_color("*", 1, 38, 40),
                                                           print_color("*", 1, 30, 47)))
                                # Inicia el juego
                                resultado = g.jugar(respuesta)  # Respuesta que el usuario digito
                                if resultado[0]:
                                    resultado.append(dificultad)
                                    g.agregar_record(j.records, p.sesion_iniciada, resultado[1:])
                            elif opcion == "2":  # Records del jugador sin aprobar
                                j.ver_records(p.sesion_iniciada)

                            elif opcion == "3":  # Cerrar sesión
                                p.sesion_iniciada = ""
                                break
                            else:
                                error_opcion()
            else:
                print("\nContraseña incorrecta\n")  # La contraseña no es la misma que esta en el registro
        else:
            print("\nUsuario inexistente\n")  # El usuario no existe en registro
    elif opcion == "3":  # Sale del juego
        break
    else:  # Error en alguna opción digitada
        error_opcion()
