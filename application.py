from flask import Flask, render_template, request
from data import get_closest, get_postage


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
