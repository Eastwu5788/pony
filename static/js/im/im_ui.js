var csrf_token = "";

// 增加一条新的会话
function insert_conversation(conversation) {
    var con_div = conversation_factory(conversation);
    $(".chat-list-scrollbar-dynamic").prepend(con_div);
}

// 向会话中新增一条新消息
function insert_message_for_conversation(conversition) {
    if (current_conversation.contact !== conversition.contact) {
        return;
    }

    var message = conversition.messages[0];
    var con_div = $("#chat-conversation-"+conversition.contact);
    con_div.find(".chat-last-message").html(message.data);

    // 显示会话详情
    var content_area = $(".chat-scrollbar-ares");

    // 需要向前查询一次，判断上一条小时是否是默认插入的时间戳消息
    if (conversition.messages.length >= 2) {
        var time_msg = conversition.messages[1];
        if (time_msg.type === "time") {
            content_area.append(message_factory(conversition.messages[1]));
        }
    }
    content_area.append(message_factory(conversition.messages[0]));

    // 滚动到底部
    content_area.stop().animate({scrollTop:content_area[0].scrollHeight},1);
}

// 设置内容区域的顶部内容
function config_content_head(content) {
    $(".chat-area-hd a").html(content);
}

// 显示一个会话的详情
function show_conversation_detail(conversation) {
    // 存储当前活跃回话
    current_conversation = conversation;

    // 移除其它回话的激活状态
    $(".chat-conversation-item.active").removeClass("active");

    var con_div = $("#chat-conversation-"+conversation.contact);
    con_div.addClass("active");

    // 设置联系人
    config_content_head(conversation.user_info === null ? conversation.contact : conversation.user_info.nick_name);

    // 显示会话详情
    var content_area = $(".chat-scrollbar-ares");
    // 清空内容
    content_area.empty();

    for (var index = conversation.messages.length - 1; index >=0; index--) {
        var message = conversation.messages[index];
        content_area.append(message_factory(message));
    }


    // 滚动到底部
    content_area.scrollTop = content_area.height();
}

function start_conversation_with_contact(contact) {
    var con = query_conversation_by_from(contact);
    if (con === null) {
        // 新建一条会话，并插入到会话列表中
        con = new Conversation(null);
        con.contact = contact;
        con.contact_user_info(function (user_info) {
            con.user_info = user_info;
            conversation_list.unshift(con);
            show_conversation();
            console.log(con);
            show_conversation_detail(con);
        });
    }else{
        show_conversation();
        show_conversation_detail(con);
    }
}


function show_conversation() {
    if ($(".chat-panel-tab-chat").hasClass("active")) {
        return;
    }

    change_tab_status(".chat-panel-tab-chat", true);
    change_tab_status(".chat-panel-tab-notification", false);
    change_tab_status(".chat-panel-tab-friends", false);


    $(".chat-list-scrollbar-dynamic").empty();
    $.each(conversation_list, function (index, conversation) {
        insert_conversation(conversation);
    });
}

function show_notification() {
    if ($(".chat-panel-tab-notification").hasClass("active")) {
        return;
    }

    change_tab_status(".chat-panel-tab-chat", false);
    change_tab_status(".chat-panel-tab-notification", true);
    change_tab_status(".chat-panel-tab-friends", false);

    $(".chat-list-scrollbar-dynamic").empty();
}

function show_friends() {
    if ($(".chat-panel-tab-friends").hasClass("active")) {
        return;
    }

    change_tab_status(".chat-panel-tab-chat", false);
    change_tab_status(".chat-panel-tab-notification", false);
    change_tab_status(".chat-panel-tab-friends", true);

    query_friend_list(function () {
        var panel_scroll = $(".chat-list-scrollbar-dynamic");
        // 置空
        panel_scroll.empty();

        $.each(friend_list, function (index, user_info) {
            var friend_div = friend_item_factory(user_info);
            panel_scroll.append(friend_div);
        });
    });
}

function change_tab_status(class_str, active) {
    var tab = $(class_str);
    if (active === true) {
        tab.removeClass("normal");
        tab.addClass("active")
    }else{
        tab.removeClass("active");
        tab.addClass("normal");
    }
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
    current_conversation.send_text_message(new_message, user_info, current_conversation.user_info, function (success, message) {
        // 清空输入框内容
        $(".chat-input").val("");
        // 不论失败或者成功，都需要向会话中插入消息
        current_conversation.add_message(message);
        insert_message_for_conversation(current_conversation);
    });
}

