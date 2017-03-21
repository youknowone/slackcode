import traceback
import discord
import engine
import asyncio

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if not message.content.startswith('!'):
        return
    try:
        team = 'ycc'
        text = message.content
        if text:
            name, out, err = engine.dispatch(text, team=team)
            outtext = ''
            if out.strip():
                outtext += '```' + out + '```'
            print(out)
            print(err)
            if err.strip():
                outtext += '\nerror:\n```' + err + '```'
            if outtext:
                await client.send_message(message.channel, outtext)
    except Exception as e:
        traceback.print_exc()
        await client.send_message(message.channel, traceback.format_exc())
    return ''

key = ''
while True:
    try:
        client.run(key)
    except KeyboardInterrupt:
        break
    else:
        continue
