from requestUtils import getLabelsFromProtectedUrl
from plotUtils import drawPlot
import urlBuilder    
import sys

testNumber, wheel, sector, station = sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
url = urlBuilder.buildUrl(testNumber, wheel, sector, station)
labels = getLabelsFromProtectedUrl(url)
drawPlot(labels)
