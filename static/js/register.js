$("#userRegister").submit(function (e) {
  e.preventDefault();
  var first_name = $("#firstName").val();
  var last_name = $("#lastName").val();
  var email = $("#newEmail").val();
  var confirmEmail = $("#confirmEmailID").val();
  var confirmPassword = $("#confirmPassword").val();
  var contactNumber = $("#contactNumber").val();
  var password = $("#password").val();
  var isAllFieldValid = true;
  $(".error").remove();
  if (first_name.length < 1) {
    $("#firstName").after('<span class="error">This field is required</span>');
    isAllFieldValid = false;
    // return;
  }
  if (last_name.length < 1) {
    $("#lastName").after('<span class="error">This field is required</span>');
    isAllFieldValid = false;
  }
  if (contactNumber.length < 1) {
    $("#contactNumber").after(
      '<span class="error">This field is required</span>'
    );
    isAllFieldValid = false;
    // return;
  }
  console.log($("#newEmail").val(), $("#confirmEmailID").val());
  if (confirmEmail != email) {
    $("#confirmEmailID").after('<span class="error">Email mismatch</span>');
    isAllFieldValid = false;
  }
  if (password.length < 5) {
    $("#password").after(
      '<span class="error">Password must be at least 6 characters long</span>'
    );
    isAllFieldValid = false;
  }
  if (confirmPassword != password) {
    $("#confirmPassword").after(
      '<span class="error">Password mismatch</span><br>'
    );
    isAllFieldValid = false;
  }
  if (isAllFieldValid) {
    $.ajax({
      url: `/signUp`,
      type: "POST",
      data: $("#userRegister").serialize(),
      dataType: "json",
      success: function (response) {
        console.log(response);
        if (response.error) {
          $("#confirmPassword").after(
            `<span class="error">${response.message}</span>`
          );
        } else {
          console.log("else");
          $("#confirmPassword").after(
            `<span class="error">User registered successfully!!</span>`
          );
          setTimeout(function () {
            window.location.href = "/login";
          }, 2500);
        }
      },
      error: function (error) {
        console.log(error);
      },
    });
  }
});
