from src.utils.utils import get_proxy, get_user_agent
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

url = 'https://www.guinnessworldrecords.com.br/records/showcase'
def find_all_records():
    with sync_playwright() as playwright:
        page = get_page(playwright, url)
        categories = page.query_selector_all('main#main div.columned-holder')
        for category in categories:
            category_title = category.query_selector('div#columned-text h4').text_content(strip=True)
            category.click()

            records = page.query_selector_all('main#main a.record-grid-item')
            for record in records:
                record_title = record.query_selector('header h3').text_content(strip=True)
                record.click()

                body = page.query_selector('main#main div#news-body-copy')
                if not body:
                    raise ValueError('')

                div_description = body.query_selector('div#body-copy')
                div_detail = body.query_selector('div#record-details-wrap')
                if not div_detail:
                    raise ValueError('')

                obj = {}
                els_detail = div_detail.query_selector_all('dl > div#equal-one')
                for el in els_detail:
                    title_el = el.query_selector('dt').text_content(strip=True)
                    value_el = el.query_selector('dd').text_content(strip=True)
                    obj[title_el] = value_el

                description = ''
                if div_description:
                    els_description = div_description.query_selector_all('p')
                    for p in els_description:
                        description += p.text_content(strip=True) + ' '
                obj['description'] = description

    obj_treated = objs_to_record(obj)
    return obj_treated

def find_records_by_category():
    with sync_playwright() as playwright:
        page = get_page(playwright, url)
        categories = page.query_selector_all('main#main div.columned-holder')
        for category in categories:
            category_title = category.query_selector('div#columned-text h4').text_content(strip=True)
            if category not in category_title:
                continue

            category.click()

            records = page.query_selector_all('main#main a.record-grid-item')
            for record in records:
                record_title = record.query_selector('header h3').text_content(strip=True)
                record.click()

                body = page.query_selector('main#main div#news-body-copy')
                if not body:
                    raise ValueError('')

                div_description = body.query_selector('div#body-copy')
                div_detail = body.query_selector('div#record-details-wrap')
                if not div_detail:
                    raise ValueError('')

                obj = {}
                els_detail = div_detail.query_selector_all('dl > div#equal-one')
                for el in els_detail:
                    title_el = el.query_selector('dt').text_content(strip=True)
                    value_el = el.query_selector('dd').text_content(strip=True)
                    obj[title_el] = value_el

                description = ''
                if div_description:
                    els_description = div_description.query_selector_all('p')
                    for p in els_description:
                        description += p.text_content(strip=True) + ' '
                obj['description'] = description

    obj_treated = objs_to_record(obj)
    return obj_treated

def find_records_by_title(title):
    with sync_playwright() as playwright:
        page = get_page(playwright, url)
        categories = page.query_selector_all('main#main div.columned-holder')
        for category in categories:
            category_title = category.query_selector('div#columned-text h4').text_content(strip=True)
            category.click()

            records = page.query_selector_all('main#main a.record-grid-item')
            for record in records:
                record_title = record.query_selector('header h3').text_content(strip=True)
                if title not in record_title:
                    continue

                record.click()
                body = page.query_selector('main#main div#news-body-copy')
                if not body:
                    raise ValueError('')

                div_description = body.query_selector('div#body-copy')
                div_detail = body.query_selector('div#record-details-wrap')
                if not div_detail:
                    raise ValueError('')

                obj = {}
                els_detail = div_detail.query_selector_all('dl > div#equal-one')
                for el in els_detail:
                    title_el = el.query_selector('dt').text_content(strip=True)
                    value_el = el.query_selector('dd').text_content(strip=True)
                    obj[title_el] = value_el

                description = ''
                if div_description:
                    els_description = div_description.query_selector_all('p')
                    for p in els_description:
                        description += p.text_content(strip=True) + ' '
                obj['description'] = description

    obj_treated = objs_to_record(obj)
    return obj_treated

def get_page(playwright, url):
    user_agent = get_user_agent()
    def handle(route, request):
        headers = {
            **request.headers,
            "user-agent": user_agent
        }
        route.continue_(headers=headers)

    browser = playwright.chromium.launch(headless=False, channel="chrome", args=["--start-maximized"])
    page = browser.new_page(no_viewport=True, ignore_https_errors=True, accept_downloads=True)
    page.route("**/*", handle)
    page.goto(url)
    page.wait_for_selector("main.main", timeout=10000)
    return page

def export_csv(obj_list):
    fieldnames = obj_list[0].__dict__.keys()
    filename = datetime.now().strftime("%y%m%d%H%M%S") + ".csv"
    filepath = os.path.join("/tmp", filename)
    with open(filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for obj in obj_list:
            writer.writerow(obj.__dict__)
    return filepath

def objs_to_record(obj):
    return obj