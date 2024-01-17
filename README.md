# README

## Folders
The project is mainly divided into two folders.

- **idoven_app/idoven**: Where the source code is located.
- **idoven_app/tests**: Where the test suite is located.


## HOW TO...?

To run the code, please, locate at the same folder level as the Makefile and run: 

``` make up ```

The recommended way to test is browsing to ```http://localhost:8080/docs``` and then authenticate with one of the provided users. If a new user wants to be created, find below the User **alice** and her credentials to be able to do so.

## USERS, ECGS AND PASSWORDS:

- To ease the execution of the code, seeds of users and ecgs have been provided. This initial data can be found under ```ìnit.sql``` and ```mongo-seed/ecg_seed.json```. Also, find here some sample:

#### Users:

- **username**: johndoe, **password**: password1, **role**: USER
- **username**: daviddoe, **password**: pwd,  **role**: USER
- **username**: alice, **password**: password2, **role**: ADMIN

#### SOME ECGS IDS:

- **johndoe**'s: 60d7c0a38e1e0a241c4b4d9c && 60d7c05c8e1e0a241c4b4d9b
- **daviddoe**'s: 60d7c1318e1e0a241c4b4d9e && 60d7c0ed8e1e0a241c4b4d9d 


To run tests:

- **Unit-tests**: ``` make test-unit``` 
- **Integration tests**: ```make test-integration```
- **Acceptance tests**: ```make test-acceptance```
- **All**: ```make test```

## IMPLEMENTATION

The project has been implemented using python 3.11 and FastAPI and implementing async workflows; it is structured following a separation of folders based on hexagonal architecture and DDD. Therefore, the main folders you will find are:

- At **root level**, we can find **ops files** such as poetry files, docker files and makefiles.

The usage of Docker, Poetry and Make is a decision to make testing easier, as well as showing a more realistic approach.
- **API**: In this folder, files related to the routers responsible for exposing the application's endpoints are located. It follows a versioned API structure. Here, we can find two folders to separate ```user``` and ```ecg``` routers. Also, health check and auth the **auth** system can be found inside.
- **Infrastructure**: In this folder, implementations of the used databases for our repositories are found (adapters); in our case, PostgreSQL, MongoDB, and an in-memory database.
- **Use Cases**: In this folder, the functionality associated with the use cases of our application is located, serving as a link between layers (ports and adapters).
- **Domain**: In this layer, the definition of the main classes of our project is found, as well as the definition of interfaces (ports) of the repositories. The core logic of the application is in these files.

As previously mentioned, the project follows a hexagonal architecture, reducing as much as possible any dependencies. 
The comunication between the ```api``` and ```infrastructure```  with ```domain``` layer happens in the ```use cases```
layer. We introduced the usage of **command pattern** to encapsulate the logic of each request performed against the API and from there, we can easily communicate the requests between layers, keeping the responsabilities as separeted as possible. Also, the existance of classes for requests like **ECGRequest** and **ECG** is because so, we can leverage the parsing capabilities of **Pydantic** bringing some sanity checks to the requests.

Some important considerations about the API layer:
- The auth system has been implemented as vanilla as possible for simplicity. Although, we have added some separations in code and the usage of custom **Role** coming from an enumerate.
- The usage of the pattern ```Client-Supplied Identifier``` is usaged to simplify testing. Providing the ids from the client bring us some benefits like the ability of knowing the user id before inserting the record into the databases,
this eases testing procedures.
- For the endpoint ```api/v1/insights/{ecg_id}`` the reason why we return a Not Found 404 is to enfuscate the existance of that ECG belonging to another user.


In the domain, Factories have been implemented in order to have one unique point of creation and validation for each domain class. All logic related to **User**, **ECG** and **Lead** has been implemented inside these classes, like 
```leads_zero_crosses```  and ```verify_password```. This way, future refactors are ease to overcome. 