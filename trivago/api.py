import requests, time

from utils import functions, datas


if __name__ == "__main__":
    id = datas.get_id("포천")
    arrival="20240901"
    departure="20240902"
    adults=1
    rooms=1
    children=[6]
    url = functions.get_url()
    payload = functions.get_payload(id=id,
                                    arrival=arrival,
                                    departure=departure,
                                    adults=adults,
                                    rooms=rooms,
                                    children=children)
    headers = functions.get_headers(id=id,
                                    arrival=arrival,
                                    departure=departure,
                                    adults=adults,
                                    rooms=rooms,
                                    children=children)
    
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    #print(response_data['data']['accommodationSearchResponse']['accommodations'])

    time.sleep(5)
    #숙소명
    print(response_data['data']['accommodationSearchResponse']['accommodations'][0]['accommodationDetails']['translatedName']['value'])
    # 가격
    print(response_data['data']['accommodationSearchResponse']['accommodations'][0]['deals']['best']['pricePerNight']['amount'])
    # 위치
    print(response_data['data']['accommodationSearchResponse']['accommodations'][0]['distanceLabel']['value'])

