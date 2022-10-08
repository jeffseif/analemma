# analemma

A library for forecasting sun positions

## Why make an analemma library?

Although there are several nice online API's for fetching sun data ([1](https://api.met.no/weatherapi/sunrise/2.0/documentation), [2](https://aa.usno.navy.mil/data/docs/api.php#rstt)), this library can provide that information for offline devices too!


## How does the library work?

Install the package:

```bash
pip install -e git+https://github.com/jeffseif/analemma.git#egg=analemma
```

Import and run it

```python
>>> from analemma import horizon
>>> horizon.sun_rise_and_set()
{'current_timestamp': 1592722800, 'latitude': 37.871667, 'longitude': -122.272778, 'solar_noon': datetime.datetime(2020, 6, 21, 13, 10, 32, 132916), 'sunlight_hours': 14.792841731732462, 'sunrise': datetime.datetime(2020, 6, 21, 5, 46, 45, 17799), 'sunset': datetime.datetime(2020, 6, 21, 20, 34, 19, 248033), 'timezone_name': 'America/Los_Angeles'}
```
