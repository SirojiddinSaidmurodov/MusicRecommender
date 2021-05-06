axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
const songsUrl = 'http://127.0.0.1:8000/songsjson/'
let app = new Vue({
    delimiters: ["[[", "]]"],
    el: '#saved',
    data: {
        message: 'Hello Vue!',
        songs: []
    },
    methods: {
        refresh() {
            axios.get(songsUrl).then(response => {
                this.songs = response.data;
            })
        }
    },
    created() {
        this.refresh()
    }
});
