$(document).ready(function () {
    /* code 1进入房间，code 2发送消息*/
    //定义一个长连接
    var conn = null;
    var name = $("#input_name").val();
    var face = $("#input_face").val();

    /*
    发送消息的函数
    name：昵称
    data：数据（服务端推送过来的消息）
    */
    function append_msg(name, data) {
        var html = "";
        if (data.code == 2) {
            /*判断用户，是自己还是别人*/
            if (data.name == name) {
                // data.JSON();
                //自己
                html += "<div class=\"row\">\n" +
                    "                        <div class=\"col-md-3\"></div>\n" +
                    "                        <div class=\"col-md-9\">\n" +
                    "                            <div class=\"media\">\n" +
                    "                                <div class=\"media-body\">\n" +
                    "                                    <h6 class=\"user-nickname text-right\">" + data.name + "[" + data.dt + "]</h6>\n" +
                    "                                    <div class=\"alert alert-success\" role=\"alert\">\n" +
                    "                                        " + data.content + "\n" +
                    "                                    </div>\n" +
                    "                                </div>\n" +
                    "                                <img class=\"ml-3 rounded-circle\" src=\"" + data.face + "\" style='width:60px;height: 60px;'>\n" +
                    "                            </div>\n" +
                    "                        </div>\n" +
                    "                    </div>";
            } else {
                //别人
                html += "<div class=\"row\">\n" +
                    "                        <div class=\"col-md-9\">\n" +
                    "                            <div class=\"media\">\n" +
                    "                                <img class=\"mr-3 rounded-circle\" src=\"" + data.face + "\" style='width: 60px;height: 60px;'>\n" +
                    "                                <div class=\"media-body\">\n" +
                    "                                    <h6 class=\"user-nickname\">" + data.name + "[" + data.dt + "]</h6>\n" +
                    "                                    <div class=\"alert alert-info\" role=\"alert\">\n" +
                    "                                        " + data.content + "\n" +
                    "                                    </div>\n" +
                    "                                </div>\n" +
                    "                            </div>\n" +
                    "                        </div>\n" +
                    "                        <div class=\"col-md-3\"></div>\n" +
                    "                    </div>";
            }
            $("#chat-list").append(html);
            SyntaxHighlighter.highlight();
            $("#chat-list").scrollTop(
                $("#chat-list").scrollTop() + 99999999
            );
        } else {
            $("#chat-list").append("<p class='text-center text-success'>欢迎" + data.name + "进入房间！<img src='/static/images/rorse.gif'><img src='/static/images/rorse.gif'><img src='/static/images/rorse.gif'></p>");
        }
    }

    /*更新UI函数*/
    function update_ui(event) {
        var recv_msg = event.data;
        append_msg(name, JSON.parse(recv_msg))
    }

    /* 定义进入房间提示，发起连接的时候进入*/
    function user_enter_tip() {
        var enter_data = {
            code: 1,
            name: name
        };
        conn.send(JSON.stringify(enter_data))
    }

    //重连
    function connect() {
        disconnect();
        var transports = ["websocket"];
        conn = new SockJS('http://' + window.location.host + '/chatroom', transports);
        /*发起连接*/
        conn.onopen = function () {
            $.ajax({
                url: "/msg/",
                type: "POST",
                dataType: "json",
                success: function (res) {
                    var msg_arr = res.data;
                    for (var k in msg_arr) {
                        append_msg(name, msg_arr[k])
                        // console.log(name, msg_arr[k].name, msg_arr[k].content)
                    }
                    /*加载完所有的消息，再来进入房间*/
                    user_enter_tip();
                }
            });
            console.log("发起连接！");
        };
        /*接受消息*/
        conn.onmessage = function (event) {
            //console.log(event);
            update_ui(event);
        };
        /*断开连接*/
        conn.onclose = function () {
            console.log("断开连接！");
            conn = null;
        };
        /*发送数据*/
        /*
        setInterval(
            function () {
                var content = {
                    "content": "好好学习，天天向上！"
                };
                conn.send(JSON.stringify(content));
            },
            2000
        )*///每隔2秒发送一次
    }

    //断开
    function disconnect() {
        if (conn != null) {
            conn.close();//断开
            conn = null;
        }
    }

    /*启动连接*/
    if (conn == null) {
        connect()
    } else {
        disconnect();
    }

    //定义一个函数，获取表单数据
    function getFormData() {
        var data = $("#form-data").serializeArray();
        var result = {};
        $.map(data, function (v, i) {
            result[v['name']] = v['value'];
        });
        return result;
    }

    //点击发送按钮触发发送消息事件！
    $("#send_msg").click(function () {
        //console.log(getFormData());
        var msg = getFormData();
        if (msg.content) {
            msg.code = 2;
            ue.setContent('');
            conn.send(JSON.stringify(msg)); //发送
        } else {
            alert("发送消息不能为空！");
        }
    });
});