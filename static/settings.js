const settings = {}

settings.showText = false; 

settings.toggleShowText = function toggleShowText(d) {
    showText = document.querySelector("#showNumbersCheck").checked
    if (cacheData) {
        createTable(cacheData)
    }
}


