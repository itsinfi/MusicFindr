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