var vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'], // 修改vue模板符号，防止与django冲突
    data: {
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        page: 1, // 当前页数
        page_size: 6, // 每页数量
        count: 0,  // 总数量
        skus: [], // 数据
        query: '',  // 查询关键字
        cart_total_count: 0, // 购物车总数量
        cart: [], // 购物车数据
        searchkey:'',
        sku_count: 1,
    },
    computed: {
        total_page: function(){  // 总页数
            return Math.ceil(this.count/this.page_size);
        },
        next: function(){  // 下一页
            if (this.page >= this.total_page) {
                return 0;
            } else {
                return this.page + 1;
            }
        },
        previous: function(){  // 上一页
            if (this.page <= 0 ) {
                return 0;
            } else {
                return this.page - 1;
            }
        },
        page_nums:function(){//页码
            var nums = [];
            if (this,this.total_page<=5){
                for (var i=1; i<=this.total_page; i++){
                    nums.push(i);
                }
            } else if(this.page <= 3){
                nums = [1, 2, 3, 4, 5];
            } else if(this.total_page - this.page <= 2){
                for (var i=this.total_page; i>this.total_page-5; i--) {
                    nums.push(i);
                }
            }else{
                for (var i=this.page-2; i<this.page+3; i++){
                    nums.push(i);
                }
            }
            return nums;
        },
    },
    mounted: function(){
        // this.query = this.get_query_string('q');
        // this.get_search_result();
        this.get_carts();
    },
    methods: {
        // 退出登录按钮
        // logoutfunc: function () {
        //     var url = this.host + '/logout/';
        //     axios.delete(url, {
        //         responseType: 'json',
        //         withCredentials:true,
        //     })
        //         .then(response => {
        //             location.href = 'login.fastdfs';
        //         })
        //         .catch(error => {
        //             console.log(error.response);
        //         })
        // },
        // 获取url路径参数
        // get_query_string: function(name){
        //     var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
        //     var r = window.location.search.substr(1).match(reg);
        //     if (r != null) {
        //         return decodeURI(r[2]);
        //     }
        //     return null;
        // },
        // 请求查询结果
        // get_search_result: function(){
        //     var url = '/search/'
        //     axios.get(url, {
        //             params: {
        //                 q: this.query,
        //                 page: this.page,
        //                 page_size: this.page_size,
        //             },
        //             responseType: 'json',
        //             withCredentials:true,
        //         })
        //         .then(response => {
        //             this.skus = [];
        //             // this.count = response.data.count;
        //             this.count = 0
        //             var results = response.data;
        //             console.log(results)
        //             // for(var i=0; i< results.length; i++){
        //             //     var sku = results[i];
        //             //     sku.url = '/goods/' + sku.id + ".fastdfs";
        //             //     this.searchkey = sku.searchkey
        //             //     this.skus.push(sku);
        //             //     this.page_size = sku.page_size;
        //             //     this.count += sku.count
        //             // }
        //         })
        //         .catch(error => {
        //             console.log(error);
        //         })
        // },
        // 点击页数
        on_page: function(num){
            if (num != this.page && num <= this.page_size){
                this.page = num;
                this.get_search_result();
            }
        },
        add_cart(i){
            var url = '/carts/';
            axios.post(url, {
                sku_id: parseInt(i),
                count: this.sku_count
            }, {
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                responseType: 'json',
                withCredentials: true
            })
                .then(response => {
                    if (response.data.code == '0') {
                        console.log(sku_id);
                        alert('添加购物车成功');
                        this.cart_total_count += this.sku_count;
                    } else { // 参数错误
                        alert(response.data.errmsg);
                        console.log(sku_id);
                    }
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
        // 获取购物车数据
        get_carts: function(){
            var url = this.host + '/carts/simple/';
            axios.get(url, {
                responseType: 'json',
            })
                .then(response => {
                    this.carts = response.data.cart_skus;
                    this.cart_total_count = 0;
                    for (var i = 0; i < this.carts.length; i++) {
                        if (this.carts[i].name.length > 25) {
                            this.carts[i].name = this.carts[i].name.substring(0, 25) + '...';
                        }
                        this.cart_total_count += this.carts[i].count;
                    }
                })
                .catch(error => {
                    console.log(error.response);
                })

        }
    }
});