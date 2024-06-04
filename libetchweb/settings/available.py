class SetVar:
    def __init__(self) -> None:
        self.name = ""
        self.table = {
            "output": "default",
            "log": False,
            "css": "enabled",
            "darkmode": False
        }

    def __repr__(self) -> str:
        return f"{self.table}"

    def set_value(self,
                  subvar: str,
                  val: str | bool) -> None:
        """Set a value to something else in the table."""

        if subvar not in self.table.keys():
            print(f"[set_value] For setvar '{self.name}':")
            print(f"[set_value]    Not setting value since subvar '{subvar}' is")
            print("[set_value]    not in the table")

            return

        if type(self.table.get(subvar)) is not type(val):
            print(f"[set_value] For setvar '{self.name}':")
            print(f"[set_value]    Not setting value '{val}' because types mismatch. Try")
            print("[set_value]    making the value a string or boolean instead")

            return

        self.table.update({subvar: val})


class Settings(SetVar):
    def __init__(self) -> None:
        super().__init__()
        self.name = "SETTINGS"

    def __repr__(self) -> str:
        return super().__repr__()

    def set_value(self, subvar: str, val: str | bool) -> None:
        return super().set_value(subvar, val)


class Warn(SetVar):
    def __init__(self) -> None:
        self.name = "WARN"
        self.table = {
            "no-settings-setvar": True
        }

    def __repr__(self) -> str:
        return super().__repr__()

    def set_value(self, subvar: str, val: str | bool) -> None:
        return super().set_value(subvar, val)


DEFAULT_SETVARS = ["WARN", "SETTINGS"]
