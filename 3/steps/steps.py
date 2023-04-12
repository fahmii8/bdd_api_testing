from behave import given, when, then
import urllib.parse
import requests

BEARER_TOKEN = "PASTE_YOUR_BEARER_TOKEN_HERE"


@given('the API endpoint URL is "{url}"')
def api_endpoint_url(context, url):
    context.url = url


@given("i am an {user_type} user")
def given_user_type(context, user_type):
    if user_type == "anonymous":
        context.url = "https://api.github.com/"
        return
    if not user_type == "authenticated":
        raise Exception(f"Invalid user_type: {user_type}")

    auth_headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    auth_url = "https://api.github.com/user"
    auth_response = requests.get(auth_url, headers=auth_headers)

    if auth_response.status_code != 200:
        raise Exception(
            f"Authentication failed, HTTP status code: {auth_response.status_code}"
        )
    context.response = auth_response


@when("I request a list of my repositories")
def when_request_repositories(context):
    repos_url = context.response.json()["repos_url"]
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    repos_response = requests.get(repos_url, headers=headers)
    context.response = repos_response.json()


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


@then("I expect a {status_code:d} response code")
def then_expect_status_code(context, status_code):
    if context.response.status_code != status_code:
        raise Exception(
            f"Unexpected HTTP Response Code: {context.response.status_code}"
        )


@then("I expect at least 1 result")
def then_expect_one_result(context):
    if len(context.response.json()["items"]) < 1:
        raise Exception(f"The search query yielded 0 results.")


@then("I expect at least {n_results:d} results")
def then_expect_multiple_results(context, n_results):
    if len(context.response.json()["items"]) < n_results:
        raise Exception(
            f"The search query yielded {len(context.response.json()['items'])} results."
        )


@then('I expect "{repo_name}" to be in the results set')
def step_impl(context, repo_name):
    if not any(repo["name"] == repo_name for repo in context.response):
        raise Exception(
            f"The expected repo name [{repo_name}] was not found in the list of repositories."
        )
