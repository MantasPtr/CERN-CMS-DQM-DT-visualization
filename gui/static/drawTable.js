import {getRainbowColor, getGreyColor, getMax, getMin, wrap} from "./drawCommon.js";
import {settings} from "./settings.js";
import {logs} from "./common.js";
import {getCheckedValues} from "./evalActions.js";
import {cached_data} from "./tableCache.js";
let maxLayers = 0;
let maxValue = 0;
let minValue = 0;
const NETWORK_SCORE_DIGITS = 3;

export function redrawTable(args = {}){
    if (settings.showInfluence) {
        args.getColor = args.getColor || getGreyColor;
        createTable(cached_data.saliency, args);
    } else {
        args.getColor = args.getColor || getRainbowColor;
        createTable(cached_data.data, args);
    }
}

function createTable(tableData, {badLayers = getCheckedValues(), getColor = getRainbowColor} = {} ) {

    if (tableData == null) {
        logs("no data given");
        return;
    }
    let emptyValue = -1;
    let scores = cached_data.scores;
    //inverting data because its done in prod
    // slice just copies data because reverse modifies array
    tableData = tableData.slice().reverse();
    scores = scores.slice().reverse();

    maxValue = getMax(tableData);
    minValue = getMin(tableData);
    minValue = minValue != emptyValue ? minValue : 0;
    drawColorPallet(getColor);
    maxLayers = tableData.length;
    let table = document.createElement("table");

    table.appendChild(_createTableHeader(tableData))
    let tableBody = document.createElement("tbody");
    tableData.forEach(_createRows);
    table.appendChild(tableBody);
    let container = document.querySelector("#image");
    container.innerHTML = "";
    container.appendChild(table);

    function _createTableHeader(tableData){
        let thead = document.createElement("thead");
        let headerRow = thead.appendChild(document.createElement("tr"));
        let cellHeader =document.createElement("th");
        cellHeader.setAttribute("colspan", tableData[0].length);
        headerRow.appendChild(cellHeader);
        let layerHeader = document.createElement("th")
        layerHeader.textContent = "Bad layers";
        headerRow.appendChild(layerHeader);
        let scoreHeader = document.createElement("th");
        scoreHeader.textContent = "Bad score";
        headerRow.appendChild(scoreHeader);
        return thead;
    }

    function _createRows(rowData, rowIndex) {  
        let row = document.createElement("tr");
        rowData.forEach(createCell);
        let layerS = addLayerSelector(rowIndex);
        row.appendChild(layerS);
        let networkScore =  addNetworkScores(rowIndex);
        row.appendChild(networkScore);
        tableBody.appendChild(row);

        function createCell(cellData) {
            let cell = document.createElement("td");
            addText(cell, cellData);
            cell.style.backgroundColor = getColor(cellData, maxValue, minValue);
            row.appendChild(cell);
        }

        function addText(cell, cellData) {
            if (settings.getShowText()) { 
                cellData = Number.isInteger(cellData) ? cellData : cellData.toFixed(1);
                cell.appendChild(document.createTextNode(cellData));
            }
        }
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
        input.checked = !!badLayers[layerIndex]; // !! converts to boolean
        span.appendChild(input);
        span.appendChild(document.createTextNode(LAYER_SUFFIX + index));
        return wrap("td", span);
    }

    function addNetworkScores(layerIndex){
        const SCORE_CLASS = "network_score";
        let td = document.createElement("td");
        td.classList.add(SCORE_CLASS);
        td.textContent = scores[layerIndex].toFixed(NETWORK_SCORE_DIGITS)
        return td
    }

};

function drawColorPallet(getColor) {
    let canvas = document.createElement("canvas")
    let canvasDiv = document.querySelector("#colorbar");
    canvasDiv.innerHTML = "";

    canvas.height = 325
    canvas.width = 30

    let ctx = canvas.getContext("2d");
    let grd = ctx.createLinearGradient(0, 0, 0, 325);
    grd.addColorStop(0     , getColor(0     * (maxValue-minValue) + minValue, minValue, maxValue));
    grd.addColorStop(0.125 , getColor(0.125 * (maxValue-minValue) + minValue, minValue, maxValue));
    grd.addColorStop(0.25  , getColor(0.25  * (maxValue-minValue) + minValue, minValue, maxValue));
    grd.addColorStop(0.375 , getColor(0.375 * (maxValue-minValue) + minValue, minValue, maxValue));
    grd.addColorStop(0.5   , getColor(0.5   * (maxValue-minValue) + minValue, minValue, maxValue));
    grd.addColorStop(0.625 , getColor(0.625 * (maxValue-minValue) + minValue, minValue, maxValue));
    grd.addColorStop(0.75  , getColor(0.75  * (maxValue-minValue) + minValue, minValue, maxValue));
    grd.addColorStop(0.875 , getColor(0.875 * (maxValue-minValue) + minValue, minValue, maxValue));
    grd.addColorStop(1     , getColor(1     * (maxValue-minValue) + minValue, minValue, maxValue));

    document.querySelector("#max_colorbar").textContent = maxValue;
    document.querySelector("#min_colorbar").textContent = minValue;

    ctx.fillStyle = grd;
    ctx.fillRect(0, 0, 30, 330);

    // TODO: drawing lines (not complete)
    // maxLog10 = Math.round(Math.max(Math.log10(Math.abs(minValue)),Math.log10(Math.abs(maxValue))))
    // logs("maxLog10 " + maxLog10)
    // stepSize = Math.pow(10,maxLog10)
    // diff = maxValue - minValue;
    // steps = diff/stepSize +1
    // logs("steps " + steps)
    // logs("diff " + diff)
    // let ctx2 = canvas.getContext("2d");
    // for (let i=0;i<=steps;i++) {
    //     y = i*steps*330/diff
    //     logs(y)
    //     ctx2.moveTo(0,y);
    //     ctx2.lineTo(30,y);
    // }
    // ctx2.stroke();
    canvasDiv.appendChild(canvas)
}