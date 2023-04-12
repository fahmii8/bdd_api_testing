Feature: API testing
  Scenario: Test GET endpoint
    Given the API endpoint URL is "https://jsonplaceholder.typicode.com/posts/1"
    When the GET method is called
    Then the response status code should be 200
    And the response body should contain property "id"
    And the response property "userId" should be equal to "1"
