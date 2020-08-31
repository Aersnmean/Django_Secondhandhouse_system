function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = window.location.search.substr(1).match(reg);  //匹配目标参数
    if (r != null) return decodeURI(r[2]); return null; //返回参数值
}

function remove_border_bottom() {
    let a = $('.detail_main_left_bottom_bottom ul').children().length;
    let b = a % 4;
    if(b>0){
        $('.detail_main_left_bottom_bottom ul li:nth-last-child(-n+'+b+')').css('border-bottom','none');
    }else if(b==0){
        $('.detail_main_left_bottom_bottom ul li:nth-last-child(-n+4)').css('border-bottom','none');
    }
}


function insert_houses(houses) {
    $('#items li').remove();
    for (let i = 0; i < houses.length; i++) {
        if (houses[i].imgs.length == 0) {
            houses[i].imgs.push('https://pages.anjukestatic.com/usersite/site/img/global/defaultImg/list-deft-img2.png');
        }
        let mark = `<li class="house_item" id="${houses[i].id}">
                        <div class="item_img">
                            <img src="${houses[i].imgs[0]}"
                                 alt="" width="180" height="135">
                        </div>
                        <div class="house_detail">
                            <div class="house_title">
                                <a href="#">${houses[i].title}</a>
                            </div>
                            <div class="details_item">
                                <span>${houses[i].bedroom[0]}室${houses[i].bedroom[1]}厅</span>
                                <span class="spe_lines">|</span>
                                <span>${houses[i].area}m²</span>
                                <span class="spe_lines">|</span>
                                <span>${houses[i].floor}</span>
                                <span class="spe_lines">|</span>
                                <span>${houses[i].year}</span>
                            </div>
                            <div class="details_item">
                                <span>${houses[i].plot}</span><span>${houses[i].position[0]}-${houses[i].position[1]}-${houses[i].position[2]}</span>
                            </div>
                        </div>
                        <div class="button">
                            <input type="button" class="hide buttons" name="http://127.0.0.1:8000/page/update.html/?id=${houses[i].id}" value="修改">
                            <input type="button" class="hide buttons buttons_red" name="http://127.0.0.1:8000/gethousebyid/${houses[i].id}/"  value="删除">
                        </div>
                        <div class="pro_price">
                            <span class="price_det">
                                <strong>${houses[i].total_price}</strong>万
                            </span><br>
                            <span class="unit-price">${houses[i].unit_price}元/m²</span>
                        </div>
                    </li>`;
        $('#items').append(mark);
    }
}

function get_datas(url, type='get', data=null){
    $.ajax({
        url: url,
        type: type,
        data: data,
        dataType: 'json',
        success: function (res) {
            insert_houses(res.list);
            $('.house_item div').on('click',function () {
                let class_name = $(this).attr("class");
                if (class_name !='button'){
                     window.open('http://127.0.0.1:8000/page/detail.html/?id='+$(this).closest('.house_item').attr("id"));
                }
            });
            $('.buttons').on('click', function () {
                if ($(this).attr('class') == 'hide buttons') {
                    window.open($(this).attr('name'));
                } else {
                    if (confirm('确定要删除吗？')) {
                        $.ajax({
                            url: $(this).attr('name'),
                            type: 'delete',
                            data: null,
                            dataType: 'json',
                            success: function (res) {
                                window.location.reload();
                            }
                        });
                    }
                }
            });
            $("#page").paging({
                pageNum: Math.ceil(res.total/20), //总页码
                buttonNum: 9,
                callback: function(num) { //回调函数,num为当前页码
                    $.ajax({
                        url: url+'?offset='+(num-1)*20,
                        type: type,
                        data: data,
                        dataType: 'json',
                        success: function (res) {
                            insert_houses(res.list);
                            $(window).scrollTop(100);
                        }
                    });
                }
            });
        }
    });
}

function getplots() {
    $.ajax({
        url: 'http://127.0.0.1:8000/getplot/',
        type: 'get',
        data: null,
        dataType: 'json',
        success: function (res) {
            insert_plots(res.list);
            $("#page").paging({
                pageNum: Math.ceil(res.total/20), //总页码
                buttonNum: 9,
                callback: function(num) { //回调函数,num为当前页码
                    $.ajax({
                        url: 'http://127.0.0.1:8000/getplot/?offset='+(num-1)*20,
                        type: 'get',
                        data: null,
                        dataType: 'json',
                        success: function (res) {
                            insert_plots(res.list);
                            $(window).scrollTop(100);
                        }
                    });
                }
            });
        }
    });
}

function insert_plots(plots) {
    $('#items li').remove();
    for (let i = 0; i < plots.length; i++) {
        if (plots[i].imgs.length == 0) {
            plots[i].imgs.push('https://pages.anjukestatic.com/usersite/site/img/global/defaultImg/list-deft-img2.png');
        }
        let mark = `<li class="house_item" onclick="window.open('http://127.0.0.1:8000/page/plothouses.html/?plot=${plots[i].plot}')">
                        <div class="item_img">
                            <img src="${plots[i].imgs[0]}"
                                 alt="" width="180" height="135">
                        </div>
                        <div class="house_detail">
                            <div class="house_title">
                                <a href="">${plots[i].plot}</a>
                            </div>
                            <div class="details_item">
                                <span class="spe_lines">建造年份</span>
                                <span>${plots[i].year}</span>
                            </div>
                            <div class="details_item">
                                <span>${plots[i].plot}</span><span>${plots[i].position[0]}-${plots[i].position[1]}-${plots[i].position[2]}</span>
                            </div>
                        </div>
                        <div class="pro_price">
                            <span class="price_det">
                                <strong>${plots[i].unit_price}</strong>元/m²
                            </span>
                        </div>
                    </li>`;
        $('#items').append(mark);
    }
}

function creatchart(data, type, num) {
    var myChart = echarts.init(document.getElementById('deal_data_box'));

        // 指定图表的配置项和数据
        var option = {
            title: {
                text: '二手房交易量'
            },
            tooltip: {},
            legend: {
                data:['销量']
            },
            xAxis: {
                data: data['date'].slice(0, num),
            },
            yAxis: {},
            series: [{
                // name: '销量',
                type: type,
                color: ['#3591d5'],
                data: data['num'].slice(0, num),
            }]
        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
}

function createweekcharts() {
    $.ajax({
            url: 'http://127.0.0.1:8000/getdealdata/',
            type: 'get',
            data: null,
            dataType: 'json',
            success: function (res) {
                creatchart(res, 'bar', 7);
            }
        });
}