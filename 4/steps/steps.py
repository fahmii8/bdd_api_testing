from behave import given, when, then
import urllib.parse
import requests

BEARER_TOKEN = "PASTE_YOUR_BEARER_TOKEN_HERE"

BASE_URL = "https://api.github.com/"
AUTH_URL = BASE_URL + "user"
CREATE_REPO_URL = AUTH_URL + "/repos"
AUTH_HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}


@given('the API endpoint URL is "{url}"')
def api_endpoint_url(context, url):
    context.url = url


@given("i am an {user_type} user")
def given_user_type(context, user_type):
    if user_type == "anonymous":
        context.url = BASE_URL
        return
    if not user_type == "authenticated":
        raise Exception(f"Invalid user_type: {user_type}")

    auth_response = requests.get(AUTH_URL, headers=AUTH_HEADERS)

    if auth_response.status_code != 200:
        raise Exception(
            f"Authentication failed, HTTP status code: {auth_response.status_code}"
        )
    context.response = auth_response


@when("I request a list of my repositories")
def when_request_repositories(context):
    repos_url = context.response.json()["repos_url"]
    repos_response = requests.get(repos_url, headers=AUTH_HEADERS)
    context.response = repos_response.json()


@when('I create a repository called "{new_repo_name}"')
def when_create_repository(context, new_repo_name):
    data = {
        "name": new_repo_name,
        "description": f"This {new_repo_name} is my new repository created using the GitHub API",
        "private": False,
        "auto_init": True,
    }
    create_response = requests.post(
        url=CREATE_REPO_URL, json=data, headers=AUTH_HEADERS
    )

    if create_response.status_code != 201:
        raise Exception(
            f"Repository creation failed, HTTP status code: {create_response.status_code},\
              with the following information: {create_response.text}"
        )

    context.response = requests.get(AUTH_URL, headers=AUTH_HEADERS)


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
def then_expect_repo_name(context, repo_name):
    if not any(repo["name"] == repo_name for repo in context.response):
        raise Exception(
            f"The expected repo name [{repo_name}] was not found in the list of repositories."
        )
