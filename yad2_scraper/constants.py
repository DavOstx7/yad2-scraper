BASE_URL = "https://www.yad2.co.il"

DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
    "Cache-Control": "max-age=0",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
}

ALLOW_REQUEST_REDIRECTS = True
VERIFY_REQUEST_SSL = True

ANTIBOT_CONTENT_IDENTIFIER = b"Are you for real"  # robot-captcha
YAD2_CONTENT_IDENTIFIER = b"https://www.yad2.co.il/"

FIRST_PAGE_NUMBER = 1
NOT_MENTIONED_PRICE_RANGE = 0, 0

NEXT_DATA_SCRIPT_ID = "__NEXT_DATA__"
