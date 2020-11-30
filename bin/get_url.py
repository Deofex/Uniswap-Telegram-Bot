import requests

# The function below retrieves the content from an URL which should be specified
# as parameter. The outpuut is the raw data extracted from the URL.
def get_url(url):
    '''URL to retrieve an URL'''
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content