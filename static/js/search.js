class Search {
    constructor() {
        // Attribs
        this.input = document.getElementById('search-input')
        this.queryContainerResult = document.getElementById("container-query-result");

        // Event Listeners
        this.input.addEventListener('input', this.makeQuery.bind(this))
    }

    makeQuery(e){

        if(this.input.value == ""){
            this.queryContainerResult.innerHTML = ""
            return 0
        }

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

    createUserCard(data){
        // Creating the review card
        let cardString = [
            '<div class="card"><div class="card-body"><h5 class="card-title">',
            data["username"],
            '</h5></div><ul class="list-group list-group-flush"><li class="list-group-item"><b>Contributions : </b>',
            data['nb_contributions'],
            '</li><li class="list-group-item"><b>Villes visitées : </b>',
            data["nb_cities_visited"],
            '</li><li class="list-group-item"><b>Trouvé depuis : </b>',
            data["attraction_review_name"],
            '</li></ul></div>'
        ].join('')
        let doc = new DOMParser().parseFromString(cardString, 'text/html');
        let card = doc.body.firstChild;
        return card
    }

}

//
// On page load
//
(function() {

    // Init
    search = new Search();

})();
