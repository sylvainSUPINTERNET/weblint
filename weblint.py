
from Core import CoreTest
coreTest = CoreTest('https://www.sslshopper.com/ssl-checker.html')

print(coreTest.getUrlPage())

print(coreTest.getPageSourceCode())
print(coreTest.getSoupPretty())

print(coreTest.renderTests())
