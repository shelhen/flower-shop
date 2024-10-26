let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        host:host,
        username: getCookie('username'),
        news: [],
    },
    mounted(){
        this.get_news();
    },
    methods: {
    	// 获取热销商品数据
        get_news(){
            let url = "/rank/"
            axios.get(url,{
                responseType: 'json'
            }).then(response => {
                this.news = response.data.hot_contents;
                for(let i=0; i<this.news.length; i++){
                    this.news[i].url = '/flowery/' + this.news[i].id + '/';
                }
            }).catch(error =>{
                console.log(error.response)
            })
        },
    }
});