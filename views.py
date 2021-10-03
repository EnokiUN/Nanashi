import random
import discord
from vars import *
from utils import *
from engine import *

class Confirm(discord.ui.View):
    def __init__(self, ctx, timeout: int =60, acceptDialouge: str =None, declineDialoug: str =None):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.acceptDialouge = acceptDialouge
        self.declineDialouge = declineDialoug
        self.value = None
       
    async def on_timeout(self):
        for i in self.children:
            i.disabled = False
            i.style = discord.ButtonStyle.secondary
            # await self.message.edit(view=self)
    
    @discord.ui.button(label="Yes", style=discord.ButtonStyle.success, emoji='<:Yes:889083163404550174>', row=1)
    async def accept_callback(self, button, interaction):
        if interaction.user != self.ctx.author:
            await interaction.reponse.defer()
            return
        for i in self.children:
            i.disabled = True
            if i != button:
                i.style = discord.ButtonStyle.secondary
        await interaction.message.edit(view=self)
        self.value = True
        if self.acceptDialouge:
            await interaction.response.send_message(self.acceptDialouge,ephemeral=False)
        else:
            await interaction.response.defer()
     
    @discord.ui.button(label="No", style=discord.ButtonStyle.danger, emoji='<:No:889083251782721586>', row=1)
    async def decline_callback(self, button, interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.defer()
            return
        for i in self.children:
            i.disabled = True
            if i != button:
                i.style = discord.ButtonStyle.secondary
        await interaction.message.edit(view=self)
        self.value = False
        if self.declineDialouge:
            await interaction.response.send_message(self.declineDialouge,ephemeral=True)
        else:
            await interaction.response.defer()
            
class BattleView(discord.ui.View):
    def __init__(self, ctx, player, enemy):
        super().__init__()
        self.ctx = ctx
        self.player = player
        self.enemy = enemy
        self.message = None
        self.log = str()
        
    def embed_function(self, newline: str) -> discord.Embed:
        loglist = self.log.split("\n")
        if len(loglist) >= 6:
            loglist.remove(loglist[0])
            loglist.append(newline)
            self.log = "\n".join(loglist)
        elif len(loglist) == 0:
            self.log = newline
        else:
            self.log += "\n" + newline
        phppercent = self.player.hp/self.player.bhp
        if phppercent > 0.75:
            pbarcolour = "🟩"
        elif phppercent > 0.5:
            pbarcolour = "🟨"
        elif phppercent > 0.25:
            pbarcolour = "🟧"
        else:
            pbarcolour = "🟥"
        ehppercent = self.enemy.hp/self.enemy.bhp
        if ehppercent > 0.75:
            ebarcolour = "🟩"
        elif ehppercent > 0.5:
            ebarcolour = "🟨"
        elif ehppercent > 0.25:
            ebarcolour = "🟧"
        else:
            ebarcolour = "🟥"
        embed = discord.Embed(title=f"__**{self.player.name}** vs **{self.enemy.name}**__", description=f"**{self.player.name}**\n**{self.player.hp}/{self.player.bhp}**\n{PercentBar(current=self.player.hp, full=self.player.bhp, body=pbarcolour, background='⬛')}\n**{self.player.mp}/{self.player.mmp}**\n{PercentBar(current=self.player.mp, full=self.player.mmp, body='🟦', background='⬛')}\n**{self.enemy.name}**\n**{self.enemy.hp}/{self.enemy.bhp}**\n{PercentBar(current=self.enemy.hp, full=self.enemy.bhp, body=ebarcolour, background='⬛')}\n**{self.enemy.mp}/{self.enemy.mmp}**\n{PercentBar(current=self.enemy.mp, full=self.enemy.mmp, body='🟦', background='⬛')}", colour=EMBED_HEX)
        embed.add_field(name="===============", value=self.log, inline=False)
        embed.set_author(name=self.player.name, icon_url=self.player.member.avatar.url, url=f"https://discordapp.com/users/{self.player.id}")
        return embed
		
    async def action_function(self, button, interaction):
        if self.ctx.author != interaction.user:
            return await interaction.response.send_message("This button isn't for you baka", ephemeral=True)
        self.message = interaction.message
        dmg = 0
        incdef = 1
        if button.label == "attack":
            dmg = min(round(random.randrange(round(self.player.atk/2), self.player.atk)/random.randrange(round(self.enemy.defence/2), self.enemy.defence)), self.enemy.hp)
            self.player.mp = min(self.player.mp+dmg, self.player.mmp)
            self.enemy.hp -= dmg
            if self.enemy.hp <= 0:
                await interaction.response.send_message(f"You defeated **{self.enemy.name}**", ephemeral=False)
                self.stop()
                await self.message.edit(view=discord.ui.View())
                return
            self.message = await self.message.edit(embed=self.embed_function(f"You dealt **{dmg}** damage to **{self.enemy.name}**"))
        elif button.label == "block":
            incdef = 20
            self.player.mp = min(self.player.mp+20, self.player.mmp) 
            self.message = await self.message.edit(embed=self.embed_function(f"You blocked"))
        elif button.label == "skill":
            dmg = min(50, self.enemy.hp)
            self.player.mp = min(self.player.mp+dmg, self.player.mmp)
            self.enemy.hp -= dmg
            self.player.mp = 0
            if self.enemy.hp <= 0:
                await interaction.response.send_message(f"You defeated **{self.enemy.name}**", ephemeral=False)
                self.stop()
                await self.message.edit(view=discord.ui.View())
                return
            self.message = await self.message.edit(embed=self.embed_function(f"You used your skill dealing **{dmg}** damage to **{self.enemy.name}**"))
        edmg = min(round(random.randrange(round(self.enemy.atk/2), self.enemy.atk)/random.randrange(round(self.player.defence/2), self.player.defence)/incdef), self.player.hp)
        self.player.hp -= edmg
        if self.player.hp <= 0:
            await interaction.response.send_message(f"You got defeated by **{self.enemy.name}**", ephemeral=False)
            self.stop()
            await self.message.edit(view=discord.ui.View())
            return
        await self.message.edit(embed=self.embed_function(f"**{self.enemy.name}** dealt **{edmg}** damage to you"))
        if self.player.mp == self.player.mmp or self.player.mp == 0:
            for i in self.children:
                if i.label == "skill":
                    if self.player.mp == 0:
                        i.disabled = True
                        i.style = discord.ButtonStyle.secondary
                    elif self.player.mp == self.player.mmp:
                        i.disabled = False
                        i.style = discord.ButtonStyle.success
            await self.message.edit(view=self)
	
    @discord.ui.button(label="attack", emoji="🗡️", disabled=False, row=1)
    async def attack_callback(self, button, interaction):
        await self.action_function(button, interaction)
	
    @discord.ui.button(label="block", emoji="🛡️", disabled=False, row=1)
    async def block_callback(self, button, interaction):
        await self.action_function(button, interaction)
		
    @discord.ui.button(label="skill", emoji="☄️", style=discord.ButtonStyle.secondary, disabled=True, row=1)
    async def skill_callback(self, button, interaction):
        await self.action_function(button, interaction)

class TestSelect(discord.ui.View):
    @discord.ui.select(placeholder='Pick your colour', min_values=1, max_values=1, options=[
        discord.SelectOption(label='Red', description='Your favourite colour is red', emoji='🟥'),
        discord.SelectOption(label='Green', description='Your favourite colour is green', emoji='🟩'),
        discord.SelectOption(label='Blue', description='Your favourite colour is blue', emoji='🟦')
    ])
    async def select_callback(self, select, interaction):
        for i in self.children:
            i.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.send_message(f'Your favourite colour is {select.values[0]}', ephemeral=True)
    
