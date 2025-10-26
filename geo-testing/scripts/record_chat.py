from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="storage/auth_state.json", viewport={"width":1280,"height":720})
    page = context.new_page()
    page.goto("https://chatgpt.com/")
    page.locator("#prompt-textarea").click()
    page.get_by_test_id("send-button").click()
    expect(page.get_by_test_id("conversation-turn-2")).to_contain_text("Here’s a great coffee spot you might like: Broadsheet Coffee Roasters 4.6•Coffee Shop•Closed Location: 100 Kirkland St, Cambridge, MA (near Harvard Yard) Why it’s good: They’re a local roaster doing specialty-coffee, so you’ll get something high quality. Broadsheet Coffee Roasters+2Off the Beaten Path Food Tours+2 It’s in a convenient Cambridge location, easy to pop into. The atmosphere looks clean, modern, good for a quick stop or a short work-session. Tip: If you like to explore flavor profiles ask the barista for a recommendation — being a roaster they’ll likely have interesting options beyond standard drip. Heads up: Since it’s a specialty café, the prices may be a bit higher than your standard chain, and seating might fill up during peak morning/afternoon hours. If you tell me what neighborhood you're in, or what vibe you’re going for (quiet study, laptop-friendly, scenic, with pastries, etc.) I can pull 2-3 options that match your preferences.")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
