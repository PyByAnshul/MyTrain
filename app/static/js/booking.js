
        // Get all images
        var images = document.querySelectorAll('.image-container img');
        var container = document.querySelector('.image-container');
        var arrow = document.createElement('div');
        arrow.classList.add('arrow');
        arrow.innerHTML = '⬇️'; // Unicode for down arrow
    
        // Append arrow to the container
        container.appendChild(arrow);
    
        // Function to randomly select checkboxes
        function selectRandomCheckboxes() {
    // Get all checkboxes
    var checkboxes = document.querySelectorAll('.mainseatconatiner input[type="checkbox"]');
    
    // Reset all checkboxes
    checkboxes.forEach(function(checkbox) {
        checkbox.checked = false;
        checkbox.classList.remove('checked-label'); // Remove the class if it exists
        checkbox.disabled = false; // Enable all checkboxes
        // Remove the tooltip text span element
        var label = checkbox.nextElementSibling;
        var tooltipText = label.querySelector('.tooltip-text');
        if (tooltipText) {
            label.removeChild(tooltipText);
        }
    });
    // Loop through each checkbox and randomly select some
    checkboxes.forEach(function(checkbox) {
        // Generate a random number between 0 and 1
        var random = Math.random();
        // If the random number is greater than 0.5, check the checkbox
        if (random > 0.5) {
            checkbox.checked = true;
            checkbox.classList.add('checked-label'); // Add the class
            checkbox.disabled = true; // Disable the checkbox
            var label = checkbox.nextElementSibling; // Get the label element
            var tooltipText = document.createElement('span'); // Create a span element for tooltip text
            tooltipText.textContent = "Hover over me to load data..."; // Initial tooltip text content
            tooltipText.classList.add('tooltip-text'); // Add tooltip text class
            label.appendChild(tooltipText); // Append the tooltip text to the label
            
            // Show tooltip on mouseover
            label.addEventListener('mouseover', function() {
                // Make XHR request to Flask app
                const currentURL = window.location.href;
                const param={train_no:currentURL}
                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/api/getData', true); // Adjust URL according to your Flask route
                xhr.setRequestHeader('Content-Type', 'application/json');

                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4) {
                        if (xhr.status === 200) {
                            tooltipText.textContent = JSON.parse(xhr.responseText); // Update tooltip text content with response
                        } else {
                            // Handle error
                            console.error('Request failed:', xhr.status, xhr.statusText);
                            tooltipText.textContent = 'Error: Unable to fetch data';
                        }
                    }
                };

                xhr.send(JSON.stringify(param));
                tooltipText.style.display = 'flex';
            });
            label.addEventListener('mouseout', function() {
                tooltipText.style.display = 'none';
            });
    
        }
    });
}

    
        // Call the function to select random checkboxes when the script runs
    
        // Loop through each image and attach click event listener
        images.forEach(function(image) {
            image.addEventListener('click', function() {
                // Scroll to the image's position within the container
                container.scrollLeft = image.offsetLeft;
    
                // Position the arrow above the selected image
                arrow.style.display = 'block';
                arrow.style.left = image.offsetLeft + (image.offsetWidth / 2) + 'px'; // Position arrow in the middle of the image
    
                // Set booking details based on alt attribute
                var coachNo = image.alt;
                if (coachNo == 'engine' || coachNo == 'last loco'){
                    console.log('wrong way')
                    var checkboxes = document.querySelectorAll('.mainseatconatiner input[type="checkbox"]');
            checkboxes.forEach(function(checkbox) {
    checkbox.checked = false;
});
                }
                else{

                    var coachImage = document.querySelector('img[alt="' + coachNo + '"]');
                    selectRandomCheckboxes();
                    document.getElementById('Ac').style.background="rgba(255, 255, 255, 0.16)";
                    document.getElementById('Sleeper').style.background="rgba(255, 255, 255, 0.16)";
                    document.getElementById('general').style.background="rgba(255, 255, 255, 0.16)";
                    if (coachImage) {
                        document.getElementById('coach-no').innerText = coachNo;
                        if (['A1', 'A2', 'A3'].includes(coachNo)) {
    document.getElementById('coach-type').innerText = 'AC First Class';
    document.getElementById('Ac').style.background="#4787e9";

}
                        // Set other details based on your data structure or logic
                    }
                        if (['B1', 'B2', 'B3'].includes(coachNo)) {
    document.getElementById('coach-type').innerText = 'Sleeper Class';
    document.getElementById('Sleeper').style.background="#4787e9";

}
                        if (['C1', 'C2', 'C3','C4'].includes(coachNo)) {
    document.getElementById('coach-type').innerText = 'General';
    document.getElementById('general').style.background="#4787e9";

}
                        // Set other details based on your data structure or logic
                    
                }
                
            });
        });
        // Select all checkboxes
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
const pricePerSeat = {
    'A': 3000,
    'B': 300,
    'C': 30
};
let totalPrice = 0;

function updateCount() {
    const selectedCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked:not(.checked-label)');
    const selectedCount = selectedCheckboxes.length;
    document.getElementById('selected-seats').innerText = selectedCount;

    const coachNo = document.getElementById('coach-no').innerText.trim().toUpperCase();
    if (coachNo[0] in pricePerSeat) {
        totalPrice = selectedCount * pricePerSeat[coachNo[0]];
        document.getElementById('total-price').innerText = totalPrice;
    }
}

checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', updateCount);
});

document.getElementById('book-button').addEventListener('click', function() {
        const trainNo = document.getElementById('train-no').innerText;
        const coachNo = document.getElementById('coach-no').innerText;
        const selectedSeats = document.getElementById('selected-seats').innerText;
        const totalPrice = document.getElementById('total-price').innerText.replace('$', '');
        const coachType = document.getElementById('coach-type').innerText;

        const urlParams = new URLSearchParams(window.location.search);
        urlParams.set('trainno', trainNo);
        urlParams.set('coachno', coachNo);
        urlParams.set('seats', selectedSeats);
        urlParams.set('totalprice', totalPrice);
        urlParams.set('coachtype', coachType);

        const newUrl = window.location.origin + '/booking/book/book_ticket'+ '?' + urlParams.toString();
        window.location.href = newUrl;
    });


    function showTooltip(checkboxId) {
        var tooltipTextId = "tooltipText_" + checkboxId;
        var tooltipText = document.getElementById(tooltipTextId);
        tooltipText.style.display = "flex";
      }
    
      function hideTooltip(checkboxId) {
        var tooltipTextId = "tooltipText_" + checkboxId;
        var tooltipText = document.getElementById(tooltipTextId);
        tooltipText.style.display = "none";
      }