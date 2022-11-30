from twitchio.ext import commands

class ResultPoll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    def vote(self):
        return self.bot.vote()

    @commands.command(name='results')
    async def vote_yes(self, ctx: commands.Context):
        vote = self.vote()
        
        latest_poll_id = vote.get_latest_poll()
        if not latest_poll_id:
            await ctx.send(f"There is no poll running.")
            return
        
        result = vote.get_poll_results(latest_poll_id)
        await ctx.send(f"Yes: {result['yes']}% | No: {result['no']}%")
        
def prepare(bot: commands.Bot):
    bot.add_cog(ResultPoll(bot))