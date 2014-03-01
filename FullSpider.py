from bs4 import BeautifulSoup
import urllib2, json

class BeautifulSpider:
    
    def __init__(self):
        #Start URL
        self.url_list = ["http://www.snopes.com/movies/movies.asp"] 
        self.url_black_list = ['http', 'mailto'] 
        self.snopes = "http://www.snopes.com/"
        self.it_count = 0

    def run_main(self):
        if not self.url_list:return
        for url in self.url_list:
            self.getUrls(url)
            self.it_count += 1
            self.url_list = self.url_list[1:]
        self.run_main()

    def getUrls(self, url):
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page)
        links = soup.find_all('a', href=True)
        self.getContent(soup, url)
        if self.it_count > 3:return

        for link in links:
            link = link['href']
            link = link and link.strip()
            if not link[0].isalpha():continue
            if link.split(":")[0] in self.url_black_list:continue 
            if link == self.snopes:continue
            self.getLinks(link) 
            print link

    def getLinks(self, link):
        movies_link = self.url_list[0].split('/')[2:-1]
        link = link.split('/')
        movies_link.extend(link)
        final_link = "http://%s" % ('/'.join(movies_link))
        self.url_list.append(final_link)
        
    def getContent(self, soup, url):
        url = url.replace(self.snopes,"")
        url = url.replace("/","-")
        main_content = soup.find_all("div", {"id":"main-content"}) or soup.find_all("div", {"class":"article_text"})
        temp_list = []
        for samp in main_content:
            internal_id = samp.find_all("div")
            if not internal_id:
                temp_list.append(samp.getText().encode('utf-8'))
                continue
            for samp2 in internal_id:
                temp_list.append(samp2.getText().encode('utf-8'))
        open(url, 'w').write(json.dumps(temp_list))

if __name__ == "__main__":
    bs = BeautifulSpider()
    bs.run_main()            
