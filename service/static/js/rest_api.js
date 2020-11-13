$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#shopcart_id").val(res._id);
        $("#user_id").val(res.user_id);
        //$("#pet_category").val(res.category);
        // if (res.available == true) {
        //     $("#pet_available").val("true");
        // } else {
        //     $("#pet_available").val("false");
        // }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#user_id").val("");
        $("#shopcart_id").val("");
        $("#search_results").empty();
        // $("#pet_category").val("");
        // $("#pet_available").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    function add_results_in_table(res){

        $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">User Id</th>'
            header += '<th style="width:40%">Created On</th>'
            header += '<th style="width:10%">Last Updated On</th></tr>'
            $("#search_results").append(header);
            var firstShopcart = "";
            for(var i = 0; i < res.length; i++) {
                var shopcart = res[i];
                var row = "<tr><td>"+shopcart.id+"</td><td>"+shopcart.user_id+"</td><td>"+shopcart.create_time+"</td><td>"+shopcart.update_time+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstShopcart = shopcart;
                }
            }

            $("#search_results").append('</table>');
            return firstShopcart;
    }

    // ****************************************
    // Create a Shopcart
    // ****************************************

    $("#create-btn").click(function () {

        var user_id = $("#user_id").val();
        // var category = $("#pet_category").val();
        // var available = $("#pet_available").val() == "true";

        var data = {
            "user_id": user_id
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/shopcarts",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="5">');
            var header = '<tr>'
            header += '<th style="width:3%">ID</th>'
            header += '<th style="width:3%">User Id</th>'
            header += '<th style="width:3%">Created On</th>'
            header += '<th style="width:3%">Last Updated On</th></tr>'
            $("#search_results").append(header);
            var firstShopcart = "";
            shopcart = res
            var row = "<tr><td>"+shopcart.id+"</td><td>"+shopcart.user_id+"</td><td>"+shopcart.create_time+"</td><td>"+shopcart.update_time+"</td></tr>";
            $("#search_results").append(row);
                

            $("#search_results").append('</table>');
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a shopcart
    // ****************************************

    $("#update-btn").click(function () {

        var pet_id = $("#pet_id").val();
        var name = $("#pet_name").val();
        var category = $("#pet_category").val();
        var available = $("#pet_available").val() == "true";

        var data = {
            "name": name,
            "category": category,
            "available": available
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/pets/" + pet_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a shopcart
    // ****************************************

    $("#retrieve-btn").click(function () {
        console.log("Hello")
        var shopcart_id = $("#shopcart_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/shopcarts/" + shopcart_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="5">');
            var header = '<tr>'
            header += '<th style="width:3%">ID</th>'
            header += '<th style="width:3%">User Id</th>'
            header += '<th style="width:3%">Created On</th>'
            header += '<th style="width:3%">Last Updated On</th></tr>'
            $("#search_results").append(header);
            var firstShopcart = "";
            shopcart = res
            var row = "<tr><td>"+shopcart.id+"</td><td>"+shopcart.user_id+"</td><td>"+shopcart.create_time+"</td><td>"+shopcart.update_time+"</td></tr>";
            $("#search_results").append(row);
                

            $("#search_results").append('</table>');



            // copy the first result to the form
           

            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a shopcart
    // ****************************************

    $("#delete-btn").click(function () {

        var shopcart_id = $("#shopcart_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/shopcarts/" + shopcart_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Shopcart has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#shopcart_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a shopcart
    // ****************************************

    $("#search-btn").click(function () {

        var user_id = $("#user_id").val();
       
        var queryString = ""

        if (user_id) {
            queryString += 'user_id=' + user_id
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/shopcarts?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            
            firstShopcart = add_results_in_table(res)

            // copy the first result to the form
            if (firstShopcart != "") {
                update_form_data(firstShopcart)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})