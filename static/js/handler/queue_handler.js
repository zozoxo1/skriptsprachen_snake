export default class Queue {

    async size() {
        let queueSize = await fetch(API_ENDPOINTS["GET_QUEUE_LENGTH"], {method: "GET"})
            .then(response => response.json())
            .then(data => {
                return data["len"];
            })
            .catch(error => {
                console.log(error);
                return -1;
            });

        return queueSize;
    }

    enqueue() {
        fetch(API_ENDPOINTS["PUT_QUEUE_JOIN"], {method: "PUT"})
            .then(response => response.json())
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.log(error);
            });
    }

    dequeue() {
        fetch(API_ENDPOINTS["PUT_QUEUE_LEAVE"], {method: "PUT"})
            .then(response => response.json())
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.log(error);
            });
    }

    // Return if its the players turn
    async isNext() {
        let isNext = await fetch(API_ENDPOINTS["GET_CURRENT_PLAYER"], {method: "GET"})
            .then(response => response.json())
            .then(data => {
                return data["success"];
            })
            .catch(error => {
                console.log(error);
                return false;
            });

        return isNext;
    }

}