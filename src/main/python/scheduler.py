import machine
import uasyncio as asyncio


class Scheduler:

    def __init__(self):
        """ constructor.
        """

    def __str__(self):
        """prints the object."""
        return "Scheduler"

    def __set_global_exception(self):
        def handle_exception(loop, context):
            import sys
            print("\t Global Error!!")
            sys.print_exception(context["exception"])
            # sys.exit()
        loop = asyncio.get_event_loop()
        loop.set_exception_handler(handle_exception)

    def schedule_once(self, task):
        asyncio.create_task(task)

    async def __start(self, task):
        self.__set_global_exception()
        await asyncio.gather(*task, return_exceptions=False)  # returns async task, has to be false to rise exception instead of returning it

    def start(self, task):
        """passed an array of corutines to be executed"""
        asyncio.run(self.__start(task))  # run needs async task
