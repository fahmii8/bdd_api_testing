Feature: GitHub API Testing

  Scenario: Make search queries for GitHub repositories
    Given I am an anonymous user
    When I search for "github test"
    Then I expect a 200 response code
    And I expect at least 22 results
