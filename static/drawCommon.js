const emptyColor = d3.hsl(0,0,0); 

const getColor = (value, max) =>{
    max = max ? max : 255 
    if (value === -1) return emptyColor;
    return d3.hsl(100, value/max, 0.5);
}

const logs = (d) => {console.log(d); return d;}

function wrap(outerElementString, innerElement){
    let outer = document.createElement(outerElementString);
    outer.appendChild(innerElement);
    return outer;
}

function getMax(array){ 
    return Math.max(...array.map(e => Array.isArray(e) ? getMax(e) : e));
}