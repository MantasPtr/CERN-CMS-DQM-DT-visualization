const settings = {}

settings.showText = null; 

settings.toggleShowText = (d) => {
    settings.showText = document.querySelector("#showNumbersCheck").checked;
    createTable(cacheData);
}

settings.getShowText = () => {
    if (settings.showText === null) {
        settings.showText = document.getElementById("showNumbersCheck").checked;
    }
    return settings.showText
}


