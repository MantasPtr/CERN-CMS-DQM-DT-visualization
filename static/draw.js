const h = 100;
const maxlight=20;
const minlight=80;

var w = 1400,
    h2 = 500,
    cubeDim = 20,
    x = w / cubeDim,
    y1 = h2 / cubeDim;
    
function drawMatrix(matrix) {
    d3.selectAll("g").remove()
    var svg = d3.select("#image").append("svg")
    .attr("width", w)
    .attr("height", h2);

    cubeDim = Math.floor(Math.min(h2/matrix.length, w/matrix[0].length));
    let rows = svg.selectAll("g")
        .data(matrix)
        .enter().append("g").selectAll("rect")
        .data(d => d)
        .enter().append("rect")
        .attr("transform", translate)
        .attr("width", cubeDim)
        .attr("height", cubeDim)
        // .on("mouseover", ()  => {
        //     console.log(d3.select(this))
        //     d3.select(this).attr("fill", "red");
        // })
        // .on("mouseout", (d, i) => {
        //     console.log(d3.select(this))
        //     d3.select(this).attr("fill","blue")
        // })
        .style("background-color", getColor);
}
var y = -1;
function translate(a, index, c) {
   if (index === 0) {
       y++;
   }
   return "translate(" + index * cubeDim + "," + y * cubeDim + ")";
}