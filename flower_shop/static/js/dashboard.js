let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        host:host,
        chart0:{
            text: '近一周用户下单情况',
            legend: ['用户下单量'],
            xcategory: dates,
            high: counts,
            highLine: [],
            lowLine:[],
            avg:[]
        },
        c1:c1,
        c2:c2,
        c3:c3
    },
    mounted(){
        this.line1();
        this.pie1();
        this.bar1();
        this.bar2();
    },
    methods: {
        send(order_id,status){
            url="/send/"+order_id+"/"+status+"/"
            axios.put(url, {
                    responseType: 'json',
                    headers: {'X-CSRFToken':getCookie('csrftoken')},
                }).then(response => {
                     alert(response.data.errmsg);
                     location.href = '/dashboard/1/';
                }).catch(error => {
                    console.log(error.response);
                });
        },
        line1(){
            var chart = echarts.init(document.getElementById('mounth_increase'));
            var colorTool = echarts.color;
            var json = {chart0:this.chart0};
            var zrUtil = echarts.util;
            zrUtil.each(json.chart0.xcategory, function(item, index){
                    json.chart0.highLine.push([{coord:[index,json.chart0.high[index]] },{coord:[index+1,json.chart0.high[index+1]]}]);
            });
            var option = {
                title: {
                    subtext: json.chart0.text
                },
                animationEasing: 'ElasticOut',
                legend: [{
                    data: json.chart0.legend[0]
                },{
                    data: json.chart0.legend[1],
                    top:15,
                }],
                calculable: true,
                xAxis: [{
                    type: 'category',
                    axisLabel:{
                        formatter:function(value){
                            var sepCount = 1;//每几个字符分隔
                            return value.replace(/(\S{1})(?=[^$])/g, "$1\n\n")
                        }},
                    boundaryGap: false,
                    data: json.chart0.xcategory
                }],
                yAxis: [{
                    type: 'value',
                    axisLabel: {
                        formatter: '{value} '
                    }
                }],
                series: [{
                    name: '注册量',
                    type: 'line',
                    data: json.chart0.high
                },{
                    // name: 'A',
                    type: 'lines',
                    coordinateSystem: 'cartesian2d',
                    zlevel: 2,
                    effect: {
                        show: true,
                        smooth: false,
                        period: 6,
                        // trailLength: 0,
                        // symbol: planePath,
                        // color:'rgba(55,155,255,0.5)',
                        symbolSize: 8
                    },
                    data: json.chart0.highLine
                }]
            };
            chart.setOption(option);

        },
        pie1(){
           var chart = echarts.init(document.getElementById('den_pie1'),null,{renderer: 'svg'});
           window.onresize = chart.resize;
           var option={
               animation: 'auto',
               animationDuration: () => 0,
               title : {},
               tooltip : {
                        trigger: 'item',
                        formatter: "{a} <br/>{b} : {c} ({d}%)"
                    },
               legend: {
                        orient: 'horizontal',
                        x:'center',
                        y:'bottom',
                        data: ['日增用户','日活用户','下单用户']
                    },
               series : [{
                            name: '访问来源',
                            type: 'pie',
                            radius : '55%',
                            center: ['50%', '45%'],
                            data:[
                                {value:this.c1, name:'日增用户'},
                                {value:this.c2, name:'日活用户'},
                                {value:this.c3, name:'下单用户'},
                            ],
                            itemStyle: {
                                emphasis: {
                                    shadowBlur: 10,
                                    shadowOffsetX: 0,
                                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                                }
                            }
                        }]
           }
           chart.setOption(option);
        },
        bar1(){
            var chart = echarts.init(document.getElementById('bar1'), null, {renderer: 'svg'});
             var data = [{
                    name: 'Flora',
                    itemStyle: {
                        color: '#da0d68'
                    },
                    children: [{
                        name: 'Black Tea',
                        value: 1,
                        itemStyle: {
                            color: '#975e6d'
                        }
                    }, {
                        name: 'Floral',
                        itemStyle: {
                            color: '#e0719c'
                        },
                        children: [{
                            name: 'Chamomile',
                            value: 1,
                            itemStyle: {
                                color: '#f99e1c'
                            }
                        }, {
                            name: 'Rose',
                            value: 1,
                            itemStyle: {
                                color: '#ef5a78'
                            }
                        }, {
                            name: 'Jasmine',
                            value: 1,
                            itemStyle: {
                                color: '#f7f1bd'
                            }
                        }]
                    }]
                }, {
                    name: 'Fruity',
                    itemStyle: {
                        color: '#da1d23'
                    },
                    children: [{
                        name: 'Berry',
                        itemStyle: {
                            color: '#dd4c51'
                        },
                        children: [{
                            name: 'Blackberry',
                            value: 1,
                            itemStyle: {
                                color: '#3e0317'
                            }
                        }, {
                            name: 'Raspberry',
                            value: 1,
                            itemStyle: {
                                color: '#e62969'
                            }
                        }, {
                            name: 'Blueberry',
                            value: 1,
                            itemStyle: {
                                color: '#6569b0'
                            }
                        }, {
                            name: 'Strawberry',
                            value: 1,
                            itemStyle: {
                                color: '#ef2d36'
                            }
                        }]
                    }, {
                        name: 'Dried Fruit',
                        itemStyle: {
                            color: '#c94a44'
                        },
                        children: [{
                            name: 'Raisin',
                            value: 1,
                            itemStyle: {
                                color: '#b53b54'
                            }
                        }, {
                            name: 'Prune',
                            value: 1,
                            itemStyle: {
                                color: '#a5446f'
                            }
                        }]
                    }, {
                        name: 'Other Fruit',
                        itemStyle: {
                            color: '#dd4c51'
                        },
                        children: [{
                            name: 'Coconut',
                            value: 1,
                            itemStyle: {
                                color: '#f2684b'
                            }
                        }, {
                            name: 'Cherry',
                            value: 1,
                            itemStyle: {
                                color: '#e73451'
                            }
                        }, {
                            name: 'Pomegranate',
                            value: 1,
                            itemStyle: {
                                color: '#e65656'
                            }
                        }, {
                            name: 'Pineapple',
                            value: 1,
                            itemStyle: {
                                color: '#f89a1c'
                            }
                        }, {
                            name: 'Grape',
                            value: 1,
                            itemStyle: {
                                color: '#aeb92c'
                            }
                        }, {
                            name: 'Apple',
                            value: 1,
                            itemStyle: {
                                color: '#4eb849'
                            }
                        }, {
                            name: 'Peach',
                            value: 1,
                            itemStyle: {
                                color: '#f68a5c'
                            }
                        }, {
                            name: 'Pear',
                            value: 1,
                            itemStyle: {
                                color: '#baa635'
                            }
                        }]
                    }, {
                        name: 'Citrus Fruit',
                        itemStyle: {
                            color: '#f7a128'
                        },
                        children: [{
                            name: 'Grapefruit',
                            value: 1,
                            itemStyle: {
                                color: '#f26355'
                            }
                        }, {
                            name: 'Orange',
                            value: 1,
                            itemStyle: {
                                color: '#e2631e'
                            }
                        }, {
                            name: 'Lemon',
                            value: 1,
                            itemStyle: {
                                color: '#fde404'
                            }
                        }, {
                            name: 'Lime',
                            value: 1,
                            itemStyle: {
                                color: '#7eb138'
                            }
                        }]
                    }]
                }, {
                    name: 'Sour/\nFermented',
                    itemStyle: {
                        color: '#ebb40f'
                    },
                    children: [{
                        name: 'Sour',
                        itemStyle: {
                            color: '#e1c315'
                        },
                        children: [{
                            name: 'Sour Aromatics',
                            value: 1,
                            itemStyle: {
                                color: '#9ea718'
                            }
                        }, {
                            name: 'Acetic Acid',
                            value: 1,
                            itemStyle: {
                                color: '#94a76f'
                            }
                        }, {
                            name: 'Butyric Acid',
                            value: 1,
                            itemStyle: {
                                color: '#d0b24f'
                            }
                        }, {
                            name: 'Isovaleric Acid',
                            value: 1,
                            itemStyle: {
                                color: '#8eb646'
                            }
                        }, {
                            name: 'Citric Acid',
                            value: 1,
                            itemStyle: {
                                color: '#faef07'
                            }
                        }, {
                            name: 'Malic Acid',
                            value: 1,
                            itemStyle: {
                                color: '#c1ba07'
                            }
                        }]
                    }, {
                        name: 'Alcohol/\nFremented',
                        itemStyle: {
                            color: '#b09733'
                        },
                        children: [{
                            name: 'Winey',
                            value: 1,
                            itemStyle: {
                                color: '#8f1c53'
                            }
                        }, {
                            name: 'Whiskey',
                            value: 1,
                            itemStyle: {
                                color: '#b34039'
                            }
                        }, {
                            name: 'Fremented',
                            value: 1,
                            itemStyle: {
                                color: '#ba9232'
                            }
                        }, {
                            name: 'Overripe',
                            value: 1,
                            itemStyle: {
                                color: '#8b6439'
                            }
                        }]
                    }]
                }, {
                    name: 'Green/\nVegetative',
                    itemStyle: {
                        color: '#187a2f'
                    },
                    children: [{
                        name: 'Olive Oil',
                        value: 1,
                        itemStyle: {
                            color: '#a2b029'
                        }
                    }, {
                        name: 'Raw',
                        value: 1,
                        itemStyle: {
                            color: '#718933'
                        }
                    }, {
                        name: 'Green/\nVegetative',
                        itemStyle: {
                            color: '#3aa255'
                        },
                        children: [{
                            name: 'Under-ripe',
                            value: 1,
                            itemStyle: {
                                color: '#a2bb2b'
                            }
                        }, {
                            name: 'Peapod',
                            value: 1,
                            itemStyle: {
                                color: '#62aa3c'
                            }
                        }, {
                            name: 'Fresh',
                            value: 1,
                            itemStyle: {
                                color: '#03a653'
                            }
                        }, {
                            name: 'Dark Green',
                            value: 1,
                            itemStyle: {
                                color: '#038549'
                            }
                        }, {
                            name: 'Vegetative',
                            value: 1,
                            itemStyle: {
                                color: '#28b44b'
                            }
                        }, {
                            name: 'Hay-like',
                            value: 1,
                            itemStyle: {
                                color: '#a3a830'
                            }
                        }, {
                            name: 'Herb-like',
                            value: 1,
                            itemStyle: {
                                color: '#7ac141'
                            }
                        }]
                    }, {
                        name: 'Beany',
                        value: 1,
                        itemStyle: {
                            color: '#5e9a80'
                        }
                    }]
                }, {
                    name: 'Other',
                    itemStyle: {
                        color: '#0aa3b5'
                    },
                    children: [{
                        name: 'Papery/Musty',
                        itemStyle: {
                            color: '#9db2b7'
                        },
                        children: [{
                            name: 'Stale',
                            value: 1,
                            itemStyle: {
                                color: '#8b8c90'
                            }
                        }, {
                            name: 'Cardboard',
                            value: 1,
                            itemStyle: {
                                color: '#beb276'
                            }
                        }, {
                            name: 'Papery',
                            value: 1,
                            itemStyle: {
                                color: '#fefef4'
                            }
                        }, {
                            name: 'Woody',
                            value: 1,
                            itemStyle: {
                                color: '#744e03'
                            }
                        }, {
                            name: 'Moldy/Damp',
                            value: 1,
                            itemStyle: {
                                color: '#a3a36f'
                            }
                        }, {
                            name: 'Musty/Dusty',
                            value: 1,
                            itemStyle: {
                                color: '#c9b583'
                            }
                        }, {
                            name: 'Musty/Earthy',
                            value: 1,
                            itemStyle: {
                                color: '#978847'
                            }
                        }, {
                            name: 'Animalic',
                            value: 1,
                            itemStyle: {
                                color: '#9d977f'
                            }
                        }, {
                            name: 'Meaty Brothy',
                            value: 1,
                            itemStyle: {
                                color: '#cc7b6a'
                            }
                        }, {
                            name: 'Phenolic',
                            value: 1,
                            itemStyle: {
                                color: '#db646a'
                            }
                        }]
                    }, {
                        name: 'Chemical',
                        itemStyle: {
                            color: '#76c0cb'
                        },
                        children: [{
                            name: 'Bitter',
                            value: 1,
                            itemStyle: {
                                color: '#80a89d'
                            }
                        }, {
                            name: 'Salty',
                            value: 1,
                            itemStyle: {
                                color: '#def2fd'
                            }
                        }, {
                            name: 'Medicinal',
                            value: 1,
                            itemStyle: {
                                color: '#7a9bae'
                            }
                        }, {
                            name: 'Petroleum',
                            value: 1,
                            itemStyle: {
                                color: '#039fb8'
                            }
                        }, {
                            name: 'Skunky',
                            value: 1,
                            itemStyle: {
                                color: '#5e777b'
                            }
                        }, {
                            name: 'Rubber',
                            value: 1,
                            itemStyle: {
                                color: '#120c0c'
                            }
                        }]
                    }]
                }, {
                    name: 'Roasted',
                    itemStyle: {
                        color: '#c94930'
                    },
                    children: [{
                        name: 'Pipe Tobacco',
                        value: 1,
                        itemStyle: {
                            color: '#caa465'
                        }
                    }, {
                        name: 'Tobacco',
                        value: 1,
                        itemStyle: {
                            color: '#dfbd7e'
                        }
                    }, {
                        name: 'Burnt',
                        itemStyle: {
                            color: '#be8663'
                        },
                        children: [{
                            name: 'Acrid',
                            value: 1,
                            itemStyle: {
                                color: '#b9a449'
                            }
                        }, {
                            name: 'Ashy',
                            value: 1,
                            itemStyle: {
                                color: '#899893'
                            }
                        }, {
                            name: 'Smoky',
                            value: 1,
                            itemStyle: {
                                color: '#a1743b'
                            }
                        }, {
                            name: 'Brown, Roast',
                            value: 1,
                            itemStyle: {
                                color: '#894810'
                            }
                        }]
                    }, {
                        name: 'Cereal',
                        itemStyle: {
                            color: '#ddaf61'
                        },
                        children: [{
                            name: 'Grain',
                            value: 1,
                            itemStyle: {
                                color: '#b7906f'
                            }
                        }, {
                            name: 'Malt',
                            value: 1,
                            itemStyle: {
                                color: '#eb9d5f'
                            }
                        }]
                    }]
                }, {
                    name: 'Spices',
                    itemStyle: {
                        color: '#ad213e'
                    },
                    children: [{
                        name: 'Pungent',
                        value: 1,
                        itemStyle: {
                            color: '#794752'
                        }
                    }, {
                        name: 'Pepper',
                        value: 1,
                        itemStyle: {
                            color: '#cc3d41'
                        }
                    }, {
                        name: 'Brown Spice',
                        itemStyle: {
                            color: '#b14d57'
                        },
                        children: [{
                            name: 'Anise',
                            value: 1,
                            itemStyle: {
                                color: '#c78936'
                            }
                        }, {
                            name: 'Nutmeg',
                            value: 1,
                            itemStyle: {
                                color: '#8c292c'
                            }
                        }, {
                            name: 'Cinnamon',
                            value: 1,
                            itemStyle: {
                                color: '#e5762e'
                            }
                        }, {
                            name: 'Clove',
                            value: 1,
                            itemStyle: {
                                color: '#a16c5a'
                            }
                        }]
                    }]
                }, {
                    name: 'Nutty/\nCocoa',
                    itemStyle: {
                        color: '#a87b64'
                    },
                    children: [{
                        name: 'Nutty',
                        itemStyle: {
                            color: '#c78869'
                        },
                        children: [ {
                            name: 'Peanuts',
                            value: 1,
                            itemStyle: {
                                color: '#d4ad12'
                            }
                        }, {
                            name: 'Hazelnut',
                            value: 1,
                            itemStyle: {
                                color: '#9d5433'
                            }
                        }, {
                            name: 'Almond',
                            value: 1,
                            itemStyle: {
                                color: '#c89f83'
                            }
                        }]
                    }, {
                        name: 'Cocoa',
                        itemStyle: {
                            color: '#bb764c'
                        },
                        children: [{
                            name: 'Chocolate',
                            value: 1,
                            itemStyle: {
                                color: '#692a19'
                            }
                        }, {
                            name: 'Dark Chocolate',
                            value: 1,
                            itemStyle: {
                                color: '#470604'
                            }
                        }]
                    }]
                }, {
                    name: 'Sweet',
                    itemStyle: {
                        color: '#e65832'
                    },
                    children: [{
                        name: 'Brown Sugar',
                        itemStyle: {
                            color: '#d45a59'
                        },
                        children: [{
                            name: 'Molasses',
                            value: 1,
                            itemStyle: {
                                color: '#310d0f'
                            }
                        }, {
                            name: 'Maple Syrup',
                            value: 1,
                            itemStyle: {
                                color: '#ae341f'
                            }
                        }, {
                            name: 'Caramelized',
                            value: 1,
                            itemStyle: {
                                color: '#d78823'
                            }
                        }, {
                            name: 'Honey',
                            value: 1,
                            itemStyle: {
                                color: '#da5c1f'
                            }
                        }]
                    }, {
                        name: 'Vanilla',
                        value: 1,
                        itemStyle: {
                            color: '#f89a80'
                        }
                    }, {
                        name: 'Vanillin',
                        value: 1,
                        itemStyle: {
                            color: '#f37674'
                        }
                    }, {
                        name: 'Overall Sweet',
                        value: 1,
                        itemStyle: {
                            color: '#e75b68'
                        }
                    }, {
                        name: 'Sweet Aromatics',
                        value: 1,
                        itemStyle: {
                            color: '#d0545f'
                        }
                    }]
                }];

                chart.setOption({
                    series: {
                        type: 'sunburst',
                        highlightPolicy: 'ancestor',
                        data: data,
                        radius: [0, '95%'],
                        sort: null,
                        label: {
                            color: 'inherit'
                        },
                        itemStyle: {
                            borderRadius: 5
                        },
                        emphasis: {
                            itemStyle: {
                                borderRadius: 2
                            }
                        },
                        levels: [{}, {
                            r0: '15%',
                            r: '35%',
                            itemStyle: {
                                borderWidth: 2
                            },
                            label: {
                                rotate: 'tangential'
                            }
                        }, {
                            r0: '35%',
                            r: '70%',
                            label: {
                                align: 'right'
                            }
                        }, {
                            r0: '70%',
                            r: '72%',
                            label: {
                                position: 'outside',
                                padding: 3,
                                silent: false
                            },
                            itemStyle: {
                                borderWidth: 3
                            }
                        }]
                    }
                });
        },
        bar2(){
            var chart = echarts.init(document.getElementById('bar2'));
            var xAxisData = [];
            var data1 = [];
            var data2 = [];
            var data3 = [];
            var data4 = [];
            for (var i = 0; i < 10; i++) {
                xAxisData.push('类目' + i);
                data1.push(i === 0 ? '-' : (Math.random() * 5).toFixed(2));
                data2.push(-Math.random().toFixed(2));
                data3.push((Math.random() + 0.5).toFixed(2));
                data4.push((Math.random() + 0.3).toFixed(2));
            }
            var itemStyle = {
                normal: {
                    barBorderRadius: 5,
                    label: {
                        show: true,
                        position: 'outside'
                    }},
                emphasis: {
                    focus: 'series',
                    label: {
                        position: 'outside'
                    },
                    // barBorderColor: '#fff',
                    // barBorderWidth: 1,
                    // shadowBlur: 10,
                    // shadowOffsetX: 0,
                    // shadowOffsetY: 0,
                    shadowColor: 'rgba(0,0,0,0.3)'
                }
            };
            chart.setOption({
                backgroundColor: '#fff',
                title: {
                    // text: '我是柱状图',
                    padding: 20
                },
                legend: {
                    left: 150,
                    inactiveColor: '#abc',
                    borderWidth: 1,
                    data: [{
                        name: 'bar'
                    }, 'bar2', '\n', 'bar3', 'bar4'],
                    selected: {
                        // 'bar': false
                    },
                    // orient: 'vertical',
                    // x: 'right',
                    // y: 'bottom',
                    align: 'left',
                    tooltip: {
                        show: true
                    }},
                brush: {
                    xAxisIndex: 0
                },
                toolbox: {
                    top: 50,
                    // right: 20,
                    feature: {
                        magicType: {
                            type: ['line', 'bar', 'stack', 'tiled']
                        },
                        dataView: {},
                        saveAsImage: {
                            pixelRatio: 2
                        },
                        brush: {
                            type: ['rect', 'polygon', 'lineX', 'lineY', 'keep', 'clear']
                        },
                        restore: {},
                        dataZoom: {},
                        myTool1: {
                            show: true,
                            title: '自定义扩展方法1',
                            icon: 'path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891',
                            onclick: function (){
                                alert('myToolHandler1')
                            }},
                        myTool2: {
                            show: true,
                            title: '自定义扩展方法2',
                            icon: 'image://./asset/echarts-logo.png',
                            onclick: function (){
                                alert('myToolHandler2')
                            }
                        }},
                    iconStyle: {
                        emphasis: {
                            textPosition: 'top'
                            // textAlign: 'right'
                        }
                    }},
                tooltip: {},
                grid: {
                    top: 100
                },
                xAxis: {
                    data: xAxisData,
                    name: '横轴',
                    silent: false,
                    axisTick: {
                        alignWithLabel: true
                    },
                    // axisLabel: {
                    //     show: false
                    // },
                    // axisTick: {
                    //     show: false
                    // },
                    axisLine: {
                        onZero: true
                        // lineStyle: {
                        //     width: 5
                        // }
                    },
                    splitLine: {
                        show: true
                    },
                    splitArea: {
                        show: true
                    }},
                yAxis: {
                    inverse: true,
                    // axisLabel: {
                    //     show: false
                    // },
                    // axisLine: {
                    //     lineStyle: {
                    //         width: 5
                    //     }
                    // },
                    axisTick: {
                        show: false
                    },
                    // splitLine: {
                    //     show: false
                    // },
                    splitArea: {
                        show: false
                    }},
                series: [{
                    name: 'bar',
                    type: 'bar',
                    stack: 'one',
                    itemStyle: itemStyle,
                    selectedMode: true,
                    cursor: 'move',
                    data: data1
                }, {
                    name: 'bar2',
                    type: 'bar',
                    stack: 'one',
                    itemStyle: itemStyle,
                    selectedMode: true,
                    cursor: 'default',
                    data: data2
                }, {
                    name: 'bar3',
                    type: 'bar',
                    stack: 'two',
                    itemStyle: itemStyle,
                    selectedMode: true,
                    data: data3
                }, {
                    name: 'bar4',
                    type: 'bar',
                    stack: 'two',
                    itemStyle: itemStyle,
                    selectedMode: true,
                    data: data4
                }]
            });
            chart.on('click', function (params) {
                console.log(params);
            });
            chart.on('legendselectchanged', function (params) {
                chart.setOption({
                    // title: {},
                    graphic: [{
                        type: 'circle',
                        shape: {
                            cx: 100,
                            cy: 100,
                            r: 20,
                        }
                    }]
                });
            });
            window.onresize = chart.resize;
        }
    }
});
