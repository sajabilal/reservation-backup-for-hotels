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
    } else {
      window.location.href = "results1.html"; // Redirect to the new HTML file
    }
  }
};

async function search_query_results(query) {
  if (!query) {
    console.error("Query is empty");
    return;
  }
  //fetch the database.txt
  try {
    const response = await fetch(
      `https://iie753rsw2.execute-api.us-east-1.amazonaws.com/prod/searchprimary`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // Tell API Gateway that we are sending form data
        },
        body: JSON.stringify({
          id: query,
        }),
      }
    );
    let data = await response.json();

    console.log("the response is:", data);

    // if (!response.ok) {
    //   throw new Error(`Server returned ${response.status}`);
    // }
    if (data.found === false) {
      // If something goes wrong, log the error in the console
      console.error("Error finding reservation");

      // Show an alert to tell the user that sending the email failed
      alert("no reservation with this number");
      data = null;
    }
    // //saving search results in "STRING" form in the tab session
    sessionStorage.setItem("results", JSON.stringify(data));
    // //return it on screen
    window.location.href = "results.html";

    // console.log(response);
  } catch (error) {
    console.error("Fetch failed:", error);
  }
}

function pass_to_search_query(query) {
  return function (text_file) {
    search_query(text_file, query); //  Uses `query` from closure
  };
}

function search_query(text_file, query) {
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
  window.location.href = "results.html";
}

function object_into_text(response) {
  return response.text();
}

function handle_fetch_error(error) {
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
