
from os import truncate
import discord
import funciones
from discord.ext import tasks,commands    
from decouple import config         #es para ver las variables definidas en el  .env
import json
from discord import Color

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

@bot.command(name='owo')
async def _owo(ctx):
    await ctx.send("owo")

## para HELP #########################################################

bot.remove_command("help")

@bot.group(invoke_without_command=True)
async def ayuda(ctx):
	embed = discord.Embed(title = "Hola",color=Color.from_rgb(255,192,203),description = "Usa /cumpleayuda <comando> para una descripcion más específica de cada comando (mentira eso no esta todavia)")
	embed.set_thumbnail(url="https://raw.githubusercontent.com/alcabvaldo/BirthdayBot/main/logo.png")

	embed.add_field(name="cumplecargar",value="carga un cumple nuevo, o actualiza uno que ya esté guardado")
	embed.add_field(name="cumpleproximo",value="te cuenta cuál será el próximo cumpleaños")
	embed.add_field(name="nose",value="nose")

	await ctx.send(embed = embed)

@ayuda.command()
async def cumplecargar(ctx):
	embed = discord.Embed(title = "cumplecargar",description = "Usa /cumpleayuda <comando> para una descripcion más específica de cada comando (mentira eso no esta todavia)")
	embed.add_field(name="cumplecargar",value="carga un cumple nuevo, o actualiza uno que ya esté guardado")
	




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

        if (cumpleañero): # por si no haya nadie

            inicial = cumpleañero["Inicial"]

            for member in guild.members:

                print("ahora intentare cambiar "+str(member))
                oldname = member.name
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
    await ctx.send(json.dumps(funciones.get_miembros(),indent=3))


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
