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
from service.models import Shopcart, ShopcartItem, DataValidationError, db
from service import app
from config import DATABASE_URI


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
        Shopcart.init_db(app)

    def setUp(self):
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # def test_repr(self):
    #     shopcart = Shopcart(id = 1).__repr__
    #     #val = shopcart.__repr__
    #     self.assertEqual(shopcart,"<Shopcart %r>" % (1))

    def test_create_a_shopcart(self):
        """ Create a shopcart and assert that it exists """
        shopcart = Shopcart(user_id=101)
        self.assertTrue(shopcart is not None)
        self.assertEqual(shopcart.id, None)
        self.assertEqual(shopcart.user_id, 101)

    def test_add_a_shopcart(self):
        """ Create a shopcart and add it to database """
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = Shopcart(user_id=12345)
        self.assertTrue(shopcart is not None)
        self.assertEqual(shopcart.id, None)
        shopcart.create()
        self.assertEqual(shopcart.id, 1)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

    def test_delete_a_shopcart(self):
        """Delete a shopcart and everything in it"""
        self.assertEqual(len(Shopcart.all()), 0)

        shopcart = Shopcart(user_id=12345)
        shopcart.create()

        self.assertEqual(shopcart.id, 1)
        self.assertEqual(len(Shopcart.all()), 1)

        self.assertEqual(len(ShopcartItem.all()), 0)

        shopcart_item = ShopcartItem(sid=1, sku=5000, name="soap", price=2.23, amount=3)
        shopcart_item.create()
        self.assertEqual(shopcart_item.id, 1)

        shopcart_item = ShopcartItem(sid=1, sku=5001, name="shampoo", price=3.77, amount=1)
        shopcart_item.create()
        self.assertEqual(shopcart_item.id, 2)

        self.assertEqual(len(ShopcartItem.all()), 2)

        shopcart.delete()
        self.assertEqual(len(ShopcartItem.all()), 0)
        self.assertEqual(len(Shopcart.all()), 0)

    def test_serialize_a_shopcart(self):
        """ Test serialization of a Shopcart """
        shopcart = Shopcart(user_id=101)
        data = shopcart.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], None)
        self.assertIn("user_id", data)
        self.assertEqual(data["user_id"], 101)

    def test_deserialize_a_shopcart(self):
        """ Test deserialization of a Shopcart """
        data = {"user_id": 120}
        shopcart = Shopcart()
        shopcart.deserialize(data)
        self.assertNotEqual(shopcart, None)
        self.assertEqual(shopcart.user_id, 120)

    def test_deserialize_shopcart_bad_data(self):
        """ Test deserialization of bad data for a Shopcart """
        data = "this is not a dictionary"
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, data)

    def test_deserialize_shopcart_key_error(self):
        """ Test deserialization of key error for a Shopcart """
        data = {"id": 100}
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, data)

    def test_deserialize_shopcart_value_error(self):
        """ Test deserialization of value error for a Shopcart """
        data = {"user_id": "100d"}
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, data)

    def test_find_shopcart(self):
        """ Find a Shopcart by id """
        data = {"id": 1, "user_id": 120,}
        Shopcart(id=1, user_id=120).create()
        shopcart_queried = Shopcart.find(1)
        self.assertEqual(data["id"], shopcart_queried.id)
        self.assertEqual(data["user_id"], shopcart_queried.user_id)

    def test_find_shopcart_with_non_existing_shopcart(self):
        """ Find a Shopcart that doesn't exist """
        shopcart_queried = Shopcart.find(1)
        self.assertIsNone(shopcart_queried)

    def test_all_shopcarts(self):
        """ Get all Shopcarts"""
        count = 5
        for i in range(1, count + 1):
            Shopcart(id=i, user_id=(i + 1)).create()
        shopcarts_queried = Shopcart.all()
        self.assertEqual(len(shopcarts_queried), count)

    def test_find_by_user(self):
        """ Find a Shopcart by user """
        Shopcart(user_id=101).create()
        Shopcart(user_id=201).create()
        shopcarts = Shopcart.find_by_user(101)
        self.assertEqual(shopcarts[0].user_id, 101)


