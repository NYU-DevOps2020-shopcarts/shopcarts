######################################################################
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
Shopcart Service with UI

Paths:
------
GET / - Displays a usage information for Selenium testing
GET /shopcarts - Returns a list of all the Shopcarts
POST /shopcarts - Creates a new Shopcart record in the database
GET /shopcarts/{id} - Returns the Shopcart with a given id number
DELETE /shopcarts/{id} - Deletes a Shopcart record in the database
PUT /shopcarts/{id}/place-order - Places an order
GET /shopcarts/{id}/items - Gets Shopcart Item list from a Shopcart
POST /shopcarts/{id}/items - Creates a new Shopcart Item record in the database
GET /shopcarts/{id}/items/{item_id} - Returns the Shopcart Item with given id and item_id number
PUT /shopcarts/{id}/items/{item_id} - Updates the Shopcart Item
DELETE /shopcarts/{id}/items/{item_id} - Deletes the Shopcart Item
"""

import sys
import logging
from flask import jsonify, request, url_for, make_response, abort
from flask.logging import create_logger
from flask_api import status  # HTTP Status Codes
from flask_restplus import Api, Resource, fields, reqparse, inputs
from service.models import Shopcart, ShopcartItem, DataValidationError
from . import app, constants

# use create_logger function to avoid no-member errors for logger in pylint
logger = create_logger(app)

######################################################################
# Configure Swagger before initializing it
######################################################################

api = Api(app,
          version='1.0.0',
          title='Shopcart REST API Service',
          description='This is a Shopcart server.',
          default='shopcarts',
          default_label='Shopcart operations',
          doc='/apidocs',
          # authorizations=authorizations,
          prefix='/api'
          )

# Define the model so that the docs reflect what can be sent
shopcart_model = api.model('Shopcart', {
    'id': fields.Integer(readOnly=True,
                          description='The unique id assigned internally by service'),
    'user_id': fields.Integer(required=True,
                              description='The id of the User'),
    'create_time': fields.DateTime(readOnly=True,
                                   description='The time the record is created'),
    'update_time': fields.DateTime(readOnly=True,
                                   description='The time the record is updated')
})

create_shopcart_model = api.model('Shopcart', {
    'user_id': fields.Integer(required=True,
                              description='The id of the User')
})

shopcart_item_model = api.model('ShopcartItem', {
    'id': fields.Integer(readOnly=True,
                          description='The unique id assigned internally by service'),
    'sid': fields.Integer(readOnly=True,
                          description='The id of the Shopcart this item belongs to'),
    'sku': fields.Integer(required=True,
                          description='The product id'),
    'name': fields.String(required=True,
                          description='The product name'),
    'price': fields.Float(required=True,
                          description='The price for one item'),
    'amount': fields.Float(required=True,
                           description='The number of product'),
    'create_time': fields.DateTime(readOnly=True,
                                   description='The time the record is created'),
    'update_time': fields.DateTime(readOnly=True,
                                   description='The time the record is updated')
})

create_shopcart_item_model = api.model('ShopcartItem', {
    'sku': fields.Integer(required=True,
                          description='The product id'),
    'name': fields.String(required=True,
                          description='The product name'),
    'price': fields.Float(required=True,
                          description='The price for one item'),
    'amount': fields.Float(required=True,
                           description='The number of product')
})

# query string arguments
shopcart_args = reqparse.RequestParser()
shopcart_args.add_argument('user_id', type=int, required=False, help='Find Shopcart by User Id')

shopcart_item_args = reqparse.RequestParser()
shopcart_item_args.add_argument('sku',
                                type=int,
                                required=False,
                                help='Find Shopcart Item by Product Id')
shopcart_item_args.add_argument('name',
                                type=str,
                                required=False,
                                help='Find Shopcart Item by Product Name')
shopcart_item_args.add_argument('price',
                                type=float,
                                required=False,
                                help='Find Shopcart Item by Product Price')
shopcart_item_args.add_argument('amount',
                                type=float,
                                required=False,
                                help='Find Shopcart Item by Product Amount')


######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """ Handles bad reuests with 400_BAD_REQUEST """
    logger.warning(str(error))
    return (
        jsonify(
            status=status.HTTP_400_BAD_REQUEST, error="Bad Request", message=str(error)
        ),
        status.HTTP_400_BAD_REQUEST,
    )


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    logger.warning(str(error))
    return (
        jsonify(
            status=status.HTTP_404_NOT_FOUND, error=constants.NOT_FOUND, message=str(error)
        ),
        status.HTTP_404_NOT_FOUND,
    )


@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    logger.warning(str(error))
    return (
        jsonify(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            error="Method not Allowed",
            message=str(error),
        ),
        status.HTTP_405_METHOD_NOT_ALLOWED,
    )


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    logger.warning(str(error))
    return (
        jsonify(
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            error="Unsupported media type",
            message=str(error),
        ),
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    )


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route('/healthcheck')
def healthcheck():
    """ Let them know our heart is still beating """
    return make_response(jsonify(status=200, message='Healthy'), status.HTTP_200_OK)


######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Root URL response """
    return app.send_static_file('index.html')


