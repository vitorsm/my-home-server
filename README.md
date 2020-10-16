# my-home-server

Python restful server of MyHome project.

It is a Flask application and use SQLAlchemy as a ORM.

[![codecov](https://codecov.io/gh/vitorsm/my-home-server/branch/master/graph/badge.svg)](https://codecov.io/gh/vitorsm/my-home-server)
![build](https://img.shields.io/github/workflow/status/vitorsm/my-home-server/Releases)


The porpuse of this project is to provide functions to create a shopping list and registered all products bought in shopping and provide reports about spend money and more bought products.

The frontend is in the my-home-app in https://github.com/vitorsm/my-home-app/

The main entity in this project is Purchase, each Purchase has a list of bought products. The products can be registered before and be linked to a brand and product type. If the product has product type and brand, is possible to generate report by brand and product type.

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

The Flask-Injector was used to manage dependency injection. After the dependencies are register in the binder,
the functions decorated with flask route can instantiate their dependencies automatically.

All DAO's and Services should be register in the binder. To register a new Service or DAO,
insert it in the dependencies_injector.py.


## Adding entity CRUD or functions

1. To create a new CRUD the first step is create the model. In this example, the model is ```User```.
When a model will be used as foreign key in other model, is required use the same base model. So, to create a new model
extends it of ```models.base_models.Base```:
    ```
    class User(Base):
        __tablename__ = "user"
        id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        name = Column(String, nullable=False)
        login = Column(String, nullable=False, unique=True)
        password = Column(String, nullable=False)
        user_group_id = Column(Integer, ForeignKey("user_group.id"), nullable=False)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
        user_group = relationship("UserGroup", lazy="select")
    
        def __eq__(self, other):
            return other and self.id == other.id
    
        def __hash__(self):
            return hash(self.id)
    
    ```

    The ```__eq__``` function is used by SQLAlchemy to compare two objects.

1. If this entity will be inserted from a HTTP request, prepare the mapper that will convert the json to object and the
object to json. Create a class in ```mappers``` that extends ```MapperInterface```.

    ```
    class UserMapper(MapperInterface):
        def __init__(self):
            self.user_group_mapper = UserGroupMapper()
        
        [...]
    ```
   
   To all services can get the mapper register it in the ```mappers.mapper.Mapper```.
   
1. Create the dao in ```dao``` extending from ```dao.dao.DAO```. The generic dao already have basic function to add,
update and delete entities. Create the other required functions:

    ```
    class UserDAO(DAO):
        def find_by_id(self, user_id: int) -> Optional[User]:
            return self.db.session.query(User).get(user_id)
    
        def find_by_login(self, login: str) -> Optional[User]:
            return self.db.session.query(User).filter(User.login == login).first()
    ``` 
   
   Register the DAO in the ```configs.dependencies_injector.AppModule```
   
1. Create the service in ```services```. The service needs to get a dao instance. Receive the DAO in the constructor.
If necessary to use ```@utils.sql_utils.transaction```, implement the ```commit``` function.
This function will be responsible to commit all changes.

    ```
    class UserService(object):
        def __init__(self, user_dao: UserDAO, user_group_service: UserGroupService):
            self.user_dao = user_dao
            self.user_group_service = user_group_service
            self.mapper = Mapper.get_mapper(User.__name__)
   
        [...]
   
        def commit(self):
            self.user_dao.commit()
    ```
   
   Register the Service in the ```configs.dependencies_injector.AppModule```

1. Create the controller in ```controllers``` to expose the functions.
The controller will be a variable in this file instead a class.

    ```
    controller = Blueprint("user_controller", __name__, url_prefix="/api/user")
    errors_handler.fill_error_handlers_to_controller(controller)
    
    
    @controller.route("<path:user_id>")
    @jwt_required()
    @authentication_utils.set_authentication_context
    def get_user(user_id: str, user_service: UserService, user_mapper: UserMapper):
        user = user_service.find_by_id(int(user_id))
        return jsonify(user_mapper.to_dto(user))

    ```
   
   Register the controller in ```configs.controllers_register```
   
