
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

        const newUrl = window.location.origin + '/book/book_ticket'+ '?' + urlParams.toString();
        window.location.href = newUrl;
    });
