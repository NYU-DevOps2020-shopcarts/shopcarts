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
import logging
from werkzeug.datastructures import MultiDict, ImmutableMultiDict
from shopcart_factory import ShopcartFactory, ShopcartItemFactory
from service.models import Shopcart, ShopcartItem, DataValidationError, db
from service import routes
from service import app

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_409_CONFLICT = 409
HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///../db/test.db")

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
        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertIn(b'Shopcart Demo REST API Service', resp.data)

    def test_healthcheck(self):
        """ Healthcheck Test """
        resp = self.app.get('/healthcheck')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertIn(b'Healthy', resp.data)

######################################################################
#  S H O P C A R T   T E S T   C A S E S
######################################################################

    def _create_shopcarts(self, count):
        """ Factory method to create shopcarts in bulk """
        shopcarts = []
        for _ in range(count):
            test_shopcart = ShopcartFactory()
            resp = self.app.post(
                "/shopcarts", json=test_shopcart.serialize(), content_type="application/json"
            )
            self.assertEqual(
                resp.status_code, HTTP_201_CREATED, "Could not create test shopcart"
            )
            new_shopcart = resp.get_json()
            test_shopcart.id = new_shopcart["id"]
            shopcarts.append(test_shopcart)
        return shopcarts

    def test_create_shopcart(self):
        """ Create a new Shopcart """
        test_shopcart = ShopcartFactory()
        resp = self.app.post(
            "/shopcarts", json=test_shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertTrue(location != None)
        # Check the data is correct
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["user_id"], test_shopcart.user_id, "User ids do not match")
        #times set by db
        self.assertIsNotNone(new_shopcart["create_time"],
                        "Creation time not set")
        self.assertIsNotNone(new_shopcart["update_time"],
                        "Update time not set")
        #TODO after Get Added
        # Check that the location header was correct
        #resp = self.app.get(location, content_type="application/json")
        #self.assertEqual(resp.status_code, HTTP_200_OK)
        #new_shopcart = resp.get_json()
        #self.assertEqual(new_shopcart["user_id"], test_shopcart.user_id, "User ids do not match")
        #times set by db
        #self.assertIsNotNone(
        #    new_shopcart["create_time"], "Creation time not set"
        #)
        #self.assertIsNotNone(
        #    new_shopcart["update_time"], "Update time not set"
        #)

######################################################################
#  S H O P C A R T I T E M   T E S T   C A S E S
######################################################################

    def _create_shopcart_items(self, count):
        """ Factory method to create shopcart_items in bulk """
        shopcart_items = []
        for _ in range(count):
            test_shopcart_item = ShopcartItemFactory()
            resp = self.app.post(
                "/shopcartitems", json=test_shopcart_item.serialize(),
                content_type="application/json"
            )
            self.assertEqual(
                resp.status_code, HTTP_201_CREATED, "Could not create test shopcart item"
            )
            new_shopcart_item = resp.get_json()
            test_shopcart_item.id = new_shopcart_item["id"]
            shopcart_items.append(test_shopcart_item)
        return shopcart_items

    def test_create_shopcart_item(self):
        """ Create a new ShopcartItem """
        test_shopcart_item = ShopcartItemFactory()
        resp = self.app.post(
            "/shopcartitems", json=test_shopcart_item.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertTrue(location != None)
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
        #times set by db
        self.assertIsNotNone(
            new_shopcart_item["create_time"], "Creation time not set"
        )
        self.assertIsNotNone(
            new_shopcart_item["update_time"], "Update time not set"
        )
        #TODO after Get functionality added
        # Check that the location header was correct
        #resp = self.app.get(location, content_type="application/json")
        #self.assertEqual(resp.status_code, HTTP_200_OK)
        #new_shopcart_item = resp.get_json()
        #self.assertEqual(new_shopcart_item["sid"], test_shopcart_item.sid,
        #                 "Shopcart ids do not match")
        #self.assertEqual(
        #    new_shopcart_item["sku"], test_shopcart_item.sku, "SKUs do not match"
        #)
        #self.assertEqual(
        #    new_shopcart_item["name"], test_shopcart_item.name, "Product names do not match"
        #)
        #self.assertEqual(
        #    new_shopcart_item["price"], test_shopcart_item.price, "Prices do not match"
        #)
        #self.assertEqual(
        #    new_shopcart_item["amount"], test_shopcart_item.amount, "Amounts do not match"
        #)
        #times set by db
        #self.assertIsNotNone(
        #    new_shopcart_item["create_time"], "Creation time not set"
        #)
        #self.assertIsNotNone(
        #    new_shopcart_item["update_time"], "Update time not set"
        #)

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
