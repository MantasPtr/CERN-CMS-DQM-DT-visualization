const bootstrapErrorClass = "is-invalid";
const apiErrorBannerId= "apiError";
function loadData(){
    let run =  getValueFromInputField("runInput");
    let wheel = getValueFromInputField("wheelInput");
    let sector = getValueFromInputField("sectorInput");
    let station = getValueFromInputField("stationInput");

    if (!(run && wheel && sector && station)) {
        console.log("some value is empty")
        return;
    }
    fetch("/" +run+ "/" + wheel + "/" + sector + "/" + station + "/labels.json").then(
            (response) => {
                validateApiResponse(response)

                response.json().then(
                    (json) => {
                    let matrix = json.hist.bins.content;
                    createTable(matrix)
                }
            )
        }
    )
}

function getValueFromInputField(selector){
    let element = document.getElementById(selector)
    return document.getElementById(selector).value.trim();
}

function validateApiResponse(response){
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

function showApiError(message){
    logs(message);
    let errorbanner = document.getElementById(apiErrorBannerId);
    errorbanner.hidden = false;
    errorbanner.textContent = message;
}

function hideApiError(){
    let errorbanner = document.getElementById(apiErrorBannerId);
    errorbanner.hidden = true;
    errorbanner.text = "";
}

// function validateInput(minValue, maxValue, errorID, inputID){
//     let inputElement = document.getElementById(errorID);
//     let errorElement = document.getElementById(inputID);
//     if (!maxValue && value < minValue) {
//         errorElement.classList.add(bootstrapErrorClass)
//         errorElement.hidden = false;
//         errorElement.text = "Value must be larger than " + minValue + " !";
//     } else if (value < minValue || value > maxValue) {
//         errorElement.classList.add(bootstrapErrorClass)
//         errorElement.hidden = false;
//         errorElement.text = "Value must be between " + minValue + " and " + maxValue + " !"
//     } else {
//         errorElement.hidden = true;
//     }
// }


// function showError(inputID, errorID, message) {
//     let inputElement = document.getElementById(errorID);
//     if (inputElement.classList.find(v=>(v=>bootstrapErrorClass)))
//     let errorElement = document.getElementById(inputID);

// }

// function hideError(inputID, errorID) {
//     let inputElement = document.getElementById(errorID);
//     let errorElement = document.getElementById(inputID);
// }