import json

from functools import lru_cache

from notifications_utils.sanitise_text import SanitiseASCII
from notifications_utils.columns import Columns


UK = 'United Kingdom'
POSTAGE_UK = UK
POSTAGE_EUROPE = 'Europe'
POSTAGE_REST_OF_WORLD = 'rest of world'


class CountryDict(Columns):

    @staticmethod
    @lru_cache(maxsize=2048, typed=False)
    def make_key(original_key):

        normalised = "".join(
            character.lower() for character in original_key
            if character not in " _-',.()+&"
        )

        if '?' in SanitiseASCII.encode(normalised):
            return normalised

        return SanitiseASCII.encode(normalised)


def _load_data(filename):
    with open(filename) as contents:
        if filename.endswith('.json'):
            return json.load(contents)
        return [line.strip() for line in contents.readlines()]


graph = _load_data('location-autocomplete-graph.json')
synonyms = _load_data('synonyms.json')
europe = _load_data('europe.txt')
uk_islands = _load_data('uk-islands.txt')


def find_canonical(item, graph, name):
    if item['meta']['canonical']:
        return name, item['names']['en-GB']
    return find_canonical(
        graph[item['edges']['from'][0]],
        graph,
        name,
    )


lookup = CountryDict({})
traceback = CountryDict({})

for item in graph.values():
    key, value = find_canonical(item, graph, item['names']['en-GB'])
    lookup[key] = value
    traceback[key] = key

for synonym, canonical in synonyms.items():
    assert CountryDict.make_key(canonical) in lookup.keys()
    lookup[synonym] = canonical
    traceback[synonym] = synonym

for synonym in uk_islands:
    lookup[synonym] = synonym
    traceback[synonym] = synonym


def get_postage_country_or_territory(search_term):

    if lookup.get(search_term):
        return lookup.get(search_term)

    if lookup.get(f'the {search_term}'):
        return lookup.get(f'the {search_term}')

    raise IndexError(f'Not found ({search_term})')


def get_postage_zone(postage_country_or_territory):
    if postage_country_or_territory in [UK] + uk_islands:
        return POSTAGE_UK
    if postage_country_or_territory in europe:
        return POSTAGE_EUROPE
    return POSTAGE_REST_OF_WORLD
