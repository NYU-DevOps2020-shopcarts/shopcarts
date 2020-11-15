$(function () {
    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function shopcart_update_form_data(res) {
        $("#shopcart_id").val(res.id);
        $("#user_id").val(res.user_id);
        $("#items_shopcart_id").val(res.id);
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").text(message);
    }

    function shopcart_add_results_in_table(res){
        $("#shopcart_search_results").empty();

        var firstShopcart;
        for(var i = 0; i < res.length; i++) {
            var shopcart = res[i];
            var row = "<tr><td>"+shopcart.id+"</td><td>"+shopcart.user_id+"</td><td>"+shopcart.create_time+"</td><td>"+shopcart.update_time+"</td><td></td></tr>";
            $("#shopcart_search_results").append(row);
            if (i === 0) {
                firstShopcart = shopcart;
            }
        }
        return firstShopcart;
    }

    // ****************************************
    // Create a Shopcart
    // ****************************************

    $("#create-btn").click(function () {
        var user_id = $("#user_id").val();

        if (user_id === "") {
            return
        }

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
            shopcart_update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            $("#shopcart_search_results").empty()
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Retrieve a shopcart
    // ****************************************

    $("#shopcart_retrieve-btn").click(function () {
        var shopcart_id = $("#shopcart_id").val();

        if (shopcart_id === '') {
            return
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/shopcarts/" + shopcart_id,
            contentType: "application/json"
        })

        ajax.done(function(res){
            shopcart_update_form_data(res)

            shopcart_add_results_in_table([res])

            flash_message("Success")
        });

        ajax.fail(function(res){
            $("#shopcart_search_results").empty()
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Delete a shopcart
    // ****************************************

    $("#shopcart_delete-btn").click(function () {
        var shopcart_id = $("#shopcart_id").val();

        if (shopcart_id === '') {
            return
        }

        var ajax = $.ajax({
            type: "DELETE",
            url: "/shopcarts/" + shopcart_id,
            contentType: "application/json"
        })

        ajax.done(function(res){
            flash_message("Shopcart has been Deleted!")
        });

        ajax.fail(function(res){
            $("#shopcart_search_results").empty()
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Search for a shopcart
    // ****************************************

    $("#shopcart_search-btn").click(function () {
        var user_id = $("#user_id").val();

        if (user_id === "") {
            return
        }

        var queryString = ""

        if (user_id) {
            queryString += 'user_id=' + user_id
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/shopcarts?" + queryString,
            contentType: "application/json"
        })

        ajax.done(function(res){
            firstShopcart = shopcart_add_results_in_table(res)

            // copy the first result to the form
            if (firstShopcart !== "") {
                shopcart_update_form_data(firstShopcart)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            $("#shopcart_search_results").empty()
            flash_message(res.responseJSON.message)
        });
    });

    $("#list-btn").click(function () {
        var ajax = $.ajax({
            type: "GET",
            url: "/shopcarts",
            contentType: "application/json"
        })

        ajax.done(function(res){
            firstShopcart = shopcart_add_results_in_table(res)

            // copy the first result to the form
            if (firstShopcart !== "") {
                shopcart_update_form_data(firstShopcart)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            $("#shopcart_search_results").empty()
            flash_message(res.responseJSON.message)
        });
    });

    $("#clear-btn").click(function () {
        $("#shopcart_search_results").empty()
    })

    // Updates the form with data from the response
    function shopcart_item_update_form_data(res) {
        $("#items_shopcart_id").val(res.sid);
        $("#shopcart_item_id").val(res.id);
        $("#product_id").val(res.sku);
        $("#product_name").val(res.name);
        $("#product_amount").val(res.amount);
        $("#product_price").val(res.price);
    }

    function add_results_in_table_for_items(res){
        $("#shopcart_items_search_results").empty();

        var firstShopcartItem;

        for(var i = 0; i < res.length; i++) {
            var shopcart_item = res[i];
            var row = "<tr><td>"+shopcart_item.id+"</td>"+
                "<td>"+shopcart_item.sid+"</td>"+
                "<td>"+shopcart_item.sku+"</td>"+
                "<td>"+shopcart_item.name+"</td>"+
                "<td>"+shopcart_item.price+"</td>"+
                "<td>"+shopcart_item.amount+"</td>"+
                "<td></td></tr>";
            $("#shopcart_items_search_results").append(row);
            if (i === 0) {
                firstShopcartItem = shopcart_item;
            }
        }

        return firstShopcartItem
    }

    $("#create-btn-items").click(function () {
        var shopcart_id = parseInt($("#items_shopcart_id").val());
        var sku = parseInt($("#product_id").val());
        var name = $("#product_name").val();
        var price = parseFloat($("#product_price").val());
        var amount = parseInt($("#product_amount").val());

        if (shopcart_id === "" || sku === "" || name === "" || price === "" || amount === "") {
            return
        }

        var data = {
            "sid":shopcart_id,
            "sku":sku,
            "name":name,
            "price":price,
            "amount":amount
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/shopcarts/"+shopcart_id+"/items",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            shopcart_item_update_form_data(res)

            flash_message("Success")
        });

        ajax.fail(function(res){
            $("#shopcart_items_search_results").empty()
            flash_message(res.responseJSON.message)
        });
    });

    $("#update-btn-items").click(function () {
        var shopcart_id = parseInt($("#items_shopcart_id").val());
        var shopcart_item_id = parseInt($("#shopcart_item_id").val())
        var sku = parseInt($("#product_id").val());
        var name = $("#product_name").val();
        var price = parseFloat($("#product_price").val());
        var amount = parseInt($("#product_amount").val());

        if (shopcart_id === "" || shopcart_item_id === "" | sku === "" || name === "" || price === "" || amount === "") {
            return
        }

        var data = {
            "sku":sku,
            "name":name,
            "price":price,
            "amount":amount
        };

        var ajax = $.ajax({
            type: "PUT",
            url: "/shopcarts/"+shopcart_id+"/items/"+shopcart_item_id,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            shopcart_item_update_form_data(res)

            flash_message("Success")
        });

        ajax.fail(function(res){
            $("#shopcart_items_search_results").empty()
            flash_message(res.responseJSON.message)
        });
    });

    $("#retrieve-btn-items").click(function () {
        var shopcart_id = $("#items_shopcart_id").val();

        if (shopcart_id === "") {
            return
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/shopcarts/" + shopcart_id + "/items/",
            contentType: "application/json"
        })

        ajax.done(function(res){
            var firstShopcart = add_results_in_table_for_items(res)

            shopcart_item_update_form_data(firstShopcart)

            flash_message("Success")
        });

        ajax.fail(function(res){
            $("#shopcart_items_search_results").empty()
            flash_message(res.responseJSON.message)
        });

    });

    $(".search-btn-items").click(function () {
        var query = $(this).data("query")
        var sku = $("#product_id").val();
        var name = $("#product_name").val();
        var price = $("#product_price").val();
        var amount = $("#product_amount").val();

        var queryString = ""

        if (query === 'sku') {
            queryString += 'sku=' + sku
        }
        else if(query === 'name'){
            queryString += 'name=' + name
        }
        else if(query === 'price'){
            queryString += 'price=' + price
        }
        else if(query === 'amount'){
            queryString += 'amount=' + amount
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/shopcarts/items?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            var firstShopcart = add_results_in_table_for_items(res)

            if (firstShopcart != null) {
                shopcart_item_update_form_data(firstShopcart)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            $("#shopcart_items_search_results").empty()
            flash_message(res.responseJSON.message)
        });
    });

    $("#shopcart_item_delete-btn").click(function () {
        var shopcart_id = $("#items_shopcart_id").val();
        var shopcart_item_id = $("#shopcart_item_id").val()

        if (shopcart_id === '' || shopcart_item_id === '') {
            return
        }

        var ajax = $.ajax({
            type: "DELETE",
            url: "/shopcarts/" + shopcart_id + "/items/" + shopcart_item_id,
            contentType: "application/json"
        })

        ajax.done(function(res){
            flash_message("ShopCart Item has been Deleted!")
        });

        ajax.fail(function(res){
            $("#shopcart_items_search_results").empty()
            flash_message("Server error!")
        });
    });

    $("#clear-btn-items").click(function () {
        $("#shopcart_items_search_results").empty()
    })
})