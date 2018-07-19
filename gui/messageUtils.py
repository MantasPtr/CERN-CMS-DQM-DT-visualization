from dataLoading.paramContainer import ParamContainer    

def getTitle(container: ParamContainer):
    return ("Run: %s, W: %s, St: %s, Sec: %s" % 
            (container.run, container.wheel, container.station, container.sector))