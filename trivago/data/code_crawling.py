from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time, trivago.tmp.utils as utils





# Chrome 옵션 설정
chrome_options = Options()
#chrome_options.add_argument('--headless')  # 브라우저 창을 띄우지 않고 백그라운드에서 실행 (옵션)
chrome_options.add_argument('--no-sandbox')  # 샌드박스 모드 비활성화
chrome_options.add_argument('--disable-dev-shm-usage')  # DevTools 모드 비활성화

# ChromeDriver 경로 설정 및 드라이버 초기화
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


for num in range(0,320):
    
    url = f"https://www.trivago.co.kr/ko-KR/srl?search=200-{num}%3Bdr-20240822-20240823-s%3Brc-1-2"
    # 웹 페이지 열기
    driver.get(url)
    time.sleep(3)
    file_path = 'trivago/country_code.json'
    # 특정 요소 찾기 및 내용 출력 (예: <h1> 태그)
    try:
        element = driver.find_element(By.TAG_NAME, 'h1')
        element_list = list(element.accessible_name.split())
        
        data = {'names' : element_list[0], 'code' : num}
        
        

        utils.add_data_to_json(file_path, data)
        print("Header text is:", element_list[0], num)


    except Exception as e:
        print("An error occurred:", e)




time.sleep(100)
# 드라이버 종료
driver.quit()
