const searchInputContainer = document.querySelector(".search-input1");
const searchInputBox = searchInputContainer.querySelector("input");
const suggestionBox = searchInputContainer.querySelector(".autocom-box1");
let searchLink = searchInputContainer.querySelector("a");
let searchQueryUrl;

searchInputBox.onkeyup = (event) => {
    const userInput = event.target.value; // user's entered data
    let suggestionsList = [];
    if (userInput) {
        suggestionsList = suggestions.filter((data) => {
            // filter data based on user input and lowercase comparison
            return data.toLocaleLowerCase().startsWith(userInput.toLocaleLowerCase());
        }).slice(0, 7);
        suggestionsList = [...new Set(suggestionsList)]; // remove duplicates
        suggestionsList = suggestionsList.map((data) => `<li>${data}</li>`);
        searchInputContainer.classList.add("active"); // show suggestion box
        updateSuggestionList(suggestionsList);
        const allListItems = suggestionBox.querySelectorAll("li");
        for (let i = 0; i < allListItems.length; i++) {
            allListItems[i].setAttribute("onclick", "onSuggestionClick(this)");
        }
    } else {
        searchInputContainer.classList.remove("active"); // hide suggestion box
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