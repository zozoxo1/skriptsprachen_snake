import ControllerHandler from './handler/controller_handler.js';

const controllerHandler = new ControllerHandler();

let statusButton = null;

var canMoveRight = true;
var canMoveLeft = true;
var canMoveUp = true;
var canMoveDown = true;

var moveTimeout = 400;

function orientationEvent(event)
{
    let beta = event.beta;
    let gamma = event.gamma;

    if(gamma < -20 && canMoveLeft) {
        canMoveLeft = false;

        resetButton();
        controllerHandler.moveLeft();

        // links
        document.getElementsByClassName("inner-circle")[0].classList = ["inner-circle"];
        document.getElementsByClassName("inner-circle")[0].classList.add("inner-circle", "left");

        setTimeout(() => {
            canMoveLeft = true;  
        }, moveTimeout);
    }

    if(gamma > 20 && canMoveRight) {
        canMoveRight = false;

        resetButton();
        controllerHandler.moveRight();

        // rechts
        document.getElementsByClassName("inner-circle")[0].classList = ["inner-circle"];
        document.getElementsByClassName("inner-circle")[0].classList.add("inner-circle", "right");

        setTimeout(() => {
            canMoveRight = true;
        }, moveTimeout);
    }

    if(beta > 40 && canMoveDown) {
        canMoveDown = false;

        resetButton();
        controllerHandler.moveDown();

        // nach unten (slow)
        document.getElementsByClassName("inner-circle")[0].classList = ["inner-circle"];
        document.getElementsByClassName("inner-circle")[0].classList.add("inner-circle", "down");

        setTimeout(() => {
            canMoveDown = true;
        }, moveTimeout);
    }

    if(beta < -15 && canMoveUp) {
        canMoveUp = false;

        resetButton();
        controllerHandler.moveUp();
        // nach oben
        document.getElementsByClassName("inner-circle")[0].classList = ["inner-circle"];
        document.getElementsByClassName("inner-circle")[0].classList.add("inner-circle", "up");

        setTimeout(() => {
            canMoveUp = true;
        }, moveTimeout);
    }
}

function resetButton() {
    document.getElementsByClassName("inner-circle")[0].classList = ["inner-circle"];
}

function requestOrientationPermission(){
    if(!(statusButton.classList.contains("playing")
            || statusButton.classList.contains("paused"))) {
        window.DeviceOrientationEvent.requestPermission()
        .then(response => {
            if (response == 'granted') {
                window.addEventListener('deviceorientation', event => orientationEvent(event))
            }
        })
        .catch(console.error)
    }
}

window.addEventListener('DOMContentLoaded', () => {

    /**=======================================================================================================================
     *                                                    MODAL
     *=======================================================================================================================**/

    const modal = document.getElementById('modal');

    setTimeout(() => {
        modal.classList.remove('modal-svg-rotate');
        modal.getElementsByTagName('svg')[0].remove();

        modal.insertAdjacentHTML('afterbegin',
        '<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-lock-open" width="200" height="200" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">'
        + '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path>'
        + '<rect x="5" y="11" width="14" height="10" rx="2"></rect>'
        + '<circle cx="12" cy="16" r="1"></circle>'
        + '<path d="M8 11v-5a4 4 0 0 1 8 0"></path>'
        + '</svg>');

        modal.getElementsByTagName('h1')[0].innerHTML = "Deaktiviere die <u>Bildschirmrotation</u>.";

        setTimeout(() => {
            modal.getElementsByTagName('svg')[0].innerHTML = '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path>'
            + '<rect x="5" y="11" width="14" height="10" rx="2"></rect>'
            + '<circle cx="12" cy="16" r="1"></circle>'
            + '<path d="M8 11v-4a4 4 0 0 1 8 0v4"></path>';
        }, 800);

        setTimeout(() => {
            modal.style.display = 'none';
        }, 2500);
    }, 1900);


    /**=======================================================================================================================
     *                                                    Controller Play / Pause Button
     *=======================================================================================================================**/

    statusButton = document.getElementsByClassName("btn-game-status")[0];

    statusButton.addEventListener('click', () => {

        if(statusButton.classList.contains("playing")) {
            controllerHandler.pauseGame();
            
            window.removeEventListener('deviceorientation', orientationEvent);

            statusButton.classList.remove("playing");
            statusButton.classList.add("paused");

            statusButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-player-play" width="75" height="75" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">'
            + '<path stroke="none" d="M0 0h75v75H0z" fill="none"></path>'
            + '<path d="M7 4v16l13 -8z"></path>'
            + '</svg>';
        } else if(statusButton.classList.contains("paused")) {
            controllerHandler.resumeGame();

            window.addEventListener('deviceorientation', event => orientationEvent(event));

            statusButton.classList.remove("paused");
            statusButton.classList.add("playing");

            statusButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-player-pause" width="75" height="75" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">'
            + '<path stroke="none" d="M0 0h75v75H0z" fill="none"></path>'
            + '<rect x="6" y="5" width="4" height="14" rx="1"></rect>'
            + '<rect x="14" y="5" width="4" height="14" rx="1"></rect>'
            + '</svg>';
        } else {
            if ( window.DeviceMotionEvent && typeof window.DeviceMotionEvent.requestPermission === 'function' ) {
                requestOrientationPermission();
            }
    
            controllerHandler.startGame();

            window.addEventListener('deviceorientation', event => orientationEvent(event));

            // check if game is over or if user is not permitted to play

            statusButton.classList.add("playing");

            statusButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-player-pause" width="75" height="75" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">'
            + '<path stroke="none" d="M0 0h75v75H0z" fill="none"></path>'
            + '<rect x="6" y="5" width="4" height="14" rx="1"></rect>'
            + '<rect x="14" y="5" width="4" height="14" rx="1"></rect>'
            + '</svg>';
        }
 
     });

});