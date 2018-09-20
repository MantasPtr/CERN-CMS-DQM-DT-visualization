import {cached_data} from "./tableCache.js";
import {redrawTable} from "./drawTable.js"
export const settings = {}

settings.showText = null; 
settings.showInfluence = null; 


settings.getShowText = () => {
    if (settings.showText === null) {
        settings.showText = document.getElementById("showNumbersCheck").checked;
    }
    return settings.showText
}

export const toggleShowText = (elem) => {
    settings.showText = elem.checked;
    redrawTable()
}

export const toggleInfluence = (elem) => {
    settings.showInfluence = elem.checked;
    redrawTable()
}

