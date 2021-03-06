axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
const songsUrl = '/search/'
let searchApp = new Vue({
    delimiters: ["[[", "]]"],
    el: '#searchApp',
    data: {
        query: '',
        result: [],
        loading: false
    },
    methods: {
        async get_result() {
            if (this.query !== '') {
                this.loading = true;
                this.result = [];
                axios.get(songsUrl + this.query).then(response => {
                    if (typeof response.data.tracks.total === undefined) {
                        this.result = []
                    } else {
                        if (response.data.tracks.total === 0) {
                            this.result = []
                        } else {
                            console.log(response)
                            this.result = response.data.tracks.items
                            this.result.forEach(item => {
                                let artists = item['artists'].map(artist => artist.name);
                                item['artistStr'] = artists.join(', ')
                            })
                        }
                    }
                    this.loading = false;
                })
            } else {
                this.result = []
                this.loading = false
            }
        },
        like(song) {
            axios.post('/songs/' + song)
            this.result.forEach(item => {
                if (item['id'] === song) {
                    item['liked'] = true
                }
            })
        },
        dislike(song) {
            axios.delete('/songs/' + song)
            this.result.forEach(item => {
                if (item['id'] === song) {
                    item['liked'] = false
                }
            })
        },
        toggle(audio) {
            if (this.oldId) {
                if (this.oldId !== audio.id) {
                    this.playing.pause()
                    document.getElementById(this.oldId).src = '/static/play.png'
                    document.getElementById(audio.id).src = '/static/pause.png'
                    this.playing = new Audio(audio.preview_url)
                    this.playing.play();
                    this.oldId = audio.id
                } else {
                    if (this.playing.paused) {
                        this.playing.play();
                        document.getElementById(audio.id).src = '/static/pause.png'
                    } else {
                        this.playing.pause();
                        document.getElementById(audio.id).src = '/static/play.png'
                    }

                }
            } else {
                this.playing = new Audio(audio.preview_url)
                this.playing.play();
                this.oldId = audio.id
                document.getElementById(audio.id).src = '/static/pause.png'
            }
        }

    }
});
