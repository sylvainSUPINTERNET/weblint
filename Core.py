import ssl

from urllib.request import urlopen
from bs4 import BeautifulSoup


class CoreTest :

    url_page = ""

    page_source_code = ""
    soup = ""

    def __init__(self, url_page):
        self.url_page = url_page
        self.page_source_code = self.sourceCode()
        self.soup = self.soupify()



    def getUrlPage(self):
        return self.url_page
    def setUrlPage(self, url):
        self.url_page = url


    #Page Source Code management
    def setPageSourceCode(self, code_source):
        self.page_source_code = code_source

    def getPageSourceCode(self):
        return self.page_source_code

    def sourceCode(self):
        content = urlopen(self.url_page)
        page_source_code = content.read()
        return page_source_code

    #Soupify
    def setSoup(self,soup):
        self.soup = soup

    def getSoup(self):
            return self.soup
    def getSoupPretty(self):
            return self.soup.prettify()

    def soupify(self):
        soup = BeautifulSoup(self.sourceCode(), 'html.parser')
        return soup



    #Results tests
    def renderTests(self):
        # TODO -> check if SSL OR NOT car ca va faire 2 block de tests differents

        # Scripts tags found
        scriptTags = 0
        for scriptTag in self.soup.find_all('script'):
            scriptTags += 1

        print(" _____________________________ RESULTS TESTS _____________________________ ")
        print("\n")
        print("\n")
        print(" URL target : " + self.url_page)
        print(" Scripts tag : " + str(scriptTags))
        
