from src.utils.utils import get_proxy, get_user_agent
from playwright.sync_api import sync_playwright
from src.model.record import obj_to_record

url = 'https://www.guinnessworldrecords.com.br/records/showcase'
def find_all_records():
    obj, objs = {}, []
    with sync_playwright() as playwright:
        page = get_page(playwright, url)
        if isinstance(page, str):
            raise ValueError(page)

        categories = page.query_selector_all('main#main div.columned-holder')
        for category in categories:
            category_title = category.query_selector('div.columned-text div.container h4').text_content().strip()
            obj['Categoria'] = category_title

            category.click()
            page.wait_for_selector("main#main a.record-grid-item", timeout=10000)
            records = page.query_selector_all('main#main a.record-grid-item')

            if not records:
                raise ValueError('Nenhum Record encontrado!')

            for record in records:
                record_title = record.query_selector('header h3').text_content().strip()
                obj['Titulo'] = record_title

                record.click()
                page.wait_for_selector("main#main div.news-body-copy", timeout=10000)
                body = page.query_selector('main#main div.news-body-copy')

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
                obj = obj_to_record(obj)
                objs.append(obj)
    return objs

def find_records_by_record_category(category_param):
    obj, objs = {}, []
    with sync_playwright() as playwright:
        page = get_page(playwright, url)
        if isinstance(page, str):
            raise ValueError(page)

        categories = page.query_selector_all('main#main div.columned-holder')
        for category in categories:
            category_title = category.query_selector('div.columned-text div.container h4').text_content().strip()
            if category_param not in category_title:
                continue
            obj['Categoria'] = category_title

            category.click()
            page.wait_for_selector("main#main a.record-grid-item", timeout=10000)
            records = page.query_selector_all('main#main a.record-grid-item')

            if not records:
                raise ValueError('Nenhum Record encontrado!')

            for record in records:
                record_title = record.query_selector('header h3').text_content().strip()
                obj['Titulo'] = record_title

                record.click()
                page.wait_for_selector("main#main div.news-body-copy", timeout=10000)
                body = page.query_selector('main#main div.news-body-copy')

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
                obj = obj_to_record(obj)
                objs.append(obj)
    return objs

def find_records_by_record_title(title_param):
    obj, objs = {}, []
    with sync_playwright() as playwright:
        page = get_page(playwright, url)
        if isinstance(page, str):
            raise ValueError(page)

        categories = page.query_selector_all('main#main div.columned-holder')
        for category in categories:
            category_title = category.query_selector('div.columned-text div.container h4').text_content().strip()
            obj['Categoria'] = category_title

            category.click()
            page.wait_for_selector("main#main a.record-grid-item", timeout=10000)
            records = page.query_selector_all('main#main a.record-grid-item')

            if not records:
                raise ValueError('Nenhum Record encontrado!')

            for record in records:
                record_title = record.query_selector('header h3').text_content().strip()
                if record_title not in title_param:
                    continue
                obj['Titulo'] = record_title

                record.click()
                page.wait_for_selector("main#main div.news-body-copy", timeout=10000)
                body = page.query_selector('main#main div.news-body-copy')

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
                obj = obj_to_record(obj)
                objs.append(obj)
    return objs

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