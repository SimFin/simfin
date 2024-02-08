#firstprogram
#pip install requests matplotlib
'''
Here's the sample code:

python

Copy code
'''
import requests

import matplotlib.pyplot as plt

# Fetch economic data (e.g., real GDP from the United States

def fetch_economic_data():

    url = 'https://api.example.com/economic-data/us-gdp'

response = requests.get(url)

if response.status_code == 200:

    return response.json() # Assuming the API returns

else:

        return None

# Simple processing of the data (e.g., extracting GDP values

def process data"("data):
    years = []
    gdp_values = []

