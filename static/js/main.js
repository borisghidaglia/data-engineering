function fetchReviews() {

    let beginAt = document.querySelectorAll('.card').length + 1

    fetch(window.location + 'api/fetch-raw-reviews/'+beginAt)
    .then(function(response) {
        return response.json()
    })
    .then(function(reviews) {
        for (var i = 0; i < reviews.length; i++) {
            insertReview(reviews[i])
        }
    });
}

function insertReview(review) {
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
    let cardColumns = document.getElementById('review-cards-container').children[0].children
    let colHeights = []
    for (var i = 0; i < cardColumns.length; i++) {
        let eltsHeight = 0
        for (var j = 0; j < cardColumns[i].children.length; j++) {
            // Storing 1 over the height because I'll use indexOfMax later
            eltsHeight += cardColumns[i].children[j].offsetHeight
        }
        colHeights[i] = 1/eltsHeight
    }

    console.log(colHeights);
    let idMax = indexOfMax(colHeights)
    cardColumns[idMax].append(card)
}

function indexOfMax(arr) {
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
