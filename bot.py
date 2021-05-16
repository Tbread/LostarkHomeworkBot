import discord
from discord.ext.commands import Bot

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

from datetime import datetime
from datetime import timedelta

db = client.dcbot

intents = discord.Intents.default()
bot = Bot(command_prefix='^', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} 에 로그인하였습니다!')


@bot.command()
async def 가입(ctx):
    uid = db.dcbot.find_one({'uid': ctx.author.id})
    if uid is None:
        doc = {'uid': ctx.author.id, 'charEA': 0}
        db.dcbot.insert_one(doc)
        await ctx.send(f'가입 완료')
    else:
        await ctx.send(f'이미 가입된 계정입니다.')


@bot.command()
async def 캐릭추가(ctx, *, text=None):
    uid = db.dcbot.find_one({'uid': ctx.author.id})
    if uid is None:
        await ctx.send(f'회원가입을 먼저 진행해주세요.')
    if text is None:
        await ctx.send(f'캐릭터명을 입력해주세요.')
    else:
        today = datetime.today()
        hour = today.strftime('%H')
        ea = db.dcbot.find_one({'uid': ctx.author.id})['charEA']
        if int(hour) < 6:
            today = today - timedelta(1)
        db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {text: 'char' + str(ea),
                                                            'char' + str(ea)+'charname': text, 'char' + str(ea)+'gd': today,
                                                                               'char' + str(ea)+'efona': today,
                                                                               'char' + str(ea)+'chaos': today, 'char' + str(ea)+'oreha': 0, 'char' + str(ea)+'dojeon': 0,
                                                                               'char' + str(ea)+'efonarest': 0, 'char' + str(ea)+'gdrest': 0,
                                                                               'char' + str(ea)+'chaosrest': 0,'char' + str(ea)+'abyssupdate': today,
                                                                               'char' + str(ea)+'djupdate': today}})
        db.dcbot.update_one({'uid': ctx.author.id}, {'$inc': {'charEA': 1}})
        await ctx.send(f'추가완료')


@bot.command()
async def 숙제목록(ctx, *, text=None):
    uid = db.dcbot.find_one({'uid': ctx.author.id})
    ea = db.dcbot.find_one({'uid': ctx.author.id})['charEA']
    if uid is None:
        await ctx.send(f'회원가입을 먼저 진행해주세요.')
    if text is None:
        for i in range(0, ea):
            charnm = db.dcbot.find_one({'uid': ctx.author.id})['char' + str(i)+'charname']
            chaos = db.dcbot.find_one({'uid': ctx.author.id})['char' + str(i)+'chaosrest']
            gd = db.dcbot.find_one({'uid': ctx.author.id})['char' + str(i)+'gdrest']
            efona = db.dcbot.find_one({'uid': ctx.author.id})['char' + str(i)+'efonarest']
            oreha = db.dcbot.find_one({'uid': ctx.author.id})['char' + str(i)+'oreha']
            if oreha == 0:
                weekabyss = '이번주는 돌지않았습니다.'
            else:
                weekabyss = '이번주는 돌았습니다.'
            dojeon = db.dcbot.find_one({'uid': ctx.author.id})['char' + str(i)+'dojeon']
            if dojeon == 0:
                weekdojeon = '이번주는 돌지않았습니다.'
            else:
                weekdojeon = '이번주는 돌았습니다.'
            chaosupdate = db.dcbot.find_one({'uid': ctx.author.id})['char' + str(i) + 'chaos']
            gdupdate = db.dcbot.find_one({'uid': ctx.author.id})['char' + str(i) + 'gd']
            efonaupdate = db.dcbot.find_one({'uid': ctx.author.id})['char' + str(i) + 'efona']
            djupdate = db.dcbot.find_one({'uid': ctx.author.id})['char' + str(i)+'djupdate']
            abyssupdate = db.dcbot.find_one({'uid': ctx.author.id})['char' + str(i) + 'abyssupdate']
            embed = discord.Embed(title="캐릭터명", description=charnm, color=0xAAFFFF)
            embed.add_field(name="카오스던전", value='휴식게이지: ' + str(chaos)+'\n업데이트일: '+chaosupdate.strftime('%Y-%m-%d'))
            embed.add_field(name="가디언토벌", value='휴식게이지: ' + str(gd)+'\n업데이트일: '+gdupdate.strftime('%Y-%m-%d'))
            embed.add_field(name="에포나", value='휴식게이지: ' + str(efona)+'\n업데이트일: '+efonaupdate.strftime('%Y-%m-%d'))
            embed.add_field(name="도전가디언토벌", value=weekdojeon+'\n업데이트일: '+djupdate.strftime('%Y-%m-%d'))
            embed.add_field(name="오레하의 우물", value=weekabyss+'\n업데이트일: '+abyssupdate.strftime('%Y-%m-%d'))
            embed.set_footer(text='06시 이전에 업데이트시엔 작일로 기록됩니다.\n휴식게이지가 -30~-10의 범위로 나오는것은 정상입니다.')
            await ctx.send(embed=embed)
    else:
        charnm = text
        whichchar = db.dcbot.find_one({'uid': ctx.author.id})[text]
        chaos = db.dcbot.find_one({'uid': ctx.author.id})[whichchar+'chaosrest']
        gd = db.dcbot.find_one({'uid': ctx.author.id})[whichchar+'gdrest']
        efona = db.dcbot.find_one({'uid': ctx.author.id})[whichchar+'efonarest']
        oreha = db.dcbot.find_one({'uid': ctx.author.id})[whichchar+'oreha']
        if oreha == 0:
            weekabyss = '이번주는 돌지않았습니다.'
        else:
            weekabyss = '이번주는 돌았습니다.'
        dojeon = db.dcbot.find_one({'uid': ctx.author.id})[whichchar+'dojeon']
        if dojeon == 0:
            weekdojeon = '이번주는 돌지않았습니다.'
        else:
            weekdojeon = '이번주는 돌았습니다.'
        chaosupdate = db.dcbot.find_one({'uid': ctx.author.id})[whichchar+ 'chaos']
        gdupdate = db.dcbot.find_one({'uid': ctx.author.id})[whichchar+ 'gd']
        efonaupdate = db.dcbot.find_one({'uid': ctx.author.id})[whichchar+ 'efona']
        abyssupdate = db.dcbot.find_one({'uid': ctx.author.id})[whichchar+'abyssupdate']
        djupdate = db.dcbot.find_one({'uid': ctx.author.id})[whichchar+'djupdate']
        embed = discord.Embed(title="캐릭터명", description=charnm, color=0xAAFFFF)
        embed.add_field(name="카오스던전", value='휴식게이지: ' + str(chaos) + '\n업데이트일: ' + chaosupdate.strftime('%Y-%m-%d'))
        embed.add_field(name="가디언토벌", value='휴식게이지: ' + str(gd) + '\n업데이트일: ' + gdupdate.strftime('%Y-%m-%d'))
        embed.add_field(name="에포나", value='휴식게이지: ' + str(efona) + '\n업데이트일: ' + efonaupdate.strftime('%Y-%m-%d'))
        embed.add_field(name="도전가디언토벌", value=weekdojeon + '\n업데이트일: ' + djupdate.strftime('%Y-%m-%d'))
        embed.add_field(name="오레하의 우물", value=weekabyss + '\n업데이트일: '+abyssupdate.strftime('%Y-%m-%d'))
        embed.set_footer(text='06시 이전에 업데이트시엔 작일로 기록됩니다.\n휴식게이지가 -30~-10의 범위로 나오는것은 정상입니다.')
        await ctx.send(embed=embed)

