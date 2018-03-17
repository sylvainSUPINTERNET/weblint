
import sys
import requests
import urllib

from django.core.validators import URLValidator
from Core import CoreTest

isValid = False

if(sys.argv.__len__() < 2):
    print(" Please enter an url to start the test")
else:
    url = str(sys.argv[1])
    val = URLValidator()
    try:
        val(url)
        isValid = True
        if (isValid):
            print(" URL is valid")
            req = requests.get(url)
            if (req.status_code == 200):
                coreTest = CoreTest(str(sys.argv[1]))

                print(coreTest.getUrlPage())

                # display code source HTML
                #print(coreTest.getPageSourceCode())
                # display code source HTML prettify
                #print(coreTest.getSoupPretty())

                print(coreTest.renderTests())

                #print(coreTest.getUrlParsed()) #For test

            else:
                print(" Error occured => " + str(req.status_code))
        else:
            print(" URL given not valid !")
    except:
        isValid = False






