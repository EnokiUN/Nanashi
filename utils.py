import sqlite3
import datetime
import math
import discord
from vars import *

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE)
        self.c = self.conn.cursor()

    def execute(self, query: str, vals: tuple):
        self.c.execute(query, vals)
        return self.c.fetchall()
    
    def exists(self, query: str, vals: tuple):
        result = self.execute(query, vals)[0]
        if result is None:
            return False, None
        else:
            return True, result
    
    def rconn(self):
        return self.conn

    def rc(self):
        return self.c

    def commit(self):
        self.conn.commit()

    def close(self):
        self.c.close()
        self.conn.close()
        self = None
        
async def DiscordLog(client, channelId: int, content: str) -> None:
    channel = await client.fetch_channel(channelId)
    await channel.send(content)
    
def NumAddComma(num: int) -> str:
    nums = str(num)
    numsn = str() 
    for i in range(len(nums)):
        if len(nums[i:]) % 3 == 0 and len(nums[:i])> 0:
            numsn += ','
        numsn += nums[i]
    return numsn

def TimeElapsed(stime: int) -> int:
    tl = datetime.datetime.now().timestamp() - stime
    ttce = ''
    if tl >= 86400:
        ttce = str(round(tl/86400)) + ' days'
    elif tl >= 3600:
        ttce = str(round(tl/3600)) + ' hours'
    elif tl >= 60:
        ttce = str(round(tl/60)) + ' minutes'
    else:
        ttce = str(round(tl, 2)) + ' seconds'
    return ttce

def process_args(args: str, suggestions: dict = {}) -> dict:
    d = dict()
    for i in args.split('~'):
        if len(tempi := i.split(' ', 1)) > 1:
            if tempi[0] in suggestions:
                tempi[0] = suggestions[tempi[0]]
            d[tempi[0]] = tempi[1]
    return d

async def ReqXp(level: int):
    preq = math.floor(5 / 6 * level * (2 * level * level + 27 * level + 91))
    req = math.floor(5 / 6 * (level + 1) * (2 * (level + 1) * (level + 1) + 27 * (level + 1) + 91))
    return req, preq 
            
def GetTime(arg: str) -> int:
    arg = arg.replace(' ', '')
    dur = str()
    for i in arg:
        if i in ['1' ,'2', '3', '4', '5', '6', '7', '8', '9', '0']:
            dur += i
    arg = arg.replace(dur, '')
    dur = int(dur)
    mults = {"s": 1, "sec": 1, "second":1, "seconds": 1, "m": 60, "min": 60, "minute": 60, "minutes": 60, "h": 3600, "hour": 3600, "hours": 3600, "d": 8400, "day":8400, "days": 8400}
    return dur * mults[arg.lower()]

def PercentBar(current: int, full: int=100, body: str="🟥", background: str="⬛", barlen: int=10) -> str:
    percent = math.ceil(current/(full/barlen))
    bar = str()
    for i in range(barlen):
        if i < percent:
            bar += body
        else:
            bar += background
    return bar

def Account(member) -> bool:
    db = Database()
    if db.exists("SELECT id FROM main WHERE id = ?", (member.id)):
        return True
    db.execute("INSERT INTO main(id) VALUES(?)", (member.id))
    return False
