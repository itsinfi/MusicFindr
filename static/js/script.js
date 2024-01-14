$(document).ready(function () {
    $('#errorDialog').modal('show');
});

function hideDialog() {
    $('#errorDialog').modal('hide')
}

function navigateBack() {
    var url = window.location.href+/playlist/+id
    var win = window.open(url, '_self');  win.focus();
}

function search() {
    var searchfield = document.getElementById("searchbar").value 
    if (event.keyCode === 13) {
        var url = window.location.href+/search/+searchfield
        var win = window.open(url, '_self');  win.focus();
    }
    
}

function openPlaylistDetail(id) {
    var url = window.location.href + /playlist/ + id
    var win = window.open(url, '_self');  win.focus();
}