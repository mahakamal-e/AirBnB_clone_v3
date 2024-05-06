$(document).ready(() => {
  function loadPlaces() {
    $.ajax({
      type: "POST",
      url: "http://0.0.0.0:5001/api/v1/places_search",
      contentType: "application/json",
      data: JSON.stringify({}),
      success: function(data) {
        renderPlaces(data);
      }
    });
  }
  function renderPlaces(places) {
    $(".places").empty();
    places.forEach(function(place) {
      var article = $("<article>");
      article.append("<div><h2>" + place.name + "</h2><div class='price-by-night'>$" + place.price_by_night + "</div></div>");
      article.append("<div class='information'><div class='max-guest'><i class='fa-solid fa-users'></i><br>" + place.max_guest + "</div><div class='number-rooms'><i class='fa-solid fa-bed'></i><br>" + place.number_rooms + "</div><div class='number-bathrooms'><i class='fa-solid fa-bath'></i><br>" + place.number_bathrooms + "</div></div>");
      article.append("<div class='description'>" + place.description + "</div>");
      $(".places").append(article);
    });
  }

  loadPlaces();
});
