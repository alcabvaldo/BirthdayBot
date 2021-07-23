
import discord
import funciones
from discord.ext import commands    
from decouple import config         #es para ver las variables definidas en el  .env



import json

bot = commands.Bot(command_prefix='cumple')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(name='owo')
async def _owo(ctx):
    await ctx.send("owo")



# cargar un usuario nuevo ##########
@bot.command(name='cargar')
async def _setcumple(ctx,dia=None,mes=None):
    nombre = ctx.message.author.name
    server = ctx.message.guild.name
    
    resultado = funciones.add_cumple(nombre,server,mes,dia)
    
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
    server = ctx.message.guild.name
    resultado = funciones.str_proximo_cumple(server)
    await ctx.send(resultado)



#funciones.add_cumple("NombrePrueba","ServerPrueba","12","20")

#funciones.test_nearest_date()

bot.run(config('BOT_KEY'))
