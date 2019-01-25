// fetch('/api/grades').then(r => r.json()).then(data => hist(data))

class PlotSearch {

    constructor() {
        // Attribs
        this.input = document.getElementById('search-input')
        this.queryContainerResult = document.getElementById("conainer-query-result");
        this.formControlSelect = document.getElementById("formControlSelect");
        this.formChoices = {
            0 : "Reviews, by title, content, attraction name and username"
            // 0 : "Users, by username",
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

        if ( this.formControlSelect.value == this.formChoices[1] ){
            this.queryUsers()
            return 0
        } else if ( this.formControlSelect.value == this.formChoices[0] ) {
            this.queryReviews()
            return 0
        }

    }

    queryUsers(){

        fetch("http://"+window.location.host + '/api/fetch-users-autocomplete/'+this.input.value)
        .then(function(response) {
            return response.json()
        }.bind(this))
        .then(function(data) {
            // removing previous result
            this.queryContainerResult.innerHTML = ""

            // adding the new ones
            if (data.hits.hits.length > 0) {
                for (var i = 0; i < data.hits.hits.length; i++) {
                    let newCard = this.createUserCard(data.hits.hits[i]["_source"])
                    this.queryContainerResult.appendChild(newCard)
                }
            }
        }.bind(this));

    }

    queryReviews(){

        fetch('/api/grades/'+this.input.value).then(response => response.json()).then(data => this.hist(data))
        // .then(function(response) {
        //     return response.json()
        // }.bind(this))
        // .then(function(data) {
        //     // removing previous result
        //     this.queryContainerResult.innerHTML = ""
        //
        //     // adding the new ones
        //     if (data.hits.hits.length > 0) {
        //         for (var i = 0; i < data.hits.hits.length; i++) {
        //             let newCard = this.createReviewCard(data.hits.hits[i]["_source"])
        //             this.queryContainerResult.appendChild(newCard)
        //         }
        //     }
        // }.bind(this));

    }

    hist(data){
        var trace = {
            x: data,
            type: 'histogram',
        };
        var layout = {
            title: 'Grade distribution of reviews',
            xaxis: {range: [10, 60]}
        };
        Plotly.newPlot('plot-div', [trace], layout);
    }
}

//
// On page load
//
(function() {

    // Init
    search = new PlotSearch();

})();
