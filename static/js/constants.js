const API_URL = window.location.origin + "/api/";

const API_ENDPOINTS = {
    "PUT_STARTGAME": API_URL + "start",
    "PUT_PAUSEGAME": API_URL + "pause",
    "PUT_RESUMEGAME": API_URL + "pause",

    "PUT_MOVE_RIGHT": API_URL + "move/right",
    "PUT_MOVE_LEFT": API_URL + "move/left",
    "PUT_MOVE_DOWN": API_URL + "move/down",
    "PUT_MOVE_UP": API_URL + "move/up",

    "PUT_QUEUE_JOIN": API_URL + "queue/join",
    "PUT_QUEUE_LEAVE": API_URL + "queue/leave",
    "GET_QUEUE_LENGTH": API_URL + "queue/length",
    "GET_CURRENT_PLAYER": API_URL + "current_user",
}

const REDIRECT_CONTROLLER = window.location.origin + "/static/controller.html";
const REDIRECT_GAMEOVER = window.location.origin + "/static/gameover.html";
const REDIRECT_MENU = window.location.origin + "/static/index.html";