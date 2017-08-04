/**
 * Created by Administrator on 2017/7/31.
 */

start_app();



/* 开启app */
function start_app() {
}


/*
 * func: 取消首页的推荐
 * article_id: 将要操作的文章ID
 * */
function cancel_recommend(article_id) {
    console.log(article_id);
}

/*
 * func: 编辑文章
 * article_id: 文章ID，如果为0表示创建新文章
 * */
function edit_article(article_id) {
    var url = "/manage/edit/"+article_id;
    window.location.href=url;
}

/* =====  正则表达式验证  =====*/

/*校验邮件地址是否合法 */
function IsEmail(str) {
	var reg=/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
	return reg.test(str);
}
