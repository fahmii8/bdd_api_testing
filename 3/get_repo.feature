Feature: Get my repositories

  Scenario: I want a list of my GitHub repositories
    Given I am an authenticated user
    When I request a list of my repositories
    Then I expect "test-repo" to be in the results set