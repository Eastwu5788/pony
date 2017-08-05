/**
 * Created by Administrator on 2017/7/31.
 */
/* === API ===*/
ARTICLE_DELETE = "/manage/article/remove";

AUTH_LOGIN = "/auth/api/login";
AUTH_LOGOUT = "/auth/api/logout";

start_app();

$(".nav-user-avatar").mouseover(function () {
    $(".navbar-right .user-dropdown-menu").css('display','block');
});

$(".nav-user-avatar").mouseout(function () {
    $(".navbar-right .user-dropdown-menu").css('display','none');
});

/* 开启app */
function start_app() {
}


/* ========  授权相关  ========= */
function login(email, password, token) {
    $.post(AUTH_LOGIN, {email: email, pass_word: password, csrfmiddlewaretoken: token}, function (data) {
        if(data.code == 200) {
            location.reload();
        }else{
            toastr.error("请求失败", data.message);
        }
    }, "json");
}

function logout(token) {
    $.post(AUTH_LOGOUT, {csrfmiddlewaretoken: token}, function (data) {
        console.log(data);
        if(data.code == 200) {
            window.location.href = "/index";
        }
    }, "json");
}


/* ======== 文章处理相关 ======== */
function delete_article(id, token) {
    if(confirm("您是否要删除这篇文章?")) {
        $.post(ARTICLE_DELETE, {article_id: id, csrfmiddlewaretoken: token}, function (data) {
            if(data.code == 200) {
                location.reload();
            }else{
                toastr.error("请求失败", data.message);
            }
        }, "json");
    }
}





/* =====  正则表达式验证  =====*/

/*校验邮件地址是否合法 */
function IsEmail(str) {
	var reg=/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
	return reg.test(str);
}
