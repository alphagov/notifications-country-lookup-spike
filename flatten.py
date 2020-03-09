#!/usr/bin/env python3
import json
import string

from flask import Flask, render_template, request


def make_key(original_key):
    if original_key is None:
        return None
    return normalise_whitespace("".join(
        character.lower() for character in original_key.strip() if character not in '_-.'
    ))


OBSCURE_WHITESPACE = (
    '\u180E'  # Mongolian vowel separator
    '\u200B'  # zero width space
    '\u200C'  # zero width non-joiner
    '\u200D'  # zero width joiner
    '\u2060'  # word joiner
    '\uFEFF'  # zero width non-breaking space
)


def strip_and_remove_obscure_whitespace(value):
    for character in OBSCURE_WHITESPACE:
        value = value.replace(character, '')

    return value.strip(string.whitespace)


def normalise_whitespace(value):
    # leading and trailing whitespace removed, all inner whitespace becomes a single space
    return ' '.join(strip_and_remove_obscure_whitespace(value).split())


with open(
    'node_modules/govuk-country-and-territory-autocomplete/dist/'
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
    europe = [
        make_key(country) for country in europe.readlines()
    ]

with open(
    'uk.txt'
) as uk:
    uk = [line.strip() for line in uk.readlines()]


def find_canonical(item, graph, name):
    if item['meta']['canonical']:
        if item['names']['en-GB'] == 'United Kingdom':
            return make_key(name), None
        return make_key(name), item['names']['en-GB']
    else:
        return find_canonical(
            graph[item['edges']['from'][0]],
            graph,
            name,
        )


lookup = {}

for _, item in graph.items():
    key, value = find_canonical(item, graph, item['names']['en-GB'])
    lookup[key] = value
    lookup[key.replace(' ', '')] = value

for synonym in uk:
    lookup[make_key(synonym)] = None

for synonym, mapping in synonyms.items():
    assert make_key(mapping) in lookup.keys()
    lookup[make_key(synonym)] = mapping


def get_closest(search_term, lookup_dict):

    search_term = make_key(search_term)

    if lookup.get(search_term):
        return lookup.get(search_term)

    if lookup.get('the {}'.format(search_term)):
        return lookup.get('the {}'.format(search_term))

    raise IndexError('Not found ({})'.format(search_term))


def get_postage(country, europe):
    if country is None:
        return 'UK'
    if make_key(country) in europe:
        return 'Europe'
    return 'rest of world'


app = Flask(__name__)


@app.route('/')
def hello():
    search_term = request.args.get('search_term', '')
    result = ''
    postage = ''

    if search_term:
        try:
            closest = get_closest(search_term, lookup)
            postage = get_postage(closest, europe)
            postage = f'({postage} postage zone)'
            result = f'✅ {closest}'
        except IndexError:
            result = f'⚠️ No country matches {search_term}'
            postage = ''

    return render_template(
        'index.html',
        search_term=search_term,
        result=result,
        postage=postage,
    )
