from src.utils.utils import get_proxy, get_user_agent
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def find_all_records():
    url = 'https://www.guinnessworldrecords.com.br/records/showcase'
    with sync_playwright() as playwright:
        agent = get_user_agent()

        def handle(route, request):
            headers = {
                **request.headers,
                "user-agent": agent
            }
            route.continue_(headers=headers)

        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.route("**/*", handle)
        page.goto(url)

        page.wait_for_selector("ul.results", timeout=10000)
        results = page.query_selector_all("ul.results > li")

        for result in results:
            href = result.query_selector("a").get_attribute("href")

def get_html_page(url):
    with sync_playwright() as playwright:
        agent = get_user_agent()
        proxy = get_proxy()

        def handle(route, request):
            headers = {
                **request.headers,
                "user-agent": agent
            }
            route.continue_(headers=headers)

        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)

        page.wait_for_selector("ul.results", timeout=10000)
        return page.content()

def export_csv(records):
    pass
