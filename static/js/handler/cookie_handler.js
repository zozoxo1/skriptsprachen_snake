export default class CookieHandler {

    #defaultCookies = [
        ["userId", this.#generateRandomString(32)]
    ];

    constructor() {
        this.#setDefaultCookies();
    }

    #dec2hex(dec) {
        return dec.toString(16).padStart(2, "0")
    }

    #generateRandomString(len) {
        var arr = new Uint8Array((len || 40) / 2)
        window.crypto.getRandomValues(arr)
        return Array.from(arr, this.#dec2hex).join('')
    }

    getCookie(cname) {
        let name = cname + "=";
        let decodedCookie = decodeURIComponent(document.cookie);
        let ca = decodedCookie.split(';');
        
        for(let i = 0; i <ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }

        return "";
    }

    setCookie(cname, cvalue, expdays) {
        const d = new Date();
        d.setTime(d.getTime() + (expdays*24*60*60*1000));
        let expires = "expires="+ d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    }

    checkDefaultCookies() {
        this.#setDefaultCookies();
    }

    #setDefaultCookies() {
        this.#defaultCookies.forEach(element => {
            if(this.getCookie(element[0]) === "") {
                this.setCookie(element[0], element[1], 1);
            }
        });
    }

}