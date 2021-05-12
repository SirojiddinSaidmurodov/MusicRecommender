axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
const songsUrl = 'http://127.0.0.1:8000/songsjson/'
let savedSongs = new Vue({
    delimiters: ["[[", "]]"],
    el: '#saved',
    data: {
        message: 'Hello ',
        songs: []
    },
    methods: {
        refresh() {
            axios.get(songsUrl).then(response => {
                this.songs = response.data;
                console.log(response.data)
            })
        },
        dislike(song) {
            axios.delete('http://127.0.0.1:8000/songs/' + song).then(response => {
                this.refresh()
            })
        }
    },
    created() {
        this.refresh()
    }
});
