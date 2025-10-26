from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

load_dotenv()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    page = context.new_page()
    
    page.goto("https://chatgpt.com/")
    page.get_by_test_id("login-button").click()
    page.get_by_role("textbox", name="Email address").fill(os.getenv("CHATGPT_EMAIL"))
    page.get_by_role("button", name="Continue", exact=True).click()
    page.get_by_role("textbox", name="Password").fill(os.getenv("CHATGPT_PASSWORD"))
    page.get_by_role("button", name="Continue", exact=True).click()
    
    input("Press Enter after completing any 2FA...")
    
    context.storage_state(path="storage/auth_state.json")
    browser.close()