import pytest

from data import get_closest, get_postage


@pytest.mark.parametrize('search, expected', (
    ('u.s.a', 'United States'),
    ('america', 'United States'),
    ('United States America', 'United States'),
    ('ROI', 'Ireland'),
    ('Irish Republic', 'Ireland'),
    ('Rep of Ireland', 'Ireland'),
    ('deutschland', 'Germany'),
    ('UK', None),
    ('Scotland', None),
    pytest.param('Wales', None, marks=pytest.mark.xfail),
    ('N. Ireland', None),
    ('GB', None),
    ('gambia', 'The Gambia'),
    ('Jersey', 'Jersey'),
    ('Guernsey', 'Guernsey'),
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
    ('Isle of Man', 'United Kingdom'),
))
def test_get_postage(search, expected):
    assert get_postage(get_closest(search)) == expected
