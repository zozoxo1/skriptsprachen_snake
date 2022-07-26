import Queue from './handler/queue_handler.js';
import CookieHandler from './handler/cookie_handler.js';

const cookieHandler = new CookieHandler();
const queue = new Queue();

window.addEventListener('DOMContentLoaded', () => {

    /**=======================================================================================================================
     *                                                    Play Button and Queue text
     *=======================================================================================================================**/

    const playBtn = document.getElementById("menu-buttons-play");
    const queueText = document.getElementsByClassName('queue-size-text')[0];

    let queueTextInQueueInterval = null;
    let queueCheckNextInterval = null;
    let queueTextRefreshInterval = setInterval(() => {

        Promise.resolve(queue.size())
            .then(data => {
                queueText.innerHTML = data + " Spieler";
            });
        
    }, 1000);

    playBtn.addEventListener('click', () => {
        if(playBtn.classList.contains('btn-cancel')) {
            queueTextInQueueInterval == null ? undefined : clearInterval(queueTextInQueueInterval);
            queueCheckNextInterval == null ? undefined : clearInterval(queueCheckNextInterval);

            queue.dequeue();

            playBtn.classList.remove('btn-cancel');
            playBtn.innerHTML = 'Spielen';

            Promise.resolve(queue.size())
                .then(data => {
                    queueText.innerHTML = data + " Spieler";
                });

            queueTextRefreshInterval = setInterval(() => {
                Promise.resolve(queue.size())
                    .then(data => {
                        queueText.innerHTML = data + " Spieler";
                    });
            }, 1000);
        } else {
            cookieHandler.checkDefaultCookies();

            queueTextRefreshInterval == null ? undefined : clearInterval(queueTextRefreshInterval);

            queue.enqueue();

            playBtn.classList.add('btn-cancel');
            playBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-x" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">'
            + '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path>'
            + '<line x1="18" y1="6" x2="6" y2="18"></line>'
            + '<line x1="6" y1="6" x2="18" y2="18"></line>'
            + '</svg>';

            queueText.innerHTML = "In Warteschlange";

            let dots = 0;
            queueTextInQueueInterval = setInterval(() => {
                queueText.innerHTML = "In Warteschlange" + ".".repeat(dots);
                dots >= 3 ? dots = 0 : dots++;
            }, 300);

            queueCheckNextInterval = setInterval(() => {
                Promise.resolve(queue.isNext())
                    .then(next => {
                        if(next) {
                            clearInterval(queueTextInQueueInterval);
                            clearInterval(queueCheckNextInterval);
        
                            window.location.href = REDIRECT_CONTROLLER;
                        }
                    });
            }, 1000);
        }
    });

})