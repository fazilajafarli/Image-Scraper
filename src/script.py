import requests
from math import ceil
from constants import SEARCHENGINEID, URL





class Result:
    """ 
        Google Custom Search API allows to show maximum 100 result, and maximum 10 result per page.
        Query limit per day is 100.
    """

    def __init__(self, exactTerms: str, dateRestrict: str, APIkey: str) -> None:
        self.exactTerms = exactTerms
        self.dateRestrict = dateRestrict
        self.APIkey = APIkey
    

    def send_request(self, **kwargs):    
        print("aaaaaaaaaaaaaaaaa")
        query_params = {
            "key": self.APIkey, 
            "cx": SEARCHENGINEID,
            "exactTerms": self.exactTerms,
            "searchType": "image",
            "dateRestrict": self.dateRestrict,
            **kwargs,
        }
        
        print(query_params)
        page = requests.get(URL, params=query_params).json()         
        self.get_result(page)

        if not query_params.get('start'):
            self.get_next_pages(page)
        
            
    def get_result(self, page: dict):
        print("bbbbbbbbbbbbbbbbbbb")
        items_list = []  
        for i in page['items']:
            item = f"{i['title']} ; {i['link']} ;"
            items_list.append(item)

        with open("search_results.csv", "a+") as opened_file:
            for j in items_list:
                opened_file.write(f"{j} \n")
            opened_file.write("\n")


    def get_next_pages(self, page):
        totalResults = page["queries"]["request"][0]["totalResults"]
        try:
            nextPage = page['queries']['nextPage'][0]['startIndex']
            print(f"Found {totalResults} results!")
            x = ceil(int(totalResults) / 10)
            print(nextPage, "ccccccccccc")
            for i in range(x):
                if nextPage < 31:  #change it 
                    self.send_request(start=nextPage)
                break
        except:
            return None
    


APIkey = input("Enter APIkey: ")
exactTerms = input("Search terms: ")
dateRestrict = input("Select date for search results: d[number]/w[number]/m[number]/y[number]. ex: \"m2\" means last 2 months. ")


result = Result(exactTerms, dateRestrict, APIkey)
result.send_request()