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

function toggleTagsForm(){

    var currentDisplay = String(document.getElementById("add-tags").style.display);

    if (currentDisplay === "") {

        document.getElementById("add-tags").style.display = "block";
        document.getElementById("add-tags").style.display = "flex";
        
        document.getElementById("toggleButton").textContent = "-";

    } else{
        document.getElementById("add-tags").style.display = "";
        
        document.getElementById("toggleButton").textContent = "+";
    }
}


function addTagsToPlaylist(pid) {

    var searchfield = document.getElementById("newTags").value.trim()
    if (event.keyCode === 13 && searchfield !== "") { 

        var tagStrings = document.getElementById('newTags').value

        request = new XMLHttpRequest()
        request.open("POST", "/addTagsToPlaylist", true)
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8")

        request.onload = function () {
            location.reload()
        }

        var data = JSON.stringify({ pid: pid, tagStrings: tagStrings })
        request.send(data)
    }

    
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

function deletePlaylist(pid) {
    var request = new XMLHttpRequest()
    request.open("POST", "/deletePlaylist", true)
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8")

    request.onload = function () {
        location.reload();
    };

    var data = JSON.stringify({ pid: pid })
    request.send(data)
}

function updatePlaylist(pid, title, description, tagStrings) {
    var request = new XMLHttpRequest()
    request.open("POST", "/updatePlaylist", true)
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8")

    request.onload = function () {
        location.reload();
    };

    var data = JSON.stringify({ pid: pid, title: title, description: description, tagStrings: tagStrings })
    request.send(data)
}