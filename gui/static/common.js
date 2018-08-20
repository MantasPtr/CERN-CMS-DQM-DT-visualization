
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

const apiErrorBannerID= "apiError";
const apiMessageBannerID = "apiMessage";


function showApiError(message){
    hideApiMessage()
    let errorbanner = document.getElementById(apiErrorBannerID);
    errorbanner.hidden = false;
    errorbanner.textContent = "Error: " + message;
}

function hideApiError(){
    let errorbanner = document.getElementById(apiErrorBannerID);
    errorbanner.hidden = true;
    errorbanner.text = "";
}

function showApiMessage(message){
    hideApiError()
    let messagebanner = document.getElementById(apiMessageBannerID);
    messagebanner.hidden = false;
    messagebanner.textContent = message;
}

function hideApiMessage(){
    let messageBanner = document.getElementById(apiMessageBannerID);
    messageBanner.hidden = true;
    messageBanner.text = "";
}   

function getStringValueFromInputField(selector){
    let element = document.getElementById(selector)
    return document.getElementById(selector).value.trim();
}

const logs = (d) => {console.log(d); return d;}