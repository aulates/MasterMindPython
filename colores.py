# coding=utf-8
def construye_tabla_formatos():
    for colortexto in range(30, 38):
        cad_cod = ''
        for colorfondo in range(40, 49):
            fmto = ';'.join([str(0),
                             str(colortexto),
                             str(colorfondo)])
            cad_cod += "\033[" + fmto + "m " + fmto + " \033[0m"
        print(cad_cod)
    print('\n')


# construye_tabla_formatos()


"""
       0: Sin efecto
       1: Debil
       2: Negrita
       3: Cursiva
       4: Subrayado
       5: Inverso
       6: Oculto
       7: Tachado

       Colores	    Texto   Fondo
       Negro	    30	    40
       Rojo	        31	    41
       Verde	    32	    42
       Amarillo	    33	    43
       Azul	        34	    44
       Morado	    35	    45
       Cian	        36	    46
       Gris         30      47
       Blanco	    37	    48
       """""


def print_color(mensaje, estilo=0, colortexto=30, colorfondo=38, end="\n"):
    cad_cod = ''
    fmto = ';'.join([str(estilo), str(colortexto), str(colorfondo)])
    cad_cod += "\033[" + fmto + "m " + mensaje + " \033[0m"  # + end
    return cad_cod


# print_color("hola mundo")

# print_color("Hola Mundo",0,30,45)