@bot.command()
async def 업데이트(ctx):
    uid = db.dcbot.find_one({'uid': ctx.author.id})
    ea = db.dcbot.find_one({'uid': ctx.author.id})['charEA']
    if uid is None:
        await ctx.send(f'회원가입을 먼저 진행해주세요.')
    if ea == 0:
        await ctx.send(f'등록된 캐릭터가 없습니다.')
    else:
        today = datetime.today()
        hour = today.strftime('%H')
        if int(hour) < 6:
            today = today - timedelta(1)
        for i in range(0, ea):
            updatechk = db.dcbot.find_one({'uid': ctx.author.id})['char'+str(i)+'chaos']
            datechk = (today.day - updatechk.day) * 20
            rest = db.dcbot.find_one({'uid': ctx.author.id})['char'+str(i)+'chaosrest']
            rest = rest + datechk
            if rest > 100:
                realrest = 100
            else:
                realrest = rest
            db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {'char'+str(i)+'chaosrest':realrest}})
            db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {'char' + str(i) + 'chaos': today}})
            #카오스
            updatechk = db.dcbot.find_one({'uid': ctx.author.id})['char' + str(i) + 'efona']
            datechk = (today.day - updatechk.day) * 30
            rest = db.dcbot.find_one({'uid': ctx.author.id})['char' + str(i) + 'efonarest']
            rest = rest + datechk
            if rest > 100:
                realrest = 100
            else:
                realrest = rest
            db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {'char' + str(i) + 'efonarest': realrest}})
            db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {'char' + str(i) + 'efona': today}})
            #에포나
            updatechk = db.dcbot.find_one({'uid': ctx.author.id})['char' + str(i) + 'gd']
            datechk = (today.day - updatechk.day) * 20
            rest = db.dcbot.find_one({'uid': ctx.author.id})['char' + str(i) + 'gdrest']
            rest = rest + datechk
            if rest > 100:
                realrest = 100
            else:
                realrest = rest
            db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {'char' + str(i) + 'gdrest': realrest}})
            db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {'char' + str(i) + 'gd': today}})
            #가디언토벌
            updatechk = db.dcbot.find_one({'uid': ctx.author.id})['char' + str(i) + 'djupdate']
            chkweek = (today.day - updatechk.day)
            if chkweek > 6:
                db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {'char' + str(i) + 'dojeon': 0}})
            elif today.weekday() == 2:
                if chkweek > 0:
                    db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {'char' + str(i) + 'dojeon': 0}})
            db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {'char' + str(i) + 'djupdate': today}})
            #도전가디언토벌
            updatechk = db.dcbot.find_one({'uid': ctx.author.id})['char' + str(i) + 'abyssupdate']
            chkweek = (today.day - updatechk.day)
            if chkweek > 6:
                db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {'char' + str(i) + 'oreha': 0}})
            elif today.weekday() == 2:
                if chkweek > 0:
                    db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {'char' + str(i) + 'oreha': 0}})
            db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {'char' + str(i) + 'abyssupdate': today}})
            #어비스
        await ctx.send(f'업데이트가 완료되었습니다.')

