function change_user_info() {
    $("#avatar-img").click(function (e) {
        e.preventDefault();
        window.location.href = "/auth/set_info";
    });
}

$(function (){
    change_user_info();
})