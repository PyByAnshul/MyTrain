const searchWrapper = document.querySelector(".search-input");
const inputBox = searchWrapper.querySelector("input");
const suggBox = searchWrapper.querySelector(".autocom-box");
// const icon = searchWrapper.querySelector(".icon");
let linkTag = searchWrapper.querySelector("a");
let webLink;

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
inputBox.onkeyup = async (e) => {
    let userData = e.target.value; //user entered data
    let emptyArray = [];
    if (userData) {
        try {
            const data = await findStations(userData); // Fetch suggestions dynamically from Flask API
            if (data) {
                emptyArray = data.filter((item) => {
                    //filtering array value and user characters to lowercase and return only those words which are start with user entered chars
                    return item.toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
                }).slice(0, 7);
                emptyArray = [...new Set(emptyArray)];
                emptyArray = emptyArray.map((item) => {
                    // passing return data inside li tag
                    return `<li>${item}</li>`;
                });
                searchWrapper.classList.add("active"); //show autocomplete box
                showSuggestions(emptyArray);
                let allList = suggBox.querySelectorAll("li");
                for (let i = 0; i < allList.length; i++) {
                    //adding onclick attribute in all li tag
                    allList[i].setAttribute("onclick", "select(this)");
                }
            } else {
                console.error('Failed to fetch suggestions');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    } else {
        searchWrapper.classList.remove("active"); //hide autocomplete box
    }
};
function select(element) {
    let selectData = element.textContent;
    inputBox.value = selectData;
    // icon.onclick = () => {
    //     webLink = `https://www.google.com/search?q=${selectData}`;
    //     linkTag.setAttribute("href", webLink);
    //     linkTag.click();
    // }
    searchWrapper.classList.remove("active");
}

function showSuggestions(list) {
    let listData;
    if (!list.length) {
        userValue = inputBox.value;
        listData = `<li>${userValue}</li>`;
    } else {
        listData = list.join('');
    }
    suggBox.innerHTML = listData;
}