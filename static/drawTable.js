let showText = false;
const LAYER_SUFFIX = "Layer ";
let maxLayers = 0;
let maxValue = 0;

let cacheData = null;

function createTable(tableData) {
    maxValue = getMax(tableData);
    drawColorPalet();
    cacheData = tableData;
    maxLayers = tableData.length;
    let table = document.createElement('table');
    let tableBody = document.createElement('tbody');
    tableData.forEach(createRows);
    table.appendChild(tableBody);
    let container = document.querySelector("#image");
    container.innerHTML = "";
    container.appendChild(table);

    function createRows(rowData, i) {
        let row = document.createElement('tr');
        rowData.forEach(createCell);
        let layerS = addLayerSelector(i);
        row.appendChild(layerS)
        tableBody.appendChild(row);

        function createCell(cellData) {
            let cell = document.createElement('td');
            if (showText)
                cell.appendChild(document.createTextNode(cellData));
            cell.style.backgroundColor = getColor(cellData, maxValue);
            row.appendChild(cell);
        };
    }

    function addLayerSelector(text){
        let span = document.createElement('span');
        span.classList.add("input-group-addon");
        let input = document.createElement("input");
        input.type = "checkbox";
        input.checked = true;
        span.appendChild(input);
        span.appendChild(document.createTextNode(LAYER_SUFFIX + (maxLayers - text)));
        return wrap("td", span);
    }
};

function drawColorPalet() {
    let canvasDiv = document.querySelector("#colorbar");
    canvasDiv.innerHTML = "";
    let canvas = document.createElement("canvas")
    let ctx = canvas.getContext("2d");

    let grd = ctx.createLinearGradient(0, 0, 0, 100);
    grd.addColorStop(0, getColor(0, maxValue));
    //grd.addColorStop(0.5, "red");
    grd.addColorStop(1, getColor(maxValue, maxValue));

    ctx.fillStyle = grd;
    ctx.fillRect(0, 0,  20, 200);
    canvasDiv.appendChild(canvas)
}


function toggleShowText(d) {
    showText = document.querySelector("#showNumbersCheck").checked
    if (cacheData) {
        createTable(cacheData)
    }
}
