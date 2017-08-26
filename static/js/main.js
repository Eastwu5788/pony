/**
 * Created by Administrator on 2017/7/31.
 */

/* === API ===*/
ARTICLE_DELETE = "/manage/article/remove";

ARTICLE_LIKE = "/article/like";

ARTICLE_COMMENT_ADD = "/article/comment/add";
ARTICLE_COMMENT_LIKE_EDIT = "/article/comment/like";
ARTICLE_COMMENT_REPLY = "/article/comment/reply";

AUTH_LOGIN = "/auth/api/login";
AUTH_LOGOUT = "/auth/api/logout";
AUTH_CHECK_EMAIL = "/auth/api/checkemail";


USER_INFO = "/user/api/info";
USER_EASE_MOB_INFO = "/user/api/easemob";
USER_SEARCH_API = "/user/api/search";

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


function has_attr(obj, attr_name) {
    var attr_value = obj.attr(attr_name);
    if (typeof(attr_value) == "undefined") {
        return false;
    }
    return true;
}

/* ======== 用户账户相关 ======= */
function get_user_info(user_id, func) {
    $.get(USER_INFO, {user_id: user_id, csrfmiddlewaretoken: csrf_token},function (data) {
        if (data) {
           func(data.user_info);
        }

    }, "json");
}

function request_user_ease_mob_info(ease_mob, func) {
    $.get(USER_EASE_MOB_INFO, {ease_mob: ease_mob, csrfmiddlewaretoken: csrf_token},function (data) {
        if (data) {
           func(data.user_info);
        }

    }, "json");
}

function search_user_by_nickname(nick_name, func) {
    $.get(USER_SEARCH_API, {nick_name: nick_name, csrfmiddlewaretoken: csrf_token}, function (data) {
        if (data.code === 200) {
            func(data.data);
        }else{
            func([]);
        }
    }, "json");
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

function check_email(email, token, func) {
    $.get(AUTH_CHECK_EMAIL, {email: email, csrfmiddlewaretoken: token}, function (result) {
        func(result);
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


/* ======= 点赞处理相关 ======= */
function edit_like_info(article_id, type_id, token, success) {
    $.post(ARTICLE_LIKE, {article_id: article_id, type_id: type_id, csrfmiddlewaretoken: token}, function (data) {
        if (data.code == 200) {
            success();
        }else{
            toastr.error("请求失败", data.message);
        }
    }, "json");
}


/* ======= 评论相关 ====== */
function comment_add(article_id, content, token) {
    $.post(ARTICLE_COMMENT_ADD, {article_id: article_id, content: content, csrfmiddlewaretoken: token}, function (result) {
        if (result.code == 200) {
            location.reload();
        }else{
            toastr.error("请求失败", result.message);
        }
    }, "json");
}

/* 评论回复 */
function comment_reply_add(comment_id, reply_add, content, token) {
    $.post(ARTICLE_COMMENT_REPLY, {comment_id: comment_id,reply_add:reply_add, content: content, csrfmiddlewaretoken: token}, function (result) {
        if (result.code == 200) {
            location.reload();
        }else{
            toastr.error("请求失败", result.message);
        }
    }, "json");
}

/* 评论点赞处理 */
function comment_like(type, comment_id, token) {
    $.post(ARTICLE_COMMENT_LIKE_EDIT, {type: type, comment_id:comment_id, csrfmiddlewaretoken: token}, function (result) {
        if (result.code == 200) {
            location.reload();
        }else{
            toastr.error("请求失败", result.message);
        }
    }, "json");
}


/* =====  正则表达式验证  =====*/

/*校验邮件地址是否合法 */
function IsEmail(str) {
	var reg=/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
	return reg.test(str);
}
