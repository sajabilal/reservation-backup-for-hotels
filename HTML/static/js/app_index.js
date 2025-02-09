const handleClick = function (event) {
  if (event.key == "Enter") {
    //take the input
    const input = document.getElementById("search_for_hotel").value; //document is a built in object in javascript which allows js to manipulate html
    // Check if input is not empty
    if (input.trim() === "") {
      //trim removes white spaces before and after query
      alert("Please enter a destination to search.");
      return;
    }

    //return it on screen
    if (input === "amsterdam") {
      window.location.href = "search_hotels.html"; // Redirect to the new HTML file
    }
  }
};

function search_query_results(query) {
  alert("search_query_results");
  console.log("the query is");
  console.log(query);
  //fetch the database.txt
  fetch("/templates/database.txt")
    //turn file object into a plain text
    .then(object_into_text)
    //query the plain text and return results
    .then(pass_to_search_query(query))
    //handle fetch error
    .catch(handle_fetch_error);
}

function pass_to_search_query(query){
        return function(text_file) {
            search_query(text_file, query); // ✅ Uses `query` from closure
        };
    }


function search_query(text_file,query) {
  alert("query search");
  console.log ("query is ");
  console.log (query);
  alert("query search1");
  //splits plain text file into lines
  var lines = text_file.split("\n");
  //loops over the lines and checks for the wanted id(query)
  var id;
  var result = [];
  for (i = 0; i < lines.length; i++) {
    var line = lines[i]; //on each itiration line variable gets a whole line
    if (line.startsWith("id: " + query)) {
      //check if the line has the wanted id
      result.push(line);
    }
  }
  //saving search results in "STRING" form in the tab session
  sessionStorage.setItem("results", JSON.stringify(result));
  //return it on screen 
  window.location.href = 'results.html';
}

function object_into_text(response) {
  alert("object_into_text");
  console.log("🚨 Fetch failed: This function is running!");
  return response.text();
}

function handle_fetch_error(error) {
  alert("handle_fetch_error");
  //log error into the console
  console.error("error fetching database file", error);
  //show error on screen
  document.getElementById("content").textContent =
    "error fetching database file";
}

const handle = function (event) {
  if (event.key == "Enter") {
    //take the input
    const input = document.getElementById("search_for_reservation").value;
    //check the input not empty
    if (input.trim() === "") {
      alert("Please insert a convinient booking number");
      return;
    }
    //search it in the database
    search_query_results(input);
  }
};

document
  .getElementById("search_for_hotel")
  .addEventListener("keydown", handleClick); //accessing the hotel search bar and adding a listener to the enter pressed
document
  .getElementById("search_for_reservation")
  .addEventListener("keydown", handle); //accessing the hotel search bar and adding a listener to the enter pressed
