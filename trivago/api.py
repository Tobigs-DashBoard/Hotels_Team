import requests, time
import psycopg2

from psycopg2 import sql
from datetime import datetime, timedelta
from utils import functions, datas, dates

def insert_accommodations_to_db(dbname, user, password, host, port, accommodations, arrival, departure, adults, children):
    """
    Inserts accommodation data into a PostgreSQL database.

    Parameters:
    -----------
    dbname : str
        The name of the database to connect to.
    user : str
        The database username.
    password : str
        The database user's password.
    host : str
        The host address of the database (e.g., 'localhost').
    port : str
        The port number of the PostgreSQL database (e.g., '5433').
    accommodations : list of dict
        A list of accommodation data. Each element in the list is a dictionary containing information about an accommodation.
    arrival : str or datetime
        The check-in date for the accommodation.
    departure : str or datetime
        The check-out date for the accommodation.
    adults : int
        The number of adults for the booking.
    children : list
        A list of children accompanying the adults for the booking.
        
    Returns:
    --------
    None
        The function does not return any value, but it inserts the provided accommodation data into the PostgreSQL database.

    Example:
    --------
    insert_accommodations_to_db(
        dbname="hwangil_db",
        user="postgres",
        password="1234",
        host="localhost",
        port="5433",
        accommodations=accommodations_list,
        arrival="2024-09-01",
        departure="2024-09-05",
        adults=2,
        children=[child1, child2]
    )
    """
    
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    cur = conn.cursor()

    for accommodation in accommodations:
        data = {
            'accommodation_name': accommodation['accommodationDetails']['translatedName']['value'],
            'rate': 0.0 if accommodation['formattedRating'] is None else float(accommodation['formattedRating']),
            'review': accommodation['ratingsCount'],
            'nearest_city': '포천',
            'is_domestic': True,
            'check_in': dates.convert_to_datetime(arrival),
            'check_out': dates.convert_to_datetime(departure),
            'check_period': dates.calculate_date_difference(arrival, departure),
            'num_adult': adults,
            'num_child': len(children) if children != [] else 0,
            'price_total': float(accommodation['deals']['best']['pricePerStayObject']['amount']),
            'price_per_day': float(accommodation['deals']['best']['pricePerNight']['amount']),
            'is_breakfast': functions.convert_breakfast(accommodation['deals']['alternatives']),
            'option': '',
            'fetched_date': datetime.today()
        }
        insert_query = '''
        INSERT INTO Accommodation_info (
            accommodation_name, rate, review, nearest_city, is_domestic, check_in, check_out, check_period, 
            num_adult, num_child, price_total, price_per_day, is_breakfast, option, fetched_date
        ) 
        VALUES (
            %(accommodation_name)s, %(rate)s, %(review)s, %(nearest_city)s, %(is_domestic)s, %(check_in)s, 
            %(check_out)s, %(check_period)s, %(num_adult)s, %(num_child)s, %(price_total)s, %(price_per_day)s, 
            %(is_breakfast)s, %(option)s, %(fetched_date)s
        );
        '''
        cur.execute(insert_query, data)
        conn.commit()
        
        cur.close()
    conn.close()

if __name__ == "__main__":
    
    id = datas.get_id("대전")
    
    for i in range(1,31):
        arrival = datetime.today() + timedelta(days=i)
        departure = datetime.today() + timedelta(days=i+1)
        adults=2
        rooms=1
        children=[]
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
        insert_accommodations_to_db(dbname="hwangil_db",
                                    user="postgres",
                                    password="1234",
                                    host="localhost",
                                    port="5433",
                                    accommodations=accommodations,
                                    arrival=arrival,
                                    departure=departure,
                                    adults=adults,
                                    children=children)
