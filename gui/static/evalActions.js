const bootstrapErrorClass = "is-invalid";
const apiErrorBannerId= "apiError";

let run;
let wheel;
let sector;
let station;


function onLoadData(){
    let runValue =  getStringValueFromInputField("runInput");
    let wheelValue = getStringValueFromInputField("wheelInput");
    let sectorValue = getStringValueFromInputField("sectorInput");
    let stationValue = getStringValueFromInputField("stationInput");

    if (!(runValue && wheelValue && sectorValue && stationValue)) {
        console.log("some value is empty")
        return;
    }

    fetch("/" +runValue+ "/" + wheelValue + "/" + sectorValue + "/" + stationValue + "/labels.json").then(
        (response) => {
            validateApiResponseCode(response);
            response.json().then(processJsonResponse);
        }
    );

    function processJsonResponse (json){
            let hist = json.hist;
            if (typeof hist === "string") {
                showApiError("Error while retrieving data - API returned: " + hist);
            }
            else {
                let matrix = hist.bins.content;
                createTable(matrix);
                hideApiError();
                run = runValue;
                wheel = wheelValue;
                sector = sectorValue;
                station = stationValue;
            }
    };

    function showApiError(message){
        let errorbanner = document.getElementById(apiErrorBannerId);
        errorbanner.hidden = false;
        errorbanner.textContent = message;
    }

    function hideApiError(){
        let errorbanner = document.getElementById(apiErrorBannerId);
        errorbanner.hidden = true;
        errorbanner.text = "";
    }   
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
    logs(saveObject)

    function getCheckedValues(){
        const checkboxes = Array.from(document.querySelectorAll(".layer-selection"));
        return checkboxes.filter(c => c.checked).map(c => c.getAttribute("index"));
    }
}