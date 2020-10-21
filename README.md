# shopcarts

[![Build Status](https://travis-ci.com/NYU-DevOps2020-shopcarts/shopcarts.svg?branch=master)](https://travis-ci.com/NYU-DevOps2020-shopcarts/shopcarts)
[![codecov](https://codecov.io/gh/NYU-DevOps2020-shopcarts/shopcarts/branch/master/graph/badge.svg?token=R1VMI8JR4X)](https://codecov.io/gh/NYU-DevOps2020-shopcarts/shopcarts)

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
```json
{
    "id": null,
    "user_id": 101,
    "create_time": null,
    "update_time": null
}
```
A shopcart item can be created with a `POST` request on `/shopcartitems'`  with required parameters: 
```json
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
```
On success the response code is 201 and the newly created shopcart or shopcart item will be contained in the response in JSON format. The location header of the response will contain the id of the newly created shopcart, for example `/shopcarts/1`, or for a shopcart item, `/shopcartitems/1`.

## Getting the items in a shopcart
To get the list of items in a shopcart, you can hit a `GET` request with the id of the shopcart you are looking for. 

``` curl --location --request GET 'http://0.0.0.0:5000/shopcartitems/10' ```

The response will be something like this if
1. There are items in the shopcart - status code 200
```json [
    {
        "amount": 1,
        "create_time": "2020-10-18T17:21:44.626229",
        "id": 1,
        "name": "hello",
        "price": 100.0,
        "sid": 10,
        "sku": 10,
        "update_time": "2020-10-18T17:21:44.626229"
    },
    {
        "amount": 1,
        "create_time": "2020-10-18T17:22:06.844597",
        "id": 2,
        "name": "hello2",
        "price": 100.0,
        "sid": 10,
        "sku": 20,
        "update_time": "2020-10-18T17:22:06.844597"
    },
    {
        "amount": 1,
        "create_time": "2020-10-18T17:22:14.123710",
        "id": 3,
        "name": "hello3",
        "price": 100.0,
        "sid": 10,
        "sku": 30,
        "update_time": "2020-10-18T17:22:14.123710"
    }
]
```

2. If the shopcart is empty or shopcart is not found 
   status code 404
```json 
{}
```

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
## Updating a Shopcart Item
A shopcart item can be updated with a `PUT` request on `'/shopcartitems/id'`. 

When an authorized user hits a PUT request on '/shopcartitems', the API will return the updated shopcart item with a status code 200. The content for the PUT request would something like this:

```json
{
    "amount": 4,
}
```

The response will contain the full shopcart item.

## Querying Shopcarts
A shopcart can be queried by user with a `GET` request on `/shopcarts` with the user_id set in the query string of the request, for example, `/shopcarts?user_id=100`
The response will be the shopcart for that user, or 404 if a shopcart does not exist for that user.

Shopcart items can be queried by sku, name, price, or amount with a `GET` request on `/shopcartitems` with the appropriate field indicated in the query of the request, for example, `/shopcartitems?sku=1000`
The response will be a list of shopcart items where the indicated field has the desired value, or 404 if no shopcart items contain a field with that value.

## Delete

### Delete a Shopcart

To delete a shopcart and everything in it, make a `DELETE` request to `/shopcarts/:sid`.

### Delete a Shopcart Item

To delete a shopcart item, make a `DELETE` request to `/shopcarts/:sid/items/:item_id`.

### Place an order from a Shopcart

To place an order, make a `PUT` request to `/shopcarts/:id/place-order`. The shopcart will be deleted after the order is placed.