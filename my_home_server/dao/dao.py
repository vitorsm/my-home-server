from typing import List

from sqlalchemy.exc import IntegrityError, InvalidRequestError

from my_home_server.exceptions.duplicate_entry_exception import DuplicateEntryException
import my_home_server.utils.sql_utils as sql_utils
from my_home_server.exceptions.error_code import ErrorCode


class DAO(object):
    def __init__(self, db):
        self.db = db

    def commit(self, raise_integrity_error: bool = False):
        try:
            self.db.session.commit()
        except IntegrityError as ex:
            if raise_integrity_error:
                raise ex
            else:
                self.__handle_integrity_error(ex, "")

    def expunge(self, entity: object):
        try:
            self.db.session.expunge(entity)
        except InvalidRequestError:
            # When a entity is not exist in the session is not necessary raise an error,
            # because it's like it's already been expunged
            pass

    def add(self, entity: object, commit: bool = False):
        self.db.session.add(entity)
        if commit:
            try:
                self.commit(raise_integrity_error=True)
            except IntegrityError as ex:
                self.__handle_integrity_error(ex, type(entity).__name__)

    def update(self, entity: object, commit: bool = False):
        if entity not in self.db.session:
            self.db.session.add(entity)
        if commit:
            self.db.session.commit()

    def delete(self, entity: object, commit: bool = False):
        self.db.session.delete(entity)
        if commit:
            self.commit()

    @staticmethod
    def __handle_integrity_error(exception: IntegrityError, entity: str):
        if "UNIQUE" in exception.orig.args[0]:
            field = exception.orig.args[0].split(': ')[1]
            value = None

            if "." in field:
                field = field.split(".")[1]

            index = sql_utils.get_position_of_field_in_insert_query(exception.statement, field)

            if exception.params and len(exception.params) > index >= 0:
                value = exception.params[index]

            raise DuplicateEntryException(ErrorCode.GENERIC_EXCEPTION, entity, field, value)

        raise exception

