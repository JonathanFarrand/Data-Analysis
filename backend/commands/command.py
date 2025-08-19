from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self, store):
        """Execute the command."""
        pass

    @classmethod
    @abstractmethod
    def from_string(cls, arguments: str):
        """Create the command from a string of arguments."""
        pass

class GenerateVariableCommand(Command):
    def __init__(self, var_name, expression):
        self.var_name = var_name
        self.expression = expression

    def execute(self, store) -> str:
        new_column_name = self.var_name.strip()
        value = store.evaluate(self.expression)
        store.set(self.var_name, value)
        return f"Generated {self.var_name} = {value}"

    @classmethod
    def from_string(cls, arguments: str):
        parts = arguments.strip().split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError("Generate command requires a variable name and expression.")
        var_name, expr = parts
        return cls(var_name, expr)

