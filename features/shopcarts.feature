Feature: The shopcart service back-end
    As an Administrator
    I need a RESTful catalog service
    So that I can keep track of all shopcarts

Background:
    Given the following shopcarts
        | user       |
        | 1          |
        | 2          |
        | 300        |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "ShopCart Demo RESTful API Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Shopcart
    When I visit the "Home Page"
    And I set the "User" to "4"
    And I press the "Create" button
    Then I should see the message "Shopcart has been created!"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "User" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "4" in the "User" field

Scenario: List all shopcarts
    When I visit the "Home Page"
    And I press the "List" button
    Then I should see "1" in the results
    And I should see "2" in the results
    And I should not see "500" in the results

Scenario: Read a shopcart
    When I visit the "Home Page"
    And I set the "User" to "12"
    And I press the "Create" button
    Then I should see the message "Shopcart has been created!"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "12" in the "User" field

Scenario: Query shopcarts
    When I visit the "Home Page"
    And I set the "User" to "2"
    And I press the "Search" button
    Then I should see "2" in the results
    And I should not see "300" in the results

Scenario: Delete a shopcart
    When I visit the "Home Page"
    And I set the "User" to "400"
    And I press the "Create" button
    Then I should see the message "Shopcart has been created!"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "User" field should be empty
    When I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Shopcart has been deleted!"
    When I press the "Retrieve" button
    Then I should see the message "not found"
    When I set the "User" to "1"
    When I press the "Search" button
    Then I should see the message "Please see the search result below!"
