import requests
from flask import current_app
from app import db
from app.models import SportGround


def get_all_sports_grounds():
    url = current_app.config['SOURCE_URL']
    params = {
        'api_key': current_app.config['API_KEY']
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    json_data = response.json()

    for grounds_element in json_data:
        original_id = grounds_element['global_id']
        ground_type = grounds_element['Cells']['NameWinter']
        ground_title = grounds_element['Cells']['ObjectName']
        location_title = grounds_element['Cells']['AdmArea']
        district = grounds_element['Cells']['District']
        address = grounds_element['Cells']['Address']
        working_hours = grounds_element['Cells']['WorkingHoursWinter'][0]['Hours']
        separated_working_hours = working_hours.split('-')
        start_working_hours, close_working_hours = separated_working_hours
        longitude, latitude = grounds_element['Cells']['geoData']['coordinates']
        save_sports_grounds_data(original_id,
                                 ground_type,
                                 ground_title,
                                 location_title,
                                 district,
                                 address,
                                 start_working_hours,
                                 close_working_hours,
                                 latitude,
                                 longitude)


def save_sports_grounds_data(original_id,
                             ground_type,
                             ground_title,
                             location_title,
                             district, address,
                             start_working_hours,
                             close_working_hours,
                             latitude,
                             longitude):
    grounds_exists = SportGround.query.filter(SportGround.original_id == original_id).count()
    # grounds_exists = SportGround.query(exists().where(SportGround.original_id == 'original_id')).scalar()

    if not grounds_exists:
        new_sports_grounds = SportGround(original_id=original_id,
                                         ground_type=ground_type,
                                         ground_title=ground_title,
                                         location_title=location_title,
                                         district=district,
                                         address=address,
                                         start_working_hours=start_working_hours,
                                         close_working_hours=close_working_hours,
                                         latitude=latitude,
                                         longitude=longitude)
        db.session.add(new_sports_grounds)
        db.session.commit()
