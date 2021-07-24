import json
import datetime
import os           #para el get current directory (gcd) (BORRAR)



######################################################
def add_cumple(nuevo_miembro):
    """
        Reciebe un miembro y lo guarda en el Json
        retorna un string diciendo si es que se añadió o no el cumpleaños
    """

    #traigo la lista de cumpleaños guardados del json
    miembros = get_miembros()

    # new_miembro sera el k-ésimo miembro
    k = miembros["count"] + 1
    
    pos = find_pos_of_miembro(nuevo_miembro,miembros)

    if ( pos == 0 ): #todavia no esta en la lista
        miembros[k] = nuevo_miembro
        miembros["count"] = miembros["count"] + 1
        actualizar_miembros(miembros)
        
        return "añadido!"
    else : #ya esta en la lista, entonces actualiza
        miembros[pos] = nuevo_miembro
        actualizar_miembros(miembros)

        return "actualizado!"


def find_pos_of_miembro(new_miembro,miembros):
    """
        Retorna la posicion de la persona en la lista
        Retorna 0 si no se encuentra
    """
    for clave, persona in miembros.items():
        #verifica que no sea count para que funcione, esto es por como hice el json
        if (clave != "count") and ((persona["Nombre"])==new_miembro["Nombre"]) and ((persona["Server"])==new_miembro["Server"]) :
            return int(clave) 
            #aca estoy asumiento que es un int, esta bien eso?
    return 0







def str_proximo_cumple(server):
    """
        Retorna un texto diciendo quien sera la proxima persona en cumplir años
    """
    mes_actual = datetime.date.today().month
    dia_actual = datetime.date.today().day
    miembros = get_miembros()
    proxima_persona = find_next_birthday(server,miembros)
    dias_que_faltan = diferencia_de_fechas(mes_actual,dia_actual,int(proxima_persona["mes"]),int(proxima_persona["dia"]))
    return ("El proximo cumple es el de "+proxima_persona["Nombre"]+" ("+proxima_persona["dia"]+"/"+proxima_persona["mes"]+"), Faltan "+str(dias_que_faltan)+" dias!!!!")







def find_next_birthday(server,miembros):
    """
        Encuentra a persona con el cumpleaños mas proximo en un server especifico
        
        Parametros:
            server (str) : nombre del server
            miembros (el json) : el json (en forma de diccionario) con los datos guardados 
    """

    #fecha actual en dias desde 1 de enero
    mes_actual = datetime.date.today().month
    dia_actual = datetime.date.today().day

    #diferencia minima encontrada entre dos fechas
    mindiff = 366

    for clave, persona in miembros.items():
        #se evita count que es el primer elemento en el json
        if (clave!= "count" and persona["Server"] == server):
            
            #halla cuanto falta para el cumpleaños de persona en relacion a fecha actual
            dif = diferencia_de_fechas(mes_actual,dia_actual,int(persona["mes"]),int(persona["dia"]))
            
            if (dif < mindiff):
                mindiff = dif
                persona_mas_cercana = persona

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
    #print(os.getcwd())
    with open("src/data_file.json","r") as archivo:
        dato = json.load(archivo)
        return dato


#############################################
def actualizar_miembros(miembro):
    with open("src/data_file.json","w") as archivo:
        json.dump(miembro,archivo,indent="   ")