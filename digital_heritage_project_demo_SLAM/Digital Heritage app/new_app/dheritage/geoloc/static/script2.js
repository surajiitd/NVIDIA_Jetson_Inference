const play_button = document.querySelector('#play-button');
const geo_button = document.querySelector('#geo-button');
const cards = document.getElementsByClassName('cards')[0];
const nearby = document.getElementsByClassName('nearby')[0];
const nearby_list = document.getElementsByClassName('nearby-list')[0];
const form = document.getElementsByClassName('mark')[0];

var appState = "OFF";
var speech = new SpeechSynthesisUtterance();
var loc = [];
var reached = false;

function buttonPress() {
    // context.resume();
    if (appState == "ON") {
        appState = "OFF";
        play_button.style.backgroundColor = "green";
        // osc.disconnect(volume);
        speech.text = "Powering Off."
        window.speechSynthesis.speak(speech);
        cards.innerHTML = "";
        nearby_list.innerHTML = "";
        reached = false;
        form.classList.add('invisible');
        nearby.classList.add('invisible');
    } else {
        appState = "ON";
        play_button.style.backgroundColor = "red";
        // osc.connect(volume);
        speech.text = "Powering On."
        window.speechSynthesis.speak(speech);
        form.classList.remove('invisible');
        nearby.classList.remove('invisible');
    }
    play_button.innerHTML = appState;
}
//var ip = "http://192.168.141.209:8080/locations/"
var ip = "http://127.0.0.1:8080/locations/"

function mark() {
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", ip, false); // false for synchronous request
    //xmlHttp.send(null);
    // console.log(xmlHttp.responseText);
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
    xhr.open("POST", ip);
    //xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            console.log(xhr.status);
            console.log(xhr.responseText);
        }
    };
    xhr.send(JSON.stringify(data));
}

function update() {
    // if (appState == "OFF")
    //     return;
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", ip, false); // false for synchronous request
    xmlHttp.send(null);
    console.log(xmlHttp.responseText);
    const obj = JSON.parse(xmlHttp.responseText);

    var f = false;
    var curLocation = obj[0];
    var cardsHTML = "";
    var nearbyHTML = "";
    for (let i = 1; i < obj.length; i++) {
        const location = obj[i];
        if (Math.abs(location.x - curLocation.x) < 10 && Math.abs(location.y - curLocation.y) < 10 && Math.abs(location.yaw - curLocation.yaw) < 15) {
            f = true;
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
        nearbyHTML += '<div>' + location.location_name + '</div>'
    }
    cards.innerHTML = cardsHTML;
    nearby_list.innerHTML = nearbyHTML;
    reached = f;
}

const interval = setInterval(() => {
    update();
}, 1000);