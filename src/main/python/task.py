class Task:
    """Task with a behaviour that can be executed"""

    def __str__(self):
        """prints the object."""
        return "General Task"

    async def get_behaviour(self):
        """":returns the behaviour of the task"""
        raise Exception("a behaviour for the task should be implemented")
