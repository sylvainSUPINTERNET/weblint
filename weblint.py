import sys
import requests
import validators


from Core import CoreTest

if(sys.argv.__len__() < 2):
    print(" Please enter a valid url to start the test, ex : http://fr.wowhead.com/death-knight-transmogrification-armor-sets-guide ")
else:
    url = str(sys.argv[1])
    if(validators.url(url) != True):
        print(" [X] Cannot test this url : Malformed")
    else:
        print(" URL is valid \n")
        try:
            req = requests.get(url)
        except requests.ConnectionError:
            print(" Can't connect to the site (dosnt exist !) \n")
        else:
            if (req.status_code == 200):
                coreTest = CoreTest(str(sys.argv[1]))
                print(" URL requested : " + coreTest.getUrlPage())
                print(" Please wait while the test runs . . .")
                print("\n")
                print(coreTest.renderTests())
            else:
                print(" Error occured : " + str(req.status_code) )




