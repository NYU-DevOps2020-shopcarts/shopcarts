Feature: The shopcart items service back-end
    As an Administrator
    I need a RESTful catalog service
    So that I can keep track of all shopcart items

Background:
    Given the following shopcarts
        | user       |
        | 1          |
        | 2          |
        | 300        |
    Given the following items
        | user       | sku  | name    | amount | price  |
        | 1          | 1000 | item_1  | 2      | 5.75   |
        | 1          | 3000 | item_3  | 3      | 10.09  |
        | 2          | 2000 | item_2  | 1      | 59.99  |
        | 300        | 1000 | item_1  | 5      | 5.75   |

Scenario: Place an order
    When I visit the "Home Page"
    And I set the "User" to "2"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "User" field should be empty
    When I paste the "Id" field
    And I press the "Order" button
    Then I should see the message "Order was successfully placed"
    When I press the "Retrieve" button
    Then I should see the message "not found"
    
Scenario: Create an item
    When I visit the "Home Page"
    And I set the "User" to "5"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "User" field should be empty
    When I paste the item "Shopcart Id" field
    And I set the item "Product Id" to "1000"
    And I set the item "Name" to "item_1"
    And I set the item "Amount" to "1"
    And I set the item "Price" to "5.75"
    And I press the item "Create" button
    Then I should see the message "Success"
    When I copy the item "Shopcart Id" field
    And I press the item "Clear" button
    Then the item "Shopcart Id" field should be empty
    And the item "Id" field should be empty
    And the item "Product Id" field should be empty
    And the item "Name" field should be empty
    And the item "Amount" field should be empty
    And the item "Price" field should be empty
    When I paste the item "Shopcart Id" field
    And I press the item "Retrieve" button
    Then I should see "1000 item_1 5.75 1" in the item results
    When I paste the item "Shopcart Id" field
    And I set the item "Product Id" to "1000"
    And I set the item "Name" to "item_1"
    And I set the item "Amount" to "1"
    And I set the item "Price" to "5.75"
    And I press the item "Create" button
    Then I should see the message "Success"
    When I press the item "Retrieve" button
    Then I should see "1000 item_1 5.75 2" in the item results
    And I should not see "1000 item_1 5.75 1" in the item results

Scenario: Delete an item
    When I visit the "Home Page"
    And I set the "User" to "1"
    And I press the "Search" button
    Then the item "Shopcart Id" field should not be empty
    When I press the item "Retrieve" button
    Then I should see the message "Success"
    When I copy the item "Shopcart Id" field
    When I press the item "Delete" button
    Then I should see the message "ShopCart Item has been Deleted!"
    When I press the item "Clear" button
    Then the item "Shopcart Id" field should be empty
    And the item "Id" field should be empty
    And the item "Product Id" field should be empty
    And the item "Name" field should be empty
    And the item "Amount" field should be empty
    And the item "Price" field should be empty
    When I paste the item "Shopcart Id" field
    And I press the item "Retrieve" button
    Then I should not see "1000 item_1 5.75 1" in the item results
    And I should not see "1000 item_1 5.75 2" in the item results
    When I press the item "Clear" button
    And I press the "Clear" button
    And I set the "User" to "2"
    And I press the "Search" button
    Then the item "Shopcart Id" field should not be empty
    When I press the item "Retrieve" button
    Then I should see the message "Success"
    When I copy the item "Shopcart Id" field
    When I press the item "Delete" button
    Then I should see the message "ShopCart Item has been Deleted!"
    When I press the item "Clear" button
    Then the item "Shopcart Id" field should be empty
    And the item "Id" field should be empty
    And the item "Product Id" field should be empty
    And the item "Name" field should be empty
    And the item "Amount" field should be empty
    And the item "Price" field should be empty
    When I paste the item "Shopcart Id" field
    And I press the item "Retrieve" button
    Then I should see the message "is empty"