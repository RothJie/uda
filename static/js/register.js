function validateEmail() {
    var email = document.getElementById("exampleInputEmail1").value;
    var error = document.getElementById("errorEmail1");

    // 验证邮件地址是否为空
    if (email === "") {
        error.innerHTML = '<small class="form-text text-muted" style="font-style: italic; font-size: 16px; align-content: inherit">邮件地址不能为空</small>';
        return false;
    }

    // 正则表达式验证邮件地址是否符合标准
    var emailRegex = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/
    if (!emailRegex.test(email)) {
        error.innerHTML = '<small class="form-text text-muted" style="font-style: italic; font-size: 24px; align-content: inherit">请输入有效的邮件地址</small>';
        return false;
    }

    // 验证通过，清空错误提示信息
    error.innerHTML = "";
    return true;
}

function bindClikForCaptchaBtn() {
    $('#captcha-btn').click(function (event) {
        // 对邮箱进行校验
        if (!validateEmail()) return;

        event.preventDefault();  // 阻止默认事件

        // 获取获取验证码的按钮
        // $this：代表的是当前按钮的jquery对象
        var captcha_btn = $(this);

        // 获取输入的邮箱
        var email = $('#exampleInputEmail1').val();

        $.ajax({
            url: '/auth/captcha/email?email=' + email,
            method: 'GET',
            success: function (rsl) {
                var code = rsl["code"];
                if (code === 200) {
                    var countdown_seconds = 30;
                    captcha_btn.off('click');
                    var timer = setInterval(function () {
                        captcha_btn.text(countdown_seconds);
                        countdown_seconds -= 1
                        if (countdown_seconds <= 0) {
                            clearInterval(timer);
                            captcha_btn.text("获取验证码")
                            bindClik4CaptchaBtn() // 重新递归
                        }
                    }, 1000)
                } else {
                    alert(rsl['message'])
                }
            },
            fail: function (error) {
                console.log(error);
            }
        });
    });
}

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
    $("#register-btn").click(function (e) {
            e.preventDefault();
            const formData = {
                "email": document.getElementById("exampleInputEmail1").value,
                "captcha": document.getElementById("captcha-ipt").value,
                "username": document.getElementById("user_name_btn").value,
                "password": document.getElementById("exampleInputPassword1").value,
                "password_confirm": document.getElementById("confirmPassword").value
            };

            $.ajax({
                url: "/auth/register",
                method: "POST",
                data: formData,
                success: function (res) {
                    let email = res.data["email"]
                    const formData = new FormData()
                    // 再添加 email 信息
                    formData.append("email", email)
                    formData.append("imageFile", $('#imageFileInput').get(0).files[0])
                    $.ajax({
                        url: "/auth/register/submit_avatar",
                        method: "POST",
                        data: formData,
                        processData: false,
                        contentType: false
                    });
                },
                error: function (error) {
                    console.error(error);
                }
            });

        }
    );
}


// 优化后
// function submitFormData() {
//     $("#register-btn").click(function (e) {
//             //e.preventDefault();
//
//             const formData = new FormData();
//             formData.append("email", document.getElementById("exampleInputEmail1").value)
//             formData.append("captcha", document.getElementById("captcha-ipt").value)
//             formData.append("username", document.getElementById("user_name_btn").value)
//             formData.append("password", document.getElementById("exampleInputPassword1").value)
//             formData.append("password_confirm", document.getElementById("confirmPassword").value)
//             formData.append("imageFile", $('#imageFileInput').get(0).files[0])
//             $.ajax({
//                 url: "/auth/register",
//                 method: "POST",
//                 data: formData,
//                 processData: false,
//                 contentType: false
//             });
//         }
//     );
// }

// 调用
$(function () {
    bindClikForCaptchaBtn();
    showPreview();
    submitFormData();
});