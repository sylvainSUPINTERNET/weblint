import ssl
import time

from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup


class CoreTest :


    url_page = ""
    domain = ""

    page_source_code = ""
    soup = ""

    def __init__(self, url_page):
        self.url_page = url_page
        self.url_parsed = urlparse(url_page)

        #global infos from URL
        self.domain = self.url_parsed.netloc
        self.protocol = self.url_parsed.scheme
        self.path = self.url_parsed.path
        self.query = self.url_parsed.query
        self.params = self.url_parsed.params
        self.fragment = self.url_parsed.fragment


        self.page_source_code = self.sourceCode()
        self.soup = self.soupify()



    # URL management
    def getUrlPage(self):
        return self.url_page
    def setUrlPage(self, url):
        self.url_page = url

    def getUrlParsed(self):
        return self.url_parsed # return scheme = http(s) netloc (domain) path (template) params query fragment

    # global infos form URL
    def getDomain(self):
        return self.domain
    def getProtocol(self):
        return self.url_parsed.scheme
    def getPath(self):
        return self.url_parsed.path
    def getQuery(self):
        return self.url_parsed.query
    def getParams(self):
        return self.url_parsed.params
    def getFragment(self):
        return self.url_parsed.fragment





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
        t0 = time.time()
        # TODO -> check if SSL OR NOT car ca va faire 2 block de tests differents

        # Scripts tags found
        scriptTags = 0
        for scriptTag in self.soup.find_all('script'):
            scriptTags += 1

        print(" _____________________________ RESULTS TESTS _____________________________ ")
        print("\n")
        print("\n")
        print(" URL : " + self.url_page)
        print(" Protocol : " + self.protocol)
        print(" Domain : " + self.domain)
        print(" Path : " + self.path)
        print(" Quey : " + self.query)
        print(" Params : " + self.params)
        print(" Fragment : " + self.fragment)
        print("")
        print("\n")
        print(" Scripts tag : " + str(scriptTags))
        print("\n")
        print("\n")
        t1 = time.time()
        return "Execution time for each tests : " + str(t1-t0)



