from bs4 import BeautifulSoup
import re
import urllib2

class BeautifulSpider:
    
    def __init__(self):
        self.movies_url = "http://www.snopes.com/movies/films/blucher.asp"
        self.content_url = "http://www.snopes.com/movies/films/zhivago.asp"
   
    def run_main(self):

        junk_list = ['http','mailto']
        data = {}
        page = urllib2.urlopen(self.movies_url).read()
        soup = BeautifulSoup(page)
        urls_list = soup.find_all('a',href=True)
        for url in urls_list:
            link = url['href']
            if link[0].isalpha():
                if not link.split(":")[0] in junk_list:
                    #print link
                    pass               

        self.content()

    
    def content(self):
        page = urllib2.urlopen(self.content_url).read()
        soup = BeautifulSoup(page)
        main_content = soup.find_all("div", {"id":"main-content"})
        for samp in main_content:
            internal_id = samp.find_all("div")
            for samp2 in internal_id:
                samp2.find_all("br")


if __name__ == "__main__":
    bs_obj = BeautifulSpider()
    bs_obj.run_main()
