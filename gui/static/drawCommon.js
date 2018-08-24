const emptyColor = "hsl(0,0%,50%)";

const getColor = (value, max) => {
    max = max ? max : 255;
    if (value === -1) {
        return emptyColor;
    }
    v =  value/max;
    return "hsl(" + (255 - value/max*255)+ ","+  "100" + "%, 50%)";
};

function wrap(outerElementString, innerElement){
    let outer = document.createElement(outerElementString);
    outer.appendChild(innerElement);
    return outer;
}

function getMax(array){
    return Math.max(...array.map(e => Array.isArray(e) ? getMax(e) : e));
}