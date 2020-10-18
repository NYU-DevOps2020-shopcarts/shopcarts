# shopcarts

![](https://travis-ci.org/NYU-DevOps2020-shopcarts/shopcarts.svg?branch=master)

The shopcarts resource allows customers to make a collection of products that they want to purchase

## Run The Service

### Development Mode

To run the service in development mode, please use:

```bash
FLASK_APP=service FLASK_ENV=development flask run -h 0.0.0.0 -p 5000
```

### Production Mode

The project uses *honcho* which gets it's commands from the `Procfile`. To start the service in production mode, simply use:

```bash
honcho start
```

## models for shopcarts 
### Shopcart
#### Attributes:
-----------
id (int) - shop cart id

user_id (int) - user id

create_time (DateTime) - the time this shopcart was created

update_time (DateTime) - the time this shopcart was updated

### ShopcartItem - Contains product information for an item in a shopcart
#### Attributes:
-----------
id (int) - for index purpose

sid (int) - shop cart id

sku (int) - product id

name (string) - product name

price (float) - price for one

amount (int) - number of product

create_time (DateTime) - the time this product was created

update_time (DateTime) - the time this product was updated

## Manually running the Tests

Run the tests using `nose`

```shell
    $ nosetests
```

Nose is configured via the included `setup.cfg` file to automatically include the flags `--with-spec --spec-color` so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

Nose is also configured to automatically run the `coverage` tool and you should see a percentage of coverage report at the end of your tests. If you want to see what lines of code were not tested use:

```shell
    $ coverage report -m
```

This is particularly useful because it reports the line numbers for the code that is not covered so that you can write more test cases to get higher code coverage.

You can also manually run `nosetests` with `coverage` (but `setup.cfg` does this already)

```shell
    $ nosetests --with-coverage --cover-package=service
```

## Logging Services

Logging is set up to track events.

## Creating a Shopcart or Shopcart Item
A shopcart can be created with a `POST` request on `'/shopcarts'` with, for example, the required conent including the following parameters:

    {

        "id": null, 

        "user_id": 101, 

        "create_time": null, 
    
        "update_time": null
    
    }

A shopcart item can be created with a `POST` request on `/shopcartitems'`  with required parameters: 

    {
        
        "id": null, 
        
        "sid": 100, 
        
        "sku": 5000, 
        
        "name": "soap", 
        
        "price": 2.23, 
        
        "amount": 3, 
        
        "create_time": null, 
        
        "update_time": null
    
    }

## Getting Shopcart list
A shopcart list can be got with a `GET` request on `'/shopcarts'`. The response will be something like 

```json
[
    {
        "create_time": "2020-10-17T04:17:28.593445",
        "id": 1,
        "update_time": "2020-10-17T04:17:28.593445",
        "user_id": 435345
    },
    {
        "create_time": "2020-10-17T04:17:29.696271",
        "id": 2,
        "update_time": "2020-10-17T04:17:29.696271",
        "user_id": 435345
    },
    {
        "create_time": "2020-10-17T04:17:30.522651",
        "id": 3,
        "update_time": "2020-10-17T04:17:30.522651",
        "user_id": 435345
    }
]
```
