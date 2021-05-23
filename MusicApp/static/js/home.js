axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

const songsUrl = '/songsjson/'
let savedSongs = new Vue({
    delimiters: ["[[", "]]"],
    el: '#saved',
    data: {
        recommendations: [],
        songs: [],
        playing: null,
        oldId: null,
        loadingRec: true,
        loadSaved: true,
    },
    methods: {

        refresh() {
            this.loadingRec = true
            this.loadSaved = true
            axios.get(songsUrl).then(response => {
                if (response.status === 200) {
                    console.log(response)
                    this.songs = response.data.tracks
                    this.songs.forEach(item => {
                        let artists = item['artists'].map(artist => artist.name);
                        item['artistStr'] = artists.join(', ')
                    })
                    console.log(this.songs)
                } else {
                    this.songs = []
                }
                this.loadSaved = false

                axios.get('/recommendation/').then(
                    response => {
                        if (response.status === 200) {
                            this.recommendations = response.data.tracks

                            this.recommendations.forEach(item => {
                                let artists = item['artists'].map(artist => artist.name);
                                item['artistStr'] = artists.join(', ')
                            })

                            console.log(this.recommendations)
                        } else {
                            this.recommendations = []
                        }
                        this.loadingRec = false
                    }
                )

            })

        },
        dislike(song) {
            axios.delete('/songs/' + song).then(response => {
                this.refresh()
            })
        },
        like(song) {
            axios.post('/songs/' + song).then(respone => {
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
