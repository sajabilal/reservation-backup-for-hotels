

const handleClick = function(event){
if (event.key == "Enter"){
    //take the input 
    const input = document.getElementById("search_for_hotel").value;//document is a built in object in javascript which allows js to manipulate html
     // Check if input is not empty
     if (input.trim() === "") {//trim removes white spaces before and after query
        alert("Please enter a destination to search.");
        return;
      }
    //search it in the web(i used booking outputs)
    const bookingURL = `https://www.booking.com/searchresults.html?ss=${encodeURIComponent(input)}`;
    //return it on screen 
    displayResults();
}
};

const handle = function(event){
    if (event == "Enter"){
        //search it in the database
        //return it on screen 
        //give options for deletition 
    }
    };

    function handleResponse(response){
        //parce url result 
        console.log(response)
        //transform to json
        return response.json()
    };

    function handleData(response){
        console.log(response)
    };

    function handleError(error){
        console.error("Error:", error)
    };

    function displayResults(url){
        fetch(url)
        .then(handleResponse)//parces the result of the search and transforms it to json
        .then(handleData) //parces the json
        .catch(handleError)//shows error in the console
    };

    document.getElementById("search_for_hotel").addEventListener("keydown", handleClick); //accessing the hotel search bar and adding a listener to the enter pressed
    document.getElementById("search_for_reservation").addEventListener("keydown", handle); //accessing the hotel search bar and adding a listener to the enter pressed
    
