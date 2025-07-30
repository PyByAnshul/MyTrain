document.getElementById('searchtrain').addEventListener('submit', getdata);
const domain = window.location.origin;


function getdata(e) {
    e.preventDefault();

    var fromDest = document.getElementById('fromDest').value;
    var toDest = document.getElementById('toDest').value;
    var toDate = document.getElementById('toDate').value;
    var params = { fromDest: fromDest, toDate: toDate, toDest: toDest }
    const wrapper = document.getElementById('wrapper');
    // Hide the wrapper initially
    wrapper.style.display = 'block';
    // send http request to our backend program of add funciton to add data in our database
    var xhr = new XMLHttpRequest()

    xhr.open('post', '../submitsearch', true)
    xhr.setRequestHeader('Content-type', 'application/json')
    xhr.onreadystatechange = function() {
            //when the data will be loaded then the form section will be closed

            console.log('coon')

            if (xhr.readyState == 4) {
                var container = document.querySelector('.tbody');
                container.innerHTML = ''

                if (xhr.status == 200) {

                    wrapper.style.display = "none";
                    flyoutEl = document.getElementById('table');
                    flyoutEl.style.display = "block";
                    // Handle the successful response
                    var arr = JSON.parse(this.responseText)
                    console.log(arr)


                    for (var i = 1; i < arr.length + 1; i++) {

                        var obj = arr[i];
                        console.log(obj)
                        displaytable(i, obj['train_name'], obj['train_number'], obj['from_sta'], obj['to_std'])

                    }
                } else {
                    // Handle the error response
                    console.log('error')
                }
            } else {
                // Request is still loading

                // Show the loader while waiting for the response
                wrapper.style.display = 'block';
            }

            //this function is use to create dynamic html content by using two parameter name and data
            // this is use to reset the form and not to store privous data
            // var element = document.getElementById('postform');
            // element.reset();
            //document.getElementById('prediction').innerHTML= this.responseText;
        }
        //send data in json format
    xhr.send(JSON.stringify(params));
}




function displaytable(count, train_name, train_number, arrival_time, departure_time) {
    // get the container 
    var container = document.querySelector('.tbody');
    // create dynamic content
    let p = `
    <div class="tr dataTableRow">
                <p>${count}</p>
                <p>${train_name}/${train_number}</p>
                <p>${arrival_time}</p>
                <p>${departure_time}</p>
                <a href="${domain}/trains/train_finder/${train_number}"><button class="searchBtn">view</button></a>
            </div>
`;
    // insert dynamic content in container
    container.insertAdjacentHTML("beforeend", p)


}