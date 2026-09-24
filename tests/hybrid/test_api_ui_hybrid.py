import pytest
from playwright.sync_api import expect

@pytest.mark.hybrid
def test_api_setup_ui_validation(created_user, login_page):
    
    # -------------------------
    # API SETUP
    # -------------------------

    print("\nUser created through API:", created_user)

    assert created_user["id"]
    assert created_user["username"]

    # -------------------------
    # UI VALIDATION
    # -------------------------
    login_page.login("Admin", "admin123")  
    login_page.page.wait_for_timeout(5000)
    expect(login_page.page).to_have_title("OrangeHRM")
    assert login_page.get_title() == "OrangeHRM" 