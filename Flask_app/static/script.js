const descriptions = JSON.parse('{{ job_descriptions|tojson|safe }}');

function updateDescription() {
    const jobTitle = document.getElementById("job_title_salary").value;
    const descriptionElement = document.getElementById("job_description");
    descriptionElement.textContent = descriptions[jobTitle] || "";
}

function updateLocationImage(section) {
    let location, imageElement;
    if (section === 'salary') {
        location = document.getElementById("location_salary").value;
        imageElement = document.getElementById("location_salary_image");
    } else if (section === 'stability') {
        location = document.getElementById("location_stability").value;
        imageElement = document.getElementById("location_stability_image");
    }

    if (location) {
        const encodedLocation = encodeURIComponent(location);
        const imageUrl = `/static/images/${encodedLocation}.jfif`;
        console.log(`Image path for ${section}: ${imageUrl}`);
        imageElement.src = imageUrl;
        imageElement.style.display = "block";

        imageElement.onerror = function () {
            console.error(`Cannot load image for location: ${location}`);
            imageElement.style.display = "none";
        };
        imageElement.onload = function () {
            console.log(`Image for ${location} loaded successfully.`);
        };
    } else {
        imageElement.style.display = "none";
    }
}
