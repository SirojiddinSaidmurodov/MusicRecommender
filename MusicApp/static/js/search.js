axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
const songsUrl = 'http://127.0.0.1:8000/search/'
let searchApp = new Vue({
    delimiters: ["[[", "]]"],
    el: '#searchApp',
    data: {
        query: '',
        result: []
    },
    methods: {
        get_result() {
            if (this.query !== '') {
                axios.get(songsUrl + this.query).then(response => {
                    if (response.data.total === 0) {
                        this.result = []
                    } else {
                        this.result = response.data.tracks.items
                    }
                })
            } else {
                this.result = []
            }
        },
        like(song) {
            axios.post('http://127.0.0.1:8000/like/' + song)
        }
    }
});
