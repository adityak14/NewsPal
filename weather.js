$(document).ready(function(){
    $('#weather').click(function(){

        var city = $("#city").val();

        if (city != '') {
            $.ajax({
                url: "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=metric"+"&appid=4ba4f0d6c853cb8b4bacbf2c8d3d1bc0",
                type: "GET",
                dataType: "jsonp",
                success: function(data){
                    console.log(data);
                }
            });
        } else {
            $("#error").html('')
        }
    });
});