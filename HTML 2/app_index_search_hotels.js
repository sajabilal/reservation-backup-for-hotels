let hotelName="";
async function confirm(event) {
  console.log(hotelName);
  event.preventDefault();
  customerEmail = document.getElementById("email").value;//user email
  if (hotelName === "Monet Garden Hotel"){
    hotelEmail = "monetgardenhotelresevation@gmail.com";
  }
  if (hotelName === "cc"){
    hotelEmail = "monetgardenhotelresevation@gmail.com";
  }
  if (hotelName === "holiday"){
    hotelEmail = "monetgardenhotelresevation@gmail.com";
  }

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
          "message" : `to DECLINE: https://lhoeea8hkl.execute-api.us-east-1.amazonaws.com/prod/decline-to-customer?email=${customerEmail}&hotel=${encodeURIComponent(hotelName)} to ACCEPT: https://lhoeea8hkl.execute-api.us-east-1.amazonaws.com/accept-to-customer?email=${customerEmail}&hotel=${encodeURIComponent(hotelName)}`
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

document
  .getElementById("Monet Garden Hotel")
  .addEventListener("click", reserve); //accessing the hotel search bar and adding a listener to the enter pressed

document
.getElementById("cc")
.addEventListener("click", reserve); //accessing the hotel search bar and adding a listener to the enter pressed

document
  .getElementById("holiday")
  .addEventListener("click", reserve); //accessing the hotel search bar and adding a listener to the enter pressed

document.getElementById("reservationForm").addEventListener("submit", confirm);
