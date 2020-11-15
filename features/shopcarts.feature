Feature: The shopcart service back-end
    As an Administrator
    I need a RESTful catalog service
    So that I can keep track of all shopcarts

Background:
    Given the following shopcarts
        | user       |
        | 1          |
        | 2          |
        | 3          |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "ShopCart Demo RESTful API Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Shopcart
    When I visit the "Home Page"
    And I set the "User" to "4"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "User" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "4" in the "User" field