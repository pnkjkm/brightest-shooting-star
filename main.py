import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class api_access:
    """
    Fetch data from the given API
    :param:
    :return:
    """
    url = "https://ssd-api.jpl.nasa.gov/fireball.api"
    date_min = '2017-01-01'
    date_max = '2020-01-01'
    payload = {
        'date-min': date_min,
        'date-max':date_max,
        'req-alt': 'true',
    }
    res = requests.get(url, data=payload, verify=False)

    if res.status_code == 400:
        raise AssertionError('Bad Request : the request contained invalid keywords and/or content: details returned')
    elif res.status_code == 405:
        raise AssertionError('Method Not Allowed : the request used a method other than GET or POST')
    elif res.status_code == 500:
        raise AssertionError('Internal Server Error : Internal Server Error')
    elif res.status_code == 503:
        raise AssertionError('Service Unavailable : the server is currently unable to handle the request due to a temporary overloading or maintenance of the server, which will likely be alleviated after some delay')

    data = res.json()
    count = int(data['count'])


class ob_loc:
	
    def __init__(self, latitude, longitude):
		
    """
    Intialise location object
    :param: latitude, longitude
    :return: Adjusted cordinates to accomodate buffer of +/- 15
    """
		
        self.latitude = latitude
        self.longitude = longitude
        self.impact_e = []
        self.data_rec = api_access()

        self.latitude_dir = self.latitude[-1]
        self.latitude_low = float(self.latitude[:-1]) - 15
        if self.latitude_low < 0:
            self.latitude_low = 0

        self.latitude_high = float(self.latitude[:-1]) + 15
        if self.latitude_high > 90:
            self.latitude_high = 90

        self.longitude_dir = self.longitude[-1]
        self.longitude_low = float(self.longitude[:-1]) - 15
        if self.longitude_low < 0:
            self.longitude_low = 0
        self.longitude_high = float(self.longitude[:-1]) + 15
        if self.longitude_high > 180:
            self.longitude_high = 180

    def max_brightness(self):
        """
        Gives the impact energy of the brightest fireball if observed for the given location
        :param
        :return: maximum impact energy
        """
        for i in range(self.data_rec.count):
            if self.data_rec.data['data'][i][4] == self.latitude_dir and self.data_rec.data['data'][i][6] == self.longitude_dir:
                if float(self.data_rec.data['data'][i][3]) >= self.latitude_low or float(self.data_rec.data['data'][i][3]) <= self.latitude_high:
                    if float(self.data_rec.data['data'][i][5]) >= self.longitude_low or float(self.data_rec.data['data'][i][5]) <= self.longitude_low:
                        self.impact_e.append(float(self.data_rec.data['data'][i][2]))

        if len(self.impact_e) < 1:
            print('No fireball observed at the given coordinates ' + self.latitude + ',' + self.longitude)
            return 0
        else:
            return max(self.impact_e)

def fireball(latitude,longitude):
    loc_1 = ob_loc(latitude, longitude)
    return loc_1.max_brightness()


Boston = fireball('42.354558N', '71.054254W')
NCR = fireball('28.574389N', '77.312638E')
SanFrancisco = fireball('37.793700N', '122.403906W')
max_b = max(Boston, NCR, SanFrancisco)

if Boston == 0 and NCR == 0 and SanFrancisco == 0:
    print('No fireball observed for the given locations')
elif max_b == Boston:
    print('Brightest fireball observed at Boston')
elif max_b == NCR:
    print('Brightest fireball observed at NCR')
else:
    print('Brightest fireball observed at San Francisco')
