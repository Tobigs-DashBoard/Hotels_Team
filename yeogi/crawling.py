"""1. 모듈 임포트"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import requests
from bs4 import BeautifulSoup
import re
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta

"""2. chrome 옵션 설정"""

chrome_options = Options()
chrome_options.add_argument("--headless")  # Headless 모드 설정 (브라우저 UI 없이 실행)
chrome_options.add_argument("--no-sandbox")  # 샌드박스 모드 비활성화
chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 비활성화
chrome_options.add_argument("--disable-gpu")  # GPU 비활성화
chrome_options.add_argument("--window-size=1920x1080")  # 윈도우 크기 설정
chrome_options.add_argument('--disable-extensions')  # 브라우저 확장 기능 비활성화
chrome_options.add_argument('--no-sandbox')  # 샌드박스 비활성화
chrome_options.add_argument('--remote-debugging-port=9222')  # 디버깅 포트 설정
chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--incognito")  # 시크릿 모드로 브라우저 실행

"""3. 국내 숙소 크롤링"""

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 총 검색 호텔 개수 및 총 검색 페이지 수 계산
def get_total_page_num(url):
  url_page = url + str(1)
  driver.get(url_page)
  html = driver.page_source
  soup = BeautifulSoup(html, "html.parser")

  try:
      WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "header.css-1psit91 h1")))
      h1_tag = driver.find_element(By.CSS_SELECTOR, "header.css-1psit91 h1")
      total_result_text = h1_tag.text.strip()
      total_result_num = "".join(char for char in total_result_text if char.isdigit())
      print("총 검색 호텔 개수:", total_result_num)
      return int(total_result_num) // 20 + 1

  except Exception as e:
      print(f"Error in get_total_page_num: {e}")
      return 0

# 날짜 차이 계산
def calculate_nights(start_date, end_date):

    checkin_date = datetime.strptime(start_date, '%Y-%m-%d')
    checkout_date = datetime.strptime(end_date, '%Y-%m-%d')

    duration = checkout_date - checkin_date

    return duration.days

# 크롤링 함수
def Crawling_domestic(url, total_page_num,  conn, cur):
    hotel_data = []
    link_list = []
    price_dict = {}

    for page_num in range(1, total_page_num+1):
        url_Crawling = url + str(page_num)
        driver.get(url_Crawling)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # 모든 상품 가져오기
        items = soup.select(".gc-thumbnail-type-seller-card")
        print(f"Found {len(items)} items on page {page_num}")

        # 유효한 상품 리스트 초기화
        valid_items = []

        # 가격 가져오기 및 필터링
        for item in items:

            # item 내에 가격이 있는지 확인
            price = item.select_one(".css-5r5920")
            price = "" if not price else price.text.strip()

            if price:
                # 가격이 있을 경우에만 유효한 상품 리스트에 추가
                price = int(price.replace(',', ''))
                valid_items.append(item)

                # 상품 접속 링크 가져오기
                link = f"https://www.yeogi.com{item.get('href')}"
                link_list.append(link)

                # 가격과 링크 딕셔너리에 저장
                price_dict[link] = price

    # 상세 페이지 접속
    for link in link_list:
        driver.get(link)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        try:
            # 호텔 이름 추출
            name = driver.find_element(By.XPATH, "//section[@aria-label='숙소 개요']//h1")
            name = "" if not name else name.text.strip()

            # 평점 추출
            wait = WebDriverWait(driver, 10)
            rating = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='review']/div[2]/div[1]/div/h2")))
            rating = rating.text.strip()  # 텍스트를 먼저 추출
            rating = re.search(r'\d+\.\d+', rating)  # 텍스트에서 숫자 추출
            rating = rating.group() if rating else "" 

            # 리뷰 수 추출
            review = driver.find_element(By.XPATH, "//section[@aria-label='리얼 리뷰']//div[2]//span")
            review = "" if not review else review.text.strip()
            match = re.search(r'(\d{1,3}(?:,\d{3})*)개 리뷰', review)
            review_count = match.group(1)
            review_count = int(review_count.replace(',', ''))

            # 방 가격
            room_price = price_dict[link]

            # 부가 옵션
            option_list = []
            room_options = driver.find_elements(By.XPATH, "//*[@id='amenity']//div//span")

            for room_option in room_options:
                option_text = room_option.text.strip()
                if option_text:  # 빈 텍스트 제외
                    option_list.append(option_text)

            option_ = ', '.join(option_list)

            # 국내/해외
            is_domestic = True

            # 머무는 기간
            period = calculate_nights(start_date, end_date)

            # 1박 당 가격
            price_per_day = int(room_price)/int(period)

            # 조식
            is_breakfast = False

            insert_time = datetime.now()

            # PostgreSQL에 데이터 삽입
            insert_query = sql.SQL("""
                INSERT INTO Accommodation_info (accommodation_name, rate, review, nearest_city, is_domestic, check_in,
                check_out, check_period, num_adult, num_child, price_total, price_per_day, is_breakfast, option, fetched_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """)

            try:
                cur.execute(insert_query, (name, rating, review_count, region, is_domestic, start_date, end_date, period, adult, child, room_price, price_per_day, is_breakfast, option_, insert_time))
                conn.commit()  # Commit after each insert
                print(f"Data inserted and committed for: {name}")
            except Exception as e:
                print(f"SQL 실행 중 오류 발생: {e}")

        except Exception as e:
            print(f"호텔 정보 추출 중 오류 발생: {e}")

    print("All data committed to the database.")
    return 0

"""4. main 함수"""

# 도시
cities = ['서울']

# 성인 및 아동 수 조합
people_combinations = [
    {'adults': 1, 'children': 1},
    {'adults': 2, 'children': 0},
    {'adults': 3, 'children': 0},
    {'adults': 4, 'children': 0},
    {'adults': 2, 'children': 2}
]

# 시작 날짜와 종료 날짜 설정
base_start_date = '2024-12-01'
base_end_date = '2024-12-31'
base_start_date_dt = datetime.strptime(base_start_date, '%Y-%m-%d')
base_end_date_dt = datetime.strptime(base_end_date, '%Y-%m-%d')

if __name__ == "__main__":

    current_date = base_start_date_dt

    while current_date <= base_end_date_dt:
        for city in cities:
            region = city

            for people in people_combinations:  # 성인/아동 수 조합을 계산
                adult = people['adults']  # 성인 수
                child = people['children']  # 아동 수
                person = adult + child

                # 체크인 날짜 설정
                start_date = current_date.strftime('%Y-%m-%d')

                # 체크아웃 날짜는 체크인 날짜의 1박 후
                end_date = (current_date + timedelta(days=1)).strftime('%Y-%m-%d')

                url = f"https://www.yeogi.com/domestic-accommodations?searchType=KEYWORD&keyword={region}&autoKeyword=&checkIn={start_date}&checkOut={end_date}&personal={person}&freeForm=false&page="
                total_page_num = get_total_page_num(url)
                print(f"총 검색 페이지 개수: {total_page_num} - {region} - {start_date} ~ {end_date}")

                # PostgreSQL 연결
                conn = psycopg2.connect(
                    dbname="yeogi_db",
                    user="suji",
                    password="tnwl1210!!",
                    host="yeogi-db-instance.crweyyo6wvel.ap-northeast-2.rds.amazonaws.com",
                    port="5432"
                )
                # DB와 상호작용하는 커서 (INSERT, DELETE 등)
                cur = conn.cursor()

                # 크롤러 작동
                if total_page_num > 0:
                    Crawling_domestic(url, total_page_num, conn, cur)

                # 커서와 연결 종료
                cur.close()
                conn.close()

        # 다음 날짜로 이동
        current_date += timedelta(days=1)

    print("Database connection closed.")