$(document).ready(function () {
    $('#errorDialog').modal('show');
});

function hideDialog() {
    $('#errorDialog').modal('hide')
}

function navigateBack() {
    console.log("navigate back!!!")
    window.history.back();
}

function search() {
    var searchfield = document.getElementById("searchbar").value 
    var url = window.location.href+/search/+searchfield
    window.open(url)
}