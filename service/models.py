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
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_time = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow,
                            onupdate=datetime.utcnow)

    ##################################################
    # INSTANCE METHODS
    ##################################################

    # def __repr__(self):
    #     return "<Shopcart %r>" % (self.id)

    def create(self):
        """
        Creates a Shopcart to the database
        """
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)

    def delete(self):
        """
        Removes a Shopcart and everything in it
        """
        items = ShopcartItem.find_by_shopcartid(self.id)

        for item in items:
            item.delete()

        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Shopcart into a dictionary """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "create_time": self.create_time,
            "update_time": self.update_time
        }

    def deserialize(self, data: dict):
        """
        Deserializes a Shopcart from a dictionary
        :param data: a dictionary of attributes
        :type data: dict
        :return: a reference to self
        :rtype: Shopcart
        """
        try:
            self.user_id = int(data["user_id"])
        except KeyError as error:
            raise DataValidationError("Invalid shopcart: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid shopcart: body of request contained bad or no data"
            ) from error
        except ValueError as error:
            raise DataValidationError(
                "Invalid shopcart: missing body of request contained bad or no data"
            ) from error

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
    def find(cls, sid):
        """ Finds a shopcart based on the id provided """
        cls.logger.info("Processing lookup for shopcart id %s ...", sid)
        return cls.query.get(sid)

    @classmethod
    def find_by_user(cls, user_id: int):
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
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_time = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow,
                            onupdate=datetime.utcnow)

    ##################################################
    # INSTANCE METHODS
    ##################################################

    # def __repr__(self):
    #     return "<ShopcartItem %r>" % (self.id)

    def create(self):
        """
        Creates a ShopcartItem to the database
        """
        shopcart = Shopcart().find(self.sid)
        if shopcart is None:
            raise DataValidationError("Invalid shopcart id: shopcart doesn't exist")
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)

    def add(self):
        """
        Adds an item to shopcart database.
        If this item already exists in then it updates it in the database.
        """

        shopcart = Shopcart().find(self.sid)
        if shopcart is None:
            raise DataValidationError("Invalid shopcart id: shopcart doesn't exist")
        shopcart_item = ShopcartItem().find_by_sku_and_sid(self.sku, self.sid)
        if shopcart_item:
            self.id = shopcart_item.id
            self.amount = shopcart_item.amount + self.amount
            shopcart_item.amount = self.amount
            shopcart_item.update()
            self.create_time = shopcart_item.create_time
            self.update_time = shopcart_item.update_time
        else:
            self.id = None
            db.session.add(self)
            db.session.commit()
            db.session.refresh(self)

    def update(self):
        """
        Updates a ShopcartItem to the database
        """
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()
        db.session.refresh(self)

    def delete(self):
        """Removes a ShopcartItem from the data store"""
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Shopcart into a dictionary """
        return {
            "id": self.id,
            "sid": self.sid,
            "sku": self.sku,
            "name": self.name,
            "price": self.price,
            "amount": self.amount,
            "create_time": self.create_time,
            "update_time": self.update_time
        }

    def deserialize(self, data: dict):
        """
        Deserializes a ShopcartItem from a dictionary
        :param data: a dictionary of attributes
        :type data: dict
        :return: a reference to self
        :rtype: ShopcartItem
        """
        try:
            if "id" in data:
                self.id = int(data["id"])

            self.sid = int(data["sid"])
            self.sku = int(data["sku"])
            self.name = str(data["name"])
            self.price = float(data["price"])
            self.amount = int(data["amount"])
            if self.price < 0 or self.amount <= 0:
                raise ValueError
        except KeyError as error:
            raise DataValidationError(
                "Invalid shopcart item: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid shopcart item: body of request contained bad or no data"
            ) from error
        except ValueError as error:
            raise DataValidationError(
                "Invalid shopcart: missing body of request contained bad or no data"
            ) from error
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
    def find_by_sku(cls, sku: int):
        """ Returns all shopcart items by sku
            :param sku: the sku to find the shopcart items for
            :type sku: int

            :return: a list of shopcart items with that sku, or 404_NOT_FOUND if not found
            :rtype: list
        """
        cls.logger.info("Processing sku query for %s ...", sku)
        return cls.query.filter(cls.sku == sku).all()

    @classmethod
    def find_by_name(cls, name: str):
        """ Returns all shopcart items by product name
            :param name: the name of the product to find shopcart items for
            :type sku: string

            :return: a list of shopcart items with that product, or 404_NOT_FOUND if not found
            :rtype: list
        """
        cls.logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name).all()

    @classmethod
    def find_by_price(cls, price: float):
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
    def find_by_amount(cls, amount: int):
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
    def find_by_shopcartid(cls, sid):
        """ Finds a items in a shopcart based on the shopcart id provided """
        cls.logger.info("Processing lookup or 404 for id %s ...", sid)
        return cls.query.filter_by(sid=sid).all()

    @classmethod
    def find(cls, item_id):
        """ Finds a items in a shopcart based on the shopcart item id provided """
        cls.logger.info("Processing lookup for shopcart item id %s ...", item_id)
        return cls.query.get(item_id)

    @classmethod
    def find_by_sku_and_sid(cls, sku, sid):
        """ Finds a items in a shopcart based on the shopcart id and sku id provided """
        cls.logger.info(
            "Processing lookup for shopcart item with sku %s and sid %s", str(sku), str(sid)
        )
        return cls.query.filter_by(sid=sid).filter_by(sku=sku).first()
