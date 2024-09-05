import requests
import json 
from itertools import islice

"""
    This script goes out to radarr, grabs missing movies and searches for them again
    Search can be limited with search with the specify_str variable(to be changed to argument parser)
"""
def main():
    #setup url and rest calls
    rest_url = "<your rest url>"
    rest_call = {
        "missing":f"{constants['api']}/wanted/missing",
        "movie":f"{constants['api']}/movie",
        "command":f"{constants['api']}/command"
    }

    #get movies in missing status
    missing = requests.get(
        url=f"{rest_url}/{rest_call['missing']}",
        params=constants["radarrPageSize"],
        headers=headers
    )
    
    #check if the movie was found
    if missing.status_code != 200:
        print(f"Error: [{missing.status_code}]-{missing.reason}")
        return
    else:
        missing = missing.json()

    
    #check for the movie filters
    if specify_str is not None:
        d = [i for i in missing['records'] if specify_str in i['title']]
        for i in d:  
             req = requests.post(
                url=f"{rest_url}/{rest_call['command']}",
                headers=headers,
                json={"name":"MoviesSearch","movieIds":[i['id']]}
            )
        return
    
    #grab all missing movies
    missing_movies = [i for i in missing['records']]
    for index,i in enumerate(islice(missing_movies,10)):  
        req = requests.post(
            url=f"{rest_url}/{rest_call['command']}",
            headers=headers,
            json={"name":"MoviesSearch","movieIds":[i['id']]}
        )

if __name__ == "__main__":
    """CONSTANT GLOBALS
       api_token from radarr -> settings -> general-> API Key
       headers- uses api_token for auth
    """
    api_token = "<your radarr api token>"
    headers={"Authorization":f"Bearer {api_token}"}

    """CONSTANTS
       radarrpagesize- defines how many missing movies are returned per page
                       pageSize is the actual parameter that radarr's rest api needs
       api-
    """
    constants = {"radarrPageSize":{"pageSize":100},"api":"api/v3"}

    """FILTER CONSTANTS
    TODO change to using argparse instead since this will be a cron job
       specify-str: this will filter out movies without this title 
    """
    specify_str = None
    main()