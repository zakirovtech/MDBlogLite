function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function deleteTag(element, name) {
    if (!confirm('Are you sure you want to delete this tag?')) {
        return;
    }

    const deleteUrl = element.getAttribute("data-url");

    fetch(deleteUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ name: name })
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        } else {
            alert("Failed to delete tag.");
        }
    })
    .catch(error => console.error("Error:", error));
}
