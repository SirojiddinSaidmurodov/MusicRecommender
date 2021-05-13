axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
const songsUrl = 'http://127.0.0.1:8000/songsjson/'
let savedSongs = new Vue({
    delimiters: ["[[", "]]"],
    el: '#saved',
    data: {
        recommendations: undefined,
        songs: undefined
    },
    methods: {
        refresh() {
            axios.get(songsUrl).then(response => {
                if (response.data !== undefined) {
                    this.songs = response.data.tracks;
                } else {
                    this.songs = []
                }
                axios.get('http://127.0.0.1:8000/recommendation/').then(
                    response => {
                        if (response.data !== undefined) {
                            this.recommendations = response.data.tracks
                        } else {
                            this.recommendations = []
                        }
                    }
                )
            })

        },
        dislike(song) {
            axios.delete('http://127.0.0.1:8000/songs/' + song).then(response => {
                this.refresh()
            })
        },
        like(song) {
            axios.post('http://127.0.0.1:8000/songs/' + song).then(respone => {
                this.refresh()
            })
        }
    },
    created() {
        this.refresh()
    }
});
