import {getStringValueFromInputField, showApiMessage, showApiError, validateApiResponseCode, logs } from "./common.js";

window.onFetchData = onFetchData;
window.onReevaluate = onReevaluate;
window.deleteRun = deleteRun;

function onFetchData(){
    let runValue =  getStringValueFromInputField("runInput");
    if (!runValue){
        showApiError("Empty RUN input value");
        return;
    }

    fetch(`/fetch/${runValue}/`, {method:"POST"}).then(
        (response) => {
            if (validateApiResponseCode(response)) {
                showApiMessage(`Fetching for run: ${runValue} initialized!`);
            }
        }
    );
}

function onReevaluate(){
    fetch(`/data/reevaluate/`, {method:"POST"}).then(
        (response) => {
            if (validateApiResponseCode(response)) {
                showApiMessage(`Reevaluation started!`);
            }
        }
    );
}


function deleteRun(identifier){
    fetch("/data/" + identifier.run, {
        method:"DELETE"
    }).then(
        (response) => { 
            if (validateApiResponseCode(response)) {
                response.text().then(text => showApiMessage(`${text} record was deleted.`))
            }
        }
    )
};