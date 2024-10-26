let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        host:host,
        username: getCookie('username'),
        ser_flag:false,
        statu_id:statu_id,
    },
    mounted() {
        this.changeCate();
    },
    methods: {
        changeCate(){
            $($(".nav-items")[parseInt(this.statu_id)]).addClass('activeTab')
        },
        oper_btn_click(order_id, status){
            if (status == '1') {
                // 待支付
                var url = '/payment/' + order_id + '/';
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.code == '0') {
                            location.href = response.data.alipay_url;
                        } else {
                            alert(response.data.errmsg);
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    });
            } else if(status == '3') {
                // 待收货,发送请求，使其收货
                var url2 = '/confirm/' + order_id +"/";
                axios.put(url2, {
                    responseType: 'json',
                    headers: {'X-CSRFToken':getCookie('csrftoken')},
                }).then(response => {
                     alert(response.data.errmsg);
                     location.href = '/orders/3/1/';
                }).catch(error => {
                    console.log(error.response);
                });

            } else if (status == '5') {
                // 待评价
                location.href = '/orders/comment/?order_id=' + order_id;
            } else {
                // 其他：待收货。。。
                location.href = '/orders/0/1/';
            }
        },
        withdraw_btn(order_id){
            location.href = '/orders/drawback/?order_id=' + order_id;
        },
    }
});