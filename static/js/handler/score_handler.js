export default class ScoreHandler {

    async getScore() {
        let score = await fetch(API_ENDPOINTS["GET_CURRENT_PLAYER"], {method: "GET"})
            .then(response => response.json())
            .then(data => {
                if(data["success"]) {
                    return data["score"];
                } else {
                    return -1;
                }
            })
            .catch(error => {
                console.log(error);
                return -2;
            });

        return score;
    }

}