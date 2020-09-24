import abc
from typing import List, Optional

from my_home_server.exceptions.error_code import ErrorCode
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

    def from_list_to_dto(self, obj_list: List[object]) -> List[dict]:
        if not obj_list:
            return list()

        return [self.to_dto(obj) for obj in obj_list]

    def validate_dto_to_insert(self, dto: dict):
        self.generic_validate_dto(dto, self.get_required_fields_to_insert(), self.get_entity_name(),
                                  self.get_error_code_when_dto_invalid_to_insert())

    def validate_dto_to_update(self, dto: dict):
        self.generic_validate_dto(dto, self.get_required_fields_to_update(), self.get_entity_name(),
                                  self.get_error_code_when_dto_invalid_to_update())

    @abc.abstractmethod
    def get_entity_name(self):
        """Entity name. Is used to show an error"""

    @abc.abstractmethod
    def get_required_fields_to_insert(self):
        """The dto fields that are required to insert a object"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_required_fields_to_update(self):
        """The dto fields that are required to update a object"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_error_code_when_dto_invalid_to_insert(self):
        """The ErrorCode when dto is invalid to insert"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_error_code_when_dto_invalid_to_update(self):
        """The ErrorCode when dto is invalid to update"""
        raise NotImplementedError

    def generic_validate_dto(self, dto: dict, required_fields: List[str], entity_name: str, error_code: ErrorCode):
        if dto is None:
            raise InvalidDTOException(error_code, entity_name, None)

        if required_fields:
            invalid_fields = list()

            for field_name in required_fields:
                if not dto.get(field_name):
                    invalid_fields.append(field_name)

            if len(invalid_fields):
                raise InvalidDTOException(error_code, entity_name, invalid_fields)
