function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  
  // Close the dropdown if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }

  


//-------------------------MODAL-------------------------

  // Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}


  // Get the modal
  var modal = document.getElementById('id02');

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
  
  var modal = document.getElementById('id02');
  
  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }

   // Get the modal
   var modal = document.getElementById('id03');

   // When the user clicks anywhere outside of the modal, close it
   window.onclick = function(event) {
     if (event.target == modal) {
       modal.style.display = "none";
     }
   }
   
   var modal = document.getElementById('id03');
   
   // When the user clicks anywhere outside of the modal, close it
   window.onclick = function(event) {
     if (event.target == modal) {
       modal.style.display = "none";
     }
   }

  //----------------------------- PROFILE PAGE-------------

  function openDetails(title, element, color) {
    // Hide all elements with class="tabcontent" by default */
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Remove the background color of all tablinks/buttons
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].style.backgroundColor = "";
    }
  
    // Show the specific tab content
    document.getElementById(title).style.display = 'block'
  
    // Add the specific color to the button used to open the tab content
    element.style.backgroundColor = color;
  }
  
  // Get the element with id="defaultOpen" and click on it
  let defaultOpenElem = document.getElementById("defaultOpen");
  defaultOpenElem && defaultOpenElem.click();


  $('.carousel').carousel()


  //----------------------------- recipient Account-------------


  function openContent(evt, contentName) {
    // Declare all variables
    var i, reccontent, reclinks;
  
    // Get all elements with class="tabcontent" and hide them
    reccontent = document.getElementsByClassName("reccontent");
    for (i = 0; i < reccontent.length; i++) {
      reccontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    reclinks = document.getElementsByClassName("reclinks");
    for (i = 0; i < reclinks.length; i++) {
      reclinks[i].className = reclinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the link that opened the tab
    document.getElementById(contentName).style.display = "block";
    evt.currentTarget.className += " active";
  }




// ------------------------Flutterwave Payment ------------------------------------

function makePayment() {
  let recipientIdForDonation = document.getElementById('recipientIdForDonation');
  recipientIdForDonation = recipientIdForDonation && recipientIdForDonation.value;
  let userIdForDonation = document.getElementById('userIdForDonation');
  userIdForDonation = userIdForDonation && userIdForDonation.value;
  
  let recipientEmailForDonation = document.getElementById('recipientEmailForDonation');
  recipientEmailForDonation = recipientEmailForDonation && recipientEmailForDonation.value;
  //recipientEmailForDonation
  let amount = '';
  // if(recipientIdForDonation) {
  //   //Only do specific donate prompt when on donate page
  //   amount = prompt('How much do you want to donate?');
  // }
  
  var checkoutfunc = FlutterwaveCheckout({
    public_key: "FLWPUBK_TEST-SANDBOXDEMOKEY-X",
    //public_key: "FLWPUBK-6013f760b6f8d0a5d153d2b5fdd6dabf-X",
    

    tx_ref: "DENTYDONATION_"+ Date.now()+`_${Math.random()}`.replace('.', ''),
    amount: amount * 1,
    currency: "NGN",
    country: "NG",
    payment_options: " ",
    meta: {
      consumer_id: 23,
      consumer_mac: "92a3-912ba-1192a",
    },
    customer: {
      email: recipientEmailForDonation || ("beepearl89@gmail.com")
    },
    callback: function (data) {
      console.log(data, $, $.post, typeof $.post);
      if(data && data.status === 'successful' && recipientIdForDonation) {
        
        $.post('/donations', {user:userIdForDonation, amount: data.amount, status: data.status, recipient: recipientIdForDonation * 1});
        checkoutfunc.close();
        alert('Thanks for your donation');
        window.location.reload();
        /*
        Number of todos:
        a/ verify that the transaction is valid server side
        b/ ensure uniqueness of payment reference (maybe store reference in donation table and make unique)
        c/ Find a way to link donation to posts and not recipients
        [Above are just random - things to do to make more robust - you can ignore for your submission]
        */
        //create donation
      }
    },
    onclose: function() {
      // close modal
    },
    customizations: {
      title: "Denty",
      description: "Donation for a campaign ",
      logo: 
      "https://cdn.glitch.me/dc8ab110-74e1-408a-9e10-7d7591b2ab97/cavities.png?v=1640395467791",
    },
  });
}






























  