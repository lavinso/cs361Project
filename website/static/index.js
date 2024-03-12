// Event listener for delete-dog-btn
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('delete-dog-btn')) {
        const dogId = event.target.getAttribute('data-dog-id');
        deleteDog(dogId);
    }
});

// Event listenter for update-dog-btn
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
    console.log("Deleting dog with ID:", dogId);
    fetch("/delete-dog", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ dogId: dogId }),
    }).then((_res) => {
        window.location.href = "/home"; // Redirect to the home page after deletion
    }).catch(error => {
        console.error('Error deleting dog:', error);
    });
}