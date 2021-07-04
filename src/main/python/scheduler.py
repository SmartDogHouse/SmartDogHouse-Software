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
            print("\t Error!!")
            sys.print_exception(context["exception"])
            # sys.exit()

        loop = asyncio.get_event_loop()
        loop.set_exception_handler(handle_exception)

    def schedule_forever(self, task):
        asyncio.create_task(self.__schedule_forever(task))

    async def __schedule_forever(self, task):
        while True:
            task()
            await asyncio.sleep(2)

    def schedule_once(self, task):
        asyncio.create_task(task)  # Or you might do this

    def __start(self, task):
        try:
            await asyncio.gather(*task, return_exceptions=True)
        except Exception as e:
            print("Caught it!" + str(e))

    def start(self, task):
        self.__set_global_exception()
        asyncio.run(self.__start(task))
