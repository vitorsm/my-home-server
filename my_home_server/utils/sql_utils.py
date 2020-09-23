import inspect
import os

import my_home_server.configs.log as log
from my_home_server.exceptions.no_commit_function_found_exeption import NoCommitFunctionFoundException

logger = log.get_logger(__name__)


def transaction(function):
    """
        This decorator function will be used to commit changes in db after the process finished.
        The after the end of the first function that uses this decorator, the changes should be committed in db.

        This function just could be used for a non static function. The class that will be used must implement
        the commit function. The commit function will commit changes to the db.
    """

    def transaction_wrapper(*args, **kwargs):
        ret = function(*args, **kwargs)

        commit = True
        count = 0

        for call_item in inspect.stack():
            if call_item and call_item[3] == "transaction_wrapper":
                self_names = __name__.split(".")
                call_names = call_item[1].split(".")[0].split(os.path.sep)

                if all(sn in call_names for sn in self_names):
                    count += 1

                if count > 1:
                    commit = False
                    break

        if commit:
            if args[0].commit:
                args[0].commit()
            else:
                exc = NoCommitFunctionFoundException(type(args[0]).__name__)
                logger.error(str(exc))
                raise exc

        return ret

    return transaction_wrapper


def get_position_of_field_in_insert_query(insert_query: str, field: str) -> int:
    if not insert_query or not field:
        return -1

    try:
        open_index = insert_query.index("(")
        close_index = insert_query.index(")")
    except ValueError:
        return -1

    if open_index < 0 or close_index < 0 or close_index - open_index < 2:
        return -1

    between_parentheses = insert_query[open_index + 1:close_index]
    fields = [f.strip() for f in between_parentheses.split(",")]

    if field in fields:
        return fields.index(field)

    return -1

