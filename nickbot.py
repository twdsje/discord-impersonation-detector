import discord
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from confusables import normalize
import logging
import os
import yaml

def main():
    apitoken = os.getenv('API_TOKEN')
    
    with open("config.yaml", "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader) 

    names = data['names']
    logguildid = data['logguild']
    logchannelid = data['logchannel']

    intents = discord.Intents.all()
    client = discord.Client(command_prefix='!', intents=intents)
    
    log = logging.getLogger('discord')
    logchannel = None
    handler = logging.FileHandler(filename='nickbot.log', encoding='utf-8', mode='w')

    @client.event
    async def on_ready():
        log.info('We have logged in as {0.user}'.format(client))
        nonlocal logchannel
        logchannel = client.get_guild(logguildid).get_channel(logchannelid)

    @client.event
    async def on_member_join(member):
        log.info(f"User join: {member.name}")
        await test (f"{member.name}", names, member, logchannel)

    @client.event
    async def on_member_update(before, after):
        if before.name != after.name:
            log.info(f"Member update name: {before.name} -> {after.name}")
            await test(f"{after.name}", names, after, logchannel)
        if before.nick != after.nick:
            log.info(f"Member update nick: {before.nick} -> {after.nick}")
            await test(f"{after.name}", names, after, logchannel)

    @client.event
    async def on_user_update(before, after):
        if before.name != after.name:
            log.info(f"User udpate name: {before.name} -> {after.name}")
            member = client.get_guild(270580115765854209).get_member(after.id)
            await test(f"{after.name}", names, member, logchannel)


    client.run(apitoken, log_handler=handler)

async def test(name, names, member, logchannel):
    for n in names:
        await testname(name, n, member, logchannel)

async def testname(name, me, member, logchannel):
    log = logging.getLogger('discord')

    normal = normalize(name, prioritize_alpha=True)
    results = []
    for s in normal:
        results.append(fuzz.ratio(me, s))
    score = max(results)
    #Worst acceptable: @Splattered 58
    if score > 80:
        try:
            msg = f"Impersonator of {me} detected {name}: <@{member.id}> " + str(score)
            await logchannel.send(msg)
            log.info(msg)
            await member.ban(reason="Impersonating server admins.")
        except Exception as Argument:
            log.exception("Error occured while trying to ban member.")
    elif score > 50:
        msg = f"Possible {me} impersonator detected {name}: <@{member.id}> " + str(score)
        await logchannel.send(msg)
        log.info(msg)
    else:
        log.info(f"Username accepted {name} testing against {me} " + str(score))
if __name__ == "__main__":
    main()
