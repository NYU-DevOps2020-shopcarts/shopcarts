# shopcarts

[![Build Status](https://travis-ci.com/NYU-DevOps2020-shopcarts/shopcarts.svg?branch=master)](https://travis-ci.com/NYU-DevOps2020-shopcarts/shopcarts)
[![codecov](https://codecov.io/gh/NYU-DevOps2020-shopcarts/shopcarts/branch/master/graph/badge.svg?token=R1VMI8JR4X)](https://codecov.io/gh/NYU-DevOps2020-shopcarts/shopcarts)

The shopcarts resource allows customers to make a collection of products that they want to purchase.

## Online Demo

IBM Cloud Foundry App for this project can be accessed at [here](https://nyu-shopcart-service-f20.us-south.cf.appdomain.cloud/).

## Prerequisite Installation using Vagrant

The easiest way to use this app is with Vagrant and VirtualBox. If you don't have this software, the first step is to download and install it.

Download [VirtualBox](https://www.virtualbox.org/)

Download [Vagrant](https://www.vagrantup.com/)

Then all you have to do is clone this repo and invoke vagrant:

```shell
    git clone https://github.com/NYU-DevOps2020-shopcarts/shopcarts.git
    cd shopcarts
    vagrant up
    vagrant ssh
    cd /vagrant
```

## Running the Service

### Development Mode

To run the service in development mode, please use:

```bash
FLASK_APP=service FLASK_ENV=development flask run -h 0.0.0.0 -p 5000
```

### Production Mode

The project uses *honcho*, which gets its commands from the `Procfile`. To start the service in production mode, simply use:

```bash
honcho start
```

## Manually Running the Tests

### For Unit Test

Run the tests using `nose`

```shell
    $ nosetests
```

### For Behavior Test

These tests require the service to be running because, unlike the TDD unit tests that test the code locally, these BDD integration tests are using Selenium to manipulate a web page on a running server.

Run BDD tests using `behave`

```shell
    $ honcho start &
    $ behave
```

Note that the `&` runs the server in the background. To stop the server, you must bring it to the foreground and then press `Ctrl+C`.

Stop the server with

```shell
    $ fg
    $ <Ctrl+C>
```

## Models for Shopcarts 

### Shopcart

| Name        | Type     | Purpose                              |
|-------------|----------|--------------------------------------|
| id          | int      | Primary key for the table            |
| user_id     | int      | User id whose shopcart this is       |
| create_time | datetime | Time when shopcart was created       |
| update_time | datetime | Time when shopcart was last modified |

### ShopcartItem - Contains product information for an item in a shopcart

| Name        | Type     | Purpose                                              |
|-------------|----------|------------------------------------------------------|
| id          | int      | Primary key for the table                            |
| sid         | int      | Shopcart id in which the item is present             |
| sku         | int      | Product/Item id                                      |
| name        | string   | Name of product/item                                 |
| price       | float    | Price of the product/item                            |
| amount      | int      | Count of the item in the shopcart                    |
| create_time | datetime | Time when item was added to the shopcart             |
| update_time | datetime | Time when the item in the shopcart was last modified |

## Routes

| URL                            | HTTP method | Description                                         |
|--------------------------------|-------------|-----------------------------------------------------|
| /shopcarts                     | GET         | Get a shopcart list, or query by user_id            |
| /shopcarts                     | POST        | Create a shopcart                                   |
| /shopcarts/:id                 | GET         | Read a shopcart                                     |
| /shopcarts/:id                 | DELETE      | Delete a shopcart                                   |
| /shopcarts/:id/place-order     | PUT         | Place an order                                      |
| /shopcarts/:id/items           | GET         | Get item list from a shopcart                       |
| /shopcarts/:id/items           | POST        | Create a shopcart item                              |
| /shopcarts/:id/items/:item_id  | GET         | Gets a shopcart item                                |
| /shopcarts/:id/items/:item_id  | PUT         | Update a shopcart item                              |
| /shopcarts/:id/items/:item_id  | DELETE      | Delete a shopcart item                              |
| /shopcarts/items               | GET         | Query shopcart items by sku, name, amount, or price |

## APIs for Shopcart

Please check the latest API Docs and live demo [here](https://nyu-shopcart-service-f20.us-south.cf.appdomain.cloud/apidocs).

### List

#### HTTP Request

`GET /shopcarts`

#### Example Request

```shell
curl -H 'Content-Type: application/json' \
     -X GET 'https://nyu-shopcart-service-f20.us-south.cf.appdomain.cloud/shopcarts'
```

#### Successful Response

```json
[
    {
        "create_time": "2020-10-30T14:28:31.480436",
        "id": 1,
        "update_time": "2020-10-30T14:28:31.480436",
        "user_id": 435345
    },
    {
        "create_time": "2020-11-03T14:16:31.372411",
        "id": 2,
        "update_time": "2020-11-03T14:16:31.372411",
        "user_id": 444
    },
    {
        "create_time": "2020-11-04T22:03:33.159086",
        "id": 3,
        "update_time": "2020-11-04T22:03:33.159086",
        "user_id": 333
    }
]
```

### Create

#### HTTP Request

`POST /shopcarts`

#### Parameters

| Name    | Type |
|---------|------|
| user_id | int  |

#### Example Request

```shell
curl -H 'Content-Type: application/json' \
     -d '{"user_id": 101}' \
     -X POST 'https://nyu-shopcart-service-f20.us-south.cf.appdomain.cloud/shopcarts'
```

#### Successful Response

```json
{
    "create_time": "2020-11-15T19:36:28.302839",
    "id": 6,
    "update_time": "2020-11-15T19:36:28.302839",
    "user_id": 101
}
```

#### Note

If a shopcart with the associated `user_id` already exists, the API will return the existing shopcart.

### Read

#### HTTP Request

`GET /shopcarts/:id`

#### Parameters

| Name | Type |
|------|------|
| id   | int  |

#### Example Request

```shell
curl -H 'Content-Type: application/json' \
     -X GET 'https://nyu-shopcart-service-f20.us-south.cf.appdomain.cloud/shopcarts/1'
```

#### Successful Response

```json
{
    "create_time": "2020-10-30T14:28:31.480436",
    "id": 1,
    "items": [],
    "update_time": "2020-10-30T14:28:31.480436",
    "user_id": 435345
}
```

### Delete

#### HTTP Request

`DELETE /shopcarts/:id`

#### Parameters

| Name | Type |
|------|------|
| id   | int  |

#### Example Request

```shell
curl -H 'Content-Type: application/json' \
     -X DELETE 'https://nyu-shopcart-service-f20.us-south.cf.appdomain.cloud/shopcarts/1'
```

### Query by User ID

#### HTTP Request

`GET /shopcarts?user_id=<user_id>`

#### Parameters

| Name    | Type |
|---------|------|
| user_id | int  |

#### Example Request

```shell
curl -H 'Content-Type: application/json' \
     -X GET 'https://nyu-shopcart-service-f20.us-south.cf.appdomain.cloud/shopcarts?user_id=333'
```

#### Successful Response

```json
{
    "create_time": "2020-11-04T22:03:33.159086",
    "id": 3,
    "update_time": "2020-11-04T22:03:33.159086",
    "user_id": 333
}
```

#### Note

If the shopcart with the associated `user_id` does not exist, the API will return `404 Not Found`.

### Place Order

#### HTTP Request

`PUT /shopcarts/:id/place-order`

#### Parameters

| Name | Type |
|------|------|
| id   | int  |

#### Example Request

```shell
curl -H 'Content-Type: application/json' \
     -X PUT 'https://nyu-shopcart-service-f20.us-south.cf.appdomain.cloud/shopcarts/2/place-order'
```

## APIs for Shopcart Items

### List

#### HTTP Request

`GET /shopcarts/:id/items`

#### Parameters

| Name | Type |
|------|------|
| id   | int  |

#### Example Request

```shell
curl -L -H 'Content-Type: application/json' \
     -X GET 'https://nyu-shopcart-service-f20.us-south.cf.appdomain.cloud/shopcarts/4/items'
```

#### Successful Response

```json
[
    {
        "amount": 3,
        "create_time": "2020-11-06T20:48:07.731641",
        "id": 4,
        "name": "soap",
        "price": 2.23,
        "sid": 4,
        "sku": 5001,
        "update_time": "2020-11-06T20:48:07.731641"
    },
    {
        "amount": 15,
        "create_time": "2020-11-04T22:33:40.954337",
        "id": 3,
        "name": "soap",
        "price": 2.23,
        "sid": 4,
        "sku": 5000,
        "update_time": "2020-11-15T05:20:19.332832"
    }
]
```

#### Note

If the shopcart is empty, you will receive 404 Not Found.

### Create

#### HTTP Request

`POST /shopcarts/:id/items`

#### Parameters

| Name   | Type   |
|--------|--------|
| id     | int    |
| sku    | int    |
| name   | string |
| price  | float  |
| amount | int    |

#### Example Request

```shell
curl -L -H 'Content-Type: application/json' \
     -d '{"sku": 5000, "name": "soap", "price": 2.23, "amount": 3}' \
     -X POST 'https://nyu-shopcart-service-f20.us-south.cf.appdomain.cloud/shopcarts/1/items'
```

#### Successful Response

```json
{
    "amount": 3,
    "create_time": "2020-11-17T15:52:25.604736",
    "id": 5,
    "name": "soap",
    "price": 2.23,
    "sid": 1,
    "sku": 5000,
    "update_time": "2020-11-17T15:52:25.604736"
}
```

#### Note

If an item is already present in a shopcart, the `POST` API will update the count of the item present in the cart. Other attributes will not be changed.

### Read

#### HTTP Request

`GET /shopcarts/:id/items/:item_id`

#### Parameters

| Name    | Type |
|---------|------|
| id      | int  |
| item_id | int  |

#### Example Request

```shell
curl -L -H 'Content-Type: application/json' \
     -X GET 'https://nyu-shopcart-service-f20.us-south.cf.appdomain.cloud/shopcarts/4/items/3'
```

#### Successful Response

```json
{
    "amount": 3,
    "create_time": "2020-11-06T20:48:07.731641",
    "id": 3,
    "name": "soap",
    "price": 2.23,
    "sid": 4,
    "sku": 5001,
    "update_time": "2020-11-06T20:48:07.731641"
}
```

### Update

#### HTTP Request

`PUT /shopcarts/:id/items/:item_id`

#### Parameters

| Name    | Type   |
|---------|--------|
| id      | int    |
| item_id | int    |
| sku     | int    |
| name    | string |
| price   | float  |
| amount  | int    |

#### Example Request

```shell
curl -L -H 'Content-Type: application/json' \
     -d '{"sku": 5000, "name": "soap", "price": 2.23, "amount": 30}' \
     -X PUT 'https://nyu-shopcart-service-f20.us-south.cf.appdomain.cloud/shopcarts/1/items/5'
```

#### Successful Response

```json
{
    "amount": 30,
    "create_time": "2020-11-06T20:48:07.731641",
    "id": 5,
    "name": "soap",
    "price": 2.23,
    "sid": 1,
    "sku": 5000,
    "update_time": "2020-11-06T20:48:07.731641"
}
```

### Delete

#### HTTP Request

`DELETE /shopcarts/:id/items/:item_id`

#### Parameters

| Name    | Type |
|---------|------|
| id      | int  |
| item_id | int  |

#### Example Request

```shell
curl -L -H 'Content-Type: application/json' \
     -X DELETE 'https://nyu-shopcart-service-f20.us-south.cf.appdomain.cloud/shopcarts/1/items/5'
```

### Query

#### HTTP Request

`GET /shopcarts/items`

#### Parameters

Please provide only one of the following parameters:

| Name    | Type   |
|---------|--------|
| sku     | int    |
| name    | string |
| price   | float  |
| amount  | int    |

#### Example Request

```shell
curl -L -H 'Content-Type: application/json' \
     -X GET 'https://nyu-shopcart-service-f20.us-south.cf.appdomain.cloud/shopcarts/items?sku=5001'
```

#### Successful Response

```json
[
    {
        "amount": 3,
        "create_time": "2020-11-06T20:48:07.731641",
        "id": 4,
        "name": "soap",
        "price": 2.23,
        "sid": 4,
        "sku": 5001,
        "update_time": "2020-11-06T20:48:07.731641"
    }
]
```
