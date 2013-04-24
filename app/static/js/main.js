
function querySearch(query) {
  $.ajax({
    //dataType: "json",
    url: "/search",
    data: {
      "query": query,
      "result_only": 1
    }
  }).done(function(result) {
    $("#workshop-results").empty();
    console.log(result);
    $("#workshop-results").append(result);
  });
};
$(function() {
  $("#testButton").click(function() {
    querySearch('FUN QUERY');
    console.log('test')
  });

  $("searchSubmitButton").click(function() {
    window.location.href("/search?query=");
  });
});
