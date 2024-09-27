from utils import is_substring_species,convert_str_to_int


class SpecieKey:
    def __init__(self,value: int):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self,value: int):
        self._value = value
        return self

    def __repr__(self) -> str:
        return f"{self.value}"

    def __str__(self) -> str:
        return f"{self.value}"

class SpecieIndex:
    pass

class SpecieName:
    def __init__(self,value: str):
        if is_substring_species(value):
            self.value = value
            return
        else:
            raise ValueError(f"{value} is not a valid specie name")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self,value: str):
        self._value = value

    def __str__(self) -> str:
        return self.value

class ReactionKey:
    def __init__(self,value: int):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self,value: int):
        self._value = value

    def __repr__(self) -> str:
        return f"{self.value}"

    def __str__(self) -> str:
        return f"{self.value}"

    def __eq__(self, value: object) -> bool:
        return self.value == int(value)

class ReactionIndex:
    pass



class Manager:
    pass