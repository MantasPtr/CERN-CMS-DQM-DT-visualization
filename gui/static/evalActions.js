let run;
let wheel;
let sector;
let station;

window.onload = onPageLoad;

function onPageLoad(){
    let inputArray = Object.values(getInput());
    if (!inputArray.includes("")){
        onLoadDataFromDB();
    }
}

function onLoadDataFromDB(){
    let { runValue, wheelValue, sectorValue, stationValue } = getInput();
    validateInput();
    fetchdata();
    
    function validateInput(){
        if (!(runValue && wheelValue && sectorValue && stationValue)) {
            showApiError("some value is empty");
            return;
        }
        hideApiError();
    }

    function fetchdata() {
        let url = "/data/" + runValue + "/" + wheelValue + "/" + sectorValue + "/" + stationValue + "/"
        fetch(url).then((response) => {
            validateApiResponseCode(response);
            response.json().then(processJsonResponse);
        });
    }

    function processJsonResponse (matrix){
        createTable(matrix);
        hideApiError();
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
    if (cacheData === null) {
        return;
    }
    const saveObject = {}
    saveObject.run = run;
    saveObject.wheel = wheel;
    saveObject.sector = sector;
    saveObject.station = station;
    saveObject.layers =  getCheckedValues();

    fetch("/save/", {
        method:"POST",
        body:JSON.stringify(saveObject),
        headers:{"Content-Type": "application/json; charset=utf-8",}
    }).then((response) => {
        validateApiResponseCode(response);
        response.json().then(processJsonResponse);
    })

    function getCheckedValues(){
        const checkboxes = Array.from(document.querySelectorAll(".layer-selection"));
        return checkboxes.filter(c => c.checked).map(c => c.getAttribute("index"));
    }

    function processJsonResponse (json){
        showApiMessage("Run " + run + (json.updated ?" updated!": " saved!"))
    }
}