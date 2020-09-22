from my_home_server.exceptions.error_code import ErrorCode


class DuplicateEntryException(Exception):
    def __init__(self, entity: str, field: str, value: str, error_code: ErrorCode = None):
        super().__init__(f"Cannot create {entity} because the field {field} is unique and the value {value} "
                         f"already exists")
        self.entity = entity
        self.field = field
        self.value = value
        self.error_code = error_code
