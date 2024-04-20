from uagents import Agent, Context
 
alice = Agent(name="alice", seed="sdksjdkwewrefwew")
 
@alice.on_event("startup")
async def say_hello(ctx: Context):
    ctx.logger.info(f'hello, my name is {ctx.name}')
 
if __name__ == "__main__":
    alice.run()