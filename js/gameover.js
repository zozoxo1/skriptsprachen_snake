import ScoreHandler from './handler/score_handler.js';

const scoreHandler = new ScoreHandler();

window.addEventListener('DOMContentLoaded', () => {

    const menuButton = document.getElementById('menu-buttons-menu');

    menuButton.addEventListener('click', () => {
        window.location.href = REDIRECT_MENU;
    });

    const scoreElement = document.getElementById('points');
    
    Promise.resolve(scoreHandler.getScore())
        .then(score => {
            scoreElement.innerHTML = score + " Punkt" + (score == 1 ? "" : "e") + "!";
        });

});