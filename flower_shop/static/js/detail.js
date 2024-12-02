var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        host:host,
        username: getCookie('username'),
        sku_id: sku_id,
        category_id:category_id,
        sku_price: sku_price,
        sku_mprice:sku_mprice,
        amount_price: sku_price,
        amount_mprice: sku_mprice,

        tab_content: {
            detail: true,
            comment: false,
            problem: false,
            service: false
        },
        deliverys:{
            comon: true,
            special: false
        },
        imgUrlList:JSON.parse(JSON.stringify(imgUrlList)),
        mainImgUrl: JSON.parse(JSON.stringify(imgUrlList))[0],
        imgActiveIndex: 0, // 当前移动图片的索引值
        histories: [],
        comments: [],
        score_classes: {
            1: 'stars_one',
            2: 'stars_two',
            3: 'stars_three',
            4: 'stars_four',
            5: 'stars_five',
        },
    },
    mounted(){
        get_carts()
        // 获取商品评价信息
        this.get_goods_comment();
        this.detail_visit();// 保存用户浏览记录
        this.save_browse_histories();
        this.browse_histories()
        //记录商品详情的访问量
    },
    watch: {
        deliverys:{
            handler(newValue){
                if(newValue['special']){
                    this.amount_price=(parseFloat(this.sku_price)+60).toString()+'.00'
                    this.amount_mprice=(parseFloat(this.sku_mprice)+60).toString()+'.00'
                } else {
                    this.amount_price=this.sku_price
                    this.amount_mprice=this.sku_mprice
                }
            },
            immediate: true
        }
    },
    methods: {
        // 控制页面标签页展示
        on_tab_content(name){
            this.tab_content = {
                detail: false,
                comment: false,
                problem: false,
                service: false
            };
            this.tab_content[name] = true;
        },
        change_delivery(name){
            this.deliverys={comon: false, special: false};
            this.deliverys[name]=true;
        },
        changeImg(item, index) {
            this.mainImgUrl = item
            this.imgActiveIndex = index
        },
        // 保存用户浏览记录
        save_browse_histories(){
            if (this.sku_id) {
                var url = '/browse_histories/';
                axios.post(url, {
                    'sku_id': this.sku_id
                }, {
                    headers: {'X-CSRFToken': getCookie('csrftoken')},
                    responseType: 'json'
                }).then(response => {
                    if (response.data.code === '0'){
                        console.log(response.data);
                    }else {
                        console.log(response.data);
                    }
                }).catch(error => {
                    console.log(error.response);
                });
            }
        },
        // 请求用户浏览记录
        browse_histories(){
            let url = '/browse_histories/';
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    this.histories = response.data.skus;
                    for(let i=0; i<this.histories.length; i++){
                        this.histories[i].url = '/detail/' + this.histories[i].id + '/';
                    }
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
        // 记录商品详情的访问量
        detail_visit(){
            if (this.category_id) {
                var url = '/detail/visit/' + this.category_id + '/';
                axios.post(url, {}, {
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.code === '0'){
                        console.log(response.data);
                    }else {
                        alert(response.data.errmsg);
                    }
                    })
                    .catch(error => {
                        console.log(error.response);
                    });
            }
        },
        comment_order(){
            var url = '/carts/';
            axios.post(url, {
                sku_id: parseInt(this.sku_id),
                count:1,
            }, {
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                responseType: 'json',
                withCredentials: true
            })
                .then(response => {
                    if (response.data.code == '0') {
                        location.href = '/carts/';
                    } else { // 参数错误
                        alert(response.data.errmsg);
                    }
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
        // 加入购物车
        add_cart(){
            // alert('点击成功');
            var url = '/carts/';
            axios.post(url, {
                sku_id: parseInt(this.sku_id),
                count:1,
            }, {
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                responseType: 'json',
                withCredentials: true
            })
                .then(response => {
                    if (response.data.code == '0') {
                        alert('添加购物车成功');
                        get_carts()
                    } else { // 参数错误
                        alert(response.data.errmsg);
                    }
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
        // 获取商品评价信息
        get_goods_comment(){
            console.log("函数调用成功",this.sku_id)
            var url = '/comment/' + this.sku_id + '/';
            axios.get(url, {
                responseType: 'json'
            }).then(response => {
                this.comments = response.data.goods_comment_list;
                for (var i = 0;i<this.comments.length;i++){
                    this.comments[i].score_class = this.score_classes[this.comments[i].score];
                }
            }).catch(error => {
                console.log(error.response);
                })
        },
    }
});
