const emptyColor = "hsl(0,0%,50%)";

export const getColor = (value,min = 0, max = 255) => {
    if (value === -1) {
        return emptyColor;
    }
    if(max == min){
        return "hsl(255, 100%, 50%)"
    }
    return "hsl(" + ((value-min)/(max-min)*255)+ ", 100%, 50%)";
}

export function wrap(outerElementString, innerElement){
    let outer = document.createElement(outerElementString);
    outer.appendChild(innerElement);
    return outer;
}

export function getMax(array){
    return Math.max(...array.map(e => Array.isArray(e) ? getMax(e) : e));
}

export function getMin(array, ignoreValue = -1 ){
    return Math.min(...array.map(e => Array.isArray(e) ? getMin(e) : _replaceIfEqual(e, ignoreValue, 0) ));
}

function _replaceIfEqual(x, value, replace) {
    return x != value ?  x : replace;
}