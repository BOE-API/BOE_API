function getYearsByMateria() {
    id = $('#year').data('id')
    url = 'http://127.0.0.1:8000/api/years/materia/' + parseInt(id);
    $.getJSON(url, function (data) {
        $.each(data, function (key, value) {

            $('#year').append($('<option>', { value: value })
                .text(value));

        })
    });
    return url;
}
function getAllYears() {
    url = 'http://127.0.0.1:8000/api/years'
    $.getJSON(url, function (data) {
        $.each(data, function (key, value) {

            $('#year').append($('<option>', { value: value })
                .text(value));

        });

    });
}
function procesarAnyos() {
    if ($('#year').doesExist()) {
        var store = []
        var url;
        var data = $('#year').data('page');
        console.log(data);
        if (data == "materias") {
            getYearsByMateria();
        }

        else {
            getAllYears();
        }

    }
}
$(document).on('ready', function(){
    procesarAnyos();


});
jQuery.fn.doesExist = function(){
        return jQuery(this).length > 0;
 };
function getJSONPaginate(url, store){
    $.getJSON(url, function(data){
        var next = data['next']
        $.each(data['results'],function(key, value){
            store.push(value);
        });
        if (next != null){
            getJSONPaginate(next, store);
        }

    });
}