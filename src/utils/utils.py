from fake_useragent import UserAgent

def get_proxy():
    proxies = [
        "http://127.0.0.1:8080"
    ]
    return proxies[0]

def get_user_agent():
    ua = UserAgent()
    return ua.chrome