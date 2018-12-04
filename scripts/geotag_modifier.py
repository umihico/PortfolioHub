
from geotag_dicts import convert_dict_usa_states, list_of_largest_cities
import re
letters_space_only = re.compile('[a-zA-Z ]')
letters_only = re.compile('[a-zA-Z]')
from common import que, raise_with_printed_args
import tqdm


@raise_with_printed_args
def geotag(raw_location_string):
    if not raw_location_string:
        return []
    if not [x for x in raw_location_string if x]:
        return []
    locations = raw_location_string.replace('/', ',').split(',')
    locations = [beautify_word(s) for s in locations]
    for index, location in enumerate(locations):
        if location in convert_dict:
            locations[index] = convert_dict[location]
    for s in locations:
        if s in add_country_dict:
            country = add_country_dict[s]
            if country not in locations:
                locations.append(country)
    locations = list(set(locations))
    return locations


def beautify_word(raw_location):
    raw_location = ''.join(letters_space_only.findall(raw_location))
    spaced = raw_location.split(' ')
    spaced = [s.strip().lower() for s in spaced if s]
    spaced = [s[0].upper() + s[1:] for s in spaced]
    string = ''.join(spaced)
    return string


convert_dict = {
    'Usa': "United States",
    "United States Of America": "United States",
    "Uk": "United Kingdom",
    **convert_dict_usa_states,
}
add_country_dict = {
    "New York": "United States",
    **list_of_largest_cities,
    **{state: "United States" for state in convert_dict_usa_states.values()},

}

for dict_ in [convert_dict, add_country_dict]:
    for key, value in list(dict_.items()):
        dict_[beautify_word(key)] = beautify_word(value)


if __name__ == '__main__':
    modify_raw_geotag_db()
