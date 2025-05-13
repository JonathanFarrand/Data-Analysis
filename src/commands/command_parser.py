from src.commands.command import GenerateVariableCommand

class CommandParser:
    def __init__(self):
        self.commands_map = {
            'gen': GenerateVariableCommand,
        }

    def parse(self, input_str):
        parts = input_str.strip().split(maxsplit=1)
        if not parts:
            raise ValueError("Empty command")

        action = parts[0]
        if action not in self.commands_map:
            raise ValueError(f"Unknown command '{action}'")
        
        # Delegate argument parsing to the appropriate command
        command_class = self.commands_map[action]
        arguments = parts[1] if len(parts) > 1 else ""
        return command_class.from_string(arguments)
