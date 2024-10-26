let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        username:getCookie('username'),
        old_pwd: '',
        new_pwd: '',
        new_cpwd: '',
        error_opwd:false,
        error_pwd: false,
        error_cpwd: false,
        origin_password_errmsg:'',
        change_password_errmsg:'',
        histories: [],
    },
    mounted() {
        // 请求浏览历史记录
        this.browse_histories();
    },
    methods: {
        // 请求浏览历史记录
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
                    // console.log(this.histories)
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
        // 检查旧密码
        check_opwd(){
            var re = /^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.old_pwd)) {
                this.error_opwd = false;
            } else {
                this.error_opwd = true;
            }
        },
        // 检查新密码
        check_pwd(){
            var re = /^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.new_pwd)) {
                this.error_pwd = false;
            } else {
                this.error_pwd = true;
            }
        },
        // 检查确认密码
        check_cpwd() {
            if (this.new_pwd != this.new_cpwd) {
                this.error_cpwd = true;
            } else {
                this.error_cpwd = false;
            }
        },
        // 取消保存密码
        cancel_pwd(){
            this.old_pwd='';
            this.new_pwd='';
            this.new_cpwd='';
        },
        //保存密码更改
        save_pwd(){
            //检查密码格式，及是否重复
            this.check_opwd();
            this.check_pwd();
            this.check_cpwd();
            if(this.error_opwd==false||this.error_pwd==false||this.error_cpwd==false){
                let url='/password/';
                axios.put(url,{
                    old_pwd:this.old_pwd,
                    new_pwd:this.new_pwd,
                    new_cpwd:this.new_cpwd,
                },{
                    headers:{
                        'X-CSRFToken':getCookie('csrftoken')
                    },
                    responseType: 'json'
                    })
                    .then(response => {
                        //改
                        if (response.data.code == '0') {
                            location.href = '/login/?next=/info/';
                        }else {
                            console.log(response);
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    });
            }
        },
    }
});