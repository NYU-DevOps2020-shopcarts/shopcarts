# shopcarts

![](https://travis-ci.org/NYU-DevOps2020-shopcarts/shopcarts.svg?branch=master)

The shopcarts resource allows customers to make a collection of products that they want to purchase

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
