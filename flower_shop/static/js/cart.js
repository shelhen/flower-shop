let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        host:host,
        username: getCookie('username'),
        carts: JSON.parse(JSON.stringify(carts)),
        total_count: 0,
        total_selected_count: 0,
        total_selected_amount: 0,
        carts_tmp: [],
        // total_amount:0,
    },
    computed: {
        selected_all(){
            let selected=true;
            for(let i=0; i<this.carts.length; i++){
                if(this.carts[i].selected===false){
                    selected=false;
                    break;
                }
            }
            return selected;
        },
    },
    mounted(){
        // 初始化购物车数据并渲染界面
        this.render_carts();
        // 计算商品总数量：无论是否勾选
        this.compute_total_count();
        // 计算被勾选的商品总金额和总数量
        this.compute_total_selected_amount_count();
    },
    methods: {
        // 初始化购物车数据并渲染界面
        render_carts(){
            // 渲染界面
            for(let i=0; i<this.carts.length; i++){
                if(this.carts[i].selected==='True'){
                    this.carts[i].selected=true;
                } else {
                    this.carts[i].selected=false;
                }
            }
            // 手动记录购物车的初始值，用于更新购物车失败时还原商品数量
            this.carts_tmp = JSON.parse(JSON.stringify(carts));
        },
        // 计算商品总数量：无论是否勾选
        compute_total_count(){
            let total_count = 0;
            for(let i=0; i<this.carts.length; i++){
                total_count += parseInt(this.carts[i].count);
            }
            this.total_count = total_count;
        },
        // 计算被勾选的商品数量和总金额
        compute_total_selected_amount_count(){
            let amount = 0;
            let total_count = 0;
            for(let i=0; i<this.carts.length; i++){
                if(this.carts[i].selected) {
                    amount += parseFloat(this.carts[i].price) * parseInt(this.carts[i].count);
                    total_count += parseInt(this.carts[i].count);
                }
            }
            this.total_selected_amount = amount.toFixed(2); // for循环中不要使用toFixed的累加
            this.total_selected_count = total_count;
        },
        // 减少操作
        on_minus(index){
            if (this.carts[index].count > 1) {
                let count = this.carts[index].count - 1;
                // this.carts[index].count = count; // 本地测试
                this.update_count(index, count); // 请求服务器
            }
        },
        // 增加操作
        on_add(index){
            let count = 1;
            if (this.carts[index].count < 5) {
                count = this.carts[index].count + 1;
            } else {
                count = 5;
                alert('超过商品数量上限');
            }
            this.update_count(index, count); // 请求服务器
        },
        // 数量输入框输入操作
        on_input(index){
            let count = parseInt(this.carts[index].count);
            if (isNaN(count) || count <= 0) {
                count = 1;
            } else if (count > 5) {
                count = 5;
                alert('超过商品数量上限');
            }
            this.update_count(index, count); // 请求服务器
        },
        // 更新购物车
        update_count(index, count){
            let url = '/carts/';
            axios.put(url, {
                sku_id: this.carts[index].id,
                count:count,
                selected: this.carts[index].selected
            }, {
                headers:{
                    'X-CSRFToken':getCookie('csrftoken')
                },
                responseType: 'json',
                withCredentials: true
            })
                .then(response => {
                    if (response.data.code == '0') {
                        // this.carts[index].count = response.data.cart_sku.count; // 无法触发页面更新
                        Vue.set(this.carts, index, response.data.cart_sku); // 触发页面更新
                        // 重新计算界面的价格和数量
                        this.compute_total_selected_amount_count();
                        this.compute_total_count();
                        // 更新成功将新购物车再次临时保存
                        this.carts_tmp = this.carts;
                    } else {
                        alert(response.data.errmsg);
                        this.carts[index].count = this.carts_tmp[index].count;
                    }
                })
                .catch(error => {
                    console.log(error.response);
                    this.carts[index].count = this.carts_tmp[index].count;
                })
        },
        // 更新购物车选中数据
        update_selected(index) {
            let url = '/carts/';
            axios.put(url, {
                sku_id: this.carts[index].id,
                count: this.carts[index].count,
                selected: this.carts[index].selected
            }, {
                headers: {
                    'X-CSRFToken':getCookie('csrftoken')
                },
                responseType: 'json',
                withCredentials: true
            })
                .then(response => {
                    if (response.data.code == '0') {
                        this.carts[index].selected = response.data.cart_sku.selected;
                        // 重新计算界面的价格和数量
                        this.compute_total_selected_amount_count();
                        this.compute_total_count();
                    } else {
                        alert(response.data.errmsg);
                    }
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
        // 删除购物车数据
        on_delete(index){
            let url = '/carts/';
            axios.delete(url, {
                data: {
                    sku_id: this.carts[index].id
                },
                headers:{
                    'X-CSRFToken':getCookie('csrftoken')
                },
                responseType: 'json',
                withCredentials: true
            })
                .then(response => {
                    if (response.data.code == '0') {
                        this.carts.splice(index, 1);
                        // 重新计算界面的价格和数量
                        this.compute_total_selected_amount_count();
                        this.compute_total_count();
                    } else {
                        alert(response.data.errmsg);
                    }
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
        // 购物车全选
        on_selected_all(){
            let selected = !this.selected_all;
            let url = '/carts/selection/';
            axios.put(url, {
                selected
            }, {
                headers:{
                    'X-CSRFToken':getCookie('csrftoken')
                },
                responseType: 'json',
                withCredentials: true
            })
                .then(response => {
                    if (response.data.code == '0') {
                        for (let i=0; i<this.carts.length;i++){
                            this.carts[i].selected = selected;
                        }
                        // 重新计算界面的价格和数量
                        this.compute_total_selected_amount_count();
                        this.compute_total_count();
                    } else {
                        alert(response.data.errmsg);
                    }
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
    }
});