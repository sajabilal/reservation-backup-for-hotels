async function reserve(){
  try {response = await fetch("https://o7w1f1d806.execute-api.us-east-1.amazonaws.com/PROD/SNS",{method:"POST", headers: {
      "Content-Type": "application/x-www-form-urlencoded"  // Tell API Gateway that we are sending form data
  },body: "Action=Publish&TopicArn=arn:aws:sns:us-east-1:476959162071:HotelEmailSending&Message=to DECLINE: https://9owvfe3g25.execute-api.us-east-1.amazonaws.com/decline to ACCEPT: https://9owvfe3g25.execute-api.us-east-1.amazonaws.com/accept"})
  data= await response.text();
  console.log("Server Response:", data);
  alert("Email Sent Successfully! Check your inbox.");}
 catch (error) {
    // If something goes wrong, log the error in the console
    console.error("Error sending email:", error);

    // Show an alert to tell the user that sending the email failed
    alert("Failed to send email. Please check the console for details.");
}}

    
document
  .getElementById("Monet Garden Hotel")
  .addEventListener("click", reserve); //accessing the hotel search bar and adding a listener to the enter pressed