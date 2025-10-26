from playwright.sync_api import sync_playwright

def launch_browser_with_auth(
    storage_state_path: str = "storage/auth_state.json",
    location: dict = None,
    proxy: dict = None
):
    """
    Launch browser with location/proxy override.
    
    Args:
        location: {"latitude": 37.7749, "longitude": -122.4194} for SF
        proxy: {"server": "http://proxy-server:port", "username": "user", "password": "pass"}
    """
    playwright = sync_playwright().start()
    
    browser = playwright.chromium.launch(
        headless=False,
        args=['--disable-blink-features=AutomationControlled'],
        proxy=proxy
    )
    
    context_options = {
        "storage_state": storage_state_path,
        "viewport": {"width": 1280, "height": 720},
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    if location:
        context_options["geolocation"] = location
        context_options["permissions"] = ["geolocation"]
    
    context = browser.new_context(**context_options)
    page = context.new_page()
    
    return playwright, browser, context, page