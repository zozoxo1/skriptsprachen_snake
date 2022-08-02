export default class ScoreHandler {

    async getScore() {
        let score = await fetch(API_ENDPOINTS["GET_SCORE"], {method: "GET"})
            .then(response => response.json())
            .then(data => {
                if(data["score"] != undefined) {
                    return data["score"];
                }
            })
            .catch(error => {
                console.log(error);
                return -2;
            });

        return score;
    }

}