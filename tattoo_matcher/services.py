# /tattoo_matcher/services.py

import requests
import os

def fetch_tattoo_artists():
    nocodb_url = os.getenv('NOCODB_URL')
    nocodb_api_key = os.getenv('NOCODB_API_KEY')
    nocodb_artist_table_id = os.getenv('NOCODB_ARTIST_TABLE_ID')
    headers = {
        'xc-token': nocodb_api_key
    }
    response = requests.get(f'{nocodb_url}/api/v2/tables/{nocodb_artist_table_id}/records', headers=headers)
    return response.json()

def match_user_with_artist(user_preferences, artists):
    # Matching logic based on user preferences and artist details
    """
    [List of artist fields]
    tattoo_style
    preferred_body_locations
    day_availability
    artist_name
    min_size
    max_size
    min_price
    max_price
    mon_start
    mon_end
    tue_start
    tue_end
    wed_start
    wed_end
    thur_start
    thur_end
    fri_start
    fri_end
    sat_start
    sat_end
    sun_start
    sun_end
    """
    matched_artist = None
    for artist in artists['list']:
        score = 100
        # If the artist's min_price is greater than the user's max_budget, skip
        if artist['min_price'] and user_preferences['max_budget'] and artist['min_price'] > int(user_preferences['max_budget']):
            score = 0
        # Add more matching criteria as needed
        if score > 0:
            if not matched_artist or score > matched_artist[1]:
                matched_artist = (artist, score)
    return matched_artist

