from bs4 import BeautifulSoup
import urllib2, json

class FullSpider:
    
    def __init__(self):
        self.url_list = ["http://www.snopes.com/movies/movies.asp"] 
        self.black_listed_keywords = ['http', 'mailto'] 
        self.snopes = "http://www.snopes.com/"
        self.it_count = 0
        self.index = None

    def run_main(self):
        for index, url in enumerate(self.url_list):
            self.index = index
            self.getUrls(url)
            self.it_count += 1

    def getUrls(self, url):
        print url
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page)
        links = soup.find_all('a', href=True)
        self.getContent(soup, url)
        if self.it_count > 3:return
        self.getLinks(links)

    def getLinks(self, links):
        
        for link in links:
            link = link['href']
            if not link:continue
            link = link.strip()
            if not link[0].isalpha():continue
            if link.split(":")[0] in self.black_listed_keywords:continue 
            if link == self.snopes:continue
            print link

            url = self.url_list[self.index].split('/')[2:-1]
            link = link.split('/')
            url.extend(link)
            new_url = "http://%s" % ('/'.join(url))
            self.url_list.append(new_url)
        

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


if __name__ == "__main__":
    bs = FullSpider()
    bs.run_main()            
