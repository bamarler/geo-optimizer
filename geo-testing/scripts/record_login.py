from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width":1280,"height":720})
    page = context.new_page()
    page.goto("https://chatgpt.com/")
    page.locator("#prompt-textarea").click()
    page.get_by_test_id("login-button").click()
    page.get_by_role("textbox", name="Email address").fill("maria@citable.xyz")
    page.get_by_role("button", name="Continue", exact=True).click()
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("citable123!!!")
    page.get_by_role("button", name="Continue", exact=True).click()

    # ---------------------
    context.storage_state(path="storage/auth_state.json")
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
