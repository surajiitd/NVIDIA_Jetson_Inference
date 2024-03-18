var ip = "http://127.0.0.1:8080";

function getObj() {
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", ip + "/locations/", false); // false for synchronous request
    xmlHttp.send(null);
    const obj = JSON.parse(xmlHttp.responseText);
    return obj
}

obj = getObj();

// console.log(obj[0])

// Initialize the scatter plot with initial data
const markerSize = 10;
const initialData = {
    datasets: [{
        label: 'User',
        data: [{ x: obj[0]['x'], y: obj[0]['y'], yaw: obj[0]['yaw'], color: 'green' }],
        backgroundColor: 'green', // This will be overwritten by individual point colors
        pointRadius: markerSize,
    },
    //Manually enter the locations and their color
    {
        label: 'location1',
        data: [{ x: obj[1]['x'], y: obj[1]['y'], yaw: obj[1]['yaw'], color: 'red' }],
        backgroundColor: 'red',
        pointRadius: markerSize
    },
    {
        label: 'location2',
        data: [{ x: obj[2]['x'], y: obj[2]['y'], yaw: obj[2]['yaw'], color: 'purple' }],
        backgroundColor: 'purple',
        pointRadius: markerSize
    }]
};

var canvas = document.getElementById('myMap');
var ctx = canvas.getContext('2d');
const chartWidth = canvas.width;
const chartHeight = canvas.height;

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
        },
        plugins: {
            legend: {
                labels: {
                    usePointStyle: true,
                },
            },
            tooltip: {
                usePointStyle: true,
            }
        }

    }
});

// Function to update scatter plot with new data
function updateScatterPlot(dataPoints) {
    const newData = dataPoints.map(point => ({
        x: point.x,
        y: point.y,
        yaw: point.yaw,
        color: point.color
    }));

    scatterPlot.data.datasets[0].data = newData;
    scatterPlot.data.datasets[0].backgroundColor = newData.map(point => point.color);

    var userHeading = newData.map(point => point.yaw);
    if (userHeading < 0) {
        userHeading = 360 - Math.abs(userHeading);
    }

    console.log(userHeading);
    scatterPlot.data.datasets[0].rotation = userHeading * (Math.PI / 180);
    // scatterPlot.data.datasets[0].rotation = 23.45;

    scatterPlot.data.datasets.forEach((dataset, index) => {
        if (index === 0) {
            dataset.pointStyle = 'triangle'; // Example: Change pointStyle to 'rect' for the first dataset
        } else {
            dataset.pointStyle = 'rect'; // Example: Change pointStyle to 'circle' for other datasets
        }
    });

    scatterPlot.update();
}

function updateMap() {
    obj = getObj();
    // console.log([{ x: obj[0]['x'], y: obj[0]['y'], yaw: obj[0]['yaw'] }])
    updateScatterPlot([{ x: obj[0]['x'], y: obj[0]['y'], yaw: obj[0]['yaw'], color: 'green' }]);
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