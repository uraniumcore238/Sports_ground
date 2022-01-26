from app.models import SportGround


def create_map_data_json_with_orm():
    all_rows = SportGround.query.filter_by(id=SportGround.id).all()

    table = {
        "type": "FeatureCollection",
        "features": []
    }

    for row in all_rows:

        features = {"type": "Feature", "id": row.id,
                    "geometry": {"type": "Point", "coordinates": [row.latitude, row.longitude]},
                    "properties": {
                        "balloonContentHeader": f"<font size=2>{row.ground_type}</font>",
                        "balloonContentBody": f"<p>Адрес: <b>{row.address}.</b><br>Время работы: <b>"
                                              f"{row.start_working_hours} - {row.close_working_hours}</p>",
                        "balloonContentFooter": f"<font size=2><a target='_blank' "
                                                f"href='/area/{row.id}/'>Перейти на страницу площадки</a>",
                        "clusterCaption": f"<font size=2>{row.ground_type}</font>",
                        "hintContent": f"{row.ground_title}<br>{row.ground_type}"}}

        table["features"].append(features)

    return table


create_map_data_json_with_orm()
