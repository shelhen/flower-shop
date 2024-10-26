let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        host:host,
        username: getCookie('username'),
        order_submitting: false,  // 控制表单提交事件，当为false时，不可以进行表单提交
        pay_method: 2,
        delivery:1,
        nowsite: default_address_id,  // 绑定默认地址
        total_amount:total_amount,
        freight:'0.00',
        freight2:freight,
        payment_amount: payment_amount, // 初始化支付金额
        words:$('#words').text(),
        num:0,
    },
    watch: {
        delivery:{
            handler(newValue){
                this.payment_amount=(parseFloat(this.total_amount)+parseFloat(this.freight2)*(newValue-1)).toString()+'.00'
                this.freight=parseFloat(this.freight2)*(newValue-1).toString()+'.00'
                }
            },
        words:{
            handler(newValue){
                this.num = newValue.length
            }
        },
        immediate: true
    },
    methods: {
        order_submit(){
            if (!this.nowsite) {
                alert('请补充收货地址');
                return;
            }
            if (!this.pay_method) {
                alert('请选择付款方式');
                return;
            }
            if(!this.delivery){
                alert('请选择配送方式')
                return;
            }
            // 禁用掉表单提交事件
            if(!this.order_submitting){
                axios.post('/orders/commit/',{
                    address_id: this.nowsite,
                    pay_method: parseInt(this.pay_method),
                    delivery:parseInt(this.delivery),
                    words:this.words
                },{
                    headers:{'X-CSRFToken':getCookie('csrftoken')},
                    responseType: 'json'
                }).then(response => {
                    if(response.data.code === '0'){
                        if(this.pay_method==1){
                            // 顾客选择货到付款，直接前往订单成功页面
                            location.href="/payment/paymethod/"+ response.data.order_id + '/';
                        }else{
                          let payment_url = '/payment/' + response.data.order_id + '/';
                            console.log('前往支付页面')
                            this.transfer(payment_url)
                        }
                    }else if(response.data.code === '4101') {
                        console.log('刷新页面')
                        location.href = '/login/?next=/orders/settlement/';
                    }else{
                        alert(response.data.errmsg);
                    }
                }).catch(error => {
                    this.order_submitting = false;
                    console.log(error.response);
                })
            }
        },
        transfer(url){
            // 获取支付页面url
            axios.get(url,{
                responseType: 'json'
            }).then(response =>{ //4101
                if (response.data.code == '0'){
                    location.href = response.data.alipay_url;
                }else {
                    console.log(response.data);
                    alert(response.data.errmsg);
                }
            }).catch(error => {
                console.log(error.response);
            })
        },
        change_word(e){
            $('#words').text(e.target.innerText)
            this.words = e.target.innerText
        }
    }
});





