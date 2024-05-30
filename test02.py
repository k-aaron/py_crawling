import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'https://www.google.co.kr/'

# 브라우저 꺼짐 방지 옵션
#https://rimeestore.tistory.com/entry/%EC%85%80%EB%A0%88%EB%8B%88%EC%9B%80-%EB%B8%8C%EB%9D%BC%EC%9A%B0%EC%A0%80%EA%B0%80-%EA%B3%84%EC%86%8D-%EA%BA%BC%EC%A7%88-%EB%95%8C
chrome_option = Options()
chrome_option.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_option)
#driver.implicitly_wait(300)

# 웹페이지 해당 주소 이동
driver.get(url)

print(driver.current_url)

#time.sleep(10)
#driver.close()
