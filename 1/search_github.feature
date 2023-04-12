Feature: GitHub API Testing

  Scenario: Search for Behat in GitHub repositories
    Given I am an anonymous user
    When I search for "behat"
    Then I get a result
