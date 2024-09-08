# trivago
---
- site : https://www.trivago.co.kr/

## 크롤링 방법

트리바고의 내부 api를 가져오는 방식을 취해서 웹사이트를 크롤링하는 방식에 비해 매우 빠르게 가져올 수 있는 방식

### 예시
- 지역날짜 : 대전
- 시작날짜 : 20241011
- 종료날짜 : 20241012
- 객실 수 : 1
- 성인 수 : 2

### 실행 방법
```python
api.py 
```

### 실행결과
DB에 내일을 기준으로 특정 지역에 있는 숙소에 대해 1박당 가격 추이에 대해 31일을 추적함

### 설명
- 파일 실행시 A 숙소에 대해 10월 2일 기준으로 31일간 1박당 가격추이 DB에 추가함. 이를 통해 각 숙소에 대해 어느 요일이 얼마나 비싼지를 그래프를 통해 확인할 수 있음.

# Table

| 컬럼명 | 데이터타입 | 설명 | 예시 |
| --- | --- | --- | --- |
| accommodation_name | varchar | 숙소 이름 |  |
| rate | float | 숙소 별점 |  |
| review | integer | 숙소 리뷰 수 |  |
| nearest_city | varchar | 가까운 도시 이름 |  |
| is_domestic | boolean | 국내 숙소 인가 |  |
| check_in | date | 체크인 날짜 |  |
| check_out | date | 체크아웃 날짜 |  |
| check_period | integer | 머무는 기간 |  |
| num_adult | integer | 성인 수 |  |
| num_child | integer | 어린이 수 |  |
| price_total | float | 총 가격 |  |
| price_per_day | float | 1박당 가격 |  |
| is_breakfast | boolean | 조식 여부 |  |
| option | text | 부가 옵션 |  |
| fetched_date | date | 수집 날짜 |  |