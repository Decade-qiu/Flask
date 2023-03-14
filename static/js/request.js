//点击事件触发请求
/*
* url，请求的地址
* rurl，跳转地址
* fields，验证的字段
* msg，成功信息
* */
function request(url, rurl, fields, msg) {
    $("#btn-sub").click(function () {
        //获取表单数据
        var data = $("#form-data").serialize();
        //触发请求，ajax
        $.ajax({
            url: url,
            data: data,
            dataType: "json",
            type: "POST",
            success: function (res) {
//                console.log(res);
                if (res.code == 1) {
                    alert(msg);
                    location.href = rurl;
                } else {
                    for (var k in fields) {
                        if (typeof res[fields[k]] == "undefined") {
                            $("#error_" + fields[k]).empty();
                        } else {
                            $("#error_" + fields[k]).empty();
                            $("#error_" + fields[k]).append(res[fields[k]]);
                        }
                    }
                }
            }
        });
    });
}