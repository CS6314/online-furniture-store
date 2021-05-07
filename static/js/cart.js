var cartProducts;
var subTotal = 0;
$(document).ready(function () {
    console.log("document ready");
    $.ajax({
        url: '/getCart',
        type: 'GET',
        dataType: "json",
        success: function (response) {
            cartProducts = response;
            $.each(response, function (index) {
                if(response[index][6]>0){
                    var listRow = '<tr id="'+response[index][0]+'"><td class="product-thumbnail"><img src="/static/images/product/' + response[index][3] + '" alt="product img" /></td><td class="product-name"><a href="#">' + response[index][1] + '</td><td class="product-price"><span class="amount">$' + response[index][6] + '</span></td><td class="product-quantity"><input type="number" value="'+response[index][4]+'" onchange ="updateProductCount(this)" /></td><td class="product-subtotal">$' + response[index][4] *response[index][6]+ '</td><td class="product-remove"><a href="#" onclick="deleteItem(this);">X</a></td></tr>';
                    subTotal = subTotal + (response[index][4] *response[index][6])
                    $('#tableBody').append(listRow);
                }
                    
            });
            var subTotalRow = '<th>Subtotal</th><td><span class="amount">$'+subTotal+'</span></td>';
            var totalRow = '<th>Total</th><td><strong><span class="amount">$'+subTotal+'</span></strong></td>'
            $('.cart-subtotal').append(subTotalRow);
            $('.order-total').append(totalRow);

            
        },
        error: function (error) {
            console.log(error);
        }
    });
    $('input[type=radio][name=delivery]').change(function() {
        if (this.value == '1') {
            $('.order-total').empty(); 
            var total = subTotal + 5;
            var totalRow = '<th>Total</th><td><strong><span class="amount">$'+total+'</span></strong></td>'
            $('.order-total').append(totalRow);
        }
        else{
            $('.order-total').empty(); 
            var totalRow = '<th>Total</th><td><strong><span class="amount">$'+subTotal+'</span></strong></td>'
            $('.order-total').append(totalRow);       
        }
    });
    
});
function deleteItem(data){
    var pID = $(data).closest("tr").attr("id");
    console.log("delete clicked",pID);
    $.ajax({
        url: '/deleteProductFromCart',
        data: JSON.stringify({ "productId": pID }),
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (response) {
            console.log("successfully deleted",response);
            window.location.reload(true);
        },
        error: function (error) {
            console.log(error);
        }
    });
   };

  function updateProductCount(data){
    var updatedProductQuantity = $(data).val();
    var pID = $(data).closest("tr").attr("id");
    console.log("changed quantity of:",pID);
    console.log("updated quantity:",updatedProductQuantity);
    if(updatedProductQuantity == 0){
        $.ajax({
            url: '/deleteProductFromCart',
            data: JSON.stringify({ "productId": pID }),
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (response) {
                console.log("successfully deleted",response);
                window.location.reload(true);
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
    $.each(cartProducts, function (index) {
        console.log(cartProducts[index][0])
        if(cartProducts[index][0] == pID){
            console.log("ids match")
            if(cartProducts[index][5] >= updatedProductQuantity){
                console.log("value increased");
                $.ajax({
                    url: '/increaseProductQuantityInCart',
                    data: JSON.stringify({ "productId": pID,"quantity":updatedProductQuantity }),
                    type: 'POST',
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    success: function (response) {
                        console.log("successfully increased");
                        window.location.reload(true);
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });

            }
            else{
                $(data).val(updatedProductQuantity-1);
            
             alert("Maximum availabilty reached");
            }
        }
    });
  };