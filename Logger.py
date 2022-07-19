class Logger:

    @staticmethod
    def log(message: str):
        """
        Log function which will print a given string to the console.
        Given string is concatenated with a Snake prefix.

        :param message: string which will be print to the console
        """

        print(f"[Snake] {message}")

