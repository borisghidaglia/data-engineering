class Search {
    constructor() {
        // Attribs
        this.input = document.getElementById('search-input')

        // Event Listeners
        this.input.addEventListener('input', this.makeQuery)
    }

    makeQuery(e){
        console.log(this.value);
    }
}

//
// On page load
//
(function() {

    // Init
    search = new Search();

})();
