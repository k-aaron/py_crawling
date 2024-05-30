import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# 메인 함수
def main():

    query = input('검색할 키워드를 입력하세요: ')

    # 반품상품 확인할 쿠팡 상품 페이지 URL
    urls = [f'https://www.google.com']

    for url in urls:
        # 크롬드라이버 실행
        driver = webdriver.Chrome()

        # 크롬 드라이버에 url 주소 넣고 실행
        driver.get(url)

        # 페이지가 완전히 로딩되도록 3초동안 기다림
        time.sleep(3)

        try:
            search_box = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
            search_box.send_keys(query)
            search_box.send_keys(Keys.ENTER)
            print(f'완료!!')
        except NoSuchElementException:
            pass

if __name__ == "__main__":
    main()
