from dataLoading.requestUtils import getLabelsFromProtectedUrl
from dataLoading.urlBuilder import validateAndBuildUrl  
from plotting.plotUtils import drawPlot
import dataLoading.urlBuilder    
import sys

testNumber, wheel, sector, station = sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
url = validateAndBuildUrl(testNumber, wheel, sector, station)
labels = getLabelsFromProtectedUrl(url)
drawPlot(labels)
