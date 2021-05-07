axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

let searchApp = new Vue({
    delimiters: ["[[", "]]"],
    el: '#app',
    data: {
        message: 'Hello Vue!'
    }
});
