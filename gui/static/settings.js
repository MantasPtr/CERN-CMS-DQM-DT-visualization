const settings = {}

settings.showText = null; 
settings.showInfluence = null; 

settings.toggleShowText = (elem) => {
    settings.showText = elem.checked;
    redrawTable()
}

settings.getShowText = () => {
    if (settings.showText === null) {
        settings.showText = document.getElementById("showNumbersCheck").checked;
    }
    return settings.showText
}

settings.toggleInfluenceText = (elem) => {
    settings.showInfluence = elem.checked;
    redrawTable()
}

function redrawTable(){
    if (settings.showInfluence) {
        createTable(cached_data.saliency);
    } else {
        createTable(cached_data.data);
    }
}