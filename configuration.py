import json
import os
import inspect
from typing import List, Dict

class Margin:
    width: int
    height: int

class StickConfiguration:
    radius: float
    radiusCarveOffset: float
    minLength: float
    usageLength: float
    lengthJigOffset: float

class Configuration(object):
    variant: str
    width: int
    height: int
    mmPerPixel: int
    margin: Margin
    stick: StickConfiguration


def _from_json(data, cls):
    annotations: dict = cls.__annotations__ if hasattr(cls, '__annotations__') else None
    if issubclass(cls, List):
        list_type = cls.__args__[0]
        instance: list = list()
        for value in data:
            instance.append(_from_json(value, list_type))
        return instance
    elif issubclass(cls, Dict):
            key_type = cls.__args__[0]
            val_type = cls.__args__[1]
            instance: dict = dict()
            for key, value in data.items():
                instance.update(_from_json(key, key_type), _from_json(value, val_type))
            return instance
    else:
        instance : cls = cls()
        for name, value in data.items():
            field_type = annotations.get(name)
            if inspect.isclass(field_type) and isinstance(value, (dict, tuple, list, set, frozenset)):
                setattr(instance, name, _from_json(value, field_type))
            else:
                setattr(instance, name, value)
        return instance

def load_configuration(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        configurations = []
        for configuration_data in data:
            configuration : Configuration = _from_json(configuration_data, Configuration)
            configurations.append(configuration)
        
        return configurations