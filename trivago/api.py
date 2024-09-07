import requests, time
import psycopg2

from psycopg2 import sql
from datetime import datetime
from utils import functions, datas, dates


if __name__ == "__main__":
    
    id = datas.get_id("포천")
    arrival="20241001"
    departure="20241003"
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


    time.sleep(2)
    accommodations = response_data['data']['accommodationSearchResponse']['accommodations']
    
    conn = psycopg2.connect(
        dbname="hwangil_db",
        user="postgres",
        password="1234",
        host="localhost",
        port="5433"
    )
    
    cur = conn.cursor()
    
    for accomodation in accommodations:
        data = {
            'accommodation_name': accomodation['accommodationDetails']['translatedName']['value'],
            'rate': 0.0 if accomodation['formattedRating'] == None else float(accomodation['formattedRating']),
            'review': accomodation['ratingsCount'],
            'nearest_city': '포천',
            'is_domestic': True,
            'check_in': dates.convert_to_datetime(arrival),
            'check_out': dates.convert_to_datetime(departure),
            'check_period': dates.calculate_date_difference(arrival, departure),
            'num_adult': adults,
            'num_child': len(children),
            'price_total': float(accomodation['deals']['best']['pricePerStayObject']['amount']),
            'price_per_day': float(accomodation['deals']['best']['pricePerNight']['amount']),
            'is_breakfast': functions.convert_breakfast(accomodation['deals']['alternatives']),
            'option': '',
            'fetched_date': datetime.today()
        }
        insert_query = '''
        INSERT INTO Accommodation_info (accommodation_name, rate, review, nearest_city, is_domestic, check_in, check_out, check_period, num_adult, num_child, price_total, price_per_day, is_breakfast, option, fetched_date) 
        VALUES (%(accommodation_name)s, %(rate)s, %(review)s, %(nearest_city)s, %(is_domestic)s, %(check_in)s, %(check_out)s, %(check_period)s, %(num_adult)s, %(num_child)s, %(price_total)s, %(price_per_day)s, %(is_breakfast)s, %(option)s, %(fetched_date)s);
        '''
        cur.execute(insert_query, data)
        conn.commit()
    cur.close()
    conn.close()
    #숙소명
    print(response_data['data']['accommodationSearchResponse']['accommodations'][0]['accommodationDetails']['translatedName']['value'])
    # 가격
    print(response_data['data']['accommodationSearchResponse']['accommodations'][0]['deals']['best']['pricePerNight']['amount'])
    # 위치
    print(response_data['data']['accommodationSearchResponse']['accommodations'][0]['distanceLabel']['value'])
    

    
