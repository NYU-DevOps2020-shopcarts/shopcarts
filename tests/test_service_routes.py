######################################################################
#
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
######################################################################

"""
Shopcart API Service Test Suite

Test cases can be run with the following:
nosetests -v --with-spec --spec-color
nosetests --stop tests/test_service.py:TestPetServer
"""
import os
import unittest
from unittest import TestCase
from unittest.mock import patch
from flask_api import status  # HTTP Status Codes
from shopcart_factory import ShopcartFactory, ShopcartItemFactory
from service.models import Shopcart, ShopcartItem, DataValidationError, db
from service import routes
from service import app, constants
from config import DATABASE_URI


######################################################################
#  T E S T   C A S E S
######################################################################
class TestShopcartServer(TestCase):
    """ Shopcart Service tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.debug = False
        app.testing = True
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        """ Run once after all tests """
        pass

    def setUp(self):
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = routes.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        """ Test the index page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn(b'ShopCart Demo RESTful API Service', resp.data)

    def test_healthcheck(self):
        """ Healthcheck Test """
        resp = self.app.get('/healthcheck')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn(b'Healthy', resp.data)

######################################################################
#  S H O P C A R T   T E S T   C A S E S
######################################################################

    def _create_shopcarts(self, count):
        """ Factory method to create shopcarts in bulk """
        shopcarts = []
        ids = []
        while len(ids) < count:
            test_shopcart = ShopcartFactory()
            resp = self.app.post(
                "/shopcarts", json=test_shopcart.serialize(), content_type="application/json"
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test shopcart"
            )
            new_shopcart = resp.get_json()
            test_shopcart.id = new_shopcart["id"]
            if test_shopcart.id not in ids:
                ids.append(test_shopcart.id)
                shopcarts.append(test_shopcart)
        return shopcarts

    def test_create_shopcart(self):
        """ Create a new Shopcart """
        test_shopcart = ShopcartFactory()
        resp = self.app.post(
            "/shopcarts", json=test_shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertTrue(location is not None)
        # Check the data is correct
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["user_id"], test_shopcart.user_id, "User ids do not match")
        # times set by db
        self.assertIsNotNone(new_shopcart["create_time"],
                             "Creation time not set")
        self.assertIsNotNone(new_shopcart["update_time"],
                             "Update time not set")

        # Check that the location header was correct
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["user_id"], test_shopcart.user_id, "User ids do not match")
        # times set by db
        self.assertIsNotNone(
            new_shopcart["create_time"], "Creation time not set"
        )
        self.assertIsNotNone(
            new_shopcart["update_time"], "Update time not set"
        )

    def test_create_duplicated_shopcart(self):
        """ Create Duplicated Shopcart """
        test_shopcart = ShopcartFactory()

        # 1st shopcart
        resp = self.app.post(
            "/shopcarts", json={'user_id': test_shopcart.user_id}, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        new_shopcart = resp.get_json()

        # duplicated shopcart
        resp = self.app.post(
            "/shopcarts", json={'user_id': test_shopcart.user_id}, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        duplicated_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["id"], duplicated_shopcart["id"])

    def test_create_shopcart_with_pure_json(self):
        """ Create a new Shopcart with pure JSON """
        test_shopcart = ShopcartFactory()
        resp = self.app.post(
            "/shopcarts", json={"user_id": test_shopcart.user_id}, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertTrue(location is not None)
        # Check the data is correct
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["user_id"], test_shopcart.user_id, "User ids do not match")
        # times set by db
        self.assertIsNotNone(new_shopcart["create_time"],
                             "Creation time not set")
        self.assertIsNotNone(new_shopcart["update_time"],
                             "Update time not set")

        # Check that the location header was correct
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["user_id"], test_shopcart.user_id, "User ids do not match")
        # times set by db
        self.assertIsNotNone(
            new_shopcart["create_time"], "Creation time not set"
        )
        self.assertIsNotNone(
            new_shopcart["update_time"], "Update time not set"
        )

    def test_non_existing_shopcart(self):
        """ Find a Shopcart by id that doesn't exist """
        shopcart_id = 1
        response = self.app.get("/shopcarts/" + str(shopcart_id), content_type="application/json")
        resp = response.get_json()
        self.assertEqual(resp["status"], status.HTTP_404_NOT_FOUND)
        self.assertEqual(resp["error"], constants.NOT_FOUND)

    def test_get_shopcart_with_zero_items(self):
        """ Find a Shopcart by id that has no items """
        shopcart_id = 1
        test_shopcart = ShopcartFactory()
        create_resp = self.app.post(
            "/shopcarts", json={"id": shopcart_id, "user_id": test_shopcart.user_id},
            content_type="application/json"
        )
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        shopcart_resp = self.app.get("/shopcarts/" + str(shopcart_id), content_type="application/json")
        resp = shopcart_resp.get_json()
        self.assertEqual(shopcart_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp["id"], shopcart_id)
        self.assertEqual(resp["user_id"], test_shopcart.user_id)
        self.assertEqual(len(resp["items"]), 0)
        self.assertIsNotNone(
            resp["create_time"], "Creation time not set"
        )
        self.assertIsNotNone(
            resp["update_time"], "Update time not set"
        )

    def is_shopcart_item_same(self, shopcart_item1, shopcart_item2):
        """ Compare if Shopcart Items are identical """
        if (shopcart_item1["id"] == shopcart_item2["id"]
                and shopcart_item1["price"] == shopcart_item2["price"]
                and shopcart_item1["amount"] == shopcart_item2["amount"]
                and shopcart_item1["sku"] == shopcart_item2["sku"]):
            return True

        return False

    def test_get_shopcart_with_items(self):
        """ Find a Shopcart by id that has multiple items"""
        test_shopcart = ShopcartFactory()
        resp = self.app.post("/shopcarts", json={"user_id": test_shopcart.user_id},
                             content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        count = 5
        shopcart_id = resp.json["id"]
        shopcart_items = self._create_shopcart_items(count, shopcart_id)
        get_items_response = self.app.get("/shopcarts/" + str(shopcart_id), content_type="application/json")
        self.assertEqual(get_items_response.status_code, status.HTTP_200_OK)
        response = get_items_response.get_json()
        self.assertEqual(response["id"], shopcart_id)
        self.assertEqual(response["user_id"], test_shopcart.user_id)
        self.assertEqual(len(response["items"]), len(shopcart_items))
        self.assertIsNotNone(
            response["create_time"], "Creation time not set"
        )
        self.assertIsNotNone(
            response["update_time"], "Update time not set"
        )
        for itr in range(len(shopcart_items)):
            self.assertTrue(self.is_shopcart_item_same(shopcart_items[itr].serialize(),
                                                       response["items"][itr]))

    def test_get_shopcart_list(self):
        """ Get a list of Shopcarts """
        shopcarts = self._create_shopcarts(5)
        shopcart_ids = set([shopcart.id for shopcart in shopcarts])
        resp = self.app.get("/shopcarts", content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(shopcart_ids))

    def test_query_shopcart_list_by_user(self):
        """ Query shopcart list by User """
        shopcarts = self._create_shopcarts(10)

        for shopcart in shopcarts:
            resp = self.app.get("/shopcarts", query_string="user_id={}".format(shopcart.user_id),
                                content_type="application/json")
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            data = resp.get_json()
            self.assertEqual(shopcart.id, data['id'])

    def test_query_shopcart_list_by_unknown_user(self):
        """ Query shopcart list by Unknown User """
        resp = self.app.get("/shopcarts", query_string="user_id={}".format(1234567890),
                            content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_shopcart(self):
        """Delete a Shopcart and everything in it"""
        self.assertEqual(len(Shopcart.all()), 0)

        shopcart = self._create_shopcarts(1)[0]

        self.assertEqual(len(Shopcart.all()), 1)
        self.assertEqual(len(ShopcartItem.all()), 0)

        self._create_shopcart_items(5, shopcart.id)

        self.assertEqual(len(ShopcartItem.all()), 5)

        resp = self.app.delete(
            "/shopcarts/{}".format(shopcart.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)

        self.assertEqual(len(Shopcart.all()), 0)
        self.assertEqual(len(ShopcartItem.all()), 0)

    def test_place_order(self):
        """ Test sending shopcart order """
        test_shopcart = ShopcartFactory()
        resp = self.app.post("/shopcarts", json={"user_id": test_shopcart.user_id},
                             content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        shopcart_id = resp.json["id"]
        shopcart_items = self._create_shopcart_items(10, shopcart_id)
        test_sku = shopcart_items[0].sku
        sku_shopcart_items = [shopcart_item for shopcart_item in shopcart_items
                              if shopcart_item.sku == test_sku]
        resp = self.app.get("/shopcarts/items", query_string="sku={}".format(test_sku), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(sku_shopcart_items))

        resp = self.app.put(
            "/shopcarts/{}/place-order".format(shopcart_id),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        self.assertEqual(len(Shopcart.all()), 0)
        self.assertEqual(len(ShopcartItem.all()), 0)

    def test_place_order_invalid_shopcart(self):
        test_shopcart = Shopcart()
        test_shopcart.id = 1
        resp = self.app.put(
            "/shopcarts/{}/place-order".format(test_shopcart.id),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_place_order_empty_shopcart(self):
        test_shopcart = ShopcartFactory()
        resp = self.app.post("/shopcarts", json={"user_id": test_shopcart.user_id},
                             content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        shopcart_id = resp.json["id"]

        resp = self.app.put(
            "/shopcarts/{}/place-order".format(shopcart_id),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

######################################################################
#  S H O P C A R T I T E M   T E S T   C A S E S
######################################################################

    def _create_shopcart_items(self, count, sid=None):
        """ Factory method to create shopcart_items in bulk """
        shopcart_items = []
        items = []
        while len(shopcart_items) < count:

            test_shopcart_item = ShopcartItemFactory()
            if test_shopcart_item.sku not in items:
                items.append(test_shopcart_item.sku)
                if sid is not None:
                    test_shopcart_item.sid = sid

                resp = self.app.post(
                    "/shopcarts/{}/items".format(sid), json=test_shopcart_item.serialize(),
                    content_type="application/json"
                )
                self.assertEqual(
                    resp.status_code, status.HTTP_201_CREATED, "Could not create test shopcart item"
                )
                new_shopcart_item = resp.get_json()
                test_shopcart_item.id = new_shopcart_item["id"]
                shopcart_items.append(test_shopcart_item)
        return shopcart_items

    def test_create_shopcart_item(self):
        """ Create a new ShopcartItem """
        test_shopcart = ShopcartFactory()
        resp = self.app.post("/shopcarts", json=test_shopcart.serialize(),
                             content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        test_shopcart_item = ShopcartItemFactory()
        test_shopcart_item.sid = resp.json["id"]
        resp = self.app.post(
            "/shopcarts/{}/items".format(test_shopcart_item.sid),
            json=test_shopcart_item.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertTrue(location is not None)
        # Check the data is correct
        new_shopcart_item = resp.get_json()
        self.assertEqual(new_shopcart_item["sid"],
                         test_shopcart_item.sid, "Shopcart ids do not match")
        self.assertEqual(
            new_shopcart_item["sku"], test_shopcart_item.sku, "SKUs do not match"
        )
        self.assertEqual(
            new_shopcart_item["name"], test_shopcart_item.name, "Product names do not match"
        )
        self.assertEqual(
            new_shopcart_item["price"], test_shopcart_item.price, "Prices do not match"
        )
        self.assertEqual(
            new_shopcart_item["amount"], test_shopcart_item.amount, "Amounts do not match"
        )
        # times set by db
        self.assertIsNotNone(
            new_shopcart_item["create_time"], "Creation time not set"
        )
        self.assertIsNotNone(
            new_shopcart_item["update_time"], "Update time not set"
        )

        # Check that the location header was correct
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_shopcart_item = resp.get_json()
        self.assertEqual(new_shopcart_item["sid"], test_shopcart_item.sid,
                         "Shopcart ids do not match")
        self.assertEqual(
            new_shopcart_item["sku"], test_shopcart_item.sku, "SKUs do not match"
        )
        self.assertEqual(
            new_shopcart_item["name"], test_shopcart_item.name, "Product names do not match"
        )
        self.assertEqual(
            new_shopcart_item["price"], test_shopcart_item.price, "Prices do not match"
        )
        self.assertEqual(
            new_shopcart_item["amount"], test_shopcart_item.amount, "Amounts do not match"
        )
        # times set by db
        self.assertIsNotNone(
            new_shopcart_item["create_time"], "Creation time not set"
        )
        self.assertIsNotNone(
            new_shopcart_item["update_time"], "Update time not set"
        )

    def test_create_shopcart_item_with_existing_item(self):
        """ Add to shopcart item when it already exists in the shopcart """

        test_shopcart = ShopcartFactory()
        resp = self.app.post("/shopcarts", json=test_shopcart.serialize(),
                             content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        test_shopcart_item = ShopcartItemFactory()
        test_shopcart_item.sid = resp.json["id"]
        original_amount = test_shopcart_item.amount
        resp = self.app.post(
            "/shopcarts/{}/items".format(test_shopcart_item.sid),
            json=test_shopcart_item.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        updated_shopcart_item = ShopcartItemFactory()
        updated_shopcart_item.sku = test_shopcart_item.sku
        updated_shopcart_item.sid = resp.json["id"]
        updated_amount = original_amount + updated_shopcart_item.amount
        resp = self.app.post(
            "/shopcarts/{}/items".format(updated_shopcart_item.sid),
            json=updated_shopcart_item.serialize(), content_type="application/json"
        )
        # check for status code
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # check for updated amount 
        new_shopcart_item = resp.get_json()
        self.assertEqual(
            new_shopcart_item["amount"], updated_amount, "Amounts do not match"
        )

    def test_update_shopcart_item(self):
        """ Update an existing shopcart item """
        test_shopcart = ShopcartFactory()
        resp = self.app.post("/shopcarts", json=test_shopcart.serialize(),
                             content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # create a shopcart item to update
        test_shopcart_item = ShopcartItemFactory()
        test_shopcart_item.sid = resp.json["id"]
        resp = self.app.post(
            "/shopcarts/{}/items".format(test_shopcart_item.sid),
            json=test_shopcart_item.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the shopcart item
        new_shopcart_item = resp.get_json()
        new_shopcart_item["price"] = 50.00
        new_shopcart_item["sku"] = 1001
        new_shopcart_item["name"] = "item_1"
        new_shopcart_item["amount"] = 4
        resp = self.app.put(
            "/shopcarts/{}/items/{}".format(new_shopcart_item["sid"], new_shopcart_item["id"]),
            json=new_shopcart_item,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_shopcart_item = resp.get_json()
        self.assertEqual(updated_shopcart_item["price"], 50.00)
        self.assertEqual(updated_shopcart_item["sku"], 1001)
        self.assertEqual(updated_shopcart_item["name"], "item_1")
        self.assertEqual(updated_shopcart_item["amount"], 4)

    def test_update_shopcart_item_not_found(self):
        """ Test update an existing shopcart item with a bad request """
        test_shopcart = ShopcartFactory()
        resp = self.app.post("/shopcarts", json=test_shopcart.serialize(),
                             content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # create a shopcart item to update
        test_shopcart_item = ShopcartItemFactory()
        test_shopcart_item.sid = resp.json["id"]
        resp = self.app.post(
            "/shopcarts/{}/items".format(test_shopcart_item.sid),
            json=test_shopcart_item.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the shopcart item
        new_shopcart_item = resp.get_json()
        new_shopcart_item["price"] = 50.00
        new_shopcart_item["sku"] = 1001
        new_shopcart_item["name"] = "item_1"
        new_shopcart_item["amount"] = 4
        resp = self.app.put(
            "/shopcarts/{}/items/{}".format(new_shopcart_item["sid"] + 1, new_shopcart_item["id"]),
            json=new_shopcart_item,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_shopcart_item_with_non_existing_shopcart(self):
        """ Update an item where shopcart doesn't exists """

        # create a shopcart item to update
        new_shopcart_item = {"price": 50.00}
        resp = self.app.put(
            "/shopcarts/{}/items/{}".format(1, 1),
            json=new_shopcart_item,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_shopcart_item(self):
        """ Query shopcart item list without any query string """
        test_shopcart = ShopcartFactory()
        resp = self.app.post("/shopcarts", json={"user_id": test_shopcart.user_id},
                             content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        shopcart_id = resp.json["id"]
        count = 10
        shopcart_items = self._create_shopcart_items(count, shopcart_id)
        resp = self.app.get("/shopcarts/items", content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), count)

    def test_query_shopcart_item_list_by_sku(self):
        """ Query shopcart item list by sku """
        test_shopcart = ShopcartFactory()
        resp = self.app.post("/shopcarts", json={"user_id": test_shopcart.user_id},
                             content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        shopcart_id = resp.json["id"]
        shopcart_items = self._create_shopcart_items(10, shopcart_id)
        test_sku = shopcart_items[0].sku
        sku_shopcart_items = [shopcart_item for shopcart_item in shopcart_items
                              if shopcart_item.sku == test_sku]
        resp = self.app.get("/shopcarts/items",
                            query_string="sku={}".format(test_sku), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(sku_shopcart_items))
        # check the data
        for shopcart_item in data:
            self.assertEqual(shopcart_item["sku"], test_sku)

    def test_query_shopcart_item_list_by_name(self):
        """ Query shopcart item list by name """
        test_shopcart = ShopcartFactory()
        resp = self.app.post("/shopcarts", json={"user_id": test_shopcart.user_id},
                             content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        shopcart_id = resp.json["id"]
        shopcart_items = self._create_shopcart_items(10, shopcart_id)
        test_name = shopcart_items[0].name
        name_shopcart_items = [shopcart_item for shopcart_item in shopcart_items
                               if shopcart_item.name == test_name]
        resp = self.app.get("/shopcarts/items",
                            query_string="name={}".format(test_name), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(name_shopcart_items))
        # check the data
        for shopcart_item in data:
            self.assertEqual(shopcart_item["name"], test_name)

    def test_query_shopcart_item_list_by_price(self):
        """ Query shopcart item list by price """
        test_shopcart = ShopcartFactory()
        resp = self.app.post("/shopcarts", json={"user_id": test_shopcart.user_id},
                             content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        shopcart_id = resp.json["id"]
        shopcart_items = self._create_shopcart_items(10, shopcart_id)
        test_price = shopcart_items[0].price
        price_shopcart_items = [shopcart_item for shopcart_item in shopcart_items
                                if shopcart_item.price == test_price]
        resp = self.app.get("/shopcarts/items",
                            query_string="price={}".format(test_price), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(price_shopcart_items))
        # check the data
        for shopcart_item in data:
            self.assertEqual(shopcart_item["price"], test_price)

    def test_query_shopcart_item_list_by_amount(self):
        """ Query shopcart item list by amount """
        test_shopcart = ShopcartFactory()
        resp = self.app.post("/shopcarts", json={"user_id": test_shopcart.user_id},
                             content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        shopcart_id = resp.json["id"]
        shopcart_items = self._create_shopcart_items(10, shopcart_id)
        test_amount = shopcart_items[0].amount
        amount_shopcart_items = [shopcart_item for shopcart_item in shopcart_items
                                 if shopcart_item.amount == test_amount]
        resp = self.app.get("/shopcarts/items",
                            query_string="amount={}".format(test_amount), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(amount_shopcart_items))
        # check the data
        for shopcart_item in data:
            self.assertEqual(shopcart_item["amount"], test_amount)

    def test_get_shopcart_items(self):
        """ Find shopcart items list by shopcart id """
        shopcart = self._create_shopcarts(1)
        shopcart_id = shopcart[0].id
        count = 5
        shopcart_items = self._create_shopcart_items(count, shopcart_id)
        response = self.app.get("/shopcarts/{}/items/".format(shopcart_id), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        shopcart_items_resp = response.get_json()
        self.assertTrue(len(shopcart_items) != 0)
        for item in shopcart_items_resp:
            self.assertEqual(item["sid"], shopcart_id)

    def test_get_shopcart_item_not_found(self):
        """ Get a Shopcart Item thats not found """
        resp = self.app.get("/shopcarts/0/items/0", content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_shopcart_items(self):
        """Delete a Shopcart Item"""
        shopcart = self._create_shopcarts(1)[0]
        shopcart_id = shopcart.id

        self.assertEqual(len(ShopcartItem.all()), 0)
        shopcart_item = self._create_shopcart_items(1, shopcart_id)[0]
        self.assertEqual(len(ShopcartItem.all()), 1)

        resp = self.app.delete(
            "/shopcarts/{}/items/{}".format(shopcart_id, shopcart_item.id),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)

        self.assertEqual(len(ShopcartItem.all()), 0)

    def test_post_request_without_content_type(self):
        """POST Request Without content_type"""
        resp = self.app.post("/shopcarts")
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        self.assertIn(b'Unsupported media type', resp.data)

    def test_post_request_with_wrong_content_type(self):
        """POST Request With Wrong content_type"""
        resp = self.app.post("/shopcarts", content_type="text/plain")
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        self.assertIn(b'Unsupported media type', resp.data)

######################################################################
#  ERROR HANDLER TEST CASES
######################################################################
    @patch('service.routes.Shopcart.create')
    def test_request_validation_error(self, bad_request_mock):
        """ Test a Data Validation error """
        bad_request_mock.side_effect = DataValidationError()
        test_shopcart = Shopcart()
        resp = self.app.post(
            "/shopcarts", json=test_shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_method_not_allowed(self):
        """ Test method not allowed """
        resp = self.app.post("/")
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertIn(b'Method not Allowed', resp.data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
