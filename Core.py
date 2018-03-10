import cgi
import ssl
import time
import urllib
import requests
import re
import os


from pprint import pprint
from pprint import pformat

from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit

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

        self.homePath = self.getHomePath()

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

    def getHomePath(self):
        return self.url_parsed.scheme + "://" + self.domain + "/"

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

    # JS
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


    # CSS
    def getLinkTag(self):
        linkTagsCount = 0
        styleLinks = self.soup.find_all('link')
        for link in styleLinks:
            if(link['rel'] != None):
                if(link['rel'][0] == "stylesheet"):
                    linkTagsCount += 1
        return linkTagsCount


    def getLinkHref(self):
        hrefValue = []
        styleLinks = self.soup.find_all('link')
        for link in styleLinks:
            if (link['rel'] != None):
                if (link['rel'][0] == "stylesheet"):
                    if(link['href'] != None):
                        linkParsed = urlparse(link['href'])
                        if(linkParsed.scheme == "http" or linkParsed.scheme == "https" ):
                            hrefValue.append(link['href'])

        if(hrefValue.__len__() == 0):
            return " Aucun href http ou https detected"
        else:
            return hrefValue

    def getLinkLoadTime(self):
        hrefValue = self.getLinkHref()
        if(type(hrefValue) != str): #if STR means 0 link found
            loadTime = {}
            for value in hrefValue:
                hrefParsed = urlparse(value)
                if (hrefParsed.scheme == "http" or hrefParsed.scheme == "https"):
                    req = urlopen(value)
                    start = time.time()
                    req.read()
                    end = time.time()
                    req.close()
                    loadTime.update({value: (end - start)})
            return loadTime
        else:
            return " 0 links found for test loading"

    def getHrefHttpCode(self):
        hrefValue = self.getLinkHref() # return 1 str if its one error

        if(type(hrefValue) != str):
            http_codes = {}
            for idx, value in enumerate(hrefValue):
                req = urlopen(value)
                response = req.read()
                http_code = req.getcode()
                http_codes.update({value: http_code})

            return http_codes
        else:
            return " No link to check HTTP code"

    def getHrefHttpCodeDetail(self):
        list_http_codes = self.getHrefHttpCode()
        if(type(list_http_codes) != str) :
            informations = 0
            success = 0
            redirection = 0
            error_client = 0
            error_server = 0

            http_details = {}

            for code in list_http_codes:
                if (list_http_codes[code] != None and list_http_codes[code] >= 100 and list_http_codes[code] <= 103):
                    informations += 1
                    http_details.update({'informations': informations})
                if (list_http_codes[code] != None and list_http_codes[code] >= 200 and list_http_codes[code] <= 226):
                    success += 1
                    http_details.update({'success': success})
                if (list_http_codes[code] != None and list_http_codes[code] >= 300 and list_http_codes[code] <= 310):
                    redirection += 1
                    http_details.update({'redirection': redirection})
                if (list_http_codes[code] != None and list_http_codes[code] >= 400 and list_http_codes[code] <= 499):
                    error_client += 1
                    http_details.update({'error_client': error_client})
                if (list_http_codes[code] != None and list_http_codes[code] >= 500 and list_http_codes[code] <= 527):
                    error_server += 1
                    http_details.update({'error_server': error_server})

            return http_details
        else:
            return " NO link found No HTTP code found for test"






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
            errorHeader.update({"No Content-Security-Policy": "No Content-Security-Policy" })
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
        if(last_update != None):
            return last_update
        else:
            return " Information not available via header"





    # Encoding

    def getPageEncoding(self):
        encod = self.soup.meta.get('charset')
        if encod == None:
            encod = self.soup.meta.get('content-type')
            if encod == None:
                content = self.soup.meta.get('content')
                match = re.search('charset=(.*)', content)
                if match:
                    encod = match.group(1)
                    return encod
                else:
                    return ' Error cannot find encoding of page'
        else:
            return ' Error cannot find encoding of page'

    def compareEncoding(self): #compare encoding header / page
        pageEncoding = self.getPageEncoding()
        if(pageEncoding != 'Error cannot find encoding of page' ):
            #check if we find charset in header
            _, params = cgi.parse_header('text/html; charset=utf-8')
            if(params['charset']):
                if(params['charset'] == pageEncoding):
                    return " Encoding same on page and header"
                else:
                    return " Encoding not same between page and header => Page : " + pageEncoding + " / Header : " + params['charset']
            else:
                return " Cannot find encoding into header details"
        else:
            return " Cannot find page encoding"

        #Robots / Security

    def robotsTxtExist(self):
        url = self.homePath
        urlRobotsTxt = url + "robots.txt"
        req = requests.get(urlRobotsTxt)
        if(req.status_code == 200):
            return " Robots.txt found"
        else:
            return " No robots.txt found"


        # TODO Analyser le robots.txt
        #exemple ces deux liens le robots na pas les même agents etc donc a regarder
        # https://stackoverflow.com/robots.txt (Cest bien, plein d'agent un sitemap etc)
        # http://www.univ-paris3.fr/robots.txt (pas de sitemap, qun seul agent etc)








    # Results tests
    def renderTests(self):
        t0 = time.time()

        #HEADER checking
        header = self.pageHeader()
        headerErrors = self.headerDetails()
        headerDate = self.headerDate()


        #DOM checking
        # - script JS
        tagScript = self.getScriptTags()
        scriptLoadingTime = str(self.getScriptLoadTime()) #only http or https parsed
        scriptHttpCode = str(self.getScriptHttpCode())
        errorResultHttpCode = str(self.countErrorHttpCode())

        # - CSS
        countStyleTag = str(self.getLinkTag())
        linkHref = self.getLinkHref() #only http or https parsed
        linkLoadingTime = str(self.getLinkLoadTime())
        linkHrefHttpCode = str(self.getHrefHttpCode())
        linkHrefHttpCodeDetail = str(self.getHrefHttpCodeDetail())

        # - Page
        pageEncoding = str(self.getPageEncoding())
        compareEncoding = str(self.compareEncoding()) #compare header encoding with page encoding
        robotsTxtExist = str(self.robotsTxtExist())


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
        print(" Path home : " + str(self.homePath))
        print("\n")


        print("- - - - - - HEADER - - - - - -")
        #print(header)
        print("\n")
        print("Last update : " + headerDate)
        for detail in headerErrors:
            print("[x] => " + headerErrors[detail])
        print("\n")

        print("- - - - - - DOM - - - - - -")
        # JS script
        print("\n JS")
        print("\n")
        print(" Scripts tag : " + tagScript)
        #pprint(" Scripts src : " + str(self.getScriptSrc()))
        print("\n")
        pprint(" GET loading time : " + scriptLoadingTime )
        print("\n")
        pprint(" Script HTTP code response (from scripts loading) : " + scriptHttpCode)
        print("\n")
        print(" Script HTTP code response ERROR (from script loading HTTPS ) / ONLY http or https parsed : " + errorResultHttpCode)
        print("\n")

        #CSS link
        print("\n CSS")
        print("\n")
        print(" Link stylesheet tag : " + countStyleTag)
        print(linkHref)
        pprint(" Loading time : " + linkLoadingTime)
        pprint(" HTTP code : " + linkHrefHttpCode)
        print(" HTTP code detail : " + linkHrefHttpCodeDetail)
        print("\n")

        #Encoding
        print("\n Page Infos ")
        print("\n")
        print(" Page encoding : " + pageEncoding)
        print(" Compare header encoding with page encoding : " + compareEncoding)
        #Robots / Security
        print(" robots.txt : " + robotsTxtExist)

        # test perso to remove later

        # TODO: check if AMP is ok (if there are)
        # TODO: If its home page, look at robots.txt
        # TODO: Présence de liens HTTP alors qu'en face y'a du HTTPS



        print("\n")
        print("\n")
        t1 = time.time()
        return "Execution time for each tests : " + str(t1 - t0)
