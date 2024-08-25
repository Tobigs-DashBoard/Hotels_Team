

def get_url():
    url = "https://www.trivago.co.kr/graphql"
    return url


def process_date(date:str) -> str:
    if len(date) != 8:
        raise ValueError
    
    date_str = f"{date[:4]}-{date[4:6]}-{date[6:]}"

    return date_str

def distribute_rooms(adults, rooms, children=[]):
    # 조건 검증
    if adults < 1:
        raise ValueError("성인의 수는 최소 1명 이상이어야 합니다.")
    if rooms < 1:
        raise ValueError("방의 수는 최소 1개 이상이어야 합니다.")
    if rooms > adults:
        raise ValueError("방의 수는 성인의 수보다 많을 수 없습니다.")

    result = []
    
    # 각 방에 성인과 어린이 배치
    for room in range(rooms):
        room_allocation = {"adults": 0, "children": []}
        
        # 첫 번째 방에는 가능한 많은 성인과 어린이를 배치
        if room == 0:
            room_allocation["adults"] = min(adults, 2)  # 최대 2명의 성인 배치
            adults -= room_allocation["adults"]
            
            # 첫 번째 방에 최대 2명의 어린이를 배치
            max_children_in_first_room = 2
            while children and len(room_allocation["children"]) < max_children_in_first_room:
                room_allocation["children"].append(children.pop(0))
        else:
            # 나머지 방에 남은 성인과 어린이를 배치
            if adults > 0:
                room_allocation["adults"] = 1
                adults -= 1
            
            if children:
                room_allocation["children"].append(children.pop(0))
            else:
                room_allocation["children"] = []  # 어린이가 없는 경우 빈 리스트로 설정
        
        result.append(room_allocation)
    
    return result


def get_payload(id:int, arrival:str, departure:str, adults:int, rooms:int,children=[], min_price=0, max_price=2147483647):
    arrival = process_date(arrival)
    departure = process_date(departure)
    room_info = distribute_rooms(adults, rooms, children)
    payload = {
        "operationName": "accommodationSearchQuery",
        "variables": {
            "pollData": None,
            "params": {
                "uiv": [{"nsid": {"ns": 200, "id": id}}],
                "stayPeriod": {"arrival": arrival, "departure": departure},
                "limit": 35,
                "dealsLimit": 3,
                "offset": 0,
                # 분배 법칙이 있음
                "rooms": room_info,
                "sorting": [{"type": 0}],
                "currency": "KRW",
                "applicationGroup": "MAIN_WARP",
                "budgetRestriction": {
                    "budgetType": "PRICE_PER_NIGHT",
                    "minPrice": min_price,
                    "maxPrice": max_price
                },
                "priceTypeRestrictions": [1],
                "includePriceHistogram": True,
                "channel": {
                    "branded": {
                        "isStandardDate": True,
                        "stayPeriodSource": {"value": 0}
                    }
                },
                "deviceType": "DESKTOP_CHROME"
            },
            "distanceLabelInput": None,
            "priceSliderParams": {
                "currency": "KRW",
                "priceHistogramAlgorithmType": "LINEAR"
            },
            "forecastedPricesInput": None,
            "monthlyForecastedPricesInput": {
                "currencyCode": "KRW",
                "filter": [
                    {"priceType": "CHEAPEST", "yearMonth": "2024-09"},
                    {"priceType": "CHEAPEST", "yearMonth": "2024-10"},
                    {"priceType": "CHEAPEST", "yearMonth": "2024-11"},
                    {"priceType": "CHEAPEST", "yearMonth": "2024-12"},
                    {"priceType": "CHEAPEST", "yearMonth": "2025-01"},
                    {"priceType": "CHEAPEST", "yearMonth": "2025-02"}
                ]
            },
            "shouldIncludeFreeWiFiStatus": False,
            "shouldIncludeSEOIndexation": False,
            "shouldIncludeCanonicalURL": False,
            "shouldIncludeEligiblePartners": True,
            "shouldIncludeForecastedPrices": False,
            "shouldIncludeMonthlyForecastedPrices": True,
            "shouldIncludeSearchAreaPolygon": False,
            "isBomCTestActive": False,
            "bookOnMetaDealCheckInput": {
                # adults 배열 첫 번째
                "rooms": room_info[0]
            },
            "shouldIncludePlusStudioSubscription": True,
            "shouldIncludeAiGeneratedHighlights": False,
            "shouldIncludeRoomTypeInfo": True,
            "shouldIncludePriceRestrictions": False,
            "shouldIncludeRestrictedDeals": False,
            "shouldIncludeFreeSearchDetails": False,
            "isPriceDropActive": False
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "845ba83784595010f4be0db3906b840a925e45c0078bb55d675c6aa824b5ce1c"
            }
        }
    }

    return payload


def get_headers(id:int, arrival:str, departure:str, rooms:int, adults:int, children=[]) -> dict:
    str_children = ""
    for age in children:
        str_children += f"-{str(age)}"

    headers = {
        # 바꿀 필요 X
        #"accept": "multipart/mixed, application/graphql-response+json, application/graphql+json, application/json",
        #"accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "apollographql-client-name": "hs-web-app",
        "apollographql-client-version": "ff962f1b",
        #"content-length": "473",
        "content-type": "application/json",
        #"origin": "https://www.trivago.co.kr",
        #"priority": "u=1, i",
        "referer": f"https://www.trivago.co.kr/ko-KR/srl?search=200-{str(id)};dr-{arrival}-{departure};rc-{str(rooms)}-{str(adults)}{str_children}",
        #"sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
        #"sec-ch-ua-mobile": "?0",
        #"sec-ch-ua-platform": "\"macOS\"",
        #"sec-fetch-dest": "empty",
        #"sec-fetch-mode": "cors",
        #"sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        #"x-trv-app-id": "HS_WEB_APP_WARP",
        #"x-trv-connection-id": "ShANUXGpqB9RIh8E2whHHme3Gks",
        #"x-trv-cst": "46164,48405,51886,52345,53192,70064,70089,70187,70218,70290,70222,70332,70418,70421,70411,70410,70407,70481,70443,70505-1,70525,70473,70579,70504,70536,70620-2,70598,70645,70586,70649,70709,70727,70787-1,70827,70703,70831,70766,70805,70871,70780,70885,70830,70928-4,70810,70940,70886,70941,70919,70834,70706,70806,70738,70951,70934-2,70907,71010,70933,70992,70953,71007,71013,71011,71035,70931,71033,70916,71044,71043,71019,70850,71042,71067,71018",
        #"x-trv-language": "ko-KR",
        #"x-trv-platform": "kr",
        #"x-trv-sequence-id": "52",
        "x-trv-tid": "29aaf309c268ace93fd7293d53"
    }

    return headers