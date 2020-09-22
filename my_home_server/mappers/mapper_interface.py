import abc
from typing import List, Optional

from my_home_server.exceptions.invalid_dto_exception import InvalidDTOException


class MapperInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def to_dto(self, obj: object) -> Optional[dict]:
        """Receives a object from models and convert to a dto of type dict"""
        raise NotImplementedError

    @abc.abstractmethod
    def to_object(self, dto: dict, loaded_object: object = None) -> Optional[object]:
        """Receives a dict dto and converts to a object from models
        :rtype: object
        """
        raise NotImplementedError

    @abc.abstractmethod
    def validate_dto(self, dto: dict):
        """Validate required fields and type of fields from dto"""
        raise NotImplementedError

    def generic_validate_dto(self, dto: dict, required_fields: List[str], entity_name: str):
        if not dto:
            raise InvalidDTOException(entity_name, None)

        if required_fields:
            invalid_fields = list()

            for field_name, value in dto.items():
                if field_name in required_fields and not value:
                    invalid_fields.append(field_name)

            if len(invalid_fields):
                raise InvalidDTOException(entity_name, invalid_fields)
