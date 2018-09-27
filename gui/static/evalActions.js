import {redrawTable} from "./drawTable.js";
import {validateApiResponseCode, showApiError, showApiMessage, hideApiError, getStringValueFromInputField, logs} from "./common.js";
import {cached_data} from "./tableCache.js";
import {toggleInfluence, toggleShowText} from "./settings.js";

let run;
let wheel;
let sector;
let station;
let containsValidData = false;

window.onLoadDataFromDB = onLoadDataFromDB;
window.onSave = onSave;
window.onSkip = onSkip;
window.onToggleInfluence = toggleInfluence;
window.onToggleText = toggleShowText;
window.onload = onPageLoad;

function onPageLoad(){
    let inputArray = Object.values(getInput());
    if (!inputArray.includes("")){
        onLoadDataFromDB();
    }
}

function onLoadDataFromDB(){
    let { runValue, wheelValue, sectorValue, stationValue } = getInput();
    if (_inputIsValid()){
        _fetchData();
    }

    function _inputIsValid(){
        if (!(runValue && wheelValue && sectorValue && stationValue)) {
            showApiError("some value is empty");
            return false;
        }
        hideApiError();
        return true;
    }

    function _fetchData() {
        let url = `/data/${runValue}/${wheelValue}/${sectorValue}/${stationValue}/`;
        fetch(url).then((response) => {
            if (!validateApiResponseCode(response)) {
                containsValidData = false;
                return;
            }
            response.json().then(_processJsonResponse);
            window.history.replaceState("","",`/eval/${runValue}/${wheelValue}/${sectorValue}/${stationValue}/`);
        });
    }
    function _processJsonResponse (data){
        cached_data.data = data.matrix;
        cached_data.saliency = data.saliency;
        cached_data.scores = data.scores;
        redrawTable({badLayers: data.evaluation ? data.evaluation.bad_layers : []});
        hideApiError();
        containsValidData = true;
        run = runValue;
        wheel = wheelValue;
        sector = sectorValue;
        station = stationValue;
    }
};


function getInput() {
    let runValue = getStringValueFromInputField("runInput");
    let wheelValue = getStringValueFromInputField("wheelInput");
    let sectorValue = getStringValueFromInputField("sectorInput");
    let stationValue = getStringValueFromInputField("stationInput");
    return { runValue, wheelValue, sectorValue, stationValue };
}

function onSave(){
    if (containsValidData === null) {
        return;
    }
    const saveObject = {}
    saveObject.run = run;
    saveObject.wheel = wheel;
    saveObject.sector = sector;
    saveObject.station = station;
    saveObject.layers =  getCheckedValues();

    fetch("/eval/save_user_scores/", {
        method:"PATCH",
        body:JSON.stringify(saveObject),
        headers:{"Content-Type": "application/json; charset=utf-8",}
    }).then((response) => {
        if (validateApiResponseCode(response)) {
            response.json().then(_processJsonResponse);
        }
    })  

    function _processJsonResponse (json){
        showApiMessage("Run " + run + (json.updated ?" updated!": " saved!"))
        let url = "/eval/next/";
        window.location.replace(url)
    }
}

export function getCheckedValues(){
    const checkBoxes = Array.from(document.querySelectorAll(".layer-selection"));
    return checkBoxes.map(c => c.checked ? 1 : 0 );
}

function onSkip(){
    if (containsValidData === null) {
        return;
    }
    let url = "/eval/skip/" + run + "/" + wheel + "/" + sector + "/" + station + "/";
    window.location.replace(url)
}