import requests
import json 
from itertools import islice
import argparse

"""
    This script goes out to radarr, grabs missing movies and searches for them again
    Search can be limited with search with the specify_str variable(to be changed to argument parser)
"""
def main():
    #setup url and rest calls
    rest_url = "http://unraid.nabil.net:7878"
    rest_call = {
        "missing":f"{constants['api']}/wanted/missing",
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

    
    #check for the movie filters and execute a post to the command api
    #this triggers the automatic search function for the movie in radarr
    if specify_str is not None:
        d = [i for i in missing['records'] if specify_str in i['title']]
        for i in d:  
             req = requests.post(
                url=f"{rest_url}/{rest_call['command']}",
                headers=headers,
                json={"name":"MoviesSearch","movieIds":[i['id']]}
            )
        return
    print("go time!")
    #grab all missing movies and execute the post to the command api 
    #this executes the automatic search function for the movie in radarr
    missing_movies = [i for i in missing['records']]
    for index,i in enumerate(islice(missing_movies,len(missing_movies))):  
        req = requests.post(
            url=f"{rest_url}/{rest_call['command']}",
            headers=headers,
            json={"name":"MoviesSearch","movieIds":[i['id']]}
        )
    with open('retried_movies.txt','w') as outfile:
        json.dump(missing_movies,outfile,indent=4)
if __name__ == "__main__":
    """CONSTANT GLOBALS
       api_token- token from radarr -> settings -> general-> API Key
       headers- uses api_token for auth
    """
    api_token = "110b36b161b046c5b9a6551ee34479fd"
    headers={"Authorization":f"Bearer {api_token}"}

    """CONSTANTS
       radarrpagesize- defines how many missing movies are returned per page
                       pageSize is the actual parameter that radarr's rest api needs
       api- radarr's constant rest api path
    """
    constants = {"radarrPageSize":{"pageSize":100},"api":"api/v3"}

    """FILTER CONSTANTS
       usage would be <exec> get_missing.py -f[--filter] 'optional movie filter' 
       specify-str: this will filter out movies without this title 
    """
    parser = argparse.ArgumentParser(description="A script to automate ur downloads")
    parser.add_argument('-f','--filter',required=False,default=None)
    args = parser.parse_args()
    specify_str = args.filter
    main()