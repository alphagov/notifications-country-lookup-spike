import json

from functools import lru_cache

from notifications_utils.sanitise_text import SanitiseASCII
from notifications_utils.columns import Columns


UK = 'United Kingdom'


class CountryDict(Columns):

    CHARACTERS_TO_NORMALISE = " _-',.()+&"

    @staticmethod
    @lru_cache(maxsize=2048, typed=False)
    def make_key(original_key):

        normalised = "".join(
            character.lower() for character in original_key
            if character not in CountryDict.CHARACTERS_TO_NORMALISE
        )

        if '?' in SanitiseASCII.encode(normalised):
            return normalised

        return SanitiseASCII.encode(normalised)

    def __init__(self, row_dict):
        super(Columns, self).__init__([
            (CountryDict.make_key(key), value)
            for key, value in row_dict.items()
        ])

    def __getitem__(self, key):
        return super(Columns, self).get(CountryDict.make_key(key))

    def __setitem__(self, key, value):
        super(Columns, self).__setitem__(CountryDict.make_key(key), value)

    def __contains__(self, key):
        return super(Columns, self).__contains__(CountryDict.make_key(key))


with open(
    'location-autocomplete-graph.json'
) as graph:
    graph = json.load(graph)

with open(
    'synonyms.json'
) as synonyms:
    synonyms = json.load(synonyms)

with open(
    'europe.txt'
) as europe:
    europe = [line.strip() for line in europe.readlines()]

with open(
    'uk.txt'
) as uk:
    uk = [line.strip() for line in uk.readlines()]

with open(
    'uk-islands.txt'
) as uk_islands:
    uk_islands = [line.strip() for line in uk_islands.readlines()]


def find_canonical(item, graph, name):
    if item['meta']['canonical']:
        return name, item['names']['en-GB']
    else:
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


def get_closest(search_term):

    if lookup.get(search_term) == UK:
        return None

    if lookup.get(search_term):
        return lookup.get(search_term)

    if lookup.get(f'the {search_term}'):
        return lookup.get(f'the {search_term}')

    raise IndexError(f'Not found ({search_term})')


def get_postage(country):
    if country is None or country in uk_islands:
        return UK
    if country in europe:
        return 'Europe'
    return 'rest of world'
