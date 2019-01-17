class Search {

    constructor() {
        // Attribs
        this.input = document.getElementById('search-input')
        this.queryContainerResult = document.getElementById("container-query-result");
        this.formControlSelect = document.getElementById("formControlSelect");
        this.formChoices = {
            0 : "Users, by username",
            1 : "Reviews, by title, content, attraction name and username"
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
            this.queryUsers()
            return 0
        } else if ( this.formControlSelect.value == this.formChoices[1] ) {
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

        fetch("http://"+window.location.host + '/api/fetch-review-autocomplete/'+this.input.value)
        .then(function(response) {
            return response.json()
        }.bind(this))
        .then(function(data) {
            // removing previous result
            this.queryContainerResult.innerHTML = ""

            // adding the new ones
            if (data.hits.hits.length > 0) {
                for (var i = 0; i < data.hits.hits.length; i++) {
                    let newCard = this.createReviewCard(data.hits.hits[i]["_source"])
                    this.queryContainerResult.appendChild(newCard)
                }
            }
        }.bind(this));

    }

    createUserCard(data){
        // Creating the user card
        let cardString = [
            '<div class="col-sm-6 col-md-4 p-2"><div class="card"><div class="card-body"><h5 class="card-title">',
            data["username"],
            '</h5></div><ul class="list-group list-group-flush"><li class="list-group-item"><b>Contributions : </b>',
            data['nb_contributions'],
            '</li><li class="list-group-item"><b>Villes visitées : </b>',
            data["nb_cities_visited"],
            '</li><li class="list-group-item"><b>Trouvé depuis : </b>',
            data["attraction_review_name"],
            '</li></ul></div></div>'
        ].join('')
        let doc = new DOMParser().parseFromString(cardString, 'text/html');
        let card = doc.body.firstChild;
        return card
    }

    createReviewCard(data){
        // Creating the review card
        let cardString = [
            '<div class="col-sm-6 col-md-4 p-2"><div class="card"><div class="card-body"><h5 class="card-title">',
            data["title"],
            '</h5><p class="card-text">',
            data["content"],
            '</p></div><ul class="list-group list-group-flush"><li class="list-group-item"><b>Attraction : </b>',
            data['attraction_review_name'],
            '</li><li class="list-group-item"><b>Username : </b>',
            data["username"],
            '</li><li class="list-group-item"><b>Grade : </b>',
            data["grade"],
            '</li></ul></div></div>'
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
