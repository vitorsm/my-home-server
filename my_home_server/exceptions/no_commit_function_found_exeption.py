

class NoCommitFunctionFoundException(Exception):
    def __init__(self, service_name: str):
        super().__init__(f"try to commit transaction but {service_name} service has no function commit")
        self.service_name = service_name
