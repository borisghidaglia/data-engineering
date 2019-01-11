// # Homepage
// Functions
class CardColumnsReviews {
    constructor() {
        // Attribs
        this.cardColumns = document.getElementById('review-cards-container').children[0].children
        this.loadMore = document.getElementById('load-more')

        // Event Listeners
        this.loadMore.addEventListener('click', function(e){this.fetchReviews()}.bind(this))
    }

    fetchReviews() {
        let beginAt = document.querySelectorAll('.card').length + 1

        fetch(window.location + 'api/fetch-raw-reviews/'+beginAt)
        .then(function(response) {
            return response.json()
        }.bind(this))
        .then(function(reviews) {
            for (var i = 0; i < reviews.length; i++) {
                this.insertReview(reviews[i])
            }
        }.bind(this));
    }

    insertReview(review) {
        // Creating the review card
        let cardString = [
            '<div class="card mb-4"><div class="card-body"><h5 class="card-title">',
            review["title"],
            '</h5><p class="card-text">',
            review["content"],
            '</p></div><ul class="list-group list-group-flush"><li class="list-group-item"><b>Attraction : </b>',
            review['attraction_review_name'],
            '</li><li class="list-group-item"><b>Username : </b>',
            review["username"],
            '</li><li class="list-group-item"><b>Grade : </b>',
            review["grade"],
            '</li></ul></div>'
        ].join('')
        let doc = new DOMParser().parseFromString(cardString, 'text/html');
        let card = doc.body.firstChild;

        // Inserting it in the smaller column to keep the document balanced
        let colHeights = []
        for (var i = 0; i < this.cardColumns.length; i++) {
            let eltsHeight = 0
            for (var j = 0; j < this.cardColumns[i].children.length; j++) {
                // Storing 1 over the height because I'll use indexOfMax later
                eltsHeight += this.cardColumns[i].children[j].offsetHeight
            }
            colHeights[i] = 1/eltsHeight
        }

        let idMax = this.indexOfMax(colHeights)
        this.cardColumns[idMax].append(card)
    }

    indexOfMax(arr) {
        if (arr.length === 0) {
            return -1;
        }

        var max = arr[0];
        var maxIndex = 0;

        for (var i = 1; i < arr.length; i++) {
            if (arr[i] > max) {
                maxIndex = i;
                max = arr[i];
            }
        }

        return maxIndex;
    }

}

//
// On page load
//
(function() {

    // Init
    card_column_reviews = new CardColumnsReviews();

})();
