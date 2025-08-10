let hotelName="";
async function confirm(event) {
  event.preventDefault();
  console.log(hotelName);
  var form = event.target;
  customerEmail = form.querySelector("#email").value;//user email
  arrivingDate = form.querySelector("#arrivingDate").value;
  leavingDate = form.querySelector("#leavingDate").value;
  roomtype = form.querySelector("#roomtype").value;

  if (hotelName === "Monet Garden Hotel"){
    hotelEmail = "monetgardenhotelresevation@gmail.com";
  }
  if (hotelName === "cc"){
    hotelEmail = "monetgardenhotelresevation@gmail.com";
  }
  if (hotelName === "holiday"){
    hotelEmail = "monetgardenhotelresevation@gmail.com";
  }

  console.log("the data is",customerEmail,arrivingDate,leavingDate,roomtype)
  try {
    response = await fetch(
      `https://lhoeea8hkl.execute-api.us-east-1.amazonaws.com/prod/ses-to-hotels`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // Tell API Gateway that we are sending form data
        },
        body: JSON.stringify({
          "toEmails": [hotelEmail.trim()],
          "subject" : "reservation request",
          "message" : `request for reservation for a ${roomtype} room on arrival date: ${arrivingDate} and leaving on: ${leavingDate}\n to DECLINE: https://lhoeea8hkl.execute-api.us-east-1.amazonaws.com/prod/decline-to-customer?email=${customerEmail}&hotel=${encodeURIComponent(hotelName)} \nto ACCEPT: https://lhoeea8hkl.execute-api.us-east-1.amazonaws.com/accept-to-customer?email=${customerEmail}&hotel=${encodeURIComponent(hotelName)}&roomtype=${roomtype}&arrivalDate=${arrivingDate}&leavingDate=${leavingDate}`
        })
      }
    );
    data = await response.text();
    console.log("Server Response:", data);
    alert("Email Sent Successfully to hotel!");
  } catch (error) {
    // If something goes wrong, log the error in the console
    console.error("Error sending email:", error);

    // Show an alert to tell the user that sending the email failed
    alert("Failed to send email. Please check the console for details.");
  }
}

function reserve(event) {
  hotelName = event.target.id;
  console.log(hotelName);
  document.getElementById("reservationForm").style.display = "block";
  document.getElementById("Monet Garden Hotel").style.display = "none";
  return hotelName; 
}
function reserve2(event) {
  hotelName = event.target.id;
  console.log(hotelName);
  document.getElementById("reservationForm2").style.display = "block";
  document.getElementById("holiday").style.display = "none";
  return hotelName; 
}
function reserve3(event) {
  hotelName = event.target.id;
  console.log(hotelName);
  document.getElementById("reservationForm3").style.display = "block";
  document.getElementById("cc").style.display = "none";
  return hotelName; 
}

document
  .getElementById("Monet Garden Hotel")
  .addEventListener("click", reserve); //accessing the hotel search bar and adding a listener to the enter pressed

document
.getElementById("cc")
.addEventListener("click", reserve3); //accessing the hotel search bar and adding a listener to the enter pressed

document
  .getElementById("holiday")
  .addEventListener("click", reserve2); //accessing the hotel search bar and adding a listener to the enter pressed

document.getElementById("reservationForm").addEventListener("submit", confirm);
document.getElementById("reservationForm2").addEventListener("submit", confirm);
document.getElementById("reservationForm3").addEventListener("submit", confirm);