######################################################################
#  PATH: /shopcarts
######################################################################
@api.route('/shopcarts', strict_slashes=False)
class ShopcartCollection(Resource):
    # ------------------------------------------------------------------
    # LIST ALL Shopcarts
    # ------------------------------------------------------------------
    @api.doc('list_shopcarts')
    @api.expect(shopcart_args, validate=True)
    @api.marshal_list_with(shopcart_model)
    def get(self):
        """ Returns all of the Shopcarts """
        logger.info('Request to list Shopcarts...')

        args = shopcart_args.parse_args()

        if args['user_id']:
            logger.info('Find by user')
            shopcarts = Shopcart.find_by_user(args['user_id'])
        else:
            logger.info('Find all')
            shopcarts = Shopcart.all()

        results = [shopcart.serialize() for shopcart in shopcarts]
        logger.info('[%s] Shopcarts returned', len(results))
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW Shopcart
    # ------------------------------------------------------------------
    @api.doc('create_shopcarts')
    @api.expect(create_shopcart_model)
    @api.response(400, 'The posted data was not valid')
    @api.response(201, 'Shopcart created successfully')
    @api.marshal_with(shopcart_model, code=201)
    def post(self):
        logger.info("Request to create a shopcart")
        check_content_type("application/json")

        logger.debug('Payload = %s', api.payload)

        shopcart = None

        if 'user_id' in api.payload:
            shopcart = Shopcart.find_by_user(api.payload['user_id']).first()

        if shopcart is None:
            shopcart = Shopcart()
            shopcart.deserialize(api.payload)
            shopcart.create()

        logger.info("Shopcart with ID [%s] created.", shopcart.id)

        location_url = url_for("get_shopcart", shopcart_id=shopcart.id, _external=True)

        return shopcart.serialize(), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# G E T  S H O P C A R T
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods=["GET"])
def get_shopcart(shopcart_id):
    """
    Gets information about a Shopcart
    This endpoint will get information about a shopcart
    """
    logger.info("Request to get information of a shopcart")
    check_content_type("application/json")

    shopcart = Shopcart.find(shopcart_id)
    if shopcart is None:
        logger.info("Shopcart with ID [%s] not found.", shopcart_id)
        return not_found("Shopcart with ID [%s] not found." % shopcart_id)

    shopcart_items = ShopcartItem.find_by_shopcartid(shopcart_id)
    response = shopcart.serialize()
    response["items"] = [item.serialize() for item in shopcart_items]

    logger.info("Shopcart with ID [%s] fetched.", shopcart.id)
    return make_response(
        jsonify(response), status.HTTP_200_OK
    )

######################################################################
# G E T  S H O P C A R T  I T E M
######################################################################
@app.route('/shopcarts/<int:shopcart_id>/items/<int:item_id>', methods=["GET"])
def get_shopcart_item(shopcart_id, item_id):
    """
    Get a shopcart item
    This endpoint will return an item in the shop cart
    """
    logger.info("Request to get an item in a shopcart")
    check_content_type("application/json")

    shopcart_item = ShopcartItem.find(item_id)

    if shopcart_item is None or shopcart_item.sid != shopcart_id:
        logger.info("Shopcart item with ID [%s] not found in shopcart [%s].", item_id, shopcart_id)
        return not_found("Shopcart item with ID [%s] not found in shopcart [%s]." % (item_id, shopcart_id))

    result = shopcart_item.serialize()
    logger.info("Fetched shopcart item with ID [%s].", item_id)
    return make_response(
        jsonify(result), status.HTTP_200_OK
    )


