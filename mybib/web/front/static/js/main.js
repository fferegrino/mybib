$(document).ready(function () {
    console.log('Loaded')
    $("#form").submit(function(e){
        e.preventDefault();
        serialised_data = $(this).serialize();
        $.get('api/papers/search?' + serialised_data, function (data) {
            console.log(data);
        })
    });
});
