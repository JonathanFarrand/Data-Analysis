from src.commands.command_parser import CommandParser
import pandas as pd

class CommandDispatcher:
    def __init__(self, store: pd.DataFrame, parser: CommandParser):
        self.store = store
        self.parser = parser

    def execute(self, input_str):
        # Parse the command using the parser
        command = self.parser.parse(input_str)
        # Execute the command
        command.execute(self.store)