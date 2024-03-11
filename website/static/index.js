function deleteDog(dogId) {
  console.log("Deleting dog with ID:", dogId);
  fetch("/delete-dog", {
    method: "POST",
    body: JSON.stringify({ dogId: dogId }),
  }).then((_res) => {
    window.location.href = "/home";
  });
}
