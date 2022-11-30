from twitchio.ext import commands

class VoteYes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        self.__vote_option = "yes"
    
    def vote(self):
        return self.bot.vote()

    @commands.command(name='yes')
    async def vote_yes(self, ctx: commands.Context):
        vote = self.vote()
        poll_id = vote.get_poll_running()
        if poll_id is None:
            await ctx.send(f"There is no poll running at the moment.")
            return
        
        author_id = ctx.author.id
        if vote.has_voted(author_id, poll_id):
            await ctx.send(f"You have already voted.")
            return
        
        if not vote.vote(poll_id, author_id, self.__vote_option):
            await ctx.send(f"An error occurred while creating the poll.")
            return
        
        await ctx.send(f"Vote registered.")
        
def prepare(bot: commands.Bot):
    bot.add_cog(VoteYes(bot))