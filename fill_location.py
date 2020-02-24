
from api import get
from db import get_db
import time
import json
from pprint import pprint


def fill_location():
    conn = get_db()
    cur = conn.cursor()
    usernames = select_targets(cur)
    if len(usernames) == 0:
        return 'zero'
    username = usernames[0]
    [conv_dict, parent_area_dict] = prepare_dict(cur)
    raw_location = username_to_location(username, cur)
    locations = parse_location(raw_location, conv_dict, parent_area_dict)
    print(username, raw_location, locations)
    update_database(username, raw_location, locations, cur)
    return {'username': username, 'raw_location': raw_location, 'locations': locations}


def select_targets(cur):
    cur.execute("select user from portfolios where gif is not null and ( locations_updated_at<date_sub(curdate(), interval 90 day) or locations_updated_at is null) order by datediff(repository_updated_at, ifnull(locations_updated_at,  STR_TO_DATE('1900,1,1','%Y,%m,%d'))) desc limit 100")
    return list(set([record[0] for record in cur.fetchall()]))


def username_to_location(username, cur):
    url = f'https://api.github.com/users/{username}'
    try:
        res = get(url)
        res.raise_for_status()
    except Exception:
        if res.status_code == 404:
            cur.execute(
                "DELETE FROM portfolios WHERE user = %(user)s",
                {'user': username}
            )
        else:
            pprint(res.json())
            print('status_code', res.status_code)
            raise
    json = res.json()
    return json['location'] if 'location' in json else ""


def prepare_dict(cur):
    cur.execute(
        "select area1, area2 from area WHERE relationship='abbreviation' group by area1, area2 having count(area1)=1")
    conv_dict = {record[0]: record[1] for record in cur.fetchall()}
    cur.execute(
        "select area1, area2 from area WHERE relationship='city_country' group by area1, area2 having count(area1)=1")
    parent_area_dict = {record[0]: record[1] for record in cur.fetchall()}
    return [conv_dict, parent_area_dict]


def parse_location(raw_location, conv_dict, parent_area_dict):
    if raw_location is None:
        return []
    raw_locations = [s.strip() for s in raw_location.split(",")]
    locations = []
    for raw_location in raw_locations:
        location = conv_dict[raw_location] if raw_location in conv_dict else raw_location
        locations.append(location)
        if location in parent_area_dict:
            parent_location = parent_area_dict[location]
            locations.append(parent_location)
            if parent_location in parent_area_dict:  # twice must be enough. recurcive is too perfectionism
                locations.append(parent_area_dict[parent_location])
    return list(set(locations))


def update_database(username, raw_location, locations, cur):
    record = {"raw_location": raw_location, "locations": json.dumps(
        locations), "locations_updated_at": time.strftime('%Y-%m-%d %H:%M:%S'), "user": username}
    cur.execute('UPDATE portfolios SET raw_location=%(raw_location)s, locations=%(locations)s, locations_updated_at=%(locations_updated_at)s WHERE user=%(user)s', record)


if __name__ == '__main__':
    fill_location()
