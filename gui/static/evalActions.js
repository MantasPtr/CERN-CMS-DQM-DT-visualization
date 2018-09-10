let run;
let wheel;
let sector;
let station;
let containsValidData = false;

window.onload = onPageLoad;

function onPageLoad(){
    let inputArray = Object.values(getInput());
    if (!inputArray.includes("")){
        onLoadDataFromDB();
    }
}

function onLoadDataFromDB(){
    let { runValue, wheelValue, sectorValue, stationValue } = getInput();
    if (inputIsValid()){
        fetchData();
    }

    function inputIsValid(){
        if (!(runValue && wheelValue && sectorValue && stationValue)) {
            showApiError("some value is empty");
            return false;
        }
        hideApiError();
        return true;
    }

    function fetchData() {
        let url = "/data/" + runValue + "/" + wheelValue + "/" + sectorValue + "/" + stationValue + "/";
        fetch(url).then((response) => {
            if (!validateApiResponseCode(response)) {
                containsValidData = false;
                return;
            }
            response.json().then(processJsonResponse);
        });
    }

    function processJsonResponse (data){
        cached_data.data = data.matrix;
        cached_data.saliency = data.saliency;
        cached_data.scores = data.scores;
        createTable(data.matrix, data.evaluation ? data.evaluation.bad_layers : []);
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

function save(){
    if (containsValidData === null) {
        return;
    }
    const saveObject = {}
    saveObject.run = run;
    saveObject.wheel = wheel;
    saveObject.sector = sector;
    saveObject.station = station;
    saveObject.layers =  _getCheckedValues();

    fetch("/save/", {
        method:"POST",
        body:JSON.stringify(saveObject),
        headers:{"Content-Type": "application/json; charset=utf-8",}
    }).then((response) => {
        if (validateApiResponseCode(response)) {
            response.json().then(processJsonResponse);
        }
    })  

    function processJsonResponse (json){
        showApiMessage("Run " + run + (json.updated ?" updated!": " saved!"))
        url = "/next/";
        window.location.replace(url)
    }
}

function _getCheckedValues(){
    const checkBoxes = Array.from(document.querySelectorAll(".layer-selection"));
    return checkBoxes.filter(c => c.checked).map(c => c.getAttribute("index"));
}

function skip(){
    if (containsValidData === null) {
        return;
    }
    let url = "/skip/" + run + "/" + wheel + "/" + sector + "/" + station + "/";
    window.location.replace(url)
}