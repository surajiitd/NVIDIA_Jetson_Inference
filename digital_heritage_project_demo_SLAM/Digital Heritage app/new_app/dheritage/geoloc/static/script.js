var ip = "http://127.0.0.1:8080";
var canvas = document.getElementById('myMap');
var ctx = canvas.getContext('2d');
const chartWidth = canvas.width;
const chartHeight = canvas.height;

function getObj() {
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", ip + "/locations/", false); // false for synchronous request
    xmlHttp.send(null);
    const obj = JSON.parse(xmlHttp.responseText);
    return obj
}

obj = getObj();
const locations = [];
for (let i = 1; i < obj.length; i++) {
    locations.push({ x: obj[i]['x'], y: obj[i]['y'], color: 'red' })
}
console.log(obj[0])
console.log(locations)

// Initialize the scatter plot with initial data
const initialData = {
    datasets: [{
        label: 'User',
        data: [{ x: obj[0]['x'], y: obj[0]['y'], color: 'green' }],
        backgroundColor: 'green' // This will be overwritten by individual point colors
    },
    {
        label: 'Locations',
        data: locations,
        backgroundColor: 'red'
    }]
};

const scatterPlot = new Chart(ctx, {
    type: 'scatter',
    data: initialData,
    options: {
        responsive: false, // Disable responsiveness
        maintainAspectRatio: false, // Disable aspect ratio
        width: chartWidth, // Set chart width to match canvas width
        height: chartHeight, // Set chart height to match canvas height
        scales: {
            x: {
                min: -0.2,
                max: 1.2
            },
            y: {
                min: -0.2,
                max: 1.8
            }
        }
    }
});

// Function to update scatter plot with new data
function updateScatterPlot(dataPoints) {
    const newData = dataPoints.map(point => ({
        x: point.x,
        y: point.y,
        color: point.color
    }));

    scatterPlot.data.datasets[0].data = newData;
    scatterPlot.data.datasets[0].backgroundColor = newData.map(point => point.color);
    scatterPlot.update();
}

function updateMap() {
    obj = getObj();
    console.log([{ x: obj[0]['x'], y: obj[0]['y'], color: 'green' }])
    updateScatterPlot([{ x: obj[0]['x'], y: obj[0]['y'], color: 'green' }]);
    updateCoordinates(obj[0]['x'], obj[0]['y'], obj[0]['yaw'])
}

function updateCoordinates(x, y, yaw) {
    document.getElementById('x-coordinate').textContent = 'X: ' + x;
    document.getElementById('y-coordinate').textContent = 'Y: ' + y;
    document.getElementById('yaw-coordinate').textContent = 'Yaw: ' + yaw;
}

updateMap()
const interval = setInterval(() => {
    updateMap()
}, 100); // Start the update initially