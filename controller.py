from os import environ
import asyncio
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn import wamp


class Component(ApplicationSession):
    def __init__(self, config):
        ApplicationSession.__init__(self, config)
        self.progress = 0
        self.running = False

    async def update(self):
        while True:
            if self.running:
                self.progress += 1
            if self.progress == 100:
                self.running = False
            self.publish('com.prepbot.window.progress', self.progress)
            await asyncio.sleep(0.01)

    async def onJoin(self, details):
        try:
            res = await self.subscribe(self)
            print("Subscribed to {0} procedure(s)".format(len(res)))
        except Exception as e:
            print("could not subscribe to procedure: {0}".format(e))
        asyncio.ensure_future(self.update())

    @wamp.subscribe('com.prepbot.window.start')
    def start(self):
        self.progress = 0
        self.running = True

if __name__ == '__main__':
    runner = ApplicationRunner(url="ws://127.0.0.1:8080/ws", realm="realm1")
    runner.run(Component)