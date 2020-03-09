import pytest

from data import get_closest, get_postage


@pytest.mark.parametrize('search, expected', (
    ('u.s.a', 'United States'),
    ('america', 'United States'),
    ('United States America', 'United States'),
    ('ROI', 'Ireland'),
    ('Irish Republic', 'Ireland'),
    ('Rep of Ireland', 'Ireland'),
    ('RepOfIreland', 'Ireland'),
    ('deutschland', 'Germany'),
    ('UK', None),
    ('England', None),
    ('Northern Ireland', None),
    ('Scotland', None),
    ('Wales', None),
    ('N. Ireland', None),
    ('GB', None),
    ('NIR', None),
    ('SCT', None),
    ('WLS', None),
    ('gambia', 'The Gambia'),
    ('Jersey', 'Jersey'),
    ('Guernsey', 'Guernsey'),
    ('Lubnān', 'Lebanon'),
    ('ESPAÑA', 'Spain'),
    ("the democratic people's republic of korea", 'North Korea'),
    ("the democratic peoples republic of korea", 'North Korea'),
    ('ALAND', 'Åland Islands')
))
def test_get_closest(search, expected):
    assert get_closest(search) == expected


@pytest.mark.parametrize('search, expected', (
    ('u.s.a', 'rest of world'),
    ('Rep of Ireland', 'Europe'),
    ('deutschland', 'Europe'),
    ('UK', 'United Kingdom'),
    ('Jersey', 'United Kingdom'),
    ('Guernsey', 'United Kingdom'),
    ('isle-of-man', 'United Kingdom'),
    ('ESPAÑA', 'Europe'),
))
def test_get_postage(search, expected):
    assert get_postage(get_closest(search)) == expected
