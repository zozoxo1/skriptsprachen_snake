export default class ControllerHandler {

    startGame() {
        fetch(API_ENDPOINTS["PUT_STARTGAME"], {method: "PUT"})
            .then(response => response.json())
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.log(error);
            });
    }

    pauseGame() {
        fetch(API_ENDPOINTS["PUT_PAUSEGAME"], {method: "PUT"})
            .then(response => response.json())
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.log(error);
            });
    }

    resumeGame() {
        fetch(API_ENDPOINTS["PUT_RESUMEGAME"], {method: "PUT"})
            .then(response => response.json())
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.log(error);
            });
    }

    async isGameOver() {
        let gameOver = await fetch(API_ENDPOINTS["GET_GAME_OVER"], {method: "GET"})
            .then(response => response.json())
            .then(data => {
                return data["success"];
            })
            .catch(error => {
                console.log(error);
                return False;
            });

        return gameOver;
    }

    moveRight() {
        fetch(API_ENDPOINTS["PUT_MOVE_RIGHT"], {method: "PUT"})
            .then(response => response.json())
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.log(error);
            });
    }

    moveLeft() {
        fetch(API_ENDPOINTS["PUT_MOVE_LEFT"], {method: "PUT"})
            .then(response => response.json())
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.log(error);
            });
    }

    moveDown() {
        fetch(API_ENDPOINTS["PUT_MOVE_DOWN"], {method: "PUT"})
            .then(response => response.json())
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.log(error);
            });
    }

    moveUp() {
        fetch(API_ENDPOINTS["PUT_MOVE_UP"], {method: "PUT"})
            .then(response => response.json())
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.log(error);
            });
    }

}