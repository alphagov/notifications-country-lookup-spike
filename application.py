from flask import Flask, render_template, request
from data import get_closest, get_postage, lookup, make_key


app = Flask(__name__)


@app.route('/')
def hello():
    search_term = request.args.get('search_term', '')
    result = ''
    postage = ''

    if search_term:
        try:
            closest = get_closest(search_term)
            postage = get_postage(closest)
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


@app.route('/list')
def country_list():
    country_list = sorted([
        str(canonical)
        for canonical in set(lookup.values())
    ])
    synonyms = {
        country: sorted([
            key for key, value in lookup.items()
            if value == country and key != make_key(country)
        ])
        for country in country_list
    }
    return render_template(
        'list.html',
        country_list=synonyms,
    )


@app.route('/list-raw')
def list_raw():
    country_list = sorted([
        str(canonical)
        for canonical in set(lookup.values())
    ])
    output = []
    for country in country_list:
        for key, value in sorted(lookup.items()):
            if value == country and key != make_key(country):
                output.append(f'({repr(key)}, {repr(country)}),')
    return '\n'.join(sorted(output))
