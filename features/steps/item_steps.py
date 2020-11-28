"""
Shopcart Steps
Steps file for Shopcarts.feature
For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""

from os import getenv
import logging
import json
import requests
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '60'))
ID_PREFIX = 'item_'

@given('the following items')
def step_impl(context):
    """ Delete all shopcart items and load new ones """
    headers = {'Content-Type': 'application/json'}
    # list all of the shopcarts and delete their items one by one
    context.resp = requests.get(context.base_url + '/api/shopcarts/items')
    expect(context.resp.status_code).to_equal(200)
    for item in context.resp.json():
        context.resp = requests.delete(context.base_url + '/api/shopcarts/' + str(item["sid"]) +
                       '/items/' + str(item["id"]), headers=headers)
        expect(context.resp.status_code).to_equal(204)
    
    create_url = context.base_url + '/api/shopcarts'
    for row in context.table:
        # Get the shopcart ID by querying the user ID
        get_url = context.base_url + '/api/shopcarts' + '?user_id=' + str(row['user'])
        context.resp = requests.get(get_url)
        expect(context.resp.status_code).to_equal(200)
        shopcart = context.resp.json()[0]
        shopcart_id = shopcart["id"]

        # Add the shopcart item data to the appropriate shopcart
        data = {
            "sid": shopcart_id,
            "sku": row['sku'],
            "name": row['name'],
            "amount": row['amount'],
            "price": row['price']
            }
        payload = json.dumps(data)
        item_url = create_url + '/' + str(shopcart_id) + '/items'
        context.resp = requests.post(item_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)

@when('I set the item "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower()
    element_id = element_id.replace(" ", "_")
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)

@then('the item "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower()
    element_id = element_id.replace(" ", "_")
    element = context.driver.find_element_by_id(element_id)
    expect(element.get_attribute('value')).to_be(u'')

@then('the item "{element_name}" field should not be empty')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower()
    element_id = element_id.replace(" ", "_")
    element = context.driver.find_element_by_id(element_id)
    expect(len(element.get_attribute('value')) > 0)

##################################################################
# These two function simulate copy and paste
##################################################################
@when('I copy the item "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower()
    element_id = element_id.replace(" ", "_")
    # element = context.driver.find_element_by_id(element_id)
    element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)

@when('I paste the item "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower()
    element_id = element_id.replace(" ", "_")
    # element = context.driver.find_element_by_id(element_id)
    element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)

##################################################################
# This code works because of the following naming convention:
# The buttons have an id in the html hat is the button text
# in lowercase followed by '-btn' so the Clean button has an id of
# id='clear-btn'. That allows us to lowercase the name and add '-btn'
# to get the element id of any button
##################################################################

@when('I press the item "{button}" button')
def step_impl(context, button):
    button_id = ID_PREFIX + button.lower() + '-btn'
    button_id = button_id.replace(" ", "_")
    context.driver.find_element_by_id(button_id).click()

@then('I should see "{name}" in the item results')
def step_impl(context, name):
    # element = context.driver.find_element_by_id(ID_PREFIX + 'search_results')
    # expect(element.text).to_contain(name)
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, ID_PREFIX + 'search_results'),
            name
        )
    )
    expect(found).to_be(True)

@then('I should not see "{name}" in the item results')
def step_impl(context, name):
    element = context.driver.find_element_by_id(ID_PREFIX + 'search_results')
    error_msg = "I should not see '%s' in '%s'" % (name, element.text)
    ensure(name in element.text, False, error_msg)

    
##################################################################
# This code works because of the following naming convention:
# The id field for text input in the html is the element name
# prefixed by ID_PREFIX so the Name field has an id='item_name'
# We can then lowercase the name and prefix with item_ to get the id
##################################################################

@then('I should see "{text_string}" in the item "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = ID_PREFIX + element_name.lower()
    element_id = element_id.replace(" ", "_")
    # element = context.driver.find_element_by_id(element_id)
    # expect(element.get_attribute('value')).to_equal(text_string)
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id),
            text_string
        )
    )
    expect(found).to_be(True)
