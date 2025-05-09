import traceback
from src.model.record import obj_to_record, RecordError
from playwright.sync_api import sync_playwright
from src.utils.utils import get_proxy, get_user_agent, create_logger, export_csv

url = 'https://www.guinnessworldrecords.com.br/records/showcase'
def get_page(playwright, url):
    page, browser = None, None
    for attempt in range(3):
        try:
            user_agent = get_user_agent()
            def handle(route, request):
                headers = {
                    **request.headers,
                    "user-agent": user_agent
                }
                route.continue_(headers=headers)

            browser = playwright.chromium.launch(headless=True, channel="chrome", args=["--start-maximized"])
            page = browser.new_page(no_viewport=True, ignore_https_errors=True, accept_downloads=True)
            page.route("**/*", handle)
            page.goto(url)
            page.wait_for_selector("main.main", timeout=10000)
            return page
        except Exception as ex:
            if page:
                page.close()
            if browser:
                browser.close()
            if attempt == 2:
                return str(ex)

def find_records_by_category(category_param):
    objs = []
    with sync_playwright() as playwright:
        page = get_page(playwright, url)
        if isinstance(page, str):
            raise ValueError(page)

        categories = page.query_selector_all('main#main div.columned-holder')
        hrefs = [link.query_selector("a").get_attribute("href") for link in categories if link.query_selector("a")]
        for i, href in enumerate(hrefs):
            category = categories[i]
            category_title = category.query_selector('div.columned-text div.container h4').text_content()
            if category_param.lower() not in category_title.lower():
                continue

            link = f"https://www.guinnessworldrecords.com.br{href}"
            records = extract_record_by_category(page, link, category_title)
            objs.extend(records)
            page.close()
            return objs

    if not objs:
        raise ValueError(f'Sem recordes para a categoria {category_param}')

def extract_record_by_category(page, link, category_title):
    obj, objs = {}, []
    page.goto(link)
    page.wait_for_load_state("load")
    page.wait_for_selector("main#main a.record-grid-item", timeout=10000)
    records = page.query_selector_all('main#main a.record-grid-item')

    hrefs = [link.get_attribute("href") for link in records if link.get_attribute("href")]
    for i, href in enumerate(hrefs):
        link = f"https://www.guinnessworldrecords.com.br{href}"
        obj = extract_record(page, link, category_title)
        if obj:
            objs.append(obj)

        page.go_back()
        page.wait_for_load_state("load")
    return objs

def extract_record(page, link, category_title=None):
    obj = {}
    try:
        page.goto(link)
        page.wait_for_load_state("load")

        page.wait_for_selector("main#main div.news-body-copy", timeout=10000)

        header = page.query_selector('main#main header.page-title')
        body = page.query_selector('main#main div.news-body-copy')

        record_title = header.query_selector('div.container h1').text_content()
        div_description = body.query_selector('div.body-copy')
        div_detail = body.query_selector('div.record-details-wrap')
        if not div_detail:
            raise ValueError('Detalhes do Record não foram encontrados!')

        els_detail = div_detail.query_selector_all('dl > div.equal-one')
        for el in els_detail:
            title_el = el.query_selector('dt').text_content().strip()
            value_el = el.query_selector('dd').text_content().strip()
            obj[title_el] = value_el

        description = ''
        if div_description:
            els_description = div_description.query_selector_all('p')
            for p in els_description:
                description += p.text_content().strip() + ' '
        obj['Descricao'] = description
        obj['Titulo'] = record_title
        obj['Categoria'] = category_title
        obj = obj_to_record(obj)
        return obj
    except Exception as ex:
        return RecordError(err= str(ex))