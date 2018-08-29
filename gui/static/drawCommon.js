const emptyColor = "hsl(0,0%,50%)";

const getColor = (value,min = 0, max = 255) => {
    if (value === -1) {
        return emptyColor;
    }
    return "hsl(" + ((value-min)/(max-min)*255)+ ","+  "100" + "%, 50%)";
};

function wrap(outerElementString, innerElement){
    let outer = document.createElement(outerElementString);
    outer.appendChild(innerElement);
    return outer;
}

function getMax(array){
    return Math.max(...array.map(e => Array.isArray(e) ? getMax(e) : e));
}

function getMin(array){
    return Math.min(...array.map(e => Array.isArray(e) ? getMin(e) : e));
}