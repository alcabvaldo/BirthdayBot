import json
import datetime
import os



######################################################
def add_cumple(nombre,server,mes,dia):
    print(mes,dia)

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


#encuentra la persona con el cumpleaños mas proximo en un server especifico####################
def find_next_birthday(server,miembros):

    #fecha actual en dias desde 1 de enero
    hoy = datetime.date.today().timetuple().tm_yday
    print("hoy hay en dias "+str(hoy))

    #diferencia minima encontrada entre dos fechas
    mindiff = 366

    for clave, persona in miembros.items():
        #se evita count que es el primer elemento en el json
        if (clave!= "count" and persona["Server"] == server):
            auxdias = dias_desde_1enero(persona["mes"],persona["dia"])
            if (auxdias>=hoy and auxdias-hoy<mindiff) : #si la fecha es despues en el año
                mindiff = auxdias-hoy
                persona_mas_cercana = persona
            elif (auxdias<hoy and auxdias+365-hoy<mindiff) : #si la fecha es antes en el año (pasado el año nuevo)
                mindiff = auxdias+365-hoy
                persona_mas_cercana = persona

    print("Faltan "+str(mindiff)+" dias para el cumple de "+persona_mas_cercana["Nombre"])
    return persona_mas_cercana    



# calcula la cantidad de dias pasados desde el 01/01 hasta esa fecha ####################
#source: https://stackoverflow.com/questions/620305/convert-year-month-day-to-day-of-year-in-python
def dias_desde_1enero(mes, dia):
    auxdate = datetime.date(datetime.MINYEAR,int(mes),int(dia))
    diasdesdeenero = auxdate.timetuple().tm_yday
    print("para el "+mes+"/"+dia+"los dias son: "+str(diasdesdeenero))
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
    print(os.getcwd())
    with open("src/data_file.json",) as archivo:
        dato = json.load(archivo)
        return dato


#############################################
def actualizar_miembros(miembro):
    with open("src/data_file.json","w") as archivo:
        json.dump(miembro,archivo,indent="   ")