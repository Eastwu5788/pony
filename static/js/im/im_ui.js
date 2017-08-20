// 当前活跃回话
var current_conversation = null;

// 缓存用户信息列表
var cache_user_info_list = [];

var csrf_token = "";

// 增加一条新的会话
function insert_conversation(conversition) {
    var con_div = conversation_factory(conversition);
    $(".chat-list-scrollbar-dynamic").prepend(con_div);

    (function (con_div, conversition) {
        query_user_info(conversition.contact, function (user_info) {
            conversition.user_info = user_info;
            con_div.find(".chat-from-avatar").attr("src", user_info.avatar.image_a);
            con_div.find(".chat-from-nickname span").html(user_info.nick_name);
        });
    })(con_div, conversition);
}

// 向会话中新增一条新消息
function insert_message_for_conversation(conversition) {
    if (current_conversation.contact != conversition.contact) {
        return;
    }

    var message = conversition.messages[0];
    var con_div = $("#chat-conversation-"+conversition.contact);
    con_div.find(".chat-last-message").html(message.data);

    // 显示会话详情
    var content_area = $(".chat-scrollbar-ares");
    content_area.append(message_factory(conversition.messages[0]));

    // 滚动到底部
    content_area.scrollTop = content_area.height();
}

// 设置内容区域的顶部内容
function config_content_head(content) {
    $(".chat-area-hd a").html(content);
}

// 显示一个会话的详情
function show_conversation_detail(conversation) {
    // 存储当前活跃回话
    current_conversation = conversation;

    // 设置联系人
    config_content_head(conversation.user_info === null ? conversation.contact : conversation.user_info.nick_name);

    // 显示会话详情
    var content_area = $(".chat-scrollbar-ares");
    for (var index = conversation.messages.length - 1; index >=0; index--) {
        var message = conversation.messages[index];
        content_area.append(message_factory(message));
    }


    // 滚动到底部
    content_area.scrollTop = content_area.height();
}

function start_conversation_with_friend(contact) {
    var con = query_conversation_by_from(contact);
    if (con === null) {
        // 新建一条会话，并插入到会话列表中
        con = new Conversation(null);
        con.contact = contact;
        conversation_list.unshift(con);
    }

    $(".chat-list-scrollbar-dynamic").empty();
    $.each(conversation_list, function (index, conversation) {
        insert_conversation(conversation);
    });
    show_conversation_detail(con);
}

function show_friends() {
    var panel_scroll = $(".chat-list-scrollbar-dynamic");
    // 置空
    panel_scroll.empty();

    conn.getRoster({
       success: function (roster) {
           $.each(roster, function (index, ros) {
                console.log(ros);
                if (ros.subscription === "both" || ros.subscription === "to") {
                    friend_list.push(ros);
                    var friend_div = friend_item_factory(ros);
                    panel_scroll.append(friend_div);

                    // 查询用户信息
                    query_user_info(ros.name, function (user_info) {
                        var chat_friend = $("#chat-friend-"+ros.name);
                        chat_friend.find(".chat-from-avatar").attr("src", user_info.avatar.image_a);
                        chat_friend.find(".chat-from-nickname span").html(user_info.nick_name);
                    });
                }
           });
       }
    });
}



// Click Handler
/*
* 发送一条新消息的处理函数
* */
function send_message_handler(user_info) {
    console.log(user_info);

    if (current_conversation === null) {
        toastr.error("Error", "当前回话不存在");
        return null;
    }

    var new_message = $(".chat-input").val();
    if ($.trim(new_message).length === 0) {
        toastr.error("Error", "您要发送的内容不能为空");
        return null;
    }
    // 发送一条文本消息
    current_conversation.send_text_message(new_message, user_info, function (success, message) {
        // 清空输入框内容
        $(".chat-input").val("");
        // 不论失败或者成功，都需要向会话中插入消息
        current_conversation.add_message(message);
        insert_message_for_conversation(current_conversation);
    });
}

/*============      Utils        ==============*/
function query_user_info(user_id, func) {
    // 1.查找缓存
    for (var i=0, len=cache_user_info_list.length; i < len; i++) {
        var user = cache_user_info_list[i];
        if (user.id === user_id) {
            func(user);
            return null;
        }
    }

    // 2.服务器异步查询
    user_info(user_id, function (data) {
        cache_user_info_list.unshift(data);
        func(data);
    });
}


/*============     UI Factory    ==============*/

function friend_item_factory(friend) {
    var div = $("<div class='chat-friend'></div>");
    div.attr("id", "chat-friend-"+friend.name);
    div.addClass("chat-friend-common");

    var click_a = $("<a class='click-href'></a>");
    click_a.attr("data", friend.name);
    click_a.click(function () {
        start_conversation_with_friend($(".click-href").attr("data"));
    });
    div.append(click_a);

    // 头像部分
    var img = $("<img class='chat-from-avatar'>");
    var avatar = $("<a class='chat-con-avatar'></a>").append(img);
    click_a.append(avatar);


    // 会话消息部分
    var con_info_div = $("<div class='chat-con-info'></div>");

    var nick_name_span = $("<span></span>");
    nick_name_span.html(friend.name);

    var nick_name = $("<h3 class='chat-from-nickname'></h3>");
    nick_name.append(nick_name_span);
    con_info_div.append(nick_name);

    click_a.append(con_info_div);

    return div;
}


// 对话消息
function message_factory(message) {
    var msg_div = $("<div class='message-container'></div>");

    var msg_user = $("<a></a>");
    var msg_user_avatar = $("<img>");
    msg_user.append(msg_user_avatar);
    msg_div.append(msg_user);

    var content_bubble = $("<div class='message-bubble'></div>");
    var content_text = $("<p class='message-content'></p>");
    content_text.html(message.data);

    content_bubble.append(content_text);
    msg_div.append(content_bubble);

    return msg_div;
}

// 创建一个新的回话的工厂函数
function conversation_factory(conversation) {
    var div = $("<div class='chat-conversation'></div>");
    div.attr("id", "chat-conversation-"+conversation.contact);
    div.addClass("chat-con-type-common");

    var click_a = $("<a></a>");
    click_a.onclick = (function (conversation) {
        show_conversation_detail(conversation);
    })(conversation);
    div.append(click_a);

    // 头像部分
    var img = $("<img class='chat-from-avatar'>");
    var avatar = $("<a class='chat-con-avatar'></a>").append(img);
    click_a.append(avatar);


    // 会话消息部分
    var con_info_div = $("<div class='chat-con-info'></div>");

    var nick_name_span = $("<span></span>");
    nick_name_span.html("喵喵");

    var nick_name = $("<h3 class='chat-from-nickname'></h3>");
    nick_name.append(nick_name_span);
    con_info_div.append(nick_name);

    var message = $("<p class='chat-last-message'></p>");
    message.html("");
    con_info_div.append(message);

    click_a.append(con_info_div);

    return div;
}