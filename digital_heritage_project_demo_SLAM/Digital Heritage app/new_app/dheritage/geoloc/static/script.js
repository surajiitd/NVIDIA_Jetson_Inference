const play_button = document.querySelector('#play-button');
const cards = document.getElementsByClassName('cards')[0];
const nearby_list = document.getElementsByClassName('nearby-list')[0];
const form = document.getElementsByClassName('mark')[0];

var speech = new SpeechSynthesisUtterance();
var loc = [];
var reached = false;
var appState = "OFF";
var ip = "http://127.0.0.1:8080";

var canvas = document.getElementById('myMap');
var ctx = canvas.getContext('2d');
var mapWidth = canvas.width;
var mapHeight = canvas.height;
var markerRadius = 10;
var centerX = mapWidth / 2;
var centerY = mapHeight / 2;

// function buttonPress() {
//     if (appState == "ON") {
//         appState = "OFF";
//         play_button.style.backgroundColor = "green";
//         speech.text = "Powering Off.";
//         window.speechSynthesis.speak(speech);
//         clearInterval(interval); // Stop the update
//         cards.innerHTML = "";
//         nearby_list.innerHTML = "";
//         reached = false;
//         form.classList.add('invisible');
//     } else {
//         appState = "ON";
//         play_button.style.backgroundColor = "red";
//         speech.text = "Powering On.";
//         window.speechSynthesis.speak(speech);
//         form.classList.remove('invisible');
//         // Execute shell script here
//         // executeShellScript();
//         interval = setInterval(update, 10); // Start the update again

//     }
//     play_button.innerHTML = appState;
// }

// function executeShellScript() {
//     // You can use AJAX to send a request to your Django backend
//     // which in turn executes the shell script.
//     var xhr = new XMLHttpRequest();
//     xhr.open("GET", ip + "/execute_script/", true);
//     xhr.send();
// }

function mark() {
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", ip + "/locations/", false); // false for synchronous request
    const obj = JSON.parse(xmlHttp.responseText);

    var curLocation = obj[0];

    var data = {
        "location_name": String(form.elements[0].value),
        "description": "",
        "voice_message": "You have reached " + String(form.elements[0].value),
        "x": String(curLocation.x),
        "y": String(curLocation.y),
        "yaw": String(curLocation.yaw)
    };

    const xhr = new XMLHttpRequest();
    xhr.open("POST", ip + "/locations/");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            console.log(xhr.status);
            console.log(xhr.responseText);
        }
    };
    xhr.send(JSON.stringify(data));
}

function updateCoordinates(x, y, yaw) {
    document.getElementById('x-coordinate').textContent = 'X: ' + x;
    document.getElementById('y-coordinate').textContent = 'Y: ' + y;
    document.getElementById('yaw-coordinate').textContent = 'Yaw: ' + yaw;
}

function drawUserMarker() {
    ctx.strokeStyle = 'green';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(centerX, centerY, markerRadius, 0, 2 * Math.PI);
    ctx.stroke();
}

function drawLocationMarker(mx, my) {
    ctx.fillStyle = 'red';
    ctx.arc(mx, my, markerRadius, 0, 2 * Math.PI);
    ctx.fill();
}

function initMap() {
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 2;
    ctx.strokeRect(0, 0, mapWidth, mapHeight);
    drawUserMarker();
}

function clearMarker(mx, my) {
    ctx.clearRect(mx - Math.SQRT2 * markerRadius, my - Math.SQRT2 * markerRadius, mx + Math.SQRT2 * markerRadius, my + Math.SQRT2 * markerRadius);
    console.log("cleared marker");
}

function updateMap(locationX, curLocationX, locationY, curLocationY) {
    const scalingFactorX = 200;
    const scalingFactorY = 200;
    markerX = centerX + scalingFactorX * (curLocationX - locationX);
    markerY = centerY + scalingFactorY * (curLocationY - locationY);

    console.log(markerX, markerY, locationX, locationY)

    if (markerX == centerX && markerY == centerY) {
        console.log("ignore !!!");
        return;
    }

    // if ((markerX >= 400 - markerRadius || markerY >= 400 - markerRadius || markerX <= markerRadius || markerY <= markerRadius)) {
    //     drawUserMarker();
    //     console.log("invalid marker !!!");
    //     return
    // }

    drawLocationMarker(markerX, markerY);
}

function updateMarkerCood(locationX, curLocationX, locationY, curLocationY) {
    const scalingFactorX = 200;
    const scalingFactorY = 300;
    markerX = centerX + scalingFactorX * (locationX - curLocationX);
    markerY = centerY + scalingFactorY * (locationY - curLocationY);

    console.log(markerX, markerY, locationX, locationY);

    return [markerX, markerY];
}

function initMarker() {
    ctx.fillStyle = 'red';
    ctx.arc(0, 0, markerRadius, 0, 2 * Math.PI);
    ctx.fill();
}

var prevMarkerX = 0;
var prevMarkerY = 0;
function update() {
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", ip + "/locations/", false); // false for synchronous request
    xmlHttp.send(null);
    const obj = JSON.parse(xmlHttp.responseText);

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    initMap();

    // Ensure that the response contains at least one object
    if (obj.length > 0) {
        var curLocation = obj[0];
        var cardsHTML = "";
        var nearbyHTML = "";
        for (let i = 1; i < obj.length; i++) {
            const location = obj[i];
            if (Math.abs(location.x - curLocation.x) < 10 && Math.abs(location.y - curLocation.y) < 10 && Math.abs(location.yaw - curLocation.yaw) < 15) {
                if (!reached) {
                    reached = true;
                    speech.text = location.voice_message;
                    window.speechSynthesis.speak(speech);
                }
                cardsHTML += '<div class="card" id="' + location.location_name + '"> \
                    <h3>' + location.location_name + '</h3> \
                    ' + location.description + ' \
                </div>';
            }
            nearbyHTML += '<div>' + location.location_name + '</div>';

            // if(i != 1) {
            //     clearMarker(prevMarkerX, prevMarkerY);
            // }



            prevMarkerX, prevMarkerY = updateMap(location.x, curLocation.x, location.y, curLocation.y);

            // if(i == 1) {
            //     continue;
            // }

        }
        cards.innerHTML = cardsHTML;
        nearby_list.innerHTML = nearbyHTML;
        reached = true; // assuming always reached if data is available

        // sleepSync(1000);
        // ctx.clearRect(2, 2, 400 - 2, 400 - 2);
        // Update coordinates
        updateCoordinates(curLocation.x, curLocation.y, curLocation.yaw);
    } else {
        console.log("No locations found in the response.");
    }
}

// play_button.addEventListener('click', buttonPress);

update();
initMap();

const interval = setInterval(() => {
    update();
}, 100); // Start the update initially