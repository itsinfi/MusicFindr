$(document).ready(function () {
    $('#errorDialog').modal('show');
});

function hideDialog() {
    $('#errorDialog').modal('hide')
}

function navigateBack() {
    window.history.back();
}

function search() {
    var searchfield = document.getElementById("searchbar").value.trim()
    if (event.keyCode === 13 && searchfield !== "") {
        var url = window.location.href+/search/+searchfield
        var win = window.open(url, '_self');  win.focus();
    }
    
}

function openPlaylistDetail(id) {
    var url = window.location.href + /playlist/ + id
    var win = window.open(url, '_self');  win.focus();
}