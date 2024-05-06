$(document).ready(() => {
  function checkApiStatus() {
    $.ajax({
      url: "http://0.0.0.0:5001/api/v1/status/",
      type: "GET",
      dataType: "json",
      success: function(data) {
        if (data.status === "OK") {
          $("#api_status").addClass("available");
        } else {
          $("#api_status").removeClass("available");
        }
      },
      error: function(xhr, status, error) {
        console.error("Error checking API status:", error);
      }
    });
  }

  checkApiStatus();

  setInterval(checkApiStatus, 5000);
});
