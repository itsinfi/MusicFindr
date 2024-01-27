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

// function playlist_order() {
//     var order = document.getelementbyid("playlist_order").value.trim()
//     var currenturl = window.location.href + order;
//     var win = window.open(currenturl, '_self');  win.focus();
// }

function vote(tid, pid, voteValue) {
    var request = new XMLHttpRequest()
    request.open("POST", "/vote", true)
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8")

    request.onload = function () {
        location.reload();
    };

    var data = JSON.stringify({ tid: tid, pid: pid, voteValue: voteValue })
    request.send(data)
}