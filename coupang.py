import os
import requests
import json
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# 슬랙으로 메시지를 보내는 함수
def send_slack_webhook(text):
    # Webhook URL
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    # 메시지 데이터
    message_data = {
        "text": text
    }

    # HTTP POST 요청 보내기
    response = requests.post(
        webhook_url,
        headers = {'Content-Type': 'application/json'},
        data = json.dumps(message_data)
    )

    # 응답 확인
    if response.status_code == 200:
        print('Message sent successfully')
    else:
        print(f'Failed to send message. Status code: {response.status_code}, Response: {response.text}')

# 메인 함수
def main():

    # 반품상품 확인할 쿠팡 상품 페이지 URL
    urls = [f'https://www.coupang.com/vp/products/1175382107?itemId=2154072063&vendorItemId=70152352732&sourceType=srp_product_ads&clickEventId=e4f86a30-1e5a-11ef-950f-6652dce19e95&korePlacement=15&koreSubPlacement=1&q=%EB%B0%A9%EB%AC%B8%EC%86%90%EC%9E%A1%EC%9D%B4&itemsCount=36&searchId=30ce0f6647d54fb0b59628968933c54a&rank=0&isAddedCart=',
        f'https://www.coupang.com/vp/products/2087516486?itemId=3545917205&vendorItemId=74943849351&q=%EB%B0%A9%EB%AC%B8%EC%86%90%EC%9E%A1%EC%9D%B4&itemsCount=36&searchId=30ce0f6647d54fb0b59628968933c54a&rank=1&isAddedCart=']

    while True:
        for url in urls:
            # 크롬드라이버 실행
            driver = webdriver.Chrome()

            # 크롬 드라이버에 url 주소 넣고 실행
            driver.get(url)

            # 페이지가 완전히 로딩되도록 3초동안 기다림
            time.sleep(3)

            prod_name = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[1]/div[3]/div[3]/h2')
            try:
                prod_offer_banner = driver.find_element(By.XPATH, '//*[@id="prod-offer-banner"]/a/div')
                if "반품" in prod_offer_banner.text:
                    send_slack_webhook(f'쿠팡 반품 상품 발견!! [{prod_name.text}][{prod_offer_banner.text}]')
            except NoSuchElementException:
                pass

        # n초 대기
        try:
            time.sleep(600)
        except KeyboardInterrupt:
            print("Process interrupted by user")
            break

if __name__ == "__main__":
    load_dotenv()
    main()