class TestShopcartItems(unittest.TestCase):
    """ Test Cases for ShopcartItems """

    @classmethod
    def setUpClass(cls):
        """ These run once before Test suite """
        app.debug = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        ShopcartItem.init_db(app)

    def setUp(self):
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_shopcart_item(self):
        """ Create a ShopcartItem and assert that it exists """
        shopcart_item = ShopcartItem(sid=100, sku=5000, name="soap", price=2.23,
                                     amount=3)
        self.assertTrue(shopcart_item is not None)
        self.assertEqual(shopcart_item.id, None)
        self.assertEqual(shopcart_item.sid, 100)
        self.assertEqual(shopcart_item.sku, 5000)
        self.assertEqual(shopcart_item.name, "soap")
        self.assertEqual(shopcart_item.price, 2.23)
        self.assertEqual(shopcart_item.amount, 3)

    def test_add_a_shopcart_item(self):
        """ Create a shopcart item and add it to the database """
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = Shopcart(user_id=12345)
        self.assertTrue(shopcart is not None)
        self.assertEqual(shopcart.id, None)
        shopcart.create()
        self.assertEqual(shopcart.id, 1)
        shopcart_item = ShopcartItem(sid=100, sku=5000, name="soap", price=2.23,
                                     amount=3)
        self.assertRaises(DataValidationError, shopcart_item.create)
        shopcart_item = ShopcartItem(sid=1, sku=5000, name="soap", price=2.23,
                                     amount=3)
        self.assertTrue(shopcart_item is not None)
        self.assertEqual(shopcart_item.id, None)
        self.assertEqual(shopcart_item.sid, 1)
        self.assertEqual(shopcart_item.sku, 5000)
        self.assertEqual(shopcart_item.name, "soap")
        self.assertEqual(shopcart_item.price, 2.23)
        self.assertEqual(shopcart_item.amount, 3)

    def test_shopcart_item_creation_using_add(self):
        """ Create a shopcart item and add it to the database using add method"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = Shopcart(user_id=12345)
        self.assertTrue(shopcart is not None)
        self.assertEqual(shopcart.id, None)
        shopcart.create()
        self.assertEqual(shopcart.id, 1)
        shopcart_item = ShopcartItem(sid=shopcart.id, sku=5000, name="soap", price=2.23,
                                     amount=3)
        shopcart_item.add()
        self.assertTrue(shopcart_item is not None)
        self.assertEqual(shopcart_item.sid, 1)
        self.assertEqual(shopcart_item.sku, 5000)
        self.assertEqual(shopcart_item.name, "soap")
        self.assertEqual(shopcart_item.price, 2.23)
        self.assertEqual(shopcart_item.amount, 3)

    def test_shopcart_item_updation_using_add(self):
        """ Create a shopcart item and update it in the database using add method"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = Shopcart(user_id=12345)
        self.assertTrue(shopcart is not None)
        self.assertEqual(shopcart.id, None)
        shopcart.create()
        self.assertEqual(shopcart.id, 1)
        shopcart_item = ShopcartItem(sid=shopcart.id, sku=5000, name="soap", price=2.23,
                                     amount=3)
        shopcart_item.add()
        self.assertEqual(shopcart_item.sid, 1)
        shopcart_item = ShopcartItem(sid=shopcart.id, sku=5000, name="soap", price=2.23,
                                     amount=3)
        shopcart_item.add()
        self.assertTrue(shopcart_item is not None)
        self.assertEqual(shopcart_item.sid, shopcart.id)
        self.assertEqual(shopcart_item.sku, 5000)
        self.assertEqual(shopcart_item.name, "soap")
        self.assertEqual(shopcart_item.price, 2.23)
        self.assertEqual(shopcart_item.amount, 6)

    def test_add_shopcart_item_with_not_existing_cart(self):
        """ Test using add shopcart_item method when shopcart doesnt exists"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = Shopcart(user_id=12345)
        self.assertTrue(shopcart is not None)
        self.assertEqual(shopcart.id, None)
        shopcart.create()
        self.assertEqual(shopcart.id, 1)
        shopcart_item = ShopcartItem(sid=1000, sku=5000, name="soap", price=2.23,
                                     amount=3)

        self.assertRaises(DataValidationError, shopcart_item.add)

    def test_update_a_shopcart_item(self):
        """ Update a shopcart item """
        shopcart = Shopcart(user_id=12345)
        shopcart.create()

        shopcart_item = ShopcartItem(sid=shopcart.id, sku=5000, name="soap", price=2.23,
                                     amount=3)
        shopcart_item.create()
        self.assertEqual(shopcart_item.id, 1)
        # Change it an update it
        shopcart_item.name = "soap"
        shopcart_item.update()
        self.assertEqual(shopcart_item.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        shopcart_item = ShopcartItem.all()
        self.assertEqual(len(shopcart_item), 1)
        self.assertEqual(shopcart_item[0].name, "soap")

    def test_update_a_shopcart_item_without_id(self):
        """ Update a shopcart item """
        shopcart = Shopcart(user_id=12345)
        shopcart.create()

        shopcart_item = ShopcartItem(sid=shopcart.id, sku=5000, name="soap", price=2.23,
                                     amount=3)
        shopcart_item.create()
        # Change it an update it
        shopcart_item.id = None
        self.assertRaises(DataValidationError, shopcart_item.update)

    def test_delete_a_shopcart_item(self):
        """Delete a shopcart item"""
        shopcart = Shopcart(user_id=12345)
        shopcart.create()
        self.assertEqual(shopcart.id, 1)

        self.assertEqual(len(ShopcartItem.all()), 0)
        shopcart_item = ShopcartItem(sid=1, sku=5000, name="soap", price=2.23, amount=3)
        shopcart_item.create()
        self.assertEqual(shopcart_item.id, 1)
        self.assertEqual(len(ShopcartItem.all()), 1)

        shopcart_item.delete()
        self.assertEqual(len(ShopcartItem.all()), 0)

    def test_serialize_a_shopcart_item(self):
        """ Test serialization of a ShopcartItem """
        shopcart_item = ShopcartItem(sid=100, sku=5000, name="soap", price=2.23,
                                     amount=3)
        data = shopcart_item.serialize()
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

    def test_deserialize_a_shopcart_item(self):
        """ Test deserialization of a ShopcartItem """
        data = {"id": 1, "sid": 202, "sku": 101, "name": "printer", "price": 101.29,
                "amount": 1}
        shopcart_item = ShopcartItem()
        shopcart_item.deserialize(data)
        self.assertNotEqual(shopcart_item, None)
        self.assertEqual(shopcart_item.id, 1)
        self.assertEqual(shopcart_item.sid, 202)
        self.assertEqual(shopcart_item.sku, 101)
        self.assertEqual(shopcart_item.name, "printer")
        self.assertEqual(shopcart_item.price, 101.29)
        self.assertEqual(shopcart_item.amount, 1)

    def test_deserialize_shopcart_item_bad_data(self):
        """ Test deserialization of bad data for a ShopcartItem """
        data = "this is not a dictionary"
        shopcart_item = ShopcartItem()
        self.assertRaises(DataValidationError, shopcart_item.deserialize, data)

    def test_deserialize_shopcart_item_key_error(self):
        """ Test deserialization of bad data with key error for a ShopcartItem """
        data = {"id": 1}
        shopcart_item = ShopcartItem()
        self.assertRaises(DataValidationError, shopcart_item.deserialize, data)

    def test_deserialize_shopcart_item_value_error(self):
        """ Test deserialization of bad data with value error for a ShopcartItem """
        data = {"sid": 123, "sku": 13435, "price": 2.2, "name": "test item", "amount": 0}
        shopcart_item = ShopcartItem()
        self.assertRaises(DataValidationError, shopcart_item.deserialize, data)

    def test_find_by_sku(self):
        """ Find Shopcart Items by sku """
        shopcart_1 = Shopcart().deserialize({"user_id": 12345})
        shopcart_1.create()
        shopcart_2 = Shopcart().deserialize({"user_id": 12345})
        shopcart_2.create()
        ShopcartItem(sid=shopcart_1.id, sku=101, name="printer", price=101.29, amount=1).create()
        ShopcartItem(sid=shopcart_2.id, sku=101, name="printer", price=101.29, amount=10).create()
        ShopcartItem(sid=shopcart_1.id, sku=201, name="printer", price=101.29, amount=1).create()
        shopcart_items = ShopcartItem.find_by_sku(101)
        self.assertEqual(len(shopcart_items), 2)
        self.assertEqual(shopcart_items[0].sku, 101)

    def test_find_by_name(self):
        """ Find Shopcart Items by name """
        shopcart = Shopcart().deserialize({"user_id": 12345})
        shopcart.create()
        ShopcartItem(sid=shopcart.id, sku=101, name="printer", price=101.29, amount=1).create()
        ShopcartItem(sid=shopcart.id, sku=201, name="laptop", price=101.29, amount=1).create()
        shopcart_items = ShopcartItem.find_by_name("printer")
        self.assertEqual(len(shopcart_items), 1)
        self.assertEqual(shopcart_items[0].name, "printer")

    def test_find_by_price(self):
        """ Find Shopcart Items by price """
        shopcart = Shopcart().deserialize({"user_id": 12345})
        shopcart.create()
        ShopcartItem(sid=shopcart.id, sku=101, name="printer", price=101.29, amount=1).create()
        ShopcartItem(sid=shopcart.id, sku=201, name="printer", price=99.99, amount=1).create()
        shopcart_items = ShopcartItem.find_by_price(99.99)
        self.assertEqual(len(shopcart_items), 1)
        self.assertEqual(shopcart_items[0].price, 99.99)

    def test_find_by_amount(self):
        """ Find Shopcart Items by amount """
        shopcart = Shopcart().deserialize({"user_id": 12345})
        shopcart.create()
        ShopcartItem(sid=shopcart.id, sku=101, name="printer", price=101.29, amount=1).create()
        ShopcartItem(sid=shopcart.id, sku=201, name="printer", price=101.29, amount=10).create()
        shopcart_items = ShopcartItem.find_by_amount(10)
        self.assertEqual(len(shopcart_items), 1)
        self.assertEqual(shopcart_items[0].amount, 10)

    def test_find_by_shopcart_id(self):
        """ Find Shopcart Items by Shopcart id for Shopcart with single item """
        shopcart = Shopcart().deserialize({"user_id": 12345})
        shopcart.create()
        data = {"id": 1, "sid": shopcart.id, "sku": 150,
                "name": "test obj1", "price": 100, "amount": 1}
        ShopcartItem(id=data["id"], sid=data["sid"], sku=data["sku"], name=data["name"],
                     price=data["price"], amount=data["amount"]).create()
        item_queried = ShopcartItem.find_by_shopcartid(data["sid"])[0]
        self.assertEqual(item_queried.id, data["id"])
        self.assertEqual(item_queried.sid, data["sid"])
        self.assertEqual(item_queried.sku, data["sku"])
        self.assertEqual(item_queried.name, data["name"])
        self.assertEqual(item_queried.price, data["price"])
        self.assertEqual(item_queried.amount, data["amount"])

    def test_find_by_shopcart_id_multiple(self):
        """ Find Shopcart Items by Shopcart id for Shopcart with multiple items """
        shopcart = Shopcart().deserialize({"user_id": 12345})
        shopcart.create()
        ShopcartItem(id=1, sid=shopcart.id, sku=3, name="obj 1", price=4, amount=5).create()
        ShopcartItem(id=6, sid=shopcart.id, sku=7, name="obj 2", price=8, amount=9).create()
        items_queried = ShopcartItem.find_by_shopcartid(shopcart.id)
        self.assertEqual(len(items_queried), 2)

    def test_find_by_shopcart_id_with_no_items(self):
        """ Find Shopcart Items by empty Shopcart """
        item_queried = ShopcartItem.find_by_shopcartid(10)
        self.assertEqual(len(item_queried), 0)

    def test_find_by_sku_and_sid(self):
        """ Find Shopcart Items by shopcart id and sku id  """
        shopcart_1 = Shopcart().deserialize({"user_id": 12345})
        shopcart_1.create()
        shopcart_2 = Shopcart().deserialize({"user_id": 1235})
        shopcart_2.create()
        sku = 3
        ShopcartItem(id=1, sid=shopcart_1.id, sku=sku, name="obj 1", price=8, amount=5).create()
        ShopcartItem(id=6, sid=shopcart_2.id, sku=sku, name="obj 1", price=8, amount=9).create()
        item_queried = ShopcartItem.find_by_sku_and_sid(sku, shopcart_1.id)
        self.assertEqual(item_queried.amount, 5)


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    unittest.main()
