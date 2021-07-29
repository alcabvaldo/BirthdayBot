import json
import datetime
import os           #para el get current directory (gcd) (BORRAR DESPUES)



######################################################
def add_cumple(nuevo_miembro):
    """
        Reciebe un miembro y lo guarda en el Json
        retorna un string diciendo si es que se añadió o no el cumpleaños
    """

    # verifico que los datos introducidos hayan sido validos
    ans = es_miembro_invalido(nuevo_miembro)
    if ( ans ):
        respuestas = {
            1: "Para introducir un cumpleaños debe ser de esta manera:\n cumplecargar <dia> <mes> <inicial>",
            2: "El formato debería ser:\n cumplecargar <dia> <mes> <inicial>",
            3: "La inicial debería tener solo una letra",
            4: "Esa fecha no es válida"
        }
        return respuestas[ans]


    #traigo la lista de cumpleaños guardados del json
    miembros = get_miembros()

    pos = find_pos_of_miembro(nuevo_miembro,miembros)
    if ( pos == 0 ): #todavia no esta en la lista

        # new_miembro sera el k-ésimo miembro
        k = miembros["count"] + 1

        miembros[k] = nuevo_miembro
        miembros["count"] = miembros["count"] + 1
        actualizar_miembros(miembros)
        
        return "añadido!"

    else : #ya esta en la lista, entonces actualiza
        miembros[str(pos)] = nuevo_miembro
        actualizar_miembros(miembros)

        return "actualizado!"


def find_pos_of_miembro(new_miembro,miembros):
    """
        Retorna la posicion de la persona en la lista
        Retorna 0 si no se encuentra
    """
    for clave, persona in miembros.items():
        #verifica que no sea count para que funcione, esto es por como hice el json
        if (clave != "count") and ((persona["Id"])==new_miembro["Id"]) and ((persona["Server"])==new_miembro["Server"]) :
            return int(clave) 
            #aca estoy asumiento que es un int, esta bien eso?
    return 0

def verificar_fecha(mes,dia):
    """Verifica si una fecha dada es válida"""
    try:
        datetime.date(datetime.MINYEAR,int(mes),int(dia))
        return True
    except Exception as e :
        return False

def es_miembro_invalido(miembro):
    """
        Verifica si el formato de un miembro es el adecuado
        retorna numericos para distintos tipos de errores
        1: datos son nulos
        2: datos no son del tipo correcto
        3: la inicial tiene mas de una letra
        4: fecha invalida
        
        0: no detectó ningun error, el miembro sí es valido
    """
    dia = miembro["dia"]
    mes = miembro["mes"]
    inicial = miembro["Inicial"]

    if (dia==None or mes==None or inicial== None):
        return 1
    if ( not(str(dia).isnumeric()) or not(str(mes).isnumeric()) ):
        return 2
    if (len(inicial)>1):
        return 3
    if (verificar_fecha(mes,dia) == False):
        return 4   
    
    return 0








def str_proximo_cumple(server):
    """
        Retorna un texto diciendo quien sera la proxima persona en cumplir años
    """
    mes_actual = datetime.date.today().month
    dia_actual = datetime.date.today().day
    miembros = get_miembros()
    proxima_persona = find_next_birthday(server,miembros)
    #para mas readability
    nombre = proxima_persona["Nombre"] 
    dia = proxima_persona["dia"]
    mes = proxima_persona["mes"]

    dias_que_faltan = diferencia_de_fechas(mes_actual,dia_actual,int(mes),int(dia))
    if (dias_que_faltan>1):
        return ("El próximo cumple es el de "+nombre+" ("+dia+"/"+mes+"). Faltan "+str(dias_que_faltan)+" dias!!!!")
    elif (dias_que_faltan==1):
        return ("El próximo cumple es el de "+nombre+" ("+dia+"/"+mes+"). Es mañana!!!")
    else: ## asumo que dias que faltan no es menor a 0 xd 
        return ("Feliz cumple "+nombre+"!!!!")







def find_next_birthday(server,miembros):
    """
        Encuentra a la persona con el cumpleaños mas proximo en un server especifico
        
        Parametros:
            server (str) : Id del server
            miembros (el json) : el json (en forma de diccionario) con los datos guardados 
        Retorna:
            persona_mas_cercana (miembro): la persona
    """

    #fecha actual en dias desde 1 de enero
    mes_actual = datetime.date.today().month
    dia_actual = datetime.date.today().day

    #diferencia minima encontrada entre dos fechas
    mindiff = 366
    persona_mas_cercana = None

    for clave, persona in miembros.items():
        #se evita count que es el primer elemento en el json
        if (clave!= "count" and persona["Server"] == server):
            
            #halla cuanto falta para el cumpleaños de persona en relacion a fecha actual
            dif = diferencia_de_fechas(mes_actual,dia_actual,int(persona["mes"]),int(persona["dia"]))
            
            if (dif < mindiff):
                mindiff = dif
                persona_mas_cercana = persona

    if (persona_mas_cercana): #por si no haya nadie
        return persona_mas_cercana    



#retorna cuanto falta desde la primera fecha para llegar a la segunda #####################
#considera que la segunda fecha siempre es despues de la primera, asi sea el año siguiente
def diferencia_de_fechas(mes1,dia1,mes2,dia2):
    hoy = dias_desde_1enero(mes1,dia1)
    futuro = dias_desde_1enero(mes2,dia2)
    if (futuro>=hoy) : #si la fecha es posterior dentro del año
        return futuro-hoy
    elif (futuro<hoy) : #si la fecha es antes en fecha (pasado el año nuevo)
        return futuro+365-hoy


# calcula la cantidad de dias pasados desde el 01/01 hasta esa fecha ####################
#source: https://stackoverflow.com/questions/620305/convert-year-month-day-to-day-of-year-in-python
def dias_desde_1enero(mes, dia):
    auxdate = datetime.date(datetime.MINYEAR,int(mes),int(dia))
    diasdesdeenero = auxdate.timetuple().tm_yday
    #print("para el "+mes+"/"+dia+"los dias son: "+str(diasdesdeenero))
    return diasdesdeenero








#aca falta considerar si es que no existe el archivo

#############################################
def get_miembros():
    """retorna <miembros>, la lista con los integrantes y sus datos"""
    #print(os.getcwd())
    with open("src/data_file.json","r") as archivo:
        miembros = json.load(archivo)
        return miembros


#############################################
def actualizar_miembros(miembro):
    """Recibe la lista actualizada <miembros> y la guarda en el json"""
    with open("src/data_file.json","w") as archivo:
        json.dump(miembro,archivo,indent="   ")