#monitoriabot.py
import os

import discord
from datetime import datetime, time
from pytz import timezone

TOKEN = "#"
GUILD = "MONITORIA PD"

client = discord.Client()

horarios = {
    'Nicolas': {
        0: [(time(8,20), time(9,10)), (time(13,00), time(13,50)), (time(18,15), time(19,00))], 
        1: [(time(8,20), time(9,10)), (time(13,00), time(13,50)), (time(17,25), time(18,15))],
        2: [(time(13,00), time(13,50))],        
        3: [(time(8,20), time(9,10)), (time(13,00), time(13,50))],
        4: [(time(8,20), time(9,10)), (time(13,00), time(13,50))],
        5: [(time(10,00), time(12,15))]
    },
    'Nouani': {
        0: [(time(7,30), time(9,10)), (time(13,00), time(13,50)), (time(18,15), time(19,00))], 
        1: [(time(13,00), time(13,50)), (time(18,15), time(19,00))],
        2: [(time(13,00), time(13,50))],
        3: [(time(7,30), time(9,10)), (time(13,00), time(13,50)), (time(18,15), time(19,00))],
        4: [(time(7,30), time(8,20)), (time(13,00), time(13,50)), (time(18,15), time(19,00))]
    },
    'Gabriel': {
        0: [(time(7,30), time(9,10)), (time(13,00), time(13,50)), (time(18,15), time(19,00))],        
        1: [(time(7,30), time(9,10)), (time(13,00), time(13,50)), (time(17,25), time(18,15)), (time(19,00), time(19,40))],
        2: [(time(13,00), time(13,50)), (time(18,15), time(19,00)), (time(21,10), time(21,50))],
        3: [(time(7,30), time(8,20))],
        4: [(time(7,30), time(8,20)), (time(13,00), time(13,50))]
    },
    'Rafael': {
        0: [(time(7,30), time(9,10)), (time(13,00), time(13,50)), (time(18,15), time(19,00))],
        1: [(time(13,00), time(13,50)), (time(18,15), time(19,00)), (time(21,10), time(22,30))],
        2: [(time(13,00), time(13,50)), (time(21,10), time(22,30))],
        3: [(time(13,00), time(13,50)), (time(18,15), time(19,00))],
        4: [(time(7,30), time(9,10)), (time(13,00), time(13,25))]
    },
    'Ricardo': {
        0: [(time(18,15), time(19,00))],
        1: [(time(18,15), time(19,00))],
        2: [(time(18,15), time(19,00)), (time(21,10), time(22,30))],
        3: [(time(17,25), time(19,00))],
        4: [(time(16,35), time(18,15)), (time(20,20), time(21,00))],
        5: [(time(7,30), time(11,30))]
    }
}


def moni_agora(hoje, dia_da_semana):
    tz = timezone('America/Sao_Paulo')
    utc_time = datetime.utcnow()
    horario = tz.fromutc(utc_time).time()
    #horario = hoje.time()
    disponiveis = []
    for nome, disponibilidade in horarios.items(): # para cada monitor
        if dia_da_semana in disponibilidade: # se atende no dia   
            for inicio, fim in disponibilidade[dia_da_semana]:
                if inicio <= horario < fim:
                    disponiveis.append(nome)
                    break
    if disponiveis:
        resposta = f'Monitores disponíveis no momento: {", ".join(disponiveis)}'
    else:
        resposta = "Não há nenhum monitor disponível no momento :("        
    return resposta

def moni_hoje(dia_da_semana):
    monitorias_hoje = []
    for nome, disponibilidade in horarios.items():
        if dia_da_semana in disponibilidade:
            str_moni = nome + ": \n"
            for inicio, fim in disponibilidade[dia_da_semana]:
                str_moni += f"        das {inicio:%H:%M} até às {fim:%H:%M}\n"
            monitorias_hoje.append(str_moni)
    if monitorias_hoje:
        resposta = f'```diff\n+ Monitorias hoje: \n\n {" ".join(monitorias_hoje)} ```'
    else:
        resposta = "Não há monitorias no dia de hoje :"
    return resposta


#----------------------------------------------------------------------------------

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return

    hoje = datetime.now()        
    dia_da_semana = hoje.weekday()
        
    if message.content == '!moni':        
        resposta = moni_agora(hoje, dia_da_semana)
    elif message.content == '!hoje':
        resposta = moni_hoje(dia_da_semana)
    await message.channel.send(resposta)
    
@client.event
async def on_error(event, *args, **kwargs):
    if event == 'on_message':
        print(f'Unhandled message: {args[0]}\n')
    else:
        raise


client.run(TOKEN)
