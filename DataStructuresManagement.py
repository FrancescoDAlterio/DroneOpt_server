import threading
from queue import *
import Utilities

class DataStructuresManagement():

    __active_clients=[]

    __dict_values = {}
    __dict_AVGs = {}

    @classmethod
    def get_active_clients(cls):
        return cls.__active_clients

    @classmethod
    def set_active_clients(cls,new_list):
        cls.__active_clients = new_list


    @classmethod
    def add_active_clients(cls,obj):
        cls.__active_clients.append(obj)
        return True

    @classmethod
    def rmv_active_clients(cls, obj):
        if obj not in cls.__active_clients:
            return False # there is a bug, he has not  find the process id to remove

        cls.__active_clients.remove(obj)
        return True

    @classmethod
    def get_dict_values(cls):
        return cls.__dict_values

    @classmethod
    def set_dict_values(cls,my_dict):
        cls.__dict_values = my_dict

    @classmethod
    def get_dict_AVGs(cls):
        return cls.__dict_AVGs

    @classmethod
    def set_dict_AVGs(cls, my_dict):
        cls.__dict_AVGs = my_dict




