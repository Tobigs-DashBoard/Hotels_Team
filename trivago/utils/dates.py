from datetime import datetime

def calculate_date_difference(arrival: str, departure: str) -> int:
    """
    주어진 두 날짜의 차이를 계산하는 함수.

    Args:
        arrival (str): 도착 날짜 (형식: YYYYMMDD)
        departure (str): 출발 날짜 (형식: YYYYMMDD)

    Returns:
        int: 두 날짜 사이의 일 수
    """
    # 문자열을 날짜 형식으로 변환
    arrival_date = datetime.strptime(arrival, "%Y%m%d")
    departure_date = datetime.strptime(departure, "%Y%m%d")
    
    # 날짜 차이 계산
    date_difference = departure_date - arrival_date
    
    # 날짜 차이를 반환 (일 단위)
    return date_difference.days


def convert_to_datetime(date_str: str) -> datetime:
    """
    주어진 날짜 문자열을 datetime 객체로 변환하는 함수.

    Args:
        date_str (str): 날짜 문자열 (형식: YYYYMMDD)

    Returns:
        datetime: 변환된 datetime 객체
    """
    year = int(date_str[:4])    # 연도 부분 추출
    month = int(date_str[4:6])  # 월 부분 추출
    day = int(date_str[6:])     # 일 부분 추출
    
    # datetime 객체로 변환
    return datetime(year, month, day)