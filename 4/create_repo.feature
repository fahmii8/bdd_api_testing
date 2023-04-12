Feature: Create a new repository

  Scenario: I need a new repository and want to confirm that it exists
    Given I am an authenticated user
    When I create a repository called "monkey"
    And I request a list of my repositories
    Then I expect "monkey" to be in the results set