@bot.command()
async def 숙제끝(ctx,text=None,texts=None):
    uid = db.dcbot.find_one({'uid': ctx.author.id})
    ea = db.dcbot.find_one({'uid': ctx.author.id})['charEA']
    whichchar = db.dcbot.find_one({'uid': ctx.author.id})[texts]
    today = datetime.today()
    hour = today.strftime('%H')
    if int(hour) < 6:
        today = today - timedelta(1)
    if uid is None:
        await ctx.send(f'회원가입을 먼저 진행해주세요.')
    if ea == 0:
        await ctx.send(f'등록된 캐릭터가 없습니다.')
    if text is None:
        await ctx.send(f'명령어가 제대로 입력되지않았습니다.\n`^숙제끝 카던 캐릭터명`\n`^숙제끝 가디언 캐릭터명`\n`^숙제끝 에포나 캐릭터명`\n`^숙제끝 도전 캐릭터명`\n`^숙제끝 오레하 캐릭터명`')
    if texts is None:
        await ctx.send(f'명령어가 제대로 입력되지않았습니다.\n`^숙제끝 카던 캐릭터명`\n`^숙제끝 가디언 캐릭터명`\n`^숙제끝 에포나 캐릭터명`\n`^숙제끝 도전 캐릭터명`\n`^숙제끝 오레하 캐릭터명`')
    if text == '카던':
        rest = db.dcbot.find_one({'uid': ctx.author.id})[whichchar+'chaosrest']
        rest = rest - 60
        if rest == -80:
            realrest = -20
        if rest == -70:
            realrest = -10
        if rest == -60:
            realrest = -20
        if rest == -50:
            realrest = -10
        if rest == -40:
            realrest = -20
        if rest == -30:
            realrest = -10
        db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {whichchar+ 'chaosrest': realrest}})
        db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {whichchar+ 'chaos': today}})
    if text == '가디언':
        rest = db.dcbot.find_one({'uid': ctx.author.id})[whichchar+'gdrest']
        rest = rest - 60
        if rest == -80:
            realrest = -20
        if rest == -70:
            realrest = -10
        if rest == -60:
            realrest = -20
        if rest == -50:
            realrest = -10
        if rest == -40:
            realrest = -20
        if rest == -30:
            realrest = -10
        db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {whichchar+ 'gdrest': realrest}})
        db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {whichchar+ 'gd': today}})
    if text == '에포나':
        rest = db.dcbot.find_one({'uid': ctx.author.id})[whichchar+'efonarest']
        rest = rest - 90
        if rest == -40:
            realrest = -20
        if rest == -50:
            realrest = -30
        if rest == -60:
            realrest = --20
        if rest == -70:
            realrest = -30
        if rest == -80:
            realrest = -20
        if rest == -90:
            realrest = -30
        db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {whichchar+ 'efonarest': realrest}})
        db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {whichchar+ 'efona': today}})
    if text == '도전':
        db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {whichchar + 'djupdate': today}})
        db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {whichchar + 'dojeon': 1}})
    if text == '오레하':
        db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {whichchar + 'abyssupdate': today}})
        db.dcbot.update_one({'uid': ctx.author.id}, {'$set': {whichchar + 'abyss': 1}})
    await ctx.send(f'업데이트가 완료되었습니다.')

@bot.command()
async def 도움말(ctx):
    embed = discord.Embed(title="명령어목록", color=0xAAFFFF)
    embed.add_field(name="^가입", value="명령어사용을위해 유저를 추가합니다", inline=False)
    embed.add_field(name="^캐릭추가", value="^캐릭추가 캐릭터명 으로 캐릭터를 추가합니다.",inline=False)
    embed.add_field(name="^업데이트", value="숙제정보를 업데이트합니다.",inline=False)
    embed.add_field(name="^숙제끝", value="^숙제끝 숙제종류 캐릭터명 으로 해당숙제를 완료합니다.\n숙제종류: 카던,가디언,에포나,도전,오레하",inline=False)
    embed.add_field(name="^숙제목록", value="숙제목록을 확인합니다.\n^숙제목록 캐릭터명 으로 단일캐릭의 숙제목록을 확인할수있습니다.\n캐릭터명을 적지않을시 모든캐릭터를 확인합니다.",inline=False)
    embed.set_footer(text='문의:itaebread@gmail.com')
    await ctx.send(embed=embed)


bot.run('NjI5MDAxOTU1NDM5ODA0NDU2.XZTZuA.Iu0zlUlcmTiPEmn35E0lqphSwqY')
