let vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法
    delimiters: ['[[', ']]'],
    data: {
        currentIndex: 0,
        list: [{
            id: 1,
            content:"账号密码",
        }, {
            id: 2,
            content:"手机短信",
        }],
        username: '',
        password: '',
        mobile:'',
        image_code:'',
        image_code_url: '',
        uuid: '',
        sms_code_tip: '短信验证码',
        send_flag: false, 
        sms_code: '',

        //v-show
        error_username: false,
        error_password: false,
        error_mobile:false,
        error_image_code: false,
        error_sms_code: false,
        remembered: false,
        error_mobile_message: '',
        error_image_code_message: '',
        error_sms_code_message: '',
    },
    mounted() { // 页面加载完会被调用的
        // 生成图形验证码
        this.generate_image_code();
    },
    methods: {
        change(index){
            this.currentIndex = index;
        },
        // 发送短信验证码
        send_sms_code() {
            // 避免恶意用户频繁的点击获取短信验证码的标签
            if (this.send_flag == true) { // 先判断是否有人正在上厕所
                return; // 有人正在上厕所，退回去
            }
            this.send_flag = true; // 如果可以进入到厕所，立即关门
            // 校验数据：mobile，image_code
            this.check_mobile();
            this.check_image_code();
            if (this.error_mobile == true || this.error_image_code == true) {
                this.send_flag = false;
                return;
            }
            let url = '/sms_codes/' + this.mobile + '/?image_code=' + this.image_code + '&uuid=' + this.uuid;
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    if (response.data.code == '0') {
                        // 展示倒计时60秒效果
                        let num = 60;
                        let t = setInterval(() => {
                            if (num == 1) { // 倒计时即将结束
                                clearInterval(t); // 停止回调函数的执行
                                this.sms_code_tip = '短信验证码'; // 还原sms_code_tip的提示文字
                                this.generate_image_code(); // 重新生成图形验证码
                                this.send_flag = false;
                            } else { // 正在倒计时
                                num -= 1; // num = num - 1;
                                this.sms_code_tip = num + '秒';
                            }
                        }, 1000)
                    } else {
                        if (response.data.code == '4001') { // 图形验证码错误
                            this.error_image_code_message = response.data.errmsg;
                            this.error_image_code = true;
                        } else { // 4002 短信验证码错误
                            this.error_sms_code_message = response.data.errmsg;
                            this.error_sms_code = true;
                            this.currentIndex=1
                        }
                        this.send_flag = false;
                    }
                })
                .catch(error => {
                    console.log(error.response);
                    this.send_flag = false;
                })
        },
        // 生成图形验证码的方法：封装的思想，代码复用
        generate_image_code() {
            this.uuid = generateUUID();
            this.image_code_url = '/image_codes/' + this.uuid + '/';
        },
        // 检查账号
        check_username(){
        	let re = /^[a-zA-Z0-9_-]{5,20}$/;
			if (re.test(this.username)) {
                this.error_username = false;
            } else {
                this.error_username = true;
            }
        },
		// 检查密码格式
        check_password(){
        	let re = /^[0-9A-Za-z]{8,20}$/;
			if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
            }
        },
        //检查手机号格式
        check_mobile() {
            let re = /^1[3-9]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile_message = '您输入的手机号格式不正确';
                this.error_mobile = true;
            }
        },// 校验图形验证码吗
        check_image_code() {
            if (this.image_code.length != 4) {
                this.error_image_code_message = '请输入图形验证码';
                this.error_image_code = true;
            } else {
                this.error_image_code = false;
            }
        },
        // 校验短信验证码
        check_sms_code(){
            if(this.sms_code.length != 6){
                this.error_sms_code_message = '请填写短信验证码';
                this.error_sms_code = true;
            } else {
                this.error_sms_code = false;
            }
        },
        // 表单提交
        on_submit1(){
            this.check_username();
            this.check_password();
            if (this.error_username == true || this.error_password == true) {
                // 不满足登录条件：禁用表单
                window.event.returnValue = false
            }
        },
        on_submit2(){
            this.check_mobile();
            this.check_sms_code();
            if (this.error_mobile == true || this.error_sms_code == true) {
                // 不满足登录条件：禁用表单
				window.event.returnValue = false}
        },
    }
});