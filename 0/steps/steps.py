from behave import given, when, then
import requests


@given('the API endpoint URL is "{url}"')
def api_endpoint_url(context, url):
    context.url = url


@given("i am an {user_type} user")
def given_user_type(context, user_type):
    context.url = "https://api.github.com/"


@when("the GET method is called")
def when_get_is_called(context):
    response = requests.get(context.url)
    context.response = response


@then("the response status code should be {status_code:d}")
def then_response_status_code(context, status_code):
    assert context.response.status_code == status_code


@then('the response body should contain property "{property_name}"')
def then_body_contain_property(context, property_name):
    response_json = context.response.json()
    assert property_name in response_json


@then('the response property "{property_name}" should be equal to "{expected_value}"')
def then_property_should_be(context, property_name, expected_value):
    response_json = context.response.json()
    assert str(response_json[property_name]) == expected_value


@when("I search for Behat")
def when_search_for_behat(context):
    context.endpoint = "search/repositories?q=Behat"
    context.response = requests.get(context.url + context.endpoint)


@then("I get a result")
def then_get_result(context):
    assert context.response.status_code == 200
    assert "items" in context.response.json()
