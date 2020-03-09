import pytest

from data import get_closest


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
    ('Wales', None),
    ('N. Ireland', None),
    ('GB', None),
    ('gambia', 'The Gambia'),
))
def test_get_closest(search, expected):
    assert get_closest(search) == expected
