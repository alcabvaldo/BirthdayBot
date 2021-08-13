
from os import truncate
import discord
import funciones
from discord.ext import tasks,commands    
from decouple import config         #es para ver las variables definidas en el  .env
import json
from discord import Color #https://stackoverflow.com/questions/63768372/color-codes-for-discord-py
import datetime

intent = discord.Intents.default() # para tener permiso de cambiar los nombres
intent.members = True

    
## Cambia la Actividad del bot para que diga "listening to cumplehelp" ###############################
#source: https://stackoverflow.com/questions/59126137/how-to-change-discord-py-bot-activity
activity = discord.Activity(type=discord.ActivityType.listening, name="/cumpleayuda")


# Inicia el Bot
bot = commands.Bot(command_prefix='/cumple',activity=activity, intents=intent)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(name='uwu')
async def _uwu(ctx):
    await ctx.send("owo")

@bot.command(name='owo')
async def _uwu(ctx):
    await ctx.send("uwu")

## para HELP #########################################################
#inspiracion: https://www.youtube.com/watch?v=ivXw9VO89jw

bot.remove_command("help")
rosadito = Color.from_rgb(255,192,203)

@bot.group(invoke_without_command=True)
async def ayuda(ctx):
	embed = discord.Embed(title = "Hola!!",color=rosadito,description = "Usa /cumpleayuda <comando> para una descripcion más específica de cada comando")
	embed.set_thumbnail(url="https://raw.githubusercontent.com/alcabvaldo/BirthdayBot/main/logo_no_bg.png")

	embed.add_field(inline=False,name="cargar",value="carga un cumple nuevo, o actualiza uno que ya esté guardado")
	embed.add_field(inline=False,name="proximo",value="te cuenta cuál será el próximo cumpleaños")
	embed.add_field(inline=False,name="ver",value="Muestra los cumpleaños que están guardados en el server")

	await ctx.send(embed = embed)

@ayuda.command()
async def cargar(ctx):
	embed = discord.Embed(title = "cargar",color=rosadito,description = "Carga un cumple nuevo")
	embed.add_field(name="syntax",value="/cumplecargar <dia> <mes> <inicial>")
	await ctx.send(embed = embed)

@ayuda.command()
async def proximo(ctx):
	embed = discord.Embed(title = "proximo",color=rosadito,description = "Dice quien sera la proxima persona en cumplir años")
	embed.add_field(name="syntax",value="escribí nomas y ya te va salir")
	await ctx.send(embed = embed)

@ayuda.command()
async def ver(ctx):
	embed = discord.Embed(title = "ver",color=rosadito,description = "Muestra los cumpleaños que están guardados en el server")
	embed.add_field(name="syntax",value="al escribir el comando ya te sale")
	await ctx.send(embed = embed)

#### Para el LOOP ###################################################

## este post me sirvio para pillar el problema de missing permissions:
# https://stackoverflow.com/questions/56117594/discord-js-bot-dosnt-have-permission-to-manage-nicknames?newreg=04518609044a4bb895f1cb6f8d0b4c7d
# el problema era que no se puede cambiar el nick al owner ni a los que tienen rol superior 


#inspiracion: https://stackoverflow.com/questions/65808190/get-all-members-discord-py
@tasks.loop(hours=24.0) #para que haga cada tanto
async def change_member_names():
    """
        Cambia las iniciales de todos los miembros en todos los servers en los
        que se encuentra el bot por la inicial del cumpleañero mas cercano
        respectivo en cada server
    """

    miembros = funciones.get_miembros()

    for guild in bot.guilds:

        cumpleañero = funciones.find_next_birthday(guild.id,miembros)
        
        mes_actual = datetime.date.today().month
        dia_actual = datetime.date.today().day
        dif = funciones.diferencia_de_fechas(mes_actual,dia_actual,int(cumpleañero["mes"]),int(cumpleañero["dia"]))

        if (cumpleañero and dif<=15): # por si no haya nadie, o falte mas de 15 dias para el cumpleaños

            inicial = cumpleañero["Inicial"]

            for member in guild.members:

                print("ahora intentare cambiar "+str(member))
                oldname = member.nick
                #cambia la primera letra
                try:
                    newname = inicial + oldname[1:len(oldname)] #desde la segunda letra hasta el final del nombre
                    await member.edit(nick=newname)
                    
                #no cambia los nombres de los miembros con roles superiores
                except Exception as e :
                    print(e)


@change_member_names.before_loop
async def waiter():
    print("Waiting for login")
    await bot.wait_until_ready()

change_member_names.start()
#######################################################################

@bot.command(name='actualizarnombres') #fuerza la llamada a changemembernames
async def _actualizarnombres(ctx):
    await change_member_names()




# cargar un usuario nuevo ##########
@bot.command(name='cargar')
async def _setcumple(ctx,dia=None,mes=None,inicial=None):
    nombre = ctx.message.author.name
    Id     = ctx.message.author.id
    server = ctx.message.guild.id
    server_name = ctx.message.guild.name

    #creo el objeto new_miembro
    nuevo_miembro = {
        "Nombre": nombre,
        "Id": Id,
        "Inicial": inicial,
        "Server": server,
        "Server_name": server_name,
        "dia": dia,
        "mes": mes
    }
    
    resultado = funciones.add_cumple(nuevo_miembro)
    # imprime un mensaje diciendo si se pudo agregar o no
    await ctx.send(resultado)


# ver los datos guardados ###########
@bot.command(name='ver')
async def _getcumple(ctx):
	miembros = funciones.get_miembros()

	mensaje = f"Estos son los cumpleaños de {ctx.message.guild.name}: \n"



	for clave, persona in miembros.items():
		#se evita count que es el primer elemento en el json
		if (clave!= "count" and persona["Server"] == ctx.message.guild.id):
			nueva_linea = ("\n**"+persona["Nombre"]+":** ("+persona["dia"]+"/"+persona["mes"]+")")
			mensaje = mensaje + nueva_linea

	embed = discord.Embed(title = "Cumpleaños!!",color=rosadito,description = mensaje)			
	await ctx.send(embed = embed)




# prueba de cambio de nick ##########
@bot.command(name='nickprueba')
async def _nickprueba(ctx,new_nick=None):
    if (new_nick):
        await ctx.author.edit(nick=new_nick)

# devulve cuanto falta para el cumple mas cercano ##########
@bot.command(name='proximo')
async def _proximo(ctx):
    server = ctx.message.guild.id
    resultado = funciones.str_proximo_cumple(server)
    await ctx.send(resultado)










# Iniciar el BOT #########
bot.run(config('BOT_KEY'))
