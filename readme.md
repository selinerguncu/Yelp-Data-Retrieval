# Yelp Project

This project has three sub-projects:

    1. Yelp Data Visualization
    2. Yelp Data Representation on Google Geodata
    3. Yelp Data Analysis and Simulation

## Installation

To run this program you will need `python` and `pip` already installed. Also, you need to install web.py and Python requests library, and create an empty sqlite database.


```bash
$ export YELP_CLIENT_ID=<your-yelp-client-id>
$ export YELP_CLIENT_SECRET=<your-yelp-client-secret>
$ pip install web.py
$ pip install requests
$ mkdir ***
$ python bin/***.py
$ python bin/***.py
```
This program can run on Python 2.x or 3.x. Your imports should change depending on the version.

For Python 3.0 and later:
```python
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
```

For Python 2.x:
```python
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode
```

After you've done this, your game should be running on localhost:8080.

##### Yelp Data Visualization

##### Yelp Data Representation on Google Geodata

##### Yelp Data Analysis and Simulation

## License
MIT
