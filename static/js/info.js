function showPreview() {
    // 监听文件选择变化，实时预览头像
    $('#imageFileInput').on('change', function () {
        // 创建一个FileReader对象，用于读取文件内容
        var reader = new FileReader();
        // 当读取完成时触发的回调函数
        reader.onload = function (e) {
            // 获取头像展示的DOM元素位置
            var previewArea = document.createElement('img');
            previewArea.className = 'avatar-preview';
            previewArea.id = 'avatarImage'
            // 设置img元素的src属性为读取到的文件URL
            previewArea.src = e.target.result;
            // 找到头像包裹元素（.avatar-wrapper），先清空可能已有的内容
            var wrapper = document.querySelector('.avatar-wrapper');
            // 将新创建的img元素添加到包裹元素中
            wrapper.appendChild(previewArea);
        }
        reader.readAsDataURL(this.files[0]);
    });
}

function submitFormData() {
    $("#confirmBtn").click(function (e) {
        const formData = new FormData()
        formData.append("imageFile", $('#imageFileInput').get(0).files[0])
        $.ajax({
            url: "/auth/upload_user_avatar",
            method: "POST",
            data: formData,
            processData: false,
            contentType: false
        });
    });
}


// 调用
$(function () {
    showPreview();
    submitFormData();
});