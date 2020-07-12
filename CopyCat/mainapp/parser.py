from bs4 import BeautifulSoup
import requests


class ParserClass:
    
    def get_fields(self):
        url = "https://news.ycombinator.com/news?p={0}"
        for i in range(1):
            url = url.format(str(i))
            parse_data = str(requests.get(url).content)
            soup = BeautifulSoup(parse_data, 'html.parser')
            url, hurl, posted_on, \
            upvotes, comments = [], [], [], [], []
            source = []
            
            for i in enumerate(soup.find_all('tr', r"\'athing\'"):
                url.append()
            
            
            
            
            



if __name__ == '__main__':
    obj = ParserClass()
    obj.get_fields()