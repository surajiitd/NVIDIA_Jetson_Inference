const currentHost = window.location.host;
const hostName = "http://" + currentHost;
console.log(hostName);

var reached = false;
var speech = new SpeechSynthesisUtterance();
var locationColor = ['orange', 'purple'];
var buttonState = 0;
var button = document.getElementById('on-button')

function getObj() {
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", hostName + "/locations/", false); // false for synchronous request
    xmlHttp.send(null);
    const obj = JSON.parse(xmlHttp.responseText);
    return obj
}

obj = getObj();
// console.log(obj[0])

// Initialize the scatter plot with initial data
const initialData = {
    datasets: [
        {
            label: 'UserH',
            data: [{ x: obj[0]['x'], y: obj[0]['y'], yaw: obj[0]['yaw'] }],
            pointStyle: 'triangle',
            pointRadius: 6,
            borderColor: 'red',
            borderWidth: 5,
            rotation: 0
        },
        {
            label: 'UserV',
            data: [{ x: obj[0]['x'], y: obj[0]['y'], yaw: obj[0]['yaw'] }],
            pointStyle: 'line',
            pointRadius: 15,
            borderColor: 'blue',
            borderWidth: 5,
            rotation: 90
        },
        //Manually enter the locations and their color
        {
            label: 'location1',
            data: [{ x: obj[1]['x'], y: obj[1]['y'], yaw: obj[1]['yaw'] }],
            pointStyle: 'rect',
            backgroundColor: locationColor[0],
            pointRadius: 10
        },
        {
            label: 'location2',
            data: [{ x: obj[2]['x'], y: obj[2]['y'], yaw: obj[2]['yaw'] }],
            pointStyle: 'rect',
            backgroundColor: locationColor[1],
            pointRadius: 10
        }]
};

var canvas1 = document.getElementById('myMap');
var ctx1 = canvas1.getContext('2d');
const chartWidth1 = canvas1.width;
const chartHeight1 = canvas1.height;

const scatterPlot = new Chart(ctx1, {
    type: 'scatter',
    data: initialData,
    options: {
        responsive: false, // Disable responsiveness
        maintainAspectRatio: false, // Disable aspect ratio
        width: chartWidth1, // Set chart width to match canvas width
        height: chartHeight1, // Set chart height to match canvas height
        scales: {
            x: {
                min: -0.2,
                max: 0.6
            },
            y: {
                min: -0.2,
                max: 1
            }
        },
        plugins: {
            legend: {
                labels: {
                    filter: function (legendItem, chartData) {
                        return legendItem.datasetIndex !== 0 && legendItem.datasetIndex !== 1;
                    },
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

    scatterPlot.data.datasets[0].data[0]['x'] = dataPoints[0]['x'];
    scatterPlot.data.datasets[0].data[0]['y'] = dataPoints[0]['y'];
    scatterPlot.data.datasets[1].data[0]['x'] = dataPoints[0]['x'];
    scatterPlot.data.datasets[1].data[0]['y'] = dataPoints[0]['y'];

    var userHeading = dataPoints[0]['yaw'];
    if (userHeading < 0) {
        userHeading = 360 - Math.abs(userHeading);
    }

    userHeading = 90 - userHeading;
    // console.log(userHeading);

    scatterPlot.data.datasets[1].rotation = userHeading;
    scatterPlot.data.datasets[0].rotation = 90 + userHeading;

    scatterPlot.update();
}

function updateMap(obj) {
    // console.log([{ x: obj[0]['x'], y: obj[0]['y'], yaw: obj[0]['yaw'] }])
    updateScatterPlot([{ x: obj[0]['x'], y: obj[0]['y'], yaw: obj[0]['yaw'] }]);
    updateCoordinates(obj[0]['x'], obj[0]['y'], obj[0]['yaw'])
}

function updateCoordinates(x, y, yaw) {
    document.getElementById('x-coordinate').textContent = 'X: ' + x;
    document.getElementById('y-coordinate').textContent = 'Y: ' + y;
    document.getElementById('yaw-coordinate').textContent = 'Yaw: ' + yaw;
}

function update() {
    obj1 = getObj();
    updateMap(obj1);
}

function toggleButton() {
    // Make the page fullscreen
    // if (document.documentElement.requestFullscreen) {
    //     document.documentElement.requestFullscreen();
    // } else if (document.documentElement.mozRequestFullScreen) { // Firefox
    //     document.documentElement.mozRequestFullScreen();
    // } else if (document.documentElement.webkitRequestFullscreen) { // Chrome, Safari and Opera
    //     document.documentElement.webkitRequestFullscreen();
    // } else if (document.documentElement.msRequestFullscreen) { // IE/Edge
    //     document.documentElement.msRequestFullscreen();
    // }

    if (!buttonState) {
        button.innerText = "ON"
        button.style.backgroundColor = '#00ff00';
        buttonState = 1;
    } else {
        button.innerText = "OFF"
        button.style.backgroundColor = '#ff0000';
        buttonState = 0;
    }
}

update();
const interval = setInterval(() => {
    if (buttonState) {
        update();
    }
}, 100); // Start the update initially