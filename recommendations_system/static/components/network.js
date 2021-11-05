function getUserInfo(userId) {
    return new Promise(function (resolve, reject) {
        const xhr = new XMLHttpRequest();
        const url = "getUserInfo/?user_id=" + userId;
        const params = "user_id=" + userId;
        xhr.open("GET", url);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.onload = function () {

            if (this.status >= 200 && this.status < 300) {
                let response = JSON.parse(xhr.response);
                resolve({history: response.history, recommendations: response.recommendations});
            } else {
                reject({
                    status: this.status,
                    statusText: xhr.statusText
                });
            }
        };

        xhr.send(params)
    });
}