######################################################################
#  PATH: /shopcarts/items
######################################################################
@api.route('/shopcarts/items', strict_slashes=False)
class ShopcartItemCollection(Resource):
    """ Handles all interactions with collections of Shopcart Items """
    #------------------------------------------------------------------
    # LIST ALL Shopcart Items
    #------------------------------------------------------------------
    @api.doc('list_shopcart_items')
    @api.expect(shopcart_item_args, validate=True)
    @api.marshal_list_with(shopcart_item_model)
    def get(self):
        """ Returns all of the Shopcart Items """
        app.logger.info('Request to list Shopcart Items...')
        shopcart_item_args = []
        args = shopcart_item_args.parse_args()
        if args['sku']:
            app.logger.info('Filtering by sku: %s', args['sku'])
            shopcart_items = ShopcartItem.find_by_sku(args['sku'])
        elif args['name']:
            app.logger.info('Filtering by name: %s', args['name'])
            shopcart_items = ShopcartItem.find_by_sku(args['name'])
        elif args['available'] is not None:
            app.logger.info('Filtering by availability: %s', args['available'])
            shopcart_items = ShopcartItem.find_by_sku(args['available'])
        else:
            shopcart_items = ShopcartItem.all()

        results = [shopcart_item.serialize() for shopcart_item in shopcart_items]
        logger.info('[%s] Shopcart Items returned', len(results))
        return results, status.HTTP_200_OK

######################################################################
# UPDATE AN EXISTING SHOPCARTITEM
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/items/<int:item_id>", methods=["PUT"])
def update(shopcart_id, item_id):
    """
    Update a Shopcart item
    This endpoint will update a Shopcart item based the body that is posted
    """
    logger.info("Request to update Shopcart item with id: %s", item_id)
    check_content_type("application/json")

    shopcart_item = ShopcartItem.find(item_id)

    if shopcart_item is None or shopcart_item.sid != shopcart_id:
        logger.info("Shopcart item with ID [%s] not found in shopcart [%s].", item_id, shopcart_id)
        return not_found("Shopcart item with id '{}' was not found.".format(item_id))

    data = request.get_json()
    data["sid"] = shopcart_id
    data["id"] = item_id
    shopcart_item.deserialize(data)
    shopcart_item.update()

    logger.info("Shopcart item with ID [%s] updated.", shopcart_item.id)
    return make_response(jsonify(shopcart_item.serialize()), status.HTTP_200_OK)


######################################################################
#  PATH: /shopcarts/items
######################################################################
@api.route('/shopcarts/items', strict_slashes=False)
class ShopcartItemQueryCollection(Resource):
    # ------------------------------------------------------------------
    # LIST ALL Shopcart Items or Query by sku, name, price, or amount
    # ------------------------------------------------------------------
    @api.doc('list_shopcart_items')
    @api.expect(shopcart_item_args, validate=True)
    @api.marshal_list_with(shopcart_item_model)
    def get(self):
        """ Returns all of the ShopcartItems """
        logger.info('Request to list ShopcartItems...')

        args = shopcart_item_args.parse_args()

        if args['sku']:
            logger.info('Find by sku')
            shopcart_items = ShopcartItem.find_by_sku(args['sku'])
        elif args['name']:
            logger.info('Find by name')
            shopcart_items = ShopcartItem.find_by_name(args['name'])
        elif args['price']:
            logger.info('Find by price')
            shopcart_items = ShopcartItem.find_by_price(args['price'])
        elif args['amount']:
            logger.info('Find by amount')
            shopcart_items = ShopcartItem.find_by_amount(args['amount'])
        else:
            logger.info('Find all')
            shopcart_items = ShopcartItem.all()

        results = [shopcart_item.serialize() for shopcart_item in shopcart_items]
        logger.info('[%s] Shopcart Items returned', len(results))
        return results, status.HTTP_200_OK


