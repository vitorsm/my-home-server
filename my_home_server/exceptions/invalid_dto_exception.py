from typing import List, Optional


class InvalidDTOException(Exception):

    required_fields: List[str]
    parent_exception: Optional[Exception]

    def __init__(self, entity_name: str, required_fields: Optional[List[str]], parent_exception: Exception = None):
        super().__init__(f"Failed to instantiate {entity_name}. "
                         f"{f'Required fields: {str(required_fields)}' if required_fields else 'Null object'}")
        self.required_fields = required_fields
        self.parent_exception = parent_exception
