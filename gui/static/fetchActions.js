

function onFetchData(){
    let runValue =  getStringValueFromInputField("runInput");
    if (!runValue){
        showApiError("Empty RUN input value");
    }

    fetch("/fetch/" + runValue).then(
        (response) => {
            validateApiResponseCode(response);
            logs(response)
        }
    );
}