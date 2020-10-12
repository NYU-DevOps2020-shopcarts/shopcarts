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
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)

    ##################################################
    # INSTANCE METHODS
    ##################################################

    def serialize(self):
        """ Serializes a Shopcart into a dictionary """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "create_time": self.create_time,
            "update_time": self.update_time,
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
            self.id = data["id"]
            self.user_id = data["user_id"]
            self.create_time = data["create_time"]
            self.update_time = data["update_time"]
        except KeyError as error:
            raise DataValidationError("Invalid shopcart: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid shopcart: body of request contained bad or no data"
            )
        return self

class ShopcartItem(db.Model):
    """
    Class that represents a ShopcartItem
    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """

    logger = logging.getLogger(__name__)
    app = None

    ##################################################
    # Shopcart Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.Integer)
    sku = db.Column(db.Integer)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    amount = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)

    ##################################################
    # INSTANCE METHODS
    ##################################################

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
            "update_time": self.update_time,
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
            self.id = data["id"]
            self.sid = data["sid"]
            self.sku = data["sku"]
            self.name = data["name"]
            self.price = data["price"]
            self.amount = data["amount"]
            self.create_time = data["create_time"]
            self.update_time = data["update_time"]
        except KeyError as error:
            raise DataValidationError("Invalid shopcart item: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid shopcart item: body of request contained bad or no data"
            )
        return self



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
