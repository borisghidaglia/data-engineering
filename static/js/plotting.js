fetch('/api/grades').then(r => r.json()).then(data => hist(data))

hist = function(data){
    console.log(data)
    var trace = {
        x: data,
        type: 'histogram',
      };
    Plotly.newPlot('plot-div', [trace]);
}
