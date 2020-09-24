# my-home-server
Python restful server of my home project.


## Requirements

These directories must exist, and the user that will execute the my-home-server should be permission to write it:
* /var/log/myhome-server
* /var/lib/myhome-server

In your development environment you can execute these commands:
```
sudo mkdir /var/log/myhome-server
sudo mkdir /var/lib/myhome-server

sudo chmod 777 /var/log/myhome-server
sudo chmod 777 /var/lib/myhome-server
```

## Tests

The tests are in the directory:
``` 
my_home_server/tests/
```

The tests are separated in two groups: unit tests and integration tests.
The purpose of integration tests is to test the database integration.

To execute all tests run the command:

```
python3 -m unittest discover -s my_home_server/tests/
```

#### Coverage

To measure the test coverage you can use the coverage tool (https://coverage.readthedocs.io/).
To install run the following command:

```
pip3 install coverage
```

Then, execute the analysis:

```
coverage run --branch --source=my_home_server --omit=my_home_server/tests/* -m unittest discover -s my_home_server/tests/
```

The analysis will generate a file that contains the coverage data. To print the coverage data run the following command:
```
coverage report -m
```

## Security

The Flask-JWT lib was used to guarantee that all endpoints will be accessed only for authorized users.
According with the Flask documentation, the route decorator must be used as a outermost.
To guarantee right behavior to access endpoint, the second decorator must be jwt_required from Flask-JWT.
In order to facilitate the use of logged user, was created a context class to save the current user: AuthenticationContext.
In any part of code you can get the current user using:
```
AuthentcationContext.get_current_user()
```

The sequence of decorators in the controller layer must be route, jwt_required and set_authentication_context:
```
@controller.route("<path:user_id>")
@jwt_required()
@authentication_utils.set_authentication_context
def get_user(user_id: int, user_service: UserService, user_mapper: UserMapper):
    user = user_service.find_by_id(user_id)
    return jsonify(user_mapper.to_dto(user))
```

## Layers and directories organization

In this project there are 3 layers that are "physically" separated and has different role:
* **controller**: the controller layer will export functions to the world, in this case, to web as endpoints.
Will receive the requests and process each using the necessary services.
Is responsible to guarantee security protecting all required endpoints;
* **service**: responsible to guarantee the business rules and provides functions to handle with system data;
* **dao**: is the data access layer. The only layer allowed to communicate to the database.
Provides functions to get and insert data.

The controller cannot access directly dao, because it don't know the business rule and can handle wrongly with the data.
The service cannot access directly database, because it don't know the address and credentials to do it.
Only dao know how to get and persist data. So each request received by controller should be sent to the service,
that will check the business rule and send some request to the dao.

### Mappers

The mapper layer is responsible for converting the models (mainly persisted models) to DTO.
Each model can have multiple DTO's. A DTO is a dict that can be converted as json to be returned in an endpoint,
or a json to be received in an endpoint.

The MapperInterface was created in order to guarantee that all mappers will be able to convert from and to dto,
and validate if a dto has all required fields to be converted to a model.
```

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
```

## Dependency Injection


## Adding new entity functions

## Adding features
