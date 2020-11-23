$(function () {
    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function shopcart_update_form_data(res) {
        $("#shopcart_id").val(res.id);
        $("#shopcart_user").val(res.user_id);
        $("#item_shopcart_id").val(res.id);
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").text(message);
    }

    function shopcart_add_results_in_table(res){
        $("#shopcart_search_results").empty();

        var firstShopcart = null;
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

    $("#shopcart_create-btn").click(function () {
        var user_id = $("#shopcart_user").val();

        if (user_id === "") {
            return
        }

        var data = {
            "user_id": user_id
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/api/shopcarts",
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
        var user_id = $("#shopcart_user").val();

        if (user_id === "") {
            return
        }

        var queryString = ""

        if (user_id) {
            queryString += 'user_id=' + user_id
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/api/shopcarts?" + queryString
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

    $("#shopcart_list-btn").click(function () {
        var ajax = $.ajax({
            type: "GET",
            url: "/api/shopcarts"
        })

        ajax.done(function(res){
            firstShopcart = shopcart_add_results_in_table(res)

            // copy the first result to the form
            if (firstShopcart !== null) {
                console.log(firstShopcart)
                shopcart_update_form_data(firstShopcart)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            $("#shopcart_search_results").empty()
            flash_message(res.responseJSON.message)
        });
    });

    $("#shopcart_order-btn").click(function () {
        var shopcart_id = $("#shopcart_id").val();

        if (shopcart_id === "") {
            return
        }
        //Get the items for this shopcart
        $.ajax({
            type: "GET",
            url: "/shopcarts/" + shopcart_id + "/items",
            contentType: "application/json",
            success: function(shopcart_data){
                // Place order
                $.ajax({
                    type: "PUT",
                    url: "/shopcarts/"+shopcart_id+"/place-order",
                    contentType: "application/json",
                    data: shopcart_data,
                    success: function(res)
                    {
                        $("#shopcart_search_results").empty()
                        $("#item_search_results").empty()
                        flash_message("Order was successfully placed")
                    },
                    fail: function(res){
                        flash_message(res.responseJSON.message)
                    }
                });
            },
            fail: function(res){
                flash_message(res.responseJSON.message)
            }
        });
    });

    $("#shopcart_clear-btn").click(function () {
        $("#shopcart_search_results").empty()
    })

    // Updates the form with data from the response
    function shopcart_item_update_form_data(res) {
        $("#item_shopcart_id").val(res.sid);
        $("#item_id").val(res.id);
        $("#item_product_id").val(res.sku);
        $("#item_name").val(res.name);
        $("#item_amount").val(res.amount);
        $("#item_price").val(res.price);
    }

    function add_results_in_table_for_items(res){
        $("#item_search_results").empty();

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
            $("#item_search_results").append(row);
            if (i === 0) {
                firstShopcartItem = shopcart_item;
            }
        }

        return firstShopcartItem
    }

    $("#item_create-btn").click(function () {
        var shopcart_id = parseInt($("#item_shopcart_id").val());
        var sku = parseInt($("#item_product_id").val());
        var name = $("#item_name").val();
        var price = parseFloat($("#item_price").val());
        var amount = parseInt($("#item_amount").val());

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
            $("#item_search_results").empty()
            flash_message(res.responseJSON.message)
        });
    });

    $("#item_update-btn").click(function () {
        var shopcart_id = parseInt($("#item_shopcart_id").val());
        var shopcart_item_id = parseInt($("#item_id").val())
        var sku = parseInt($("#item_product_id").val());
        var name = $("#item_name").val();
        var price = parseFloat($("#item_price").val());
        var amount = parseInt($("#item_amount").val());

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
            $("#item_search_results").empty()
            flash_message(res.responseJSON.message)
        });
    });

    $("#item_retrieve-btn").click(function () {
        var shopcart_id = $("#item_shopcart_id").val();

        if (shopcart_id === "") {
            return
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/shopcarts/" + shopcart_id + "/items/",
            contentType: "application/json"
        })

        ajax.done(function(res){
            if (res.length == 0){
                $("#item_search_results").empty()
                flash_message("Shopcart with ID ["+ shopcart_id + "] is empty")
            }
            else{
                var firstShopcart = add_results_in_table_for_items(res)

                shopcart_item_update_form_data(firstShopcart)

                flash_message("Success")
            }
        });

        ajax.fail(function(res){
            $("#item_search_results").empty()
            flash_message(res.responseJSON.message)
        });

    });

    $(".search-btn-items").click(function () {
        var query = $(this).data("query")
        var sku = $("#item_product_id").val();
        var name = $("#item_name").val();
        var price = $("#item_price").val();
        var amount = $("#item_amount").val();

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
            url: "/api/shopcarts/items?" + queryString
        })

        ajax.done(function(res){
            var firstShopcart = add_results_in_table_for_items(res)

            if (firstShopcart != null) {
                shopcart_item_update_form_data(firstShopcart)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            $("#item_search_results").empty()
            flash_message(res.responseJSON.message)
        });
    });

    $("#item_delete-btn").click(function () {
        var shopcart_id = $("#item_shopcart_id").val();
        var shopcart_item_id = $("#item_id").val()

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
            $("#item_search_results").empty()
            flash_message("Server error!")
        });
    });

    $("#item_clear-btn").click(function () {
        $("#item_search_results").empty()
    })
})
