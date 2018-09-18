function onFetchData(){
    let runValue =  getStringValueFromInputField("runInput");
    if (!runValue){
        showApiError("Empty RUN input value");
    }

    fetch(`/fetch/${runValue}/`, {method:"POST"}).then(
        (response) => {
            if (validateApiResponseCode(response)) {
                showApiMessage("Fetching for run: " + runValue +  " initialized!")
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