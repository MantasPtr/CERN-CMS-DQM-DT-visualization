from logic.runContainer import RunContainer 

def getTitle(container: RunContainer):
    return ("Run: %s, W: %s, St: %s, Sec: %s" % 
            (container.run, container.wheel, container.station, container.sector))