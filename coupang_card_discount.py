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

    # 반복체크 주기(초)
    sleep_sec = 86400

    # n% 이상 할인시 슬랙으로 알림
    target_per = 8

    # 확인할 쿠팡 상품 페이지 URL
    urls = [f'https://www.coupang.com/vp/products/7630891988?itemId=20252617948&vendorItemId=87340572848&pickType=COU_PICK&q=Apple+%EC%95%A0%ED%94%8C%EC%9B%8C%EC%B9%98+Ultra+2&itemsCount=36&searchId=d1953534bbc74edea4a856cbdde41ce6&rank=1&isAddedCart=']

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
                card_offer_banner = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[1]/div[3]/div[5]/div[1]/div/div[4]/div/div/div/span')
                discount_strings = card_offer_banner.text.split()
                discount_per = int(discount_strings[1].replace('%', ''))
                if target_per <= discount_per:
                    send_slack_webhook(f'쿠팡 카드 할인!! <{url}|{prod_name.text}> [{card_offer_banner.text}]')
            except NoSuchElementException:
                pass

        # n초 대기
        try:
            time.sleep(sleep_sec)
        except KeyboardInterrupt:
            print("Process interrupted by user")
            break

if __name__ == "__main__":
    load_dotenv()
    main()