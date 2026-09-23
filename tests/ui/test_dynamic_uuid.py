
import pytest
import uuid

from faker import Faker

from playwright.sync_api import expect

from pages.loginPage import LoginPage

faker = Faker()


@pytest.mark.dynamic
def test_dynamic_uuid(login_page: LoginPage, config):
    # Generate a dynamic UUID for the username
    
    dynamic_username = faker.user_name() + "_" + str(uuid.uuid4().hex[:6])
    dynamic_password = faker.password()
    dynamic_email = faker.email()

    print(f"\n Dynamic username: {dynamic_username} and email: {dynamic_email}")
    login_page.login(dynamic_username, dynamic_password)
    expect(login_page.invalid_credentials).to_be_visible()  

@pytest.mark.dynamic   
@pytest.mark.parametrize("username, password", [pytest.param("Admin", faker.password(), id="valid_username_invalid_password"), pytest.param(faker.user_name(), "admin123", id="invalid_username_valid_password"), pytest.param(faker.user_name(), faker.password(), id="invalid_username_invalid_password")])
def test_invalid_login(login_page: LoginPage, config, username, password):
    print(f"\n Dynamic username: {username}")
    login_page.login(username, password)
    expect(login_page.invalid_credentials).to_be_visible()
