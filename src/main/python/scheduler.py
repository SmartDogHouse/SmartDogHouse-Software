import machine
import uasyncio as asyncio


class Scheduler:

    def __init__(self):
        """ constructor.
        """
    def __str__(self):
        """prints the object."""
        return "Motor currently is running: {}"

    def __set_global_exception(self):
        def handle_exception(loop, context):
            import sys
            print("\t Eroore!!")
            sys.print_exception(context["exception"])
            #sys.exit()
        loop = asyncio.get_event_loop()
        loop.set_exception_handler(handle_exception)

    def scheduleForever(self, task):
        asyncio.create_task(self.__scheduleForever(task))

    async def __scheduleForever(self, task):
        while True:
            task()
            await asyncio.sleep(2)


    def scheduleOnce(self, task):
        asyncio.create_task(task)  # Or you might do this

    def __start(self, task):
        try:
            await asyncio.gather(*task, return_exceptions=True)
        except Exception as e:
            print("Caught it!"+str(e))
        # await task()  # Non-terminating method

    def start(self, task):
        self.__set_global_exception()
        asyncio.run(self.__start(task))
