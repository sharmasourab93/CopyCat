from bs4 import BeautifulSoup
import requests
from re import compile
from itertools import chain


class ParserClass:
    
    def get_fields(self):
        
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
            
            # Hacker ID or Hackernews URL
            hurl = [i.text
                    for i in soup.find_all("span",
                                           {"class": "age"})]
            
            # Posted Time
            posted_on = [i.a.get('href')
                         for i in soup.find_all("span",
                                                {"class": "age"})]
            
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
            
            pattern = compile(r"\d+")
            
            for i in comments:
                try:
                    new_comments.append(pattern.findall(i)[0])
                except IndexError:
                    new_comments.append(0)
                
            # Filtered Comments
            new_comments = list(map(int, new_comments))
            
            zipped = list(zip(url, title,
                              hurl, author,
                              posted_on, upvotes,
                              new_comments)
                          )
            
            set_of_three.append(zipped)
            
        return list(chain.from_iterable(set_of_three))


if __name__ == '__main__':
    obj = ParserClass()
    print(obj.get_fields())
