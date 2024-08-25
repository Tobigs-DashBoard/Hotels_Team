from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time, trivago.tmp.utils as utils





# Chrome 옵션 설정
chrome_options = Options()
#chrome_options.add_argument('--headless')  # 브라우저 창을 띄우지 않고 백그라운드에서 실행 (옵션)
chrome_options.add_argument('--no-sandbox')  # 샌드박스 모드 비활성화
chrome_options.add_argument('--disable-dev-shm-usage')  # DevTools 모드 비활성화

# ChromeDriver 경로 설정 및 드라이버 초기화
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)



    



def scrape_hotel_data():
    # data-testid="accommodation-list-element" 속성을 가진 요소를 찾습니다.
    accommodation_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="accommodation-list-element"]')
    print("서울 호텔 리스트\n")
    # 각 요소에서 호텔 이름과 가격을 추출합니다.
    for element in accommodation_elements:
        # 호텔 이름 추출
        hotel_name = element.find_element(By.CSS_SELECTOR, 'button[data-testid="item-name"] span').text
        
        # 가격 추출
        price = element.find_element(By.CSS_SELECTOR, 'span[data-testid="recommended-price"]').text
        
        # 결과 출력
        print(f'호텔: {hotel_name}')
        print(f'가격: {price}')
        print('---')

if __name__ == "__main__":
    url = f"https://www.trivago.co.kr/ko-KR/srl?search=200-81322;dr-20240821-20240824-s;rc-2-3-7-8"
    # 웹 페이지 열기
    driver.get(url)
    time.sleep(3)
    # 현재 페이지의 호텔 데이터 크롤링
    scrape_hotel_data()

    # 브라우저를 닫습니다.
    driver.quit()