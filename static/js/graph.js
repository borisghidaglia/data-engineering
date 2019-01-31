class Graph {

    constructor() {
        // Attribs
        this.input = document.getElementById('search-input')
        this.queryContainerResult = document.getElementById("conainer-query-result");
        this.formControlSelect = document.getElementById("formControlSelect");
        this.formChoices = {
            0 : "Reviews, by title, content, attraction name and username",
            1 : "Specific User"
        }

        // Event Listeners
        this.input.addEventListener('input', this.choseQuery.bind(this))

        // Init form
        this.addChoices()
    }

    addChoices(){
        for (var i = 0; i < Object.keys(this.formChoices).length; i++) {
            let option = document.createElement("option");
            option.innerText = this.formChoices[i]
            this.formControlSelect.appendChild(option)
        }
    }

    choseQuery(e){

        if(this.input.value == ""){
            this.queryContainerResult.innerHTML = ""
            return 0
        }

        if ( this.formControlSelect.value == this.formChoices[0] ){
            this.queryReviews()
            return 0
        } else if ( this.formControlSelect.value == this.formChoices[1] ) {
            this.queryUser()
            return 0
        }

    }

    queryUser(){

        fetch('/api/user-grades/'+this.input.value).then(response => response.json()).then(data => {
            console.log(data)
            var colors = ["#bc2026", "#ef4723", "#f68e1f", "#7dbb42", "#0f9246"]
            var bar_plot = {
                type: 'bar',
                name: 'Bar Plot',
                showlegend: false,
                x: Object.keys(data),
                y: Object.values(data),
                marker: {color: colors}
            }
            var average = {
                mode: 'lines',
                name: 'Average: '+this.average(data),
                x: [this.average(data),this.average(data)],
                y: [0,30],
                line: {
                    dash: 'dot'
                }
            }
            var layout = {
                title: 'Grade distribution of reviews for user '+ this.input.value,
                xaxis: {range: [0, 60]},
                yaxis: {range: [0, 10]}
            };
            Plotly.newPlot('plot-div', [bar_plot, average], layout);
        })
    }

    queryReviews(){

        fetch('/api/grades/'+this.input.value).then(response => response.json()).then(data => {
            console.log(data)
            console.log(this.average(data))
            var colors = ["#bc2026", "#ef4723", "#f68e1f", "#7dbb42", "#0f9246"]
            var bar_plot = {
                type: 'bar',
                name: 'Bar Plot',
                showlegend: false,
                x: Object.keys(data),
                y: Object.values(data),
                marker: {color: colors}
            };
            var average = {
                mode: 'lines',
                name: 'Average: '+this.average(data),
                x: [this.average(data),this.average(data)],
                y: [0,30],
                line: {
                    dash: 'dot'
                }
            }
            var layout = {
                title: 'Grade distribution of reviews',
                xaxis: {range: [0, 60]},
                yaxis: {range: [0, 30]}
            };
            Plotly.newPlot('plot-div', [bar_plot, average], layout);
        })
    }

    average(dict){
        var sum = 0
        var nb_instances = 0
        for (var key in dict){
            sum += key*dict[key]
            nb_instances += dict[key]
        }
        return sum/nb_instances
    }
}

//
// On page load
//
(function() {

    // Init
    search = new Graph();

})();
