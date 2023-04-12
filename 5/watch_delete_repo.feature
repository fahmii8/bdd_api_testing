Feature: Watch, and delete a repository

  Scenario: I want to watch my repository and delete it
    Given I am an authenticated user
      And I have a repository called "monkey"
    When I watch the "monkey" repository
    Then the "monkey" repository will list me as a watcher
      And I delete the repository called "monkey"