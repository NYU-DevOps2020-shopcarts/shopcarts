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
import unittest
from unittest import TestCase
import logging
from werkzeug.datastructures import MultiDict, ImmutableMultiDict
from service import routes

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_409_CONFLICT = 409
HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415


######################################################################
#  T E S T   C A S E S
######################################################################
class TestShopcartServer(TestCase):
    """ Shopcart Service tests """

    def setUp(self):
        self.app = routes.app.test_client()

    def test_index(self):
        """ Test the index page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertIn(b'Shopcart Demo REST API Service', resp.data)

    def test_healthcheck(self):
        resp = self.app.get('/healthcheck')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertIn(b'Healthy', resp.data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
