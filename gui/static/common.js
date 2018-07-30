
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

function getStringValueFromInputField(selector){
    let element = document.getElementById(selector)
    return document.getElementById(selector).value.trim();
}

const logs = (d) => {console.log(d); return d;}