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
            var row = `<tr><td>${shopcart.id}</td><td>${shopcart.user_id}</td><td>`
                + `<button class="btn btn-primary btn-sm shopcart_retrieve-btn" data-shopcart-id="${shopcart.id}">Retrieve</button> `
                + `<button class="btn btn-info btn-sm shopcart_list-btn" data-shopcart-id="${shopcart.id}">List</button> `
                + `<button class="btn btn-primary btn-sm shopcart_order-btn" data-shopcart-id="${shopcart.id}">Place Order</button> `
                + `<button class="btn btn-danger btn-sm shopcart_delete-btn" data-shopcart-id="${shopcart.id}">Delete</button>`
                + `</td></tr>`;
            $("#shopcart_search_results").append(row);
            if (i === 0) {
                firstShopcart = shopcart;
            }
        }

        shopcart_list_bind_events()

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
            flash_message("Shopcart has been created!")
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
            url: "/api/shopcarts/" + shopcart_id,
            contentType: "application/json"
        })

        ajax.done(function(res){
            shopcart_update_form_data(res)

            shopcart_add_results_in_table([res])

            flash_message("Shopcart has been retrieved!")
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
            url: "/api/shopcarts/" + shopcart_id,
            contentType: "application/json"
        })

        ajax.done(function(res){
            $("#shopcart_clear-btn").click()
            $("#item_clear-btn").click()
            flash_message("Shopcart has been deleted!")
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

            flash_message("Please see the search result below!")
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

            flash_message("Please see the list result below!")
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
            url: "/api/shopcarts/" + shopcart_id + "/items",
            success: function(shopcart_data){
                if (shopcart_data.length === 0) {
                    alert(`Shopcart [${shopcart_id}] is empty!`)
                    return
                }

                // Place order
                $.ajax({
                    type: "PUT",
                    url: "/api/shopcarts/"+shopcart_id+"/place-order",
                    success: function(res)
                    {
                        $("#shopcart_search_results").empty()
                        $("#item_search_results").empty()
                        flash_message("Order was successfully placed!")
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
        flash_message("")
    })

    function shopcart_list_bind_events() {
        // Those events have to be bound after the buttons pop up

        $(".shopcart_retrieve-btn").click(function () {
            $("#shopcart_id").val($(this).data("shopcart-id"))
            $("#shopcart_retrieve-btn").click()
        })

        $(".shopcart_list-btn").click(function () {
            $("#item_shopcart_id").val($(this).data("shopcart-id"))
            $("#item_list-btn").click()
        })

        $(".shopcart_order-btn").click(function () {
            $("#shopcart_id").val($(this).data("shopcart-id"))
            $("#shopcart_order-btn").click()
        })

        $(".shopcart_delete-btn").click(function () {
            $("#shopcart_id").val($(this).data("shopcart-id"))
            $("#shopcart_delete-btn").click()
        })
    }

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
                "<td>"+`<button class="btn btn-primary btn-sm item_retrieve-btn" data-item-id="${shopcart_item.id}">Retrieve</button> `
                +`<button class="btn btn-danger btn-sm item_delete-btn" data-item-id="${shopcart_item.id}">Delete</button>` + "</td></tr>";
            $("#item_search_results").append(row);
            if (i === 0) {
                firstShopcartItem = shopcart_item;
            }
        }

        item_list_bind_events()

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
            url: "/api/shopcarts/"+shopcart_id+"/items",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            shopcart_item_update_form_data(res)

            flash_message("Item has been created!")
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
            url: "/api/shopcarts/" + shopcart_id + "/items/" + shopcart_item_id,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            shopcart_item_update_form_data(res)

            flash_message("Item has been updated!")
        });

        ajax.fail(function(res){
            $("#item_search_results").empty()
            flash_message(res.responseJSON.message)
        });
    });

    $("#item_list-btn").click(function () {
        var shopcart_id = $("#item_shopcart_id").val();

        if (shopcart_id === "") {
            return
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/api/shopcarts/" + shopcart_id + "/items/"
        })

        ajax.done(function(res){
            if (res.length == 0){
                $("#item_search_results").empty()
                flash_message("Shopcart with ID ["+ shopcart_id + "] is empty")
            }
            else{
                var firstShopcart = add_results_in_table_for_items(res)

                shopcart_item_update_form_data(firstShopcart)

                flash_message("Please see the item list results below!")
            }
        });

        ajax.fail(function(res){
            $("#item_search_results").empty()
            flash_message(res.responseJSON.message)
        });

    });

    $("#item_retrieve-btn").click(function () {
        var shopcart_id = $("#item_shopcart_id").val();
        var item_id = $("#item_id").val();

        if (item_id === '' || shopcart_id === "") {
            return
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/api/shopcarts/" + shopcart_id + "/items/" + item_id,
            contentType: "application/json"
        })

        ajax.done(function (res) {
            shopcart_item_update_form_data(res);

            add_results_in_table_for_items([res]);

            flash_message("Item has been retrieved!")
        });

        ajax.fail(function (res) {
            $("#shopcart_search_results").empty()
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

            flash_message("Please see the item search results below!")
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
            url: "/api/shopcarts/" + shopcart_id + "/items/" + shopcart_item_id,
            contentType: "application/json"
        })

        ajax.done(function(res){
            $("#item_clear-btn").click()
            flash_message("ShopCart Item has been deleted!")
        });

        ajax.fail(function(res){
            $("#item_search_results").empty()
            flash_message("Server error!")
        });
    });

    $("#item_clear-btn").click(function () {
        $("#item_search_results").empty()
        flash_message("")
    })

    function item_list_bind_events() {
        $(".item_retrieve-btn").click(function () {
            $("#item_id").val($(this).data("item-id"))
            $("#item_retrieve-btn").click()
        })

        $(".item_delete-btn").click(function () {
            $("#item_id").val($(this).data("item-id"))
            $("#item_delete-btn").click()
        })
    }
})
