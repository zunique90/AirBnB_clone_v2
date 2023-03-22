#!/usr/bin/python3
"""This is the file storage class for AirBnB"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored
    """
    all_classes = {"BaseModel", "User", "State", "City",
                   "Amenity", "Place", "Review"}
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object"""
        if cls is None:
            return self.__objects
        if type(cls) is str:
            cls = eval(cls)

        filtered_dict = {}
        cls_name = cls.__name__
        if cls_name in self.all_classes:
            for k in self.__objects.keys():
                sp = k.split(".")
                if sp[0] == cls_name:
                    filtered_dict[k] = self.__objects[k]
        return filtered_dict

    def delete(self, obj=None):
        """delete obj
        Return:
            nothing
        """
        if obj is None:
            return
        else:
            obj_key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if obj_key in self.__objects.keys():
                del self.__objects[obj_key]

    def new(self, obj):
        """sets __object to given obj
        Args:
            obj: given object
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """serialize the file path to JSON file path
        """
        my_dict = {}
        for key, value in self.__objects.items():
            my_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """serialize the file path to JSON file path
        """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in (json.load(f)).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass

    def close(self):
        """calls reload() deserializes objects"""
        self.reload()
