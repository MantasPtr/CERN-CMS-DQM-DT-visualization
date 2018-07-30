

function onFetchData(){
    let runValue =  getStringValueFromInputField("runInput");
    if (!runValue){
        console.log("empty run value");
    }

    fetch("/fetch/" + runValue).then(
        (response) => {
            validateApiResponseCode(response);
            logs(response)
        }
    );
}