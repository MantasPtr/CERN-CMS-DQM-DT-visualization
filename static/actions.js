function loadData(){
    let run =  getValueFromInputField("#runInput");
    let wheel = getValueFromInputField("#wheelInput");
    let sector = getValueFromInputField("#sectorInput");
    let station = getValueFromInputField("#stationInput");
    if (!(run && wheel && sector && station)) {
        console.log("some value is empty")
        return
    }
    fetch("/" +run+ "/" + wheel + "/" + sector + "/" + station + "/labels.json").then(
        (data) => console.log("OK",data)
    ).catch(
        (error) => console.log("ERROR:",error) 
    )


}

function getValueFromInputField(selector){
    value =  document.querySelector(selector).value.trim();
    console.log(value)
    return value;
}