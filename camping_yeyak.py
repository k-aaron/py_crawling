import os
import requests
import json
import time
import random
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime

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
    sleep_seconds = [10, 14, 18, 22, 30, 33, 41, 45, 49, 55, 60, 67, 73, 79, 85, 90, 97, 104, 111, 116, 120]

    # 확인할 페이지 URL
    urls = [f'https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S240503153510301175&code=T500&dCode=T502&sch_order=1&sch_choose_list=&sch_type=&sch_text=%EB%82%9C%EC%A7%80&sch_recpt_begin_dt=&sch_recpt_end_dt=&sch_use_begin_dt=&sch_use_end_dt=&svc_prior=N&sch_reqst_value=']
    check_dates = ['20240622', '20240629']

    while True:
        for url in urls:
            # 크롬드라이버 실행
            driver = webdriver.Chrome()

            # 크롬 드라이버에 url 주소 넣고 실행
            driver.get(url)

            # 페이지가 완전히 로딩되도록 3초동안 기다림
            time.sleep(3)

            # 현재 예약 개수
            current_cnt = 0

            # 예약 가능 개수
            available_cnt = 0
            
            for check_date in check_dates:
                try:
                    status_value = driver.find_element(By.XPATH, f'//*[@id="div_cal_{check_date}"]/span')
                    split_strings = status_value.text.split('/')
                    current_cnt = split_strings[0]
                    available_cnt = split_strings[1]
                    if current_cnt < available_cnt:
                        # 슬랙으로 메시지 보내기
                        send_slack_webhook(f'[{check_date}][예약현황:{status_value.text}] 예약가능! \n {url}')
                    else:
                        print(f'[{datetime.today().strftime("%Y-%m-%d %H:%M:%S")}][{check_date}][예약현황:{status_value.text}] 예약불가.')

                # 예외 처리
                except NoSuchElementException:
                    pass

        # n초 대기
        try:
            sleep_sec = sleep_seconds[random.randint(0, len(sleep_seconds))]
            print(f'({sleep_sec}초 대기)')
            time.sleep(sleep_sec)
        except KeyboardInterrupt:
            print("Process interrupted by user")
            break

if __name__ == "__main__":
    load_dotenv()
    main()