# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Shopcart and ShopcartItem Models
Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from datetime import datetime
from service.models import Shopcart, ShopcartItem, DataValidationError, db
from service import app

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///../db/test.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

######################################################################
#  T E S T   C A S E S
######################################################################
class TestShopcarts(unittest.TestCase):
    """ Test Cases for Shopcarts """

    @classmethod
    def setUpClass(cls):
        """ These run once before Test suite """
        app.debug = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        """ These run once after Test suite """
        pass

    def setUp(self):
        Shopcart.init_db(app)
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_shopcart(self):
        """ Create a shopcart and assert that it exists """
        date_time = datetime.now()
        shopcart = Shopcart(user_id=101, create_time=date_time, update_time=date_time)
        self.assertTrue(shopcart != None)
        self.assertEqual(shopcart.id, None)
        self.assertEqual(shopcart.user_id, 101)
        self.assertEqual(shopcart.create_time, date_time)
        self.assertEqual(shopcart.update_time, date_time)

    def test_serialize_a_shopcart(self):
        """ Test serialization of a Shopcart """
        date_time = datetime.now()
        shopcart = Shopcart(user_id=101, create_time=date_time, update_time=date_time)
        data = shopcart.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], None)
        self.assertIn("user_id", data)
        self.assertEqual(data["user_id"], 101)
        self.assertIn("create_time", data)
        self.assertEqual(data["create_time"], date_time)
        self.assertIn("update_time", data)
        self.assertEqual(data["update_time"], date_time)

    def test_deserialize_a_shopcart(self):
        """ Test deserialization of a Shopcart """
        date_time = datetime.now()
        data = {"id": 1, "user_id": 120, "create_time": date_time, "update_time": date_time}
        shopcart = Shopcart()
        shopcart.deserialize(data)
        self.assertNotEqual(shopcart, None)
        self.assertEqual(shopcart.id, None)
        self.assertEqual(shopcart.user_id, 120)
        self.assertEqual(shopcart.create_time, date_time)
        self.assertEqual(shopcart.update_time, date_time)

    def test_deserialize__shopcart_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, data)

class TestShopcartItems(unittest.TestCase):
    """ Test Cases for ShopcartItems """

    @classmethod
    def setUpClass(cls):
        """ These run once before Test suite """
        app.debug = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        """ These run once after Test suite """
        pass

    def setUp(self):
        ShopcartItem.init_db(app)
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_shopcartitem(self):
        """ Create a ShopcartItem and assert that it exists """
        date_time = datetime.now()
        shopcartitem = ShopcartItem(sid=100, sku=5000, name="soap", price=2.23,
                                    amount=3, create_time=date_time, update_time=date_time)
        self.assertTrue(shopcartitem != None)
        self.assertEqual(shopcartitem.id, None)
        self.assertEqual(shopcartitem.sid, 100)
        self.assertEqual(shopcartitem.sku, 5000)
        self.assertEqual(shopcartitem.name, "soap")
        self.assertEqual(shopcartitem.price, 2.23)
        self.assertEqual(shopcartitem.amount, 3)
        self.assertEqual(shopcartitem.create_time, date_time)
        self.assertEqual(shopcartitem.update_time, date_time)

    def test_serialize_a_shopcartitem(self):
        """ Test serialization of a ShopcartItem """
        date_time = datetime.now()
        shopcartitem = ShopcartItem(sid=100, sku=5000, name="soap", price=2.23,
                                    amount=3, create_time=date_time, update_time=date_time)
        data = shopcartitem.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], None)
        self.assertIn("sid", data)
        self.assertEqual(data["sid"], 100)
        self.assertIn("sku", data)
        self.assertEqual(data["sku"], 5000)
        self.assertIn("name", data)
        self.assertEqual(data["name"], "soap")
        self.assertIn("price", data)
        self.assertEqual(data["price"], 2.23)
        self.assertIn("amount", data)
        self.assertEqual(data["amount"], 3)
        self.assertIn("create_time", data)
        self.assertEqual(data["create_time"], date_time)
        self.assertIn("update_time", data)
        self.assertEqual(data["update_time"], date_time)

    def test_deserialize_a_shopcartitem(self):
        """ Test deserialization of a ShopcartItem """
        date_time = datetime.now()
        data = {"id": 1, "sid":202, "sku":101, "name":"printer", "price":101.29,
                "amount":1, "create_time":date_time, "update_time":date_time}
        shopcartitem = ShopcartItem()
        shopcartitem.deserialize(data)
        self.assertNotEqual(shopcartitem, None)
        self.assertEqual(shopcartitem.id, None)
        self.assertEqual(shopcartitem.sid, 202)
        self.assertEqual(shopcartitem.sku, 101)
        self.assertEqual(shopcartitem.name, "printer")
        self.assertEqual(shopcartitem.price, 101.29)
        self.assertEqual(shopcartitem.amount, 1)
        self.assertEqual(shopcartitem.create_time, date_time)
        self.assertEqual(shopcartitem.update_time, date_time)

    def test_deserialize_shopcaritem_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        shopcartitem = ShopcartItem()
        self.assertRaises(DataValidationError, shopcartitem.deserialize, data)


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    unittest.main()