######################################################################
# DELETE A SHOPCARTITEM
######################################################################
@app.route('/shopcarts/<int:shopcart_id>/items/<int:item_id>', methods=['DELETE'])
def delete_shopcart_items(shopcart_id, item_id):
    """
    Delete a ShopcartItem
    This endpoint will delete a ShopcartItem based the id specified in the path
    """
    logger.info('Request to delete ShopcartItem with id: %s from Shopcart %s', item_id, shopcart_id)
    check_content_type("application/json")

    shopcart_item = ShopcartItem.find(item_id)

    if shopcart_item is not None and shopcart_item.sid == shopcart_id:
        shopcart_item.delete()

    logger.info('ShopcartItem with id: %s has been deleted', item_id)
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
# DELETE A SHOPCART
######################################################################
@app.route('/shopcarts/<int:shopcart_id>', methods=['DELETE'])
def delete_shopcarts(shopcart_id):
    """
    Delete a Shopcart
    This endpoint will delete a Shopcart based the id specified in the path
    """
    logger.info('Request to delete Shopcart with id: %s', shopcart_id)
    check_content_type("application/json")

    item = Shopcart.find(shopcart_id)
    if item:
        item.delete()

    logger.info('Shopcart with id: %s has been deleted', shopcart_id)
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
# PATH: /shopcarts/{id}}/place-order
######################################################################
@api.route('/shopcarts/<int:shopcart_id>/place-order')
@api.param('shopcart_id', 'The Shopcart identifier')
class PlaceOrderResource(Resource):
    """ Place Order action on a Shopcart"""
    @api.doc('place_order')
    @api.response(404, 'Shopcart not found or is empty')
    @api.response(204, 'Shopcart has been deleted')
    def put(self, shopcart_id):
        """
        Place Order for a Shopcart
        This endpoint will place an order for a Shopcart based the id specified in the path
        """
        logger.info('Request to place order for Shopcart with id: %s', shopcart_id)

        shopcart = Shopcart.find(shopcart_id)
        if shopcart:
            shopcart_items = ShopcartItem.find_by_shopcartid(shopcart_id)
            if shopcart_items is None or len(shopcart_items) == 0:
                logger.info("Shopcart with ID [%s] is empty.", shopcart_id)
                api.abort(status.HTTP_404_NOT_FOUND, "Shopcart with ID [%s] is empty." % shopcart_id)
            shopcart_items_list = [item.serialize() for item in shopcart_items]

            # once we have the list of shopcart items we can send in JSON format to the orders team
            # SEND shocart_items_list TO ORDERS TEAM

            shopcart.delete()

            logger.info('Shopcart with id: %s has been deleted', shopcart_id)
            return make_response("", status.HTTP_204_NO_CONTENT)

        logger.info("Shopcart with ID [%s] is does not exist.", shopcart_id)
        api.abort(status.HTTP_404_NOT_FOUND, "Shopcart with ID [%s] is does not exist." % shopcart_id)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(content_type):
    """ Checks that the media type is correct """
    if 'Content-Type' not in request.headers:
        logger.error('No Content-Type specified.')
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
              'Content-Type must be {}'.format(content_type))

    if request.headers['Content-Type'] == content_type:
        return

    logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 'Content-Type must be {}'.format(content_type))


# # @app.before_first_request
# def initialize_logging(log_level=app.config['LOGGING_LEVEL']):
#     """ Initialized the default logging to STDOUT """
#     if not app.debug:
#         print('Setting up logging...')
#         # Set up default logging for submodules to use STDOUT
#         # datefmt='%m/%d/%Y %I:%M:%S %p'
#         fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
#         logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
#         # Make a new log handler that uses STDOUT
#         handler = logging.StreamHandler(sys.stdout)
#         handler.setFormatter(logging.Formatter(fmt))
#         handler.setLevel(log_level)
#         # Remove the Flask default handlers and use our own
#         handler_list = list(logger.handlers)
#         for log_handler in handler_list:
#             logger.removeHandler(log_handler)
#         logger.addHandler(handler)
#         logger.setLevel(log_level)
#         logger.info('Logging handler established')


def init_db():
    """ Initialies the SQLAlchemy app """
    Shopcart.init_db(app)
    ShopcartItem.init_db(app)
    logger.info("Database has been initialized!")
