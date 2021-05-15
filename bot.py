import discord
from discord.ext.commands import Bot

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

from datetime import datetime
from datetime import timedelta

db = client.dcbot

intents = discord.Intents.default()
bot = Bot(command_prefix='^', intents=intents)


async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'틀린 명령어 사용법입니다.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'명령어를 사용할 권한이 없습니다.')
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send(f'봇이 명령어를 사용할 권한이 없습니다.')


@bot.event
async def on_ready():
    print(f'{bot.user} 에 로그인하였습니다!')


@bot.command()
async def 가입(ctx):
    uid = db.dcbot.find_one({'uid': bot.user.id})
    if uid is None:
        doc = {'uid': bot.user.id, 'charEA': 0}
        db.dcbot.insert_one(doc)
        await ctx.send(f'가입 완료')
    else:
        await ctx.send(f'이미 가입된 계정입니다.')


@bot.command()
async def 캐릭추가(ctx, *, text=None):
    uid = db.dcbot.find_one({'uid': bot.user.id})
    if uid is None:
        await ctx.send(f'회원가입을 먼저 진행해주세요.')
    if text is None:
        await ctx.send(f'캐릭터명을 입력해주세요.')
    else:
        today = datetime.today()
        hour = today.strftime('%H')
        ea = db.dcbot.find_one({'uid': bot.user.id})['charEA']
        if int(hour) < 6:
            today = today - timedelta(1)
        db.dcbot.update_one({'uid': bot.user.id}, {'$set': {text: 'char' + str(ea),
                                                            'char' + str(ea): {'charname': text, 'gd': today,
                                                                               'efona': today,
                                                                               'chaos': today, 'oreha': 0, 'dojeon': 0,
                                                                               'efonarest': 0, 'gdrest': 0,
                                                                               'chaosrest': 0,
                                                                               'update': today}}})
        db.dcbot.update_one({'uid': bot.user.id}, {'$inc': {'charEA': 1}})
        await ctx.send(f'추가완료')


@bot.command()
async def 숙제목록(ctx, *, text=None):
    uid = db.dcbot.find_one({'uid': bot.user.id})
    ea = db.dcbot.find_one({'uid': bot.user.id})['charEA']
    if uid is None:
        await ctx.send(f'회원가입을 먼저 진행해주세요.')
    if text is None:
        for i in range(0, ea):
            charnm = db.dcbot.find_one({'uid': bot.user.id})['char' + str(i)]['charname']
            chaos = db.dcbot.find_one({'uid': bot.user.id})['char' + str(i)]['chaosrest']
            gd = db.dcbot.find_one({'uid': bot.user.id})['char' + str(i)]['gdrest']
            efona = db.dcbot.find_one({'uid': bot.user.id})['char' + str(i)]['efonarest']
            oreha = db.dcbot.find_one({'uid': bot.user.id})['char' + str(i)]['oreha']
            if oreha == 0:
                weekabyss = '이번주는 돌지않았습니다.'
            if oreha == 1:
                weekabyss = '이번주는 돌았습니다.'
            dojeon = db.dcbot.find_one({'uid': bot.user.id})['char' + str(i)]['dojeon']
            if dojeon == 0:
                weekdojeon = '이번주는 돌지않았습니다.'
            if dojeon == 1:
                weekdojeon = '이번주는 돌았습니다.'
            update = db.dcbot.find_one({'uid': bot.user.id})['char' + str(i)]['update']
            embed = discord.Embed(title="캐릭터명", description=charnm, color=0xAAFFFF)
            embed.add_field(name="카오스던전", value='휴식게이지: ' + str(chaos))
            embed.add_field(name="가디언토벌", value='휴식게이지: ' + str(gd))
            embed.add_field(name="에포나", value='휴식게이지: ' + str(efona))
            embed.add_field(name="도전가디언토벌", value=weekdojeon)
            embed.add_field(name="오레하의 우물", value=weekabyss)
            embed.set_footer(text='마지막 업데이트일은 ' + update.strftime('%Y-%m-%d') + ' 입니다.\n06시 이전에 업데이트시엔 작일로 기록됩니다.')
            await ctx.send(embed=embed)
    else:
        charnm = text
        whichchar = db.dcbot.find_one({'uid': bot.user.id})[text]
        chaos = db.dcbot.find_one({'uid': bot.user.id})[whichchar]['chaosrest']
        gd = db.dcbot.find_one({'uid': bot.user.id})[whichchar]['gdrest']
        efona = db.dcbot.find_one({'uid': bot.user.id})[whichchar]['efonarest']
        oreha = db.dcbot.find_one({'uid': bot.user.id})[whichchar]['oreha']
        if oreha == 0:
            weekabyss = '이번주는 돌지않았습니다.'
        if oreha == 1:
            weekabyss = '이번주는 돌았습니다.'
        dojeon = db.dcbot.find_one({'uid': bot.user.id})[whichchar]['dojeon']
        if dojeon == 0:
            weekdojeon = '이번주는 돌지않았습니다.'
        if dojeon == 1:
            weekdojeon = '이번주는 돌았습니다.'
        update = db.dcbot.find_one({'uid': bot.user.id})[whichchar]['update']
        embed = discord.Embed(title="캐릭터명", description=charnm, color=0xAAFFFF)
        embed.add_field(name="카오스던전", value='휴식게이지: ' + str(chaos))
        embed.add_field(name="가디언토벌", value='휴식게이지: ' + str(gd))
        embed.add_field(name="에포나", value='휴식게이지: ' + str(efona))
        embed.add_field(name="도전가디언토벌", value=weekdojeon)
        embed.add_field(name="오레하의 우물", value=weekabyss)
        embed.set_footer(text='마지막 업데이트일은 ' + update.strftime('%Y-%m-%d') + ' 입니다.\n06시 이전에 업데이트시엔 작일로 기록됩니다.')
        await ctx.send(embed=embed)

bot.run('여기에 토큰입력')
