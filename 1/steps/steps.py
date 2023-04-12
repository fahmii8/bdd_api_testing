from behave import given, when, then
import urllib.parse
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


@when('I search for "{search_query}"')
def when_search_for_query(context, search_query):
    encoded_query = urllib.parse.quote(search_query)
    context.endpoint = f"search/repositories?q={encoded_query}"
    context.response = requests.get(context.url + context.endpoint)


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


@then("I get a result")
def then_get_result(context):
    if context.response.status_code != 200:
        raise Exception(f"HTTP Response Code: {context.response.status_code}")
    if "items" not in context.response.json():
        raise Exception(
            f'"Items" not found in the response. The response may be empty.'
        )
    if len(context.response.json()["items"]) < 1:
        raise Exception(f"The search query yielded 0 results.")
