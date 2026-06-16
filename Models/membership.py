from abc import ABC, abstractmethod

class Membership(ABC):
    def __init__(self, member_id, name, months):
        self.__member_id = member_id
        self.__name = name
        self.__months = months

    @property
    def member_id(self):
        return self.__member_id

    @property
    def name(self):
        return self.__name

    @property
    def months(self):
        return self.__months

    @abstractmethod
    def calculate_fee(self):
        pass