


class StringPipeline:
    def __init__(self, string: str):
        self.string = string

    def extract_action(self) -> str:
        """
        Extracts the action from the string.
        """
        action = self.string.split(" ")[0]
        return action
        