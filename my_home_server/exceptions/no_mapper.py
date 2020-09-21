

class NoMapper(Exception):
    def __init__(self, entity_name):
        super().__init__(f"Mapper not found to {entity_name}")
