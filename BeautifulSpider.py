from bs4 import BeautifulSoup
import urllib2, json

class BeautifulSpider:
    
    def __init__(self):
        self.url_list = ["http://www.snopes.com/movies/movies.asp"] 
        self.black_listed_keywords = ['http', 'mailto'] 
        self.snopes = "http://www.snopes.com/"
  

    def run_main_back(self):
        self.url_list = [
        "http://www.snopes.com/sports/baseball/bttf2.asp",
        "http://www.snopes.com/horrors/ghosts/blair.asp",
        "http://www.snopes.com/movies/films/c3po.asp",
        "http://www.snopes.com/movies/films/3menbaby.asp",
        "http://www.snopes.com/sports/baseball/ripkenstreak.asp",
        "http://www.snopes.com/autos/cursed/spyder.asp",
        "http://www.snopes.com/glurge/beautytips.asp",
        "http://www.snopes.com/disney/films/tinkerbell.asp",
        "http://www.snopes.com/glurge/duke.asp"
        ]
        for url in self.url_list:
            page = urllib2.urlopen(url).read()
            soup = BeautifulSoup(page)
            self.getContent(soup, url)
 

    def run_main(self):
        self.url_list = [
        "http://www.snopes.com/movies/other/spielberg.asp"
        ]
        for url in self.url_list:
            page = urllib2.urlopen(url).read()
            soup = BeautifulSoup(page)
            self.getContent(soup, url)

    def getContent(self, soup, url):
        #Scrapes the content from the given url
       
        url = url.replace(self.snopes,"")
        url = url.replace("/","-")

        content = []
        main_content = soup.get_text()
        if not main_content:return
        content.append(main_content.encode('utf-8'))
        main_content = [x for x in main_content if x]
        open(url, 'w').write(json.dumps(content))
        #main_content = soup.find_all("div", {"id":"main-content"})
        #main_content.extend(soup.find_all("div", {"class":"article_text"}))
        #main_content.extend(soup.find_all("div", {"class":"quoteBlockEnd"}))
       
        #for samp in main_content:
        #    content.append(samp.encode('utf-8'))
        #url = url.replace(".asp", ".txt") 


if __name__ == "__main__":
    bs_obj = BeautifulSpider()
    bs_obj.run_main()