/*============     UI Factory    ==============*/

function friend_item_factory(friend) {
    var div = $("<div class='chat-friend-item'></div>");
    div.attr("id", "chat-friend-"+friend.id);

    var click_a = $("<a class='click-href'></a>");
    click_a.attr("data", friend.id);
    click_a.click(function () {
        start_conversation_with_contact($(".click-href").attr("data"));
    });
    div.append(click_a);

    // 头像部分
    var img = $("<img class='chat-from-avatar'>");
    img.attr("src", friend.avatar.image_a);
    var avatar = $("<a class='chat-con-avatar'></a>").append(img);
    click_a.append(avatar);


    // 会话消息部分
    var con_info_div = $("<div class='chat-con-info'></div>");

    var nick_name_span = $("<span></span>");
    nick_name_span.html(friend.nick_name);

    var nick_name = $("<h3 class='chat-from-nickname'></h3>");
    nick_name.append(nick_name_span);
    con_info_div.append(nick_name);

    click_a.append(con_info_div);

    return div;
}

// 时间戳消息工厂
function time_message_factory(message) {
    var time_div = $("<div class='message-time-container'></div>");

    var span = $("<span class='message-time-text'></span>");

    var date = new Date(message.timeStamp);
    span.html(date.getHours() + ":" + date.getMinutes());

    time_div.append(span);

    return time_div;
}

// 对话消息
function message_factory(message) {
    if (message.type === "time") {
        return time_message_factory(message)
    }

    var msg_div = $("<div class='message-container'></div>");

    var msg_user = $("<a class='message-user-href'></a>");
    var msg_user_avatar = $("<img class='message-user-avatar'>");
    msg_user.append(msg_user_avatar);
    msg_div.append(msg_user);

    var content_bubble = $("<div class='message-bubble'></div>");
    var content_text = $("<p class='message-content'></p>");
    content_text.html(message.data);

    content_bubble.append(content_text);
    msg_div.append(content_bubble);

    var user_info = null;
    // 我发送给对方的消息
    if (message.from.toString() === current_user_id.toString()) {
        user_info = query_user_info_from_message(message, current_user_id);

        // 内容居于右侧
        msg_user.addClass("message-user-href-right");
        content_bubble.addClass("message-bubble-right");
        content_text.addClass("message-content-right");
    }
    // 对方发送给我的消息
    else{
        user_info = query_user_info_from_message(message, message.from);

        // 内容居于右侧
        msg_user.addClass("message-user-href-left");
        content_bubble.addClass("message-bubble-left");
        content_text.addClass("message-content-left");
    }

    // 用户信息存在
    if (user_info !== null) {
        msg_user_avatar.attr("src", user_info.avatar.image_a);
    }

    console.log("ssasdafd");

    return msg_div;
}

// 创建一个新的回话的工厂函数
function conversation_factory(conversation) {
    var div = $("<div class='chat-conversation-item'></div>");
    div.attr("id", "chat-conversation-"+conversation.contact);

    var click_a = $("<a class='click-href'></a>");
    click_a.attr("data", conversation.contact);
    click_a.click(function () {
        start_conversation_with_contact($(".click-href").attr("data"));
    });
    div.append(click_a);

    // 头像部分
    var img = $("<img class='chat-from-avatar'>");
    img.attr("src", conversation.user_info.avatar.image_a);
    var avatar = $("<a class='chat-con-avatar'></a>").append(img);
    click_a.append(avatar);


    // 会话消息部分
    var con_info_div = $("<div class='chat-con-info'></div>");

    var nick_name_span = $("<span></span>");
    nick_name_span.html(conversation.user_info.nick_name);

    var nick_name = $("<h3 class='chat-from-nickname'></h3>");
    nick_name.append(nick_name_span);
    con_info_div.append(nick_name);

    var message = $("<p class='chat-last-message'></p>");
    message.html(conversation.last_message());
    con_info_div.append(message);

    click_a.append(con_info_div);

    return div;
}