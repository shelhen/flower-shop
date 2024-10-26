let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        host:host,
        username: getCookie('username'),
        category_id: category_id,
        sku_count: 1,
        hot_skus: [],
    },
    mounted(){
        this.changeCate();
        // 获取热销商品数据
        this.get_hot_skus();
    },
    methods: {
    	// 获取热销商品数据
        get_hot_skus(){
            if (this.category_id) {
                let url = '/hot/';
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {
                        this.hot_skus = response.data.hot_skus;
                        for(let i=0; i<this.hot_skus.length; i++){
                            this.hot_skus[i].url = '/detail/' + this.hot_skus[i].id + '/';
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }
        },
        changeCate(){
            $($(".top_wrap li a")[this.category_id]).css("color", "#F06867")
        },
    }
});