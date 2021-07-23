import json
import datetime
import os           #para el get current directory (gcd)



######################################################
def add_cumple(nombre,server,mes,dia):
    #print(mes,dia)

    #creo el objeto new_miembro
    new_miembro = {
        "Nombre": nombre,
        "Server": server,
        "dia": dia,
        "mes": mes
    }

    #traigo la lista de cumpleaños guardados del json
    miembros = get_miembros()

    # new_miembro sera el k-ésimo miembro
    k = miembros["count"] + 1
    
    if (not_already_there(new_miembro,miembros)):
        miembros[k] = new_miembro
        miembros["count"] = miembros["count"] + 1
        actualizar_miembros(miembros)
        
        return "añadido!"
    else :
        return "ya tenes ya guardado un cumpleaños"

    #print(json.dumps(miembros,indent="   "))


def test_nearest_date():
    miembros = get_miembros()
    auxpersona = find_next_birthday("Noice",miembros)
    print(auxpersona)
def str_proximo_cumple(server):
    mes_actual = datetime.date.today().month
    dia_actual = datetime.date.today().day
    miembros = get_miembros()
    proxima_persona = find_next_birthday(server,miembros)
    dias_que_faltan = diferencia_de_fechas(mes_actual,dia_actual,int(proxima_persona["mes"]),int(proxima_persona["dia"]))
    return ("El proximo cumple es el de "+proxima_persona["Nombre"]+" ("+proxima_persona["dia"]+"/"+proxima_persona["mes"]+"), Faltan "+str(dias_que_faltan)+" dias!!!!")


#encuentra la persona con el cumpleaños mas proximo en un server especifico####################
def find_next_birthday(server,miembros):

    #fecha actual en dias desde 1 de enero
    mes_actual = datetime.date.today().month
    dia_actual = datetime.date.today().day
    #print("hoy hay en dias "+str(hoy))

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

    print("Faltan "+str(mindiff)+" dias para el cumple de "+persona_mas_cercana["Nombre"])
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



#busca si una persona no se encuentra ya en la lista###############
def not_already_there(new_miembro,miembros):
    for clave, persona in miembros.items():
        #verifica que no sea count para que funcione, esto es por como hice el json
        if (clave != "count") and ((persona["Nombre"])==new_miembro["Nombre"]) and ((persona["Server"])==new_miembro["Server"]) :
            return False
    return True


#############################################
def get_miembros():
    #print(os.getcwd())
    with open("src/data_file.json",) as archivo:
        dato = json.load(archivo)
        return dato


#############################################
def actualizar_miembros(miembro):
    with open("src/data_file.json","w") as archivo:
        json.dump(miembro,archivo,indent="   ")