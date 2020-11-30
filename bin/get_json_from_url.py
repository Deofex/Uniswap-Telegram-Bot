import json
from bin.get_url import get_url

# The function below retrieves a JSON file from an URL. The function ask the
# content of an URL via the get_URL function and convert to content to the JSON
# format.
def get_json_from_url(url):
    '''Function to retrieve a JSON file from an URL'''
    content = get_url(url)
    js = json.loads(content)
    return js