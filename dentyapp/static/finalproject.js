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
  document.getElementById("defaultOpen").click();


  $('.carousel').carousel()


  //----------------------------- recipient PAGE-------------


  function openCity(evt, cityName) {
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
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  }




// ------------------------Flutterwave Payment ------------------------------------

function makePayment() {
  let recipientIdForDonation = document.getElementById('recipientIdForDonation');
  recipientIdForDonation = recipientIdForDonation && recipientIdForDonation.value;
  let amount = 50;
  // if(recipientIdForDonation) {
  //   //Only do specific donate prompt when on donate page
  //   amount = prompt('How much do you want to donate?');
  // }
  
  var checkoutfunc = FlutterwaveCheckout({
    public_key: "FLWPUBK_TEST-SANDBOXDEMOKEY-X",
    tx_ref: "RX1"+ Date.now(),
    amount: amount * 1,
    currency: "NGN",
    country: "NG",
    payment_options: " ",
    /*redirect_url: "http://127.0.0.1:5000/payment_successful", */
    meta: {
      consumer_id: 23,
      consumer_mac: "92a3-912ba-1192a",
    },
    customer: {
      email: "beepearl89@gmail.com",
      phone_number: "08067353992",
      name: "Debbie",
    },
    callback: function (data) {
      console.log(data);
      if(data && data.status === 'successful' && recipientIdForDonation) {
        
        $.post('/donations', {amount: data.amount, status: data.status, recipient: recipientIdForDonation * 1});
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
      "https://assets.piedpiper.com/logo.png",
    },
  });
}




























  