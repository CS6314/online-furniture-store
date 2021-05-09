var allProducts;
$(document).ready(function () {
  console.log("document ready");
  getAllProducts();

  // Get the category
  $.ajax({
    url: "/categories",
    type: "GET",
    dataType: "json",
    success: function (response) {
      var $dropdown = $("#category");
      $.each(response, function (index) {
        $dropdown.append(
          $("<option />").val(response[index]).text(response[index])
        );
      });
      $dropdown.append($("<option />").val("*").text("Show all"));
    },
    error: function (error) {
      console.log(error);
    },
  });

  // Search button click event
  $("#searchButton").click(function (event) {
    event.preventDefault();
    console.log("clicked");
    let searchFormValues = $("#search-form")[0];
    console.log($('#category').val());    
    if($('#category').val()=='*' && $('#price').val() == '*' && $('#quantity').val() == '*' && $('#searchText').val() == ''){
        $("#products").empty();
        getAllProducts();
    }
    else{
        $.ajax({
            url: "/searchProducts?pageNumber=1",
            type: "POST",
            data: $("#search-form").serialize(),
            dataType: "json",
            success: function (response) {
              $("#products").empty();
              console.log(response);
              console.log(response.html)
              if(response.html){
                  $("#products").append(response.html)
              }else{
                  $.each(response, function (index) {
                      // var listRow = '<tr id="'+response[index][0]+'"><td class="product-thumbnail"><img src="/static/images/product/' + response[index][3] + '" alt="Image Unavailable" /></td><td class="product-name"><a href="#">' + response[index][1] + '</td><td class="product-name">' + response[index][2] + '</td><td class="product-name">'+response[index][4]+'</td><td class="product-name">' + response[index][6]+'</td><td class="product-name">'+response[index][5]+'</td><td class="product-name">Available</td><td class="product-remove"><a href="#" onclick="editProduct(this);"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16"><path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/></svg></a></td></tr>';
            
                      // $('#tableBody').append(listRow);
            
                      product = `
                            <div class='col-sm-4 product'>
                            <div class='product-inner text-center' >
                            <img src=${
                              "/static/images/product/" + response[index][3]
                            } ><br />
                            <div class='pt-10' id=${response[index][0]}>
                            Title: ${response[index][1]}<br />
                            Description: ${response[index][2]}<br />
                            Price: $${response[index][4]}<br />
                            Quantity: ${response[index][5]}<br />
                            Category: ${response[index][6]}<br />
                            Available <br />
                            <form class="form-signin" action="/addToCart" method="post">
                            <div class="form-group">
                            <input type="hidden" name="productId" id="productId" class="form-control" value=" ${response[index][0]}"></div>
                            <button class="btn btn-secondary btn-block" type="submit">Add to Cart</button>
                            </form>
                            
                            </div>
                            </div></div>`;
            
                      $("#products").append(product);
                    });
                    paginationTable(response);
              }
              
            },
            error: function (error) {
              console.log(error);
            },
          });
    }
    
  });
});

//   pagination function

function paginationTable(data) {
  // create the buttons according to the length of the response
  $("#pagination-container").empty();
  $("#pagination-container").append(`<button>&laquo;</button>`);
  //  only 10 elements per page
  data = data.filter(eachData => eachData[7] !=1);
  noOfPages = Math.ceil(data.length / 9);
  for (i = 0; i < noOfPages; i++) {
    $("#pagination-container").append(
      `<button id='paginate' ${i == 0 ? 'class="active"' : ""}>${
        i + 1
      }</button>`
    );
  }
  $("#pagination-container").append(`<button>&raquo;</button>`);

  $("button#paginate").click(function (event) {
    //  change the state to active
    console.log("paginate button clicked");
    $(".active").removeClass("active");
    $(this).addClass("active");

    console.log($(this).html());
    //   get the list for the specific pageNumber
    $.ajax({
      url: `/searchProducts?pageNumber=${$(this).html()}`,
      type: "POST",
      data: $("#search-form").serialize(),
      dataType: "json",
      success: function (response) {
        $("#products").empty();
        console.log(response.html)

        $.each(response, function (index) {
          // var listRow = '<tr id="'+response[index][0]+'"><td class="product-thumbnail"><img src="/static/images/product/' + response[index][3] + '" alt="Image Unavailable" /></td><td class="product-name"><a href="#">' + response[index][1] + '</td><td class="product-name">' + response[index][2] + '</td><td class="product-name">'+response[index][4]+'</td><td class="product-name">' + response[index][6]+'</td><td class="product-name">'+response[index][5]+'</td><td class="product-name">Available</td><td class="product-remove"><a href="#" onclick="editProduct(this);"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16"><path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/></svg></a></td></tr>';

          // $('#tableBody').append(listRow);

          product = `
                <div class='col-sm-4 product'>
                <div class='product-inner text-center' >
                <img src=${
                  "/static/images/product/" + response[index][3]
                } ><br />
                <div class='pt-10' id=${response[index][0]}>
                Title: ${response[index][1]}<br />
                Description: ${response[index][2]}<br />
                Price: $${response[index][4]}<br />
                Quantity: ${response[index][5]}<br />
                Category: ${response[index][6]}<br />
                Available <br />
                <form class="form-signin" action="/addToCart" method="post">
                <div class="form-group">
                <input type="hidden" name="productId" id="productId" class="form-control" value=" ${response[index][0]}"></div>
                <button class="btn btn-secondary btn-block" type="submit">Add to Cart</button>
                </form>
               
                </div>
                </div></div>`;

          $("#products").append(product);
        });
      },
      error: function (error) {
        console.log(error);
      },
    });
  });
}
function getAllProducts(){
    $("#products").empty();
    $.ajax({
        url: "/getProductsForUser",
        type: "GET",
        dataType: "json",
        success: function (response) {
          allProducts = response;
          let length = response.length < 9 ? response.length : 9;
          for (let index = 0; index < length; index++) {
              product = `
                    <div class='col-sm-4 product'>
                    <div class='product-inner text-center' >
                    <img src=${
                        "/static/images/product/" + response[index][3]
                      } ><br />
                    <div class='pt-10'>
                     Title: ${response[index][1]}<br />
                    Description: ${response[index][2]}<br />
                    Price: $${response[index][4]}<br />
                    Category: ${response[index][6]}<br />
                    Available <br />
                    <form class="form-signin" action="/addToCart" method="post">
                    <div class="form-group">
                    <input type="hidden" name="productId" id="productId" class="form-control" value=" ${response[index][0]}"></div>
                    <button class="btn btn-secondary btn-block" type="submit">Add to Cart</button>
                    </form>
                    
                    </div>
                    </div></div>`;
             
            
            $("#products").append(product);
          }
    
          paginationTable(response);
        },
        error: function (error) {
          console.log(error);
        },
      });
}