
function validateApiResponseCode(response){
    if (response.status == 200) {
        hideApiError();
        return true;
    } else {
        if (response.BodyUsed) {
            response.json().then(v => showApiError(v))
        } else {
            showApiError(response.status + ": " + response.statusText )
        }
    }
}

const apiErrorBannerId= "apiError";

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

function getStringValueFromInputField(selector){
    let element = document.getElementById(selector)
    return document.getElementById(selector).value.trim();
}

const logs = (d) => {console.log(d); return d;}