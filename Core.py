import ssl
import time
import urllib
import requests


from pprint import pprint
from pprint import pformat

from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.core.validators import URLValidator


class CoreTest:
    url_page = ""
    domain = ""

    page_source_code = ""
    soup = ""

    def __init__(self, url_page):
        self.url_page = url_page
        self.url_parsed = urlparse(url_page)

        # global infos from URL
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
        return self.url_parsed  # return scheme = http(s) netloc (domain) path (template) params query fragment

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

    # Page Source Code management
    def setPageSourceCode(self, code_source):
        self.page_source_code = code_source

    def getPageSourceCode(self):
        return self.page_source_code

    def sourceCode(self):
        content = urlopen(self.url_page)
        page_source_code = content.read()
        return page_source_code

    # Soupify
    def setSoup(self, soup):
        self.soup = soup

    def getSoup(self):
        return self.soup

    def getSoupPretty(self):
        return self.soup.prettify()

    def soupify(self):
        soup = BeautifulSoup(self.sourceCode(), 'html.parser')
        return soup

    # DOM

    # script tag
    """
    def getScriptTags(self):
        # Scripts tags found
        scriptTags = 0
        for scriptTag in self.soup.find_all('script'):
            scriptTags += 1
        return str(scriptTags)

    def getScriptSrc(self):
        srcValue = []
        for scriptTag in self.soup.find_all('script'):

            if (scriptTag.has_attr('src')):
                srcValue.append(scriptTag['src'])
            else:
                srcValue.append('NoResult')

        return srcValue

    def getScriptLoadTime(self):
        srcValue = self.getScriptSrc()
        loadTime = {}
        for value in srcValue:
            if (value != 'NoResult'):
                urlScriptParsed = urlparse(value)
                if (urlScriptParsed.scheme == "http" or urlScriptParsed.scheme == "https"):
                    req = urlopen(value)
                    start = time.time()
                    req.read()
                    end = time.time()
                    req.close()
                    loadTime.update({value: (end - start)})
                else:
                    loadTime.update({value: 'NoResult'})
        return loadTime

   #dosnt work
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


    def getScriptHttpCode(self):

        srcValue = self.getScriptSrc()

        http_codes = {}

        for idx, value in enumerate(srcValue):

            if (value != 'NoResult'):
                urlParsed = urlparse(value)
                if(urlParsed.scheme == "http" or urlParsed.scheme == "https"):
                    req = urlopen(value)
                    response = req.read()
                    http_code = req.getcode()
                    http_codes.update({value: http_code})

        return http_codes

    def countErrorHttpCode(self):
        list_http_codes = self.getScriptHttpCode()
        informations = 0
        success = 0
        redirection = 0
        error_client = 0
        error_server = 0

        http_details = {}

        for code in list_http_codes:
            if (list_http_codes[code] != None and list_http_codes[code] >= 100 and list_http_codes[code] <= 103):
                informations += 1
                http_details.update({'informations': informations })
            if(list_http_codes[code] != None and list_http_codes[code] >= 200 and list_http_codes[code] <= 226):
                success += 1
                http_details.update({'success': success})
            if(list_http_codes[code] != None and list_http_codes[code] >= 300 and list_http_codes[code] <= 310):
                redirection += 1
                http_details.update({'redirection': redirection})
            if(list_http_codes[code] != None and list_http_codes[code] >= 400 and list_http_codes[code] <= 499):
                error_client += 1
                http_details.update({'error_client': error_client})
            if (list_http_codes[code] != None and list_http_codes[code] >= 500 and list_http_codes[code] <= 527):
                error_server += 1
                http_details.update({'error_server': error_server})


        return http_details
    """

    # PAGE
    # - informations
    def pageLoadingTime(self):
        return requests.get(self.url_page).elapsed.total_seconds()

    # - header
    def pageHeader(self):
        req = urlopen(self.url_page)
        response = req.read()
        header = req.headers
        return header

    def headerDetails(self):
        errorHeader = {}
        header = self.pageHeader()

        # options header check
        CSP = header['Content-Security-Policy']
        x_frame_options = header['X-Frame-Options']
        x_request_guid = header['X-Request-Guid']
        strict_transport_security = header['Strict-Transport-Security']
        vary = header['Vary']
        x_server_by = header['X-Served-By']
        x_cache = header['X-Cache']
        x_timer = header['X-Timer']
        x_DNS_prefetch_control = header['X-DNS-Prefetch-Control']

        if(CSP == None):
            errorHeader.update({"CSP": "No Content-Security-Policy" })
        if(x_frame_options == None):
            errorHeader.update({"X-Frame-Options" : "No X-Frame-Options"})
        if(x_request_guid == None):
            errorHeader.update({"X-Request-Guid" : "No X-Request-Guid"})
        if(strict_transport_security  == None):
            errorHeader.update({"Strict-Transport-Security": "No Strict-Transport-Security"})
        if (vary == None):
            errorHeader.update({"Vary": "No Vary"})
        if(x_server_by == None):
            errorHeader.update({"X-Served-By" : "No X-Served-By"})
        if(x_cache == None):
            errorHeader.update({"X-Cache" : "No X-Cache"})
        if (x_timer  == None):
            errorHeader.update({"X-Timer": "No X-Timer"})
        if (x_DNS_prefetch_control  == None):
            errorHeader.update({"X-DNS-Prefetch-Control": "No X-DNS-Prefetch-Control"})

        return errorHeader

    def headerDate(self):
        header = self.pageHeader()

        last_update = header['Last-Modified']

        return last_update







    """
    def encodingCheck(self):
        header = self.pageHeader()
        contentType = header['Content-Type']


        encodingMeta = 0
        balisesMeta = self.soup.find_all('meta')
        for balise in balisesMeta:
            print(balise)

        print(contentType)
    """


    # Results tests
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
        print(" Loading time : " + str(self.pageLoadingTime()))
        print("\n")
        print("- - - - - - HEADER - - - - - -")
        print("\n")
        print(self.pageHeader())
        print("\n")
        print("Last update : " + str(self.headerDate()) )
        print("\n")
        pprint(self.headerDetails())
        print("\n")
        #print(self.encodingCheck())



        print("- - - - - - DOM - - - - - -")
        """
        print("\n")
        print(" Scripts tag : " + self.getScriptTags())
        print("\n")
        pprint(" Scripts src : " + str(self.getScriptSrc()))
        print("\n")
        pprint(" GET loading time : " + str(self.getScriptLoadTime()))
        print("\n")
        pprint(" Script HTTP code response (from scripts loading) : " + str(self.getScriptHttpCode()))
        print("\n")
        pprint(" Script HTTP code response ERROR (from script loading) : " + str(self.countErrorHttpCode()))
        """


        # test perso to remove later
        # TODO: faire analyse du header sur les scripts





        print("\n")
        print("\n")
        t1 = time.time()
        return "Execution time for each tests : " + str(t1 - t0)
