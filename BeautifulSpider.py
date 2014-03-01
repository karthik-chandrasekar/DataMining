from bs4 import BeautifulSoup
import re
import urllib2

class BeautifulSpider:
    
    def __init__(self):
        self.movies_url = "http://www.snopes.com/movies/films/blucher.asp"
        self.content_url = "http://www.snopes.com/sports/baseball/ripkenstreak.asp"
   
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
        main_content.extend(soup.find_all("div", {"class":"article_text"}))
        main_content.extend(soup.find_all("div", {"class":"quoteBlockEnd"}))
        main_content = [x for x in main_content if x]


        for samp in main_content:
            internal_id = samp.find_all("div")
            print samp.getText()
            for samp2 in internal_id:
                print samp2.getText().encode('utf-8')

if __name__ == "__main__":
    bs_obj = BeautifulSpider()
    bs_obj.run_main()
