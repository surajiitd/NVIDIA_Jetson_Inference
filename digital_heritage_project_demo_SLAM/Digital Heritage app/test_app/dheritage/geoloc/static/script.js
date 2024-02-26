document.addEventListener('DOMContentLoaded', function() {
    // Function to fetch data from the server
    function fetchData() {
        fetch('{% url 'update_current' %}')
        .then(response => response.json())
        .then(data => {
            // Update the values in the HTML
            document.getElementById('x-value').innerText = data.x;
            document.getElementById('y-value').innerText = data.y;
            document.getElementById('yaw-value').innerText = data.yaw;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    }

    // Fetch data initially when the page loads
    fetchData();

    // Fetch data every 5 seconds
    setInterval(fetchData, 5000);
});
