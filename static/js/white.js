var sdkToken = "NETLESSSDK_YWs9RnZabTVnT3ZndzVvZmV6ayZub25jZT00ZmU1OGE2MC1jN2Q4LTExZWQtYjliMC0yNzQ4MDgwOTZjNGEmcm9sZT0wJnNpZz0zZjIzMjhiNjE5OTcwOWQ3NDEyMTllZmNmMmIyMmI3NWMzMTk2NGEwYzJhZDFiNzU1ZTYzZmEzZmNmN2ZmM2Yy";
var appIdentifier = "A07CcMfYEe25sCdICAlsSg/wdKVTtESdpX6oQ";
// AK = FvZm5gOvgw5ofezk
// SK = OWCgRQT0uKEFKXm1Kh1T-P0tYb8Aw4-P
//sdk = NETLESSSDK_YWs9RnZabTVnT3ZndzVvZmV6ayZub25jZT00ZmU1OGE2MC1jN2Q4LTExZWQtYjliMC0yNzQ4MDgwOTZjNGEmcm9sZT0wJnNpZz0zZjIzMjhiNjE5OTcwOWQ3NDEyMTllZmNmMmIyMmI3NWMzMTk2NGEwYzJhZDFiNzU1ZTYzZmEzZmNmN2ZmM2Yy
// 构造创建房间的 Request
var url = "https://api.netless.link/v5/rooms";
var requestInit = {
    method: "POST",
    headers: {
        "content-type": "application/json",
        "token": sdkToken,
        "region": "cn-hz",
    },
};

window.fetch(url, requestInit).then(function(response) {
    return response.json();

}).then(function(json) {
    // 创建房间成功，获取房间的 uuid
    var roomUUID = json.uuid;

    // 构造申请 Room Token 的 Request
    var url = "https://api.netless.link/v5/tokens/rooms/" + roomUUID;
    var requestInit = {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "token": sdkToken,
        },
        body: JSON.stringify({
            "lifespan": 0, // 表明 Room Token 永不失效
            "role": "admin", // 表明 Room Token 有 Admin 的权限
        }),
    };
    fetch(url, requestInit).then(function(response) {
        return response.json();

    }).then(function(roomToken) {
        // 成功获取房间的 Room Token
        joinRoom(roomUUID, roomToken);

    }).catch(function(err) {
        console.error(err);
    });
}).catch(function(err) {
    console.error(err);
});

function joinRoom(roomUUID, roomToken) {
    var whiteWebSdk = new WhiteWebSdk({
        appIdentifier: appIdentifier,
    });
    var joinRoomParams = {
        uuid: roomUUID,
        roomToken: roomToken,
        uid: "my-uid",
    };
    whiteWebSdk.joinRoom(joinRoomParams).then(function(room) {
        // 加入房间成功，获取 room 对象
        // 并将之前的 <div id="whiteboard"/> 占位符变成白板
        room.bindHtmlElement(document.getElementById("whiteboard"));
        room.setMemberState({currentApplianceName: "pencil"});

    }).catch(function(err) {
        // 加入房间失败
        console.error(err);
    });
}

// 实现所有教具切换的代码
var pencil = document.getElementById("pencil");
var eraser = document.getElementById("eraser");
var text = document.getElementById("text");
var selector = document.getElementById("selector");
var color = document.getElementById("color");
var stroke = document.getElementById("stroke");
var undo = document.getElementById("undo");
var redo = document.getElementById("redo");
var clear = document.getElementById("clear");
var zoomIn = document.getElementById("zoom-in");
var zoomOut = document.getElementById("zoom-out");
var zoomReset = document.getElementById("zoom-reset");
// 为所有教具绑定点击事件
pencil.addEventListener("click", function() {
    room.setMemberState({currentApplianceName: "pencil"});
});
eraser.addEventListener("click", function() {
    room.setMemberState({currentApplianceName: "eraser"});
});
text.addEventListener("click", function() {
    room.setMemberState({currentApplianceName: "text"});
});
selector.addEventListener("click", function() {
    room.setMemberState({currentApplianceName: "selector"});
});
color.addEventListener("click", function() {
    room.setMemberState({currentApplianceName: "color"});
});
stroke.addEventListener("click", function() {
    room.setMemberState({currentApplianceName: "stroke"});
});
undo.addEventListener("click", function() {
    room.undoMagix();
});
redo.addEventListener("click", function() {
    room.redoMagix();
});
clear.addEventListener("click", function() {
    room.clear();
});
zoomIn.addEventListener("click", function() {
    room.zoomIn();
});
zoomOut.addEventListener("click", function() {
    room.zoomOut();
});
zoomReset.addEventListener("click", function() {
    room.zoomReset();
});
// 实现颜色选择的代码
var colorPicker = document.getElementById("color-picker");
colorPicker.addEventListener("change", function() {
    room.setMemberState({strokeColor: colorPicker.value});
});
// 实现笔触粗细选择的代码
var strokePicker = document.getElementById("stroke-picker");
strokePicker.addEventListener("change", function() {
    room.setMemberState({strokeWidth: parseInt(strokePicker.value)});
});
// 实现文字输入的代码
var textInput = document.getElementById("text-input");
textInput.addEventListener("change", function() {
    room.setMemberState({text: textInput.value});
});
// 实现文字大小选择的代码
var textSizePicker = document.getElementById("text-size-picker");
textSizePicker.addEventListener("change", function() {
    room.setMemberState({fontSize: parseInt(textSizePicker.value)});
});
// 实现文字字体选择的代码
var textFontPicker = document.getElementById("text-font-picker");
textFontPicker.addEventListener("change", function() {
    room.setMemberState({fontFamily: textFontPicker.value});
});
// 实现文字粗细选择的代码
var textBoldPicker = document.getElementById("text-bold-picker");
textBoldPicker.addEventListener("change", function() {
    room.setMemberState({bold: textBoldPicker.value});
});
// 实现文字斜体选择的代码
var textItalicPicker = document.getElementById("text-italic-picker");
textItalicPicker.addEventListener("change", function() {
    room.setMemberState({italic: textItalicPicker.value});
});
// 实现文字下划线选择的代码
var textUnderlinePicker = document.getElementById("text-underline-picker");
textUnderlinePicker.addEventListener("change", function() {
    room.setMemberState({underline: textUnderlinePicker.value});
});
