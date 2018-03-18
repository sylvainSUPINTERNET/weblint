import cgi
import time
import requests
import re


from pprint import pprint


from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup


from http.client import responses


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



    # DOM tests

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
                if (urlParsed.scheme == "http" or urlParsed.scheme == "https"):
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

    # CSS
    def getLinkTag(self):
        linkTagsCount = 0
        styleLinks = self.soup.find_all('link')
        for link in styleLinks:
            if (link['rel'] != None):
                if (link['rel'][0] == "stylesheet"):
                    linkTagsCount += 1
        return linkTagsCount

    def getLinkHref(self):
        hrefValue = []
        styleLinks = self.soup.find_all('link')
        for link in styleLinks:
            if (link['rel'] != None):
                if (link['rel'][0] == "stylesheet"):
                    if (link['href'] != None):
                        linkParsed = urlparse(link['href'])
                        if (linkParsed.scheme == "http" or linkParsed.scheme == "https"):
                            hrefValue.append(link['href'])

        if (hrefValue.__len__() == 0):
            return " No links with http ou https href detected"
        else:
            return hrefValue

    def getLinkLoadTime(self):
        hrefValue = self.getLinkHref()
        if (type(hrefValue) != str):  # if STR means 0 link found
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
        hrefValue = self.getLinkHref()  # return 1 str if its one error

        if (type(hrefValue) != str):
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
        if (type(list_http_codes) != str):
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
            return " No link found No HTTP code found for test"


    def httpsNoHttpSource(self):
        allLink = []

        error = []

        if(self.url_parsed.scheme == "https"):

            links = self.soup.find_all('a')
            styles = self.soup.find_all('link')
            scripts = self.soup.find_all('script')
            images = self.soup.find_all('img')

            for link in links:
                if (link.has_attr('href')):
                    allLink.append(link['href'])

            for style in styles:
                if (style.has_attr('href')):
                    allLink.append(style['href'])

            for image in images:
                if (image.has_attr('src')):
                    allLink.append(image['src'])

            for script in scripts:
                if (script.has_attr('src')):
                    allLink.append(script['src'])


            for value in allLink:
                urlParsed = urlparse(value)
                if(urlParsed.scheme == "http"):
                    error.append(value)

            if(error.__len__() > 0):
                return error
            else:
                return " 0 http external link found "


        else:
            return " URL is not HTTPS, so not checking for extern link source"

    # PAGE
    # - informations
    def pageLoadingTime(self):
        return requests.get(self.url_page).elapsed.total_seconds()

    # - header
    def pageHeader(self):
        req = urlopen(self.url_page)
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

        if (CSP == None):
            errorHeader.update({"No Content-Security-Policy": "No Content-Security-Policy"})
        if (x_frame_options == None):
            errorHeader.update({"X-Frame-Options": "No X-Frame-Options"})
        if (x_request_guid == None):
            errorHeader.update({"X-Request-Guid": "No X-Request-Guid"})
        if (strict_transport_security == None):
            errorHeader.update({"Strict-Transport-Security": "No Strict-Transport-Security"})
        if (vary == None):
            errorHeader.update({"Vary": "No Vary"})
        if (x_server_by == None):
            errorHeader.update({"X-Served-By": "No X-Served-By"})
        if (x_cache == None):
            errorHeader.update({"X-Cache": "No X-Cache"})
        if (x_timer == None):
            errorHeader.update({"X-Timer": "No X-Timer"})
        if (x_DNS_prefetch_control == None):
            errorHeader.update({"X-DNS-Prefetch-Control": "No X-DNS-Prefetch-Control"})

        return errorHeader

    def headerDate(self):
        header = self.pageHeader()
        last_update = header['Last-Modified']
        if (last_update != None):
            return last_update
        else:
            return " Information not available via header"

    # encoding
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

    def compareEncoding(self):  # compare encoding header / page
        pageEncoding = self.getPageEncoding()
        if (pageEncoding != 'Error cannot find encoding of page'):
            # check if we find charset in header
            _, params = cgi.parse_header('text/html; charset=utf-8')
            if (params['charset']):
                if (params['charset'] == pageEncoding):
                    return " Encoding same on page and header"
                else:
                    return " Encoding not same between page and header => Page : " + pageEncoding + " / Header : " + \
                           params['charset']
            else:
                return " Cannot find encoding into header details"
        else:
            return " Cannot find page encoding"

    # Robots / Security / SiteMap
    def robotsTxtExist(self):
        url = self.homePath
        urlRobotsTxt = url + "robots.txt"
        req = requests.get(urlRobotsTxt)
        if (req.status_code == 200):
            return urlRobotsTxt
        else:
            return " No robots.txt found"

    def sitemapAccess(self):
        trimHomePathURL = self.homePath[:-1] #remove last " / " at the end of URL*

        req = requests.get(trimHomePathURL + "/sitemap.xml")
        if(req.status_code == 200):
            return "accessible at " + trimHomePathURL + "/sitemap.xml"
        else:
            return "not accessible at " + trimHomePathURL + "/sitemap.xml ( error : " + str(req.status_code)+" )"

    def getUrlFromSiteMap(self):
        trimHomePathURL = self.homePath[:-1]  # remove last " / " at the end of URL*

        req = requests.get(trimHomePathURL + "/sitemap.xml")

        if (req.status_code == 200):
            xml = req.text
            soup = BeautifulSoup(xml, "html.parser")

            if(soup.find_all('loc').__len__() == 0):
                return " [X] Cannot parse the sitemap.xml, pages url must be wrapped into <loc></loc> balises if you want the test parsed them"
            else:
                pages_urls = []
                urlsWrapper = soup.find_all('loc')
                for url in urlsWrapper:
                    pages_urls.append(url.text)

                if(pages_urls.__len__() > 0):
                    URLCodeHttp = {}

                    for url in pages_urls:
                        testURL = requests.get(url)
                        URLCodeHttp.update({url: testURL.status_code})
                    return URLCodeHttp


                else:
                    return " URLS parsed, but an error occured !"
        else:
            return " cannot access to the ressource " + str(req.status_code)

    def countHttpErrorFromSiteMap(self):
        URLCodeHttp = self.getUrlFromSiteMap()

        clientErrorCount = 0
        serverErrorCount = 0
        informationResponseCount = 0
        redirectionCount = 0
        successCount = 0

        result = {}

        if(type(URLCodeHttp) != str):
            for code in URLCodeHttp:
                if (URLCodeHttp[code] >= 100 and URLCodeHttp[code] <= 199):
                    informationResponseCount += 1
                if (URLCodeHttp[code] >= 200 and URLCodeHttp[code] <= 299):
                    successCount += 1
                if (URLCodeHttp[code] >= 300 and URLCodeHttp[code] <= 399):
                    redirectionCount += 1
                if(URLCodeHttp[code] >= 400 and URLCodeHttp[code] <= 499 ):
                    clientErrorCount += 1
                if(URLCodeHttp[code] >= 500 and URLCodeHttp[code] <= 599):
                    serverErrorCount += 1

            return {"success": successCount, "informationsResponse": informationResponseCount, "redirection": redirectionCount, "clientError": clientErrorCount, "serverError": serverErrorCount}

        else:
            return " No count for URL HTTP CODE error, because 0 urls gave and parsed by the the test (check at your sitemap.xml, and wrap each links into <loc></loc> xml balise "




    # RSS / ATOM

    # RSS
    def getRSS(self):
        linkTags = self.soup.find_all('link')

        linkRSS = []
        rssType = "application/rss+xml"

        for link in linkTags:
            if(link.has_attr('type')):
                if(link['type'] == rssType):
                    linkRSS.append(link["href"])

        if(linkRSS.__len__() == 0):
            return " No RSS on this URL"
        else:
            return linkRSS

    # Atom
    def getAtom(self):
        linkTags = self.soup.find_all('link')

        linkAtom = []
        atomType = "application/atom+xml"

        for link in linkTags:
            if(link.has_attr('type')):
                if(link['type'] == atomType):
                    linkAtom.append(link["href"])

        if(linkAtom.__len__() == 0):
            return " No Atom on this URL"
        else:
            return linkAtom


    # Get only RSS/ATOM valid URL (http/https)
    def getValidUrlRSS(self):
        rssLinks = self.getRSS()

        validLinkRSS = []

        if(rssLinks != " No RSS on this URL"):
            for link in rssLinks:
                urlParsed = urlparse(link)
                if(urlParsed.scheme == "http" or urlParsed.scheme == "https" ):

                    validLinkRSS.append(link)
                    if(validLinkRSS.__len__() == 0):
                        return " RSS link cannot be testing (only http / http can be)"
                    else:
                        return validLinkRSS
        else:
            return " No RSS links for the validitor test"


    def getValidUrlAtom(self):
        atomLinks = self.getAtom()

        validLinkAtom = []

        if(atomLinks != " No Atom on this URL"):
            for link in atomLinks:
                urlParsed = urlparse(link)
                if(urlParsed.scheme == "http" or urlParsed.scheme == "https" ):

                    validLinkAtom.append(link)
                    if(validLinkAtom.__len__() == 0):
                        return " Atom link cannot be testing (only http / http can be)"
                    else:
                        return validLinkAtom
        else:
            return " No Atom links for the validitor test"


    # RSS / Atom -> loding time / HTTP / HTTPS error / header infos

    def getLoadingTimeRSS(self): # Return time / HTTP | HTTPS code / URL target for RSS
        urlsRss = self.getValidUrlRSS()

        testResultsRSS = {}

        if(type(urlsRss) != str ):
            for url in urlsRss:
                t0 = time.time()
                req = requests.get(url)
                t1 = time.time()
                resTime = t1 - t0

                timeReport = ""
                if (resTime > 5):
                    timeReport = " Long "
                if (resTime > 10):
                    timeReport = " Très long"
                if (resTime < 5):
                    timeReport = " Moyen"
                if (resTime < 2):
                    timeReport = " Rapide"
                if (resTime < 1):
                    timeReport = " Très Rapide"

                resCode = req.status_code

                testResultsRSS.update(
                    {"rss URL": url,
                     "time":  str(resTime),
                     "Loading time": timeReport,
                     "HTTP message": responses[req.status_code]
                     }
                )
                return testResultsRSS

        else:
            return " No RSS url for loading test"

    def getLoadingTimeAtom(self): # Return time / HTTP | HTTPS code / URL target for Atom
        urlsAtom = self.getValidUrlAtom()

        testResultsAtom = {}

        if(type(urlsAtom) != str ):
            for url in urlsAtom:
                t0 = time.time()
                req = requests.get(url)
                t1 = time.time()

                resTime = t1 - t0
                timeReport = ""
                if (resTime > 5):
                    timeReport = " Long "
                if (resTime > 10):
                    timeReport = " Très long"
                if (resTime < 5):
                    timeReport = " Moyen"
                if (resTime < 2):
                    timeReport = " Rapide"
                if (resTime < 1):
                    timeReport = " Très Rapide"

                resCode = req.status_code

                testResultsAtom.update(
                    {"atom URL": url,
                     "time":  str(resTime),
                     "Loading time" : timeReport,
                     "HTTP/HTTPS code": resCode,
                     "HTTP message": responses[req.status_code]}
                )
                return testResultsAtom

        else:
            return " No Atom url for loading test"



    #text/xml OR application/xml -> for /rss.xml

    def checkHeaderRSS(self):
        urlsRSS = self.getValidUrlRSS()

        checkHeaderRSSResults = {}

        if(type(urlsRSS) != str):
            for url in urlsRSS:
                req = requests.get(url)

                extension = urlparse(url)
                isXml = extension.path[-3:]

                if(extension != None or isXml != None):
                    if(isXml == "xml"):
                        header_content_type = req.headers['Content-Type']
                        if(header_content_type == "text/xml" or header_content_type == "application/xml"):
                            checkHeaderRSSResults.update(
                                {"RSS URL": url,
                                 "Header[Content-Type]": header_content_type,
                                 "RSS type": isXml,
                                 "Error": "No"
                                 }
                            )
                            return checkHeaderRSSResults
                        else:
                            checkHeaderRSSResults.update(
                                {"RSS URL": url,
                                 "Header[Content-Type]": header_content_type,
                                 "Atom type": isXml,
                                 "Error": "Yes, content-type not good"
                                 }
                            )
                            return checkHeaderRSSResults
        else:
            return " No RSS urls given for the header test "


    def checkHeaderAtom(self):
        urlsAtom = self.getValidUrlAtom()

        checkHeaderAtomResults = {}

        if(type(urlsAtom) != str):
            for url in urlsAtom:
                req = requests.get(url)

                extension = urlparse(url)
                isXml = extension.path[-3:]

                if(extension != None or isXml != None):
                    if(isXml == "xml"):
                        header_content_type = req.headers['Content-Type']
                        if(header_content_type == "text/xml" or header_content_type == "application/xml"):
                            checkHeaderAtomResults.update(
                                {"Atom URL": url,
                                 "Header[Content-Type]": header_content_type,
                                 "Atom type": isXml,
                                 "Error": "No"
                                 }
                            )
                            return checkHeaderAtomResults
                        else:
                            checkHeaderAtomResults.update(
                                {"Atom URL": url,
                                 "Header[Content-Type]": header_content_type,
                                 "Atom type": isXml,
                                 "Error": "Yes, content-type not good"
                                 }
                            )
                            return checkHeaderAtomResults
        else:
            return " No Atom urls given for the header test "









    # Results tests
    def renderTests(self):
        t0 = time.time() # global timer for all the tests

        # DOM checking
        # - script JS
        tagScript = self.getScriptTags()
        scriptLoadingTime = str(self.getScriptLoadTime())  # only http or https parsed
        scriptHttpCode = str(self.getScriptHttpCode())
        errorResultHttpCode = str(self.countErrorHttpCode())

        # - CSS
        countStyleTag = str(self.getLinkTag())
        linkHref = self.getLinkHref()  # only http or https parsed
        linkLoadingTime = str(self.getLinkLoadTime())
        linkHrefHttpCode = str(self.getHrefHttpCode())
        linkHrefHttpCodeDetail = str(self.getHrefHttpCodeDetail())

        # - Page infos
        header = self.pageHeader()
        headerErrors = self.headerDetails()
        headerDate = self.headerDate()
        pageEncoding = str(self.getPageEncoding())
        compareEncoding = str(self.compareEncoding())  # compare header encoding with page encoding
        robotsTxtExist = str(self.robotsTxtExist())
        httpExternLinkOnHttps = str(self.httpsNoHttpSource())
        sitemapIsAccessible = str(self.sitemapAccess())
        sitemapURLTest = str(self.getUrlFromSiteMap())
        sitemapHTTPCodeResume = str(self.countHttpErrorFromSiteMap())

        # - RSS / ATOM
        RSS = str(self.getRSS())
        validRSS = str(self.getValidUrlRSS())
        loadingTimeRSS = str(self.getLoadingTimeRSS())
        headerRSS = str(self.checkHeaderRSS())

        atom = str(self.getAtom())
        validAtom = str(self.getValidUrlAtom())
        loadingTimeAtom = str(self.getLoadingTimeAtom())
        headerAtom = str(self.checkHeaderAtom())

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
        print(" Sitemap.xml access : " + sitemapIsAccessible)
        print("\n")

        print("- - - - - - HEADER - - - - - -")
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
        print("\n")
        pprint(" GET loading time : " + scriptLoadingTime)
        print("\n")
        pprint(" Script HTTP code response (from scripts loading) : " + scriptHttpCode)
        print("\n")
        print(
            " Script HTTP code response ERROR (from script loading HTTPS ) / ONLY http or https parsed : " + errorResultHttpCode)
        print("\n")

        # CSS link
        print("\n CSS")
        print("\n")
        print(" Link stylesheet tag : " + countStyleTag)
        print("\n")
        print(linkHref)
        print("\n")
        pprint(" Loading time : " + linkLoadingTime)
        print("\n")
        pprint(" HTTP code : " + linkHrefHttpCode)
        print("\n")
        print(" HTTP code detail : " + linkHrefHttpCodeDetail)
        print("\n")

        # Encoding
        print("\n Page Infos ")
        print("\n")
        print(" Page encoding : " + pageEncoding)
        print("\n")
        print(" Compare header encoding with page encoding : " + compareEncoding)
        print("\n")
        # Robots / Security / Sitemap
        print(" robots.txt : " + robotsTxtExist)
        print("\n")
        pprint(" HTTP external link on your HTTPS : " + httpExternLinkOnHttps)
        print("\n")
        pprint(" URL parsed and tests from sitemap.xml : " + sitemapURLTest)
        print("\n")
        pprint(sitemapHTTPCodeResume)
        print("\n")

        # RSS / ATOM
        print("- - - - - - RSS & ATOM - - - - - -")

        print("\n")
        print(" RSS")
        print("\n")
        pprint(" RSS tags : " + RSS)
        print("\n")
        pprint(" RSS HTTP / HTTPS (testable) : " + validRSS)
        print("\n")
        pprint(" RSS Loading time (http / https only tested) : " + loadingTimeRSS)
        print("\n")
        pprint(" RSS Header checking content-type (http / https only tested) : " + headerRSS)
        print("\n")


        print("\n")
        print(" Atom")
        print("\n")
        pprint(" Atom tags : " + atom)
        print("\n")
        pprint(" Atom HTTP / HTTPS (testable) : " + validAtom)
        print("\n")
        pprint(" Atom Loading time (http / https only tested) : " + loadingTimeAtom)
        print("\n")
        pprint(" Atom Header checking content-type (http / https only tested) : " + headerAtom)


        print("\n")
        print("\n")
        t1 = time.time()
        return " Execution time for all the test : " + str(t1 - t0) + "\n" + "______________________________________________________________________" + "\n"
