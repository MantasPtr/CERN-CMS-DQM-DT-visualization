var w = 960,
    h = 500,
    z = 20,
    x = w / z,
    y = h / z;

var svg = d3.select("#image").append("svg")
    .attr("width", w)
    .attr("height", h);

svg.selectAll("rect")
    .data(d3.range(x * y))
    .enter().append("rect")
    .attr("transform", translate)
    .attr("width", z)
    .attr("height", z)
    .style("fill", (d) => d3.hsl(d % x / x * 360, 1, Math.floor(d / x) / y))

function translate(d) {
   return "translate(" + (d % x) * z + "," + Math.floor(d / x) * z + ")";
}