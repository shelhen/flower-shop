let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        host:host,
        username: getCookie('username'),
        hour:'',
        minute:'',
        second:'',
    },
    mounted(){
        get_carts()
        this.countDown();
    },
    methods: {
        countDown(){
            let t = setInterval(() => {
                let yy = new Date().getFullYear();
                let mm = new Date().getMonth() + 1;
                let dd = new Date().getDate();
                let hh = new Date().getHours();//时
                var inputTime = +new Date(yy+'-'+mm+'-'+dd+' '+(hh+1)+':00:00'); // 返回的是用户输入时间总的毫秒数
                var nowTime = +new Date(); // 返回的是当前时间总的毫秒数
                var times = (inputTime - nowTime) / 1000; // times是剩余时间总的秒数
                var h = parseInt(times / 60 / 60 % 24); //时
		        h = h < 10 ? '0' + h : h;
		        this.hour= h; // 把剩余的小时给 小时黑色盒子
		        var m = parseInt(times / 60 % 60); // 分
		        m = m < 10 ? '0' + m : m;
		        this.minute = m;
		        var s = parseInt(times % 60); // 当前的秒
		        s = s < 10 ? '0' + s : s;
		        this.second = s;
            }, 1000)
        },
    }
});