import configparser

headers = {
    'Content-Type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
}

proxies = {
    'http': 'socks5://127.0.0.1:8080',
    'https': 'socks5://127.0.0.1:8080'
}


def get_config(filepath: str) -> dict:
    config = configparser.ConfigParser()
    config.read(filepath, encoding='utf-8-sig')
    items = config._sections
    items = dict(items)
    for item in items:
        items[item] = dict(items[item])
    return items
