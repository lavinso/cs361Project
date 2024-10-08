// Event listener for delete-dog-btn
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('delete-dog-btn')) {
        const dogId = event.target.getAttribute('data-dog-id');

        // Show a confirmation dialog
        if (confirm(`Are you sure you want to delete? This action cannot be undone.`)) {
            // Call the deleteDog function
            deleteDog(dogId);
        }
    }
});

// Event listener for update-dog-btn
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('update-dog-btn')) {
        const dogId = event.target.getAttribute('data-dog-id');
        console.log("Update dog with ID:", dogId);
        //Redirect to the update page with the dog ID in the URL
        window.location.href = "/update-dog/" + dogId;
    }
});

// Function to delete a dog
function deleteDog(dogId) {
    fetch("/delete-dog", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ dogId: dogId }),
    }).then((_res) => {
        // Redirect to the home page after deletion
        window.location.href = "/home";
    }).catch(error => {
        console.error('Error deleting dog:', error);
    });
}