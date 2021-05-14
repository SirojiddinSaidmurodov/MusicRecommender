axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
const songsUrl = 'http://127.0.0.1:8000/songsjson/'
let savedSongs = new Vue({
    delimiters: ["[[", "]]"],
    el: '#saved',
    data: {
        recommendations: undefined,
        songs: undefined,
        playing: null,
        oldId: null
    },
    methods: {
        refresh() {
            axios.get(songsUrl).then(response => {
                if (response.data !== undefined) {
                    this.songs = response.data.tracks;
                    console.log(this.songs)
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
        },
        toggleDark(audio) {
            this.toggleCom(audio, '-dark')
        },
        toggle(audio) {
            this.toggleCom(audio, '')
        },
        toggleCom(audio, suffix) {
            if (this.oldId) {
                if (this.oldId !== audio.id) {
                    this.playing.pause()
                    document.getElementById(this.oldId).src = '/static/play' + suffix + '.png'
                    document.getElementById(audio.id).src = '/static/pause' + suffix + '.png'
                    this.playing = new Audio(audio.preview_url)
                    this.playing.play();
                    this.oldId = audio.id
                } else {
                    if (this.playing.paused) {
                        this.playing.play();
                        document.getElementById(audio.id).src = '/static/pause' + suffix + '.png'
                    } else {
                        this.playing.pause();
                        document.getElementById(audio.id).src = '/static/play' + suffix + '.png'
                    }

                }
            } else {
                this.playing = new Audio(audio.preview_url)
                this.playing.play();
                this.oldId = audio.id
                document.getElementById(audio.id).src = '/static/pause' + suffix + '.png'
            }
        }
    },
    created() {
        this.refresh()
    }
});
