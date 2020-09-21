import abc


class MapperInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def to_dto(self, obj: object) -> dict:
        """Receives a object from models and convert to a dto of type dict"""
        raise NotImplementedError

    @abc.abstractmethod
    def to_object(self, dto: dict, loaded_object: object = None) -> object:
        """Receives a dict dto and converts to a object from models
        :rtype: object
        """
        raise NotImplementedError

    @abc.abstractmethod
    def validate_dto(self, dto: dict):
        """Validate required fields and type of fields from dto"""
        raise NotImplementedError
