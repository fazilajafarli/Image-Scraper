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
        query_params = {
            "key": self.APIkey, 
            "cx": SEARCHENGINEID,
            "exactTerms": self.exactTerms,
            "searchType": "image",
            "dateRestrict": self.dateRestrict,
            **kwargs,
        }
        
        page = requests.get(URL, params=query_params).json()   
        
        try:      
            totalResults = int(page["queries"]["request"][0]["totalResults"])

            if totalResults > 0:
                self.get_result(page)

            return page, totalResults
        except:
            print("No search result found!")


            
    def get_result(self, page: dict):
        items_list = []  
        for i in page.get('items'):
            item = f"{i['title']} ; {i['link']} ;"
            items_list.append(item)

        with open("src/search_results.csv", "a+") as opened_file:
            for j in items_list:
                opened_file.write(f"{j} \n")
            opened_file.write("\n")
  

    def get_next_page(self, page: dict):
        try:
            nextPage = page['queries']['nextPage'][0]['startIndex']
            return nextPage
        except:
            return None
    



def search():
    APIkey = input("Enter APIkey: ")
    exactTerms = input("Search terms: ")
    dateRestrict = input("Select date for search results: d[number]/w[number]/m[number]/y[number]. ex: \"m2\" means last 2 months. ")

    result_obj = Result(exactTerms, dateRestrict, APIkey)
    try:
        page, totalResults = result_obj.send_request()  
        x = ceil(totalResults / 10)
        for i in range(x):
            nextPage = result_obj.get_next_page(page)
            print(f"Next page - {nextPage}")
            if nextPage and nextPage < 101:  
                page, totalResults = result_obj.send_request(start=nextPage)
            else:
                print("Results are ready!")
                break
    except:
        return None
        


search()