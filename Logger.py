from enums.Prefix import Prefix


class Logger:

    @staticmethod
    def log(message: str, prefix: Prefix = Prefix.SNAKE):
        """
        Log function which will print a given string to the console.
        Given string is concatenated with a Snake prefix.

        :param message: string which will be print to the console
        :param prefix: changes the prefix
        """

        print(f"{prefix.value}:\t {message}")

