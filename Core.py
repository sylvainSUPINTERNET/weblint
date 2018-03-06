import ssl
import time
import urllib

from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.core.validators import URLValidator




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


    # DOM

    #script tag
    def getScriptTags(self):
        # Scripts tags found
        scriptTags = 0
        for scriptTag in self.soup.find_all('script'):
            scriptTags += 1
        return str(scriptTags)

    def getScriptSrc(self):
        srcValue = []
        for scriptTag in self.soup.find_all('script'):

            if(scriptTag.has_attr('src')):
                srcValue.append(scriptTag['src'])
            else:
                srcValue.append('N/A')

        return srcValue
    def getScriptLoadTime(self):
        srcValue = self.getScriptSrc()
        loadTime = {}
        for value in srcValue:
            if(value != 'N\A'):

                #rajouter un if IF value is not valid URL, update value to NA
                req = urlopen(value)
                #

                start = time.time()
                req.read()
                end = time.time()
                req.close()
                loadTime.update({value: (end - start)})
            else:
                loadTime.update({value: 'N\A'})
        return loadTime


    """ TODO get header et les return
    def getScriptHeadInfos(self):
        srcValue = self.getScriptSrc()
        headerInfos = {}
        for value in srcValue:
            req = urlopen(value)
            header = req.headers
            print(header)
            response = req.read()
            http_code_response = response.getcode()  # TODO after to check if some script return 404 etc
            headerInfos.update({"header": header})
        return headerInfos
    """

    def getScriptHttpCode(self):
        srcValue = self.getScriptSrc()
        http_codes = {}
        for value in srcValue:

            # rajouter un if IF value is not valid URL, update value to NA
            req = urlopen(value)
            #

            response = req.read()
            if(http_codes[value] != 'N\A'):
                http_code = req.getcode()
                http_codes[value] = http_code #equivalent of list.update(...)
            else:
                http_codes[value] = 'N\A'

        return http_codes
    def countErrorHttpCode(self):
        list_http_codes = self.getScriptHttpCode()
        http_error_count = 0
        for code in list_http_codes:
            if(list_http_codes[code] != None and list_http_codes[code] < 200 or list_http_codes[code] > 200 and  list_http_codes[code] != 'N\A'):
                http_error_count += 1
        return http_error_count









    #Results tests
    def renderTests(self):
        t0 = time.time()
        # TODO -> check if SSL OR NOT car ca va faire 2 block de tests differents


        print(" _____________________________ RESULTS TESTS _____________________________ ")
        print("\n")
        print("- - - - - - GENERAL - - - - - -")
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
        print("- - - - - - DOM - - - - - -")
        print("\n")
        print(" Scripts tag : " + self.getScriptTags())
        print(" Scripts src : " + str(self.getScriptSrc()))
        print(" GET loading time : " + str(self.getScriptLoadTime()))
        print(" Script HTTP code response (from scripts loading) : " + str(self.getScriptHttpCode()))
        print(" Script HTTP code response ERROR : " + str(self.countErrorHttpCode()))

        #test perso to remove later
        # TODO: faire analyse du header sur les scripts


        print("\n")
        print("\n")
        t1 = time.time()
        return "Execution time for each tests : " + str(t1-t0)



