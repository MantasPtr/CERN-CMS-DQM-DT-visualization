export function validateApiResponseCode(response){
    if (response.ok) {
        hideApiError();
        return true;
    } else {
        return response.text().then(text => { 
            if (text) {
                showApiError(text)
            } else {
                showApiError(response.status + ": " + response.statusText )
            }
            return false;
        })
    }
}

const apiErrorBannerID= "apiError";
const apiMessageBannerID = "apiMessage";

export function showApiError(message){
    hideApiMessage()
    let errorBanner = document.getElementById(apiErrorBannerID);
    errorBanner.hidden = false;
    errorBanner.textContent = "Error: " + message;
}

export function hideApiError(){
    let errorBanner = document.getElementById(apiErrorBannerID);
    errorBanner.hidden = true;
    errorBanner.text = "";
}

export function showApiMessage(message){
    hideApiError()
    let messageBanner = document.getElementById(apiMessageBannerID);
    messageBanner.hidden = false;
    messageBanner.textContent = message;
}

export function hideApiMessage(){
    let messageBanner = document.getElementById(apiMessageBannerID);
    messageBanner.hidden = true;
    messageBanner.text = "";
}   

export function getStringValueFromInputField(selector){
    let element = document.getElementById(selector)
    return document.getElementById(selector).value.trim();
}

export const logs = (d) => {console.log(d); return d;}