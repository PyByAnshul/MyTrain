const searchInputContainer = document.querySelector(".search-input1");
const searchInputBox = searchInputContainer.querySelector("input");
const suggestionBox = searchInputContainer.querySelector(".autocom-box1");
let searchLink = searchInputContainer.querySelector("a");
let searchQueryUrl;

// searchInputBox.onkeyup = (event) => {
//     const userInput = event.target.value; // user's entered data
//     let suggestionsList = [];
//     if (userInput) {
//         suggestionsList = suggestions.filter((data) => {
//             // filter data based on user input and lowercase comparison
//             return data.toLocaleLowerCase().startsWith(userInput.toLocaleLowerCase());
//         }).slice(0, 7);
//         suggestionsList = [...new Set(suggestionsList)]; // remove duplicates
//         suggestionsList = suggestionsList.map((data) => `<li>${data}</li>`);
//         searchInputContainer.classList.add("active"); // show suggestion box
//         updateSuggestionList(suggestionsList);
//         const allListItems = suggestionBox.querySelectorAll("li");
//         for (let i = 0; i < allListItems.length; i++) {
//             allListItems[i].setAttribute("onclick", "onSuggestionClick(this)");
//         }
//     } else {
//         searchInputContainer.classList.remove("active"); // hide suggestion box
//     }
// };


async function findStations(stationName) {
    return new Promise((resolve, reject) => {
        const url = '/find_stations';
        const xhr = new XMLHttpRequest();
        
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                try {
                    const data = JSON.parse(xhr.responseText);
                    resolve(data);
                } catch (error) {
                    reject(error);
                }
            } else {
                reject(new Error('Failed to fetch stations'));
            }
        };

        xhr.onerror = function () {
            reject(new Error('Network error occurred'));
        };

        const body = JSON.stringify({ station_name: stationName });
        xhr.send(body);
    });
}
searchInputBox.onkeyup = async (e) => {
    const userInput = e.target.value; // user's entered data
    if (userInput) {
        try {
            const data = await findStations(userInput); // Fetch suggestions dynamically from Flask API
            if (data) {
                const emptyArray = data.filter((item) => {
                    // Filtering array value and user characters to lowercase and return only those words which start with user entered chars
                    return item.toLocaleLowerCase().startsWith(userInput.toLocaleLowerCase());
                }).slice(0, 7).map((item) => {
                    // Passing return data inside li tag
                    return `<li>${item}</li>`;
                });
                searchInputContainer.classList.add("active"); // Show autocomplete box
                updateSuggestionList(emptyArray);
                const allListItems = suggestionBox.querySelectorAll("li");
                for (let i = 0; i < allListItems.length; i++) {
                    // Adding onclick attribute in all li tag
                    allListItems[i].setAttribute("onclick", "onSuggestionClick(this)");
                }
            } else {
                console.error('Failed to fetch suggestions');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    } else {
        searchInputContainer.classList.remove("active"); // Hide autocomplete box
    }
};

function onSuggestionClick(element) {
    const selectedData = element.textContent;
    searchInputBox.value = selectedData;
    searchQueryUrl = `https://www.google.com/search?q=${selectedData}`;
    searchLink.setAttribute("href", searchQueryUrl);
    searchInputContainer.classList.remove("active");
}

function updateSuggestionList(list) {
    let listData;
    if (!list.length) {
        listData = `<li>${userInput}</li>`; // show user input if no suggestions
    } else {
        listData = list.join("");
    }
    suggestionBox.innerHTML = listData;
}