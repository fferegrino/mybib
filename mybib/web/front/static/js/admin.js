$(document).ready(function() {

    var currentVisibleNodes = {};
    var entryTextArea = $('#entry');
    var userText = $('#user');
    var passwordText = $('#password');
    var referenceButton = $('#reference');
    var referenceMessageText = $("#referenceMessage");
    var paper1Text = $('#paper1');
    var paper2Text = $('#paper2');
    var addEntryButton = $('#addEntry');

    function setAuth(xhr) {
        xhr.setRequestHeader("Authorization", "Basic " + btoa(userText.val() + ":" + passwordText.val()));
    }


    referenceButton.click(function(e) {
        var referee = paper1Text.val();
        var referenced = paper2Text.val();
        var message = referenceMessageText.val();
        var url = "/api/references/" + referee + "/" + referenced;
        $.ajax({
            url: url,
            type: "POST",
            beforeSend: setAuth,
            data: JSON.stringify({message:message}),
            contentType: "application/json",
            success: function(result) {
                alert("Success!");
            },
            error: function(result) {
                if(result.status == 409) {
                    alert("Relationship already exists!");
                } else {
                    alert(result.status + " " + result.statusText);
                }
            }
        });
    });

    addEntryButton.click(function(e) {
        var entry = entryTextArea.val();

        $.ajax({
            url: "/api/papers",
            type: "POST",
            beforeSend: setAuth,
            data: entry,
            contentType: "text/plain",
            success: function(data) {
                alert("Inserted!");
            }
        })

    });

}); 