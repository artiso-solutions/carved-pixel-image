import json
import os
import inspect
from typing import List, Dict

class Margin:
    """ Margin of the produced pixels to define the absolute size of the carved art. 
    
    Width is added as margin to the left and right. 
    Height is aded as margin to the top and bottom.
    """

    width: int
    height: int

    
class StickConfiguration:
    """ Configuration for one stick per pixel. There are some additional parameters which are relevant especially for cutting the stick lengths.
    
    Attributes
    ----------
    radius : float
        the radius of the sticks used for generating the dxf file
    radiusCarveOffset : float
        the carve offset which helps in fine tuning the tolerances of the cnc and the sticks to get a good fit
    minLength : float
        the length of a complete white pixel
    usageLength : float
        the difference in length between a white and a black pixel.
    lengthJigOffset : float
        helper for printing out the stick length reduced by the jig offset. This helps on faster 
        cutting if using a jig with a ruler which has some offset to the actual length of the stick.
    """

    radius: float
    radiusCarveOffset: float
    minLength: float
    usageLength: float
    lengthJigOffset: float


class Configuration(object):
    """ Configuration for one variant. This contains the main information about number and size of pixels and margin. 
    
    Any additional informationen needed will be specified in attributes per variant which are optional.
    
    Attributes
    ----------
    variant : str
        the weel known name of the variant. These are circle | band | stick.
    width : int
        the number of pixels in width
    height : int
        the number of pixels in height
    mmPerPixel : int
        the size for each pixel which will be used for generating the dxf file
    margin : Margin
        the margin outside the pixels which will be used for calculating the pixel positions and the margin around 
        the pixles when generating the dxf file
    stick : StickConfiguration
        variant specific configuration for the stick variant
    """

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
    """ Loads an array of variant configuration from the json file found at file_path. """
    
    with open(file_path, 'r') as file:
        data = json.load(file)
        configurations = []
        for configuration_data in data:
            configuration : Configuration = _from_json(configuration_data, Configuration)
            configurations.append(configuration)
        
        return configurations