$(document).ready(function () {
    console.log("document ready");
    $.ajax({
        url: '/getOrders',
        type: 'GET',
        dataType: "json",
        success: function (response) {
                console.log(response);
            $.each(response, function (index) {
                var orderDate = new Date(response[index][3]).toLocaleDateString();
                var deliveryDate = new Date(response[index][4]).toLocaleDateString();
                var orderDetails = '<p>Product Name: <a href="#"> ' + response[index][1] +'</a></p> <p> Order Id: ' +response[index][0] + '</p><p> Ordered Date: '+orderDate+'</p><p>Delivery Date: '+deliveryDate+'</p>';
                var address = '<p>Name: '+ response[index][7]+ '</p><p>Street: '+response[index][8]+'</p><p>City: '+response[index][9]+'</p><p>State: '+response[index][10]+'</p><p>Zipcode: '+response[index][11]+'</p><p>Phone: '+response[index][12]+'</p>';
                console.log(index);
                if(response[index][6]>0){
                    var listRow = '<tr id="'+response[index][0]+'"><td class="product-thumbnail"><img src="/static/images/product/' + response[index][2] + '" alt="product img" /></td><td class="product-name">'+orderDetails+'</td><td class="product-name">' + address + '</td><td class="product-quantity">'+response[index][6]+'</td><td class="product-subtotal">$' + response[index][5] + '</td></tr>';
                    // subTotal = subTotal + (response[index][4] *response[index][6])
                    $('#tableBody').append(listRow);
                }
                    
            });
            // var subTotalRow = '<th>Subtotal</th><td><span class="amount">$'+subTotal+'</span></td>';
            // var totalRow = '<th>Total</th><td><strong><span class="amount">$'+subTotal+'</span></strong></td>'
            // $('.cart-subtotal').append(subTotalRow);
            // $('.order-total').append(totalRow);

            
        },
        error: function (error) {
            console.log(error);
        }
    });
});