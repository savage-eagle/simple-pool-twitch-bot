from twitchio.ext import commands

import sqlite3 
import logging

class Poll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    def vote(self):
        return self.bot.vote()

    @commands.command(name='poll')
    async def poll(self, ctx: commands.Context):
        vote = self.vote()
        
        if (ctx.author.name != ctx.channel.name):
            await ctx.send(f"You are not the owner of this channel.")
            return
        
        split = ctx.message.content.split('!poll ')
        if (len(split) < 2):
            await ctx.send(f"!poll <question>")
            return

        if vote.get_poll_running():
            await ctx.send(f"There is a poll running. Please wait until it is finished.")
            return

        question = split[1].strip()
        
        author_id = ctx.author.id
        if not vote.create_poll(author_id, question):
            await ctx.send(f"An error occurred while creating the poll.")
            return
        
        await ctx.send(f"Poll started! Question: {question}")
        await ctx.send(f"Vote with !yes or !no")
        
def prepare(bot: commands.Bot):
    bot.add_cog(Poll(bot))