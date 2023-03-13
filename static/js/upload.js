/*
* k，文件名称
* w，图片宽度
* h，图片高度
* url，上传接口地址
* */

function upload(k, w, h, url) {
    $("#upload_" + k).click(function () {
        var img = $("#file_" + k)[0].files[0];
        if (img) {
            var formData = new FormData();
            formData.append("img", img);
            $.ajax({
                url: url,
                type: "POST",
                dataType: "json",
                cache: false,
                contentType: false,
                processData: false,
                data: formData,
                success: function (res) {
                    if (res.code == 1) {
                        var img = res.image;
                        var content = "<img src='/static/uploads/" + img + "' style='width: " + w + "px;height: " + h + "px;'>";
                        $("#image_" + k).empty();
                        $("#image_" + k).append(content);
                        $("#input_" + k).attr("value", img);
                    }
                }
            });
        }
    });
}