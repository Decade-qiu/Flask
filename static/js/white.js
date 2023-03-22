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

// 把教具切换为「铅笔