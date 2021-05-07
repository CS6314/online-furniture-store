var allProducts;
$(document).ready(function () {
    console.log("document ready");
    $.ajax({
        url: '/getProducts',
        type: 'GET',
        dataType: "json",
        success: function (response) {
            allProducts = response;
            console.log(response);
            $.each(response, function (index) {
                    if(response[index][7]){
                        var listRow = '<tr id="'+response[index][0]+'"><td class="product-thumbnail"><img src="/static/images/product/' + response[index][3] + '" alt="Image Unavailable" /></td><td class="product-name"><a href="#">' + response[index][1] + '</td><td class="product-name">' + response[index][2] + '</td><td class="product-name">'+response[index][4]+'</td><td class="product-name">' + response[index][6]+'</td><td class="product-name">'+response[index][5]+'</td><td class="product-name">Marked Deleted</td><td class="product-remove"><a href="#" onclick="editProduct(this);"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16"><path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/></svg></a></td></tr>';                    
                    }
                    else {
                        var listRow = '<tr id="'+response[index][0]+'"><td class="product-thumbnail"><img src="/static/images/product/' + response[index][3] + '" alt="Image Unavailable" /></td><td class="product-name"><a href="#">' + response[index][1] + '</td><td class="product-name">' + response[index][2] + '</td><td class="product-name">'+response[index][4]+'</td><td class="product-name">' + response[index][6]+'</td><td class="product-name">'+response[index][5]+'</td><td class="product-name">Available</td><td class="product-remove"><a href="#" onclick="editProduct(this);"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16"><path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/></svg></a></td></tr>';                    
                    }
                    $('#tableBody').append(listRow);
                
                    
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
function editProduct(data){
    var pID = $(data).closest("tr").attr("id");
    var id = '#'+pID;
    var product;
    $.each(allProducts, function (index) {
    if(allProducts[index][0]==pID){
        product = allProducts[index]
    }
    });
    console.log(product);
    console.log("edit clicked",id);
    idRow = '<div id="editProduct" class="form-group"><input type="hidden" name="productId" id="productId" class="form-control" value="' + product[0] + '"></div>'
    if (product[7])
isDeletedRow = '<div class="form-group"><label for="isDeleted" class=" dark">Available</label><input type="radio" value="0" name="isDeleted" class="form-control"><label for="isDeleted" class=" dark">Marked Deleted</label><input type="radio" value="1" name="isDeleted" id="isDeleted" class="form-control" checked ></div>';
else
isDeletedRow = '<div class="form-group"><label for="isDeleted" class=" dark">Available</label><input type="radio" value="0" name="isDeleted" class="form-control" checked><label for="isDeleted" class=" dark">Marked Deleted</label><input type="radio" value="1" name="isDeleted" id="isDeleted" class="form-control" ></div>';
    var productForm = `<div><form class="form-signin" enctype="multipart/form-data"sssrc action="/editProduct" method="POST">
    <h1>Edit Item</h1>
    <div id="filledEditForm">
    <div class="form-group"><label for="productName" class=" dark">Product Name</label><input type="name" name="productName" id="productName" class="form-control" value="` + product[1] + `"required autofocus></div>
    <div class="form-group"><label for="productDescription" class=" dark">Product Description</label><input type="name" name="productDescription" id="productDescription" class="form-control" value="` + product[2] + `"required autofocus></div>
    <div class="form-group"><label for="price" class=" dark">Price</label><input type="name" name="price" id="price" class="form-control" value="` + product[4] + `"required autofocus></div>
    <div class="form-group"><label for="quantity" class=" dark">Quantity</label><input type="name" name="quantity" id="quantity" class="form-control" value="` + product[5] + `"required autofocus></div>
    <div class="form-group"><label for="category" class=" dark">Category</label><input type="name" name="category" id="category" class="form-control" value="` + product[6] + `"required autofocus></div>
    `+isDeletedRow+idRow+`
    <div class="form-group"><label for="image" class=" dark">Image</label><input type="file" id="image" name="image" value="/static/images/product/`+product[3]+`" accept="image/png, image/jpeg"></div>
    </div>
    <button id="btnEdit" class="btn btn-lg btn-primary btn-block" type="submit">Edit</button>
</form></div>`;

    $('.table-content').after(productForm);
    $('#editProduct').focus();
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