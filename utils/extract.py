from playwright.sync_api import sync_playwright


def extract_full_body_html(from_url, wait_for="None"):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url=from_url)
        page.wait_for_load_state(state='networkidle')
        page.evaluate("() => window.scroll(0, document.body.scrollHeight)")
        page.wait_for_load_state(state="domcontentloaded")
        if wait_for:
            page.wait_for_selector(wait_for)
        # page.screenshot(path="steam.png", full_page=True)
        html = page.inner_html("body")
        return html