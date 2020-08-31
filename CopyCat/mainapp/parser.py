from bs4 import BeautifulSoup
import requests
from re import compile
from itertools import chain
from datetime import timedelta, datetime


class ParserClass:
    
    def get_time_field(self, posted_arr):
        new_posted_arr = []
        
        for i in posted_arr:
            integer, time, ago = i.split()
            
            if time == 'minutes':
                x = datetime.now() - timedelta(minutes=int(integer))
                new_posted_arr.append(x)
                
            else:
                x = datetime.now() - timedelta(hours=int(integer))
                new_posted_arr.append(x)
                
        return new_posted_arr
        
    def get_fields(self):
        pattern = compile(r"\d+")
        set_of_three = list()
        
        for i in range(1, 4):
            url = "https://news.ycombinator.com/news?p={0}"\
                .format(str(i))
            
            parse_data = str(requests.get(url).content)
            soup = BeautifulSoup(parse_data, 'html.parser')
            
            # Extract Title
            title = [i.text
                     for i in soup.find_all("a",
                                            {"class": "storylink"})]
            # Extract Href's URL Value
            url = [i.get('href')
                   for i in soup.find_all("a",
                                          {"class": "storylink"})]
            
            # Count of Upvotes
            upvotes = [int(i.text.split()[0])
                       for i in soup.find_all("span",
                                              {"class": "score"})]
            
            # Author
            author = [i.text
                      for i in soup.find_all("a",
                                             {"class": "hnuser"})]

            # Posted Time
            posted_on = [i.text
                         for i in soup.find_all("span",
                                                {"class": "age"})]
            print(posted_on)
            posted_on = self.get_time_field(posted_on)
            posted_on = ["{:%d-%m-%Y %H:%M:%S}".format(i)
                         for i in posted_on]

            # Hacker ID or Hackernews URL
            hurl = [pattern.findall(i.a.get('href'))[0]
                    for i in soup.find_all("span",
                                           {"class": "age"})]
            print()
            
            # Comments Count
            comments = [i.text
                        for i in soup.find_all("a",
                                               href=
                                               compile(
                                                   r'item\?id=\d+'
                                                   )
                                               )[1::2]
                        ]

            new_comments = []
            
            for i in comments:
                try:
                    new_comments.append(pattern.findall(i)[0])
                except IndexError:
                    new_comments.append(0)
                
            # Filtered Comments
            comments = list(map(int, new_comments))
            
            zipped = list(zip(url, title,
                              hurl, author,
                              posted_on, upvotes,
                              comments)
                          )
            
            set_of_three.append(zipped)
            
        return list(chain.from_iterable(set_of_three))


if __name__ == '__main__':
    obj = ParserClass()
    print(obj.get_fields())
