let maxLayers = 0;
let maxValue = 0;

let cacheData = null;

function createTable(tableData) {
    //inverting data because its done in prod
    // slice just copies data because reverse modifies array
    tableData.slice().reverse();

    maxValue = getMax(tableData);
    drawColorPalet();
    cacheData = tableData;
    maxLayers = tableData.length;
    let table = document.createElement("table");

    table.appendChild(createTableHeader(tableData))
    let tableBody = document.createElement("tbody");
    tableData.forEach(createRows);
    table.appendChild(tableBody);
    let container = document.querySelector("#image");
    container.innerHTML = "";
    container.appendChild(table);

    function createTableHeader(tableData){
        let thead = document.createElement("thead");
        let headerRow = thead.appendChild(document.createElement("tr"));
        let cellHeader =document.createElement("th");
        cellHeader.setAttribute("colspan", tableData[0].length);
        headerRow.appendChild(cellHeader);
        let layerHeader = document.createElement("th")
        layerHeader.textContent = "Bad layers:";
        headerRow.appendChild(layerHeader);
        return thead;
    }

    function createRows(rowData, rowIndex) {
        let row = document.createElement("tr");
        rowData.forEach(createCell);
        let layerS = addLayerSelector(rowIndex);
        row.appendChild(layerS)
        tableBody.appendChild(row);

        function createCell(cellData) {
            let cell = document.createElement("td");
            if (settings.getShowText())
                cell.appendChild(document.createTextNode(cellData));
            cell.style.backgroundColor = getColor(cellData, maxValue);
            row.appendChild(cell);
        };
    }

    function addLayerSelector(layerIndex){
        const LAYER_SUFFIX = "Layer ";
        const LAYER_CLASS = "layer-selection";
        const index = layerIndex + 1 ; // zero based -> one based
        let span = document.createElement("span");
        span.classList.add("input-group-addon");
        let input = document.createElement("input");
        input.classList.add(LAYER_CLASS);
        input.setAttribute("index", index); 
        input.type = "checkbox";
        input.checked = false;
        span.appendChild(input);
        span.appendChild(document.createTextNode(LAYER_SUFFIX + index));
        return wrap("td", span);
    }
};

function drawColorPalet() {
    let canvas = document.createElement("canvas")
    let canvasDiv = document.querySelector("#colorbar");
    canvasDiv.innerHTML = "";

    canvas.height = 325
    canvas.width = 30

    let ctx = canvas.getContext("2d");
    let grd = ctx.createLinearGradient(0, 0, 0, 325);
    grd.addColorStop(0     , getColor(1     * maxValue, maxValue));
    grd.addColorStop(0.125 , getColor(0.875 * maxValue, maxValue));
    grd.addColorStop(0.25  , getColor(0.75  * maxValue, maxValue));
    grd.addColorStop(0.375 , getColor(0.625 * maxValue, maxValue));
    grd.addColorStop(0.5   , getColor(0.5   * maxValue, maxValue));
    grd.addColorStop(0.625 , getColor(0.375 * maxValue, maxValue));
    grd.addColorStop(0.75  , getColor(0.25  * maxValue, maxValue));
    grd.addColorStop(0.875 , getColor(0.125 * maxValue, maxValue));
    grd.addColorStop(1     , getColor(0     * maxValue, maxValue));

    document.querySelector("#max_colorbar").textContent = maxValue;
    document.querySelector("#min_colorbar").textContent = 0;

    ctx.fillStyle = grd;
    ctx.fillRect(0, 0, 30, 325);
    canvasDiv.appendChild(canvas)
}