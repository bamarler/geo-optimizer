from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="storage/auth_state.json", viewport={"width":1280,"height":720})
    page = context.new_page()
    page.goto("https://chatgpt.com/")
    page.locator("#prompt-textarea").click()
    page.get_by_text("EUExample UserFreeUpgrade").click()
    page.get_by_role("menuitem", name="Personalization").click()
    page.get_by_role("button", name="Manage").click()
    page.get_by_test_id("reset-memories-button").click()
    page.get_by_test_id("confirm-reset-memories-button").click()
    page.locator("div").filter(has_text="Saved memoriesAs you chat").nth(1).click()
    page.get_by_test_id("modal-memories").get_by_test_id("close-button").click()
    page.locator("div").filter(has_text="GeneralGeneralNotificationsPersonalizationApps & ConnectorsOrdersData").nth(1).click()
    page.get_by_role("tablist").get_by_test_id("close-button").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
