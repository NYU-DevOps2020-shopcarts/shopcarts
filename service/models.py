# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Models for Shopcarts
All of the models are stored in this module
Models
------
Shopcart -
Attributes:
-----------
id (int) - shop cart id
user_id (int) - user id
create_time (DateTime) - the time this shopcart was created
update_time (DateTime) - the time this shopcart was updated
ShopcartItem - Contains product information for an item in a shopcart
Attributes:
-----------
id (int) - for index purpose
sid (int) - shop cart id
sku (int) - product id
name (string) - product name
price (float) - price for one
amount (int) - number of product
create_time (DateTime) - the time this product was created
update_time (DateTime) - the time this product was updated
"""

import logging
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass

class Shopcart(db.Model):
    """
    Class that represents a Shopcart
    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """

    logger = logging.getLogger(__name__)
    app = None

    ##################################################
    # Shopcart Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)

    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return "<Shopcart %r>" % (self.id)

    def create(self):
        """
        Creates a Shopcart to the database
        """
        date_time = datetime.now()
        self.id = None  # id must be none to generate next primary key
        #if time fields not set, use current time
        self.create_time = date_time
        self.update_time = date_time
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Shopcart into a dictionary """
        #ensure the (optional) time fields are strings
        if isinstance(self.create_time, datetime):
            create_time = datetime.isoformat(self.create_time)
        else:
            create_time = self.create_time

        if isinstance(self.update_time, datetime):
            update_time = datetime.isoformat(self.update_time)
        else:
            update_time = self.update_time

        return {
            "id": self.id,
            "user_id": self.user_id,
            "create_time": create_time,
            "update_time": update_time,
        }

    def deserialize(self, data: dict):
        """
        Deserializes a Shopcart from a dictionary
        :param data: a dictionary of attributes
        :type data: dict
        :return: a reference to self
        :rtype: Shopcart
        """
        #ensure the (optional) time fields are datetime objs
        try:
            if "create_time" in data and "update_time" in data:
                if isinstance(data["create_time"], str):
                    data_create_time = datetime.strptime(data["create_time"],
                                                              '%Y-%m-%dT%H:%M:%S.%f')
                else:
                    data_create_time = data["create_time"]

                if isinstance(data["update_time"], str):
                    data_update_time = datetime.strptime(data["update_time"],
                                                              '%Y-%m-%dT%H:%M:%S.%f')
                else:
                    data_update_time = data["update_time"]
                self.create_time = data_create_time
                self.update_time = data_update_time
            else:
                self.create_time = None
                self.update_time = None

            if "id" in data:
                self.id = data["id"]

            self.user_id = data["user_id"]
        except KeyError as error:
            raise DataValidationError("Invalid shopcart: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid shopcart: body of request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database session
        :param app: the Flask app
        :type data: Flask
        """
        cls.logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Shopcarts in the database """
        cls.logger.info("Processing all Shopcarts")
        return cls.query.all()

    @classmethod
    def find(cls, id):
        """ Finds a shopcart based on the id provided """
        cls.logger.info("Processing lookup for shopcart id %s ...", id)
        return cls.query.get(id)

    @classmethod
    def find_by_user(cls, user_id : int):
        """ Returns shopcart for a user
            :param user_id: the id of the user to find the shopcart for
            :type user_id: int

            :return: a shopcart with that user id, or 404_NOT_FOUND if not found
            :rtype: Shopcart
        """
        cls.logger.info("Processing user id query for %s ...", user_id)
        return cls.query.filter(cls.user_id == user_id)


class ShopcartItem(db.Model):
    """
    Class that represents a ShopcartItem
    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """

    logger = logging.getLogger(__name__)
    app = None

    ##################################################
    # ShopcartItems Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.Integer)
    sku = db.Column(db.Integer)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    amount = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, server_default=func.now())
    update_time = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return "<ShopcartItem %r>" % (self.id)

    def create(self):
        """
        Creates a ShopcartItem to the database
        """
        shopcart = Shopcart().find(self.sid)
        if shopcart is None:
            raise DataValidationError("Invalid shopcart id: shopcart doesn't exist")
        date_time = datetime.now()
        self.id = None  # id must be none to generate next primary key
        self.create_time = date_time
        self.update_time = date_time
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a ShopcartItem to the database
        """
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def serialize(self):
        """ Serializes a Shopcart into a dictionary """
        #ensure the (optional) time fields are strings
        if isinstance(self.create_time, datetime):
            create_time = datetime.isoformat(self.create_time)
        else:
            create_time = self.create_time

        if isinstance(self.update_time, datetime):
            update_time = datetime.isoformat(self.update_time)
        else:
            update_time = self.update_time

        return {
            "id": self.id,
            "sid": self.sid,
            "sku": self.sku,
            "name": self.name,
            "price": self.price,
            "amount": self.amount,
            "create_time": create_time,
            "update_time": update_time,
        }

    def deserialize(self, data: dict):
        """
        Deserializes a ShopcartItem from a dictionary
        :param data: a dictionary of attributes
        :type data: dict
        :return: a reference to self
        :rtype: ShopcartItem
        """
        #ensure the (optional) time fields are datetime objs
        try:
            if "create_time" in data and "update_time" in data:
                if isinstance(data["create_time"], str):
                    data_create_time = datetime.strptime(data["create_time"],
                                                              '%Y-%m-%dT%H:%M:%S.%f')
                else:
                    data_create_time = data["create_time"]

                if isinstance(data["update_time"], str):
                    data_update_time = datetime.strptime(data["update_time"],
                                                              '%Y-%m-%dT%H:%M:%S.%f')
                else:
                    data_update_time = data["update_time"]
                self.create_time = data_create_time
                self.update_time = data_update_time
            else:
                self.create_time = None
                self.update_time = None

            if "id" in data:
                self.id = data["id"]

            self.sid = data["sid"]
            self.sku = data["sku"]
            self.name = data["name"]
            self.price = data["price"]
            self.amount = data["amount"]
        except KeyError as error:
            raise DataValidationError("Invalid shopcart item: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid shopcart item: body of request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database session
        :param app: the Flask app
        :type data: Flask
        """
        cls.logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Shopcart Items in the database """
        cls.logger.info("Processing all Shopcart Items")
        return cls.query.all()

    @classmethod
    def find_by_sku(cls, sku : int):
        """ Returns all shopcart items by sku
            :param sku: the sku to find the shopcart items for
            :type sku: int

            :return: a list of shopcart items with that sku, or 404_NOT_FOUND if not found
            :rtype: list
        """
        cls.logger.info("Processing sku query for %s ...", sku)
        return cls.query.filter(cls.sku == sku).all()

    @classmethod
    def find_by_name(cls, name : str):
        """ Returns all shopcart items by product name
            :param name: the name of the product to find shopcart items for
            :type sku: string

            :return: a list of shopcart items with that product, or 404_NOT_FOUND if not found
            :rtype: list
        """
        cls.logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name).all()

    @classmethod
    def find_by_price(cls, price : float):
        """ Returns all shopcart items by product price
            :param sku: the price to find the shopcart items for
            :type sku: float

            :return: a list of shopcart items with that products with that price,
            or 404_NOT_FOUND if not found
            :rtype: list
        """
        cls.logger.info("Processing price query for %s ...", price)
        return cls.query.filter(cls.price == price).all()

    @classmethod
    def find_by_amount(cls, amount : int):
        """ Returns all shopcart items by amount of a product
            :param sku: the amount to find the shopcart items for
            :type sku: int

            :return: a list of shopcart items with that product amount,
            or 404_NOT_FOUND if not found
            :rtype: list
        """
        cls.logger.info("Processing sku amount for %s ...", amount)
        return cls.query.filter(cls.amount == amount).all()

    @classmethod
    def find_by_shopcartid(cls, id):
        """ Finds a items in a shopcart based on the shopcart id provided """
        cls.logger.info("Processing lookup or 404 for id %s ...", id)
        return cls.query.filter_by(sid = id).all()

    @classmethod
    def find(cls, id):
        """ Finds a items in a shopcart based on the shopcart id provided """
        cls.logger.info("Processing lookup for shopcart id %s ...", id)
        return cls.query.get(id)
