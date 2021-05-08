// window.onload = function()
// {
//     var resetForm = true;

//     var firstName = document.getElementById("firstName");
//     var lastName = document.getElementById("lastName");
//     var inputEmail = document.getElementById("inputEmail");
//     var confirmEmail = document.getElementById("confirmEmail");
//     var contactNumber = document.getElementById("contactNumber");
//     var inputPassword = document.getElementById("inputPassword");
//     var confirmPassword = document.getElementById("confirmPassword");

//     var nameError = appendSpan("Name must contain only letters")
//     var emailError = appendSpan("Please enter the email in the format:abc@def.xyz")
//     var confirmEmailError = appendSpan("Email and Confirm Email field should match")
//     var passwordError = appendSpan("The password field should contain at least six characters.")
//     var confirmPasswordError = appendSpan("Password and confirm password fields should match")

//     firstName.onfocus = ()=> {handleOnFocus(firstName,nameError);}
//     firstName.onblur = ()=> {handleOnBlur(firstName,nameError);}
//     firstName.onchange = () => {handleOnChange(firstName,nameError)};

//     lastName.onfocus = ()=> {handleOnFocus(lastName,nameError);}
//     lastName.onblur = ()=> {handleOnBlur(lastName,nameError);}
//     lastName.onchange = () => {handleOnChange(lastName,nameError)};

//     inputEmail.onfocus = ()=> {handleOnFocus(inputEmail,emailError);}
//     inputEmail.onblur = ()=> {handleOnBlur(inputEmail,emailError);}
//     inputEmail.onchange = () => {handleOnChange(inputEmail,emailError)};

//     confirmEmail.onfocus = ()=> {handleOnFocus(confirmEmail,confirmEmailError);}
//     confirmEmail.onblur = ()=> {handleOnBlur(confirmEmail,confirmEmailError);}
//     confirmEmail.onchange = () => {handleOnChange(confirmEmail,confirmEmailError)};

//     inputPassword.onfocus = ()=> {handleOnFocus(inputPassword,passwordError);}
//     inputPassword.onblur = ()=> {handleOnBlur(inputPassword,passwordError);}
//     inputPassword.onchange = ()=> {handleOnChange(inputPassword,passwordError);}

//     confirmPassword.onfocus = ()=> {handleOnFocus(confirmPassword,confirmPasswordError);}
//     confirmPassword.onblur = ()=> {handleOnBlur(confirmPassword,confirmPasswordError);}
//     confirmPassword.onchange = ()=> {handleOnChange(confirmPassword,confirmPasswordError);}

//     onsubmit = function(event)
//     {
//         resetForm = true;
//         event.preventDefault();
//         //validateName();
//         validateEmail();
//         //validateConfirmEmail();
//         validatePassword();
//         validateConfirmPassword();
//         if(resetForm)
//         {
//             document.getElementById("login").reset();
//         }
//     }

//     function handleOnFocus(element, span)
//     {
//         element.parentNode.appendChild(span);
//     }

//     function handleOnBlur(element, span)
//     {
//         element.parentNode.removeChild(span);
//     }

//     function handleOnChange(element,span)
//     {
//         if(element.classList.contains("validationError"))
//         {
//             element.classList.remove("validationError");
//             element.parentNode.removeChild(span);
//         }
//     }    

//     function appendSpan(message)
//     {
//         var span = document.createElement("span");
//         var text = document.createTextNode(message);
//         span.appendChild(text);
//         return span;
    
//     }

//     function validateEmail()
//     {
//         var emailRegex = /^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$/; 
//         if(emailRegex.test(inputEmail.value))
//         {
//             return true;
//         }    
//         else
//         {
//             if(inputEmail.classList.contains("validationError"))
//             {
//                 inputEmail.classList.remove("validationError");
//                 inputEmail.parentNode.removeChild(span1)
//             }
//             inputEmail.classList.add("validationError");
//             span1 = appendSpan("Incorect email. Please enter the email in the format:abc@def.xyz");
//             inputEmail.parentNode.appendChild(span1);
//             resetForm =false;
            
//         }
//     }


//     function validatePassword()
//     {
//         if(inputPassword.value.length > 5)
//         {
//             return true;
//         }
//         else
//         {
//             if(inputPassword.classList.contains("validationError"))
//             {
//                 inputPassword.classList.remove("validationError");
//                 inputPassword.parentNode.removeChild(span2)
//             }
//             inputPassword.classList.add("validationError");
//             span2 = appendSpan("Incorect password format. The password field should contain at least six characters.");
//             inputPassword.parentNode.appendChild(span2);
//             resetForm = false;
//         }

//     }

//     function validateConfirmPassword()
//     {
//         if(confirmPassword.value.length > 5 && password.value == confirmPassword.value)
//         {
//             return true;
//         }
//         else
//         {
//             if(confirmPassword.classList.contains("validationError"))
//             {
//                 confirmPassword.classList.remove("validationError");
//                 confirmPassword.parentNode.removeChild(span3)
//             }
//             confirmPassword.classList.add("validationError");
//             span3 = appendSpan("Password did not match");
//             confirmPassword.parentNode.appendChild(span3);
//             resetForm = false;
//         }
//     }

// }