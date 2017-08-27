// 存储所有回话的列表
var conversation_list = [];
// 存储所有好友列表
var friend_list = [];

var current_user_id = "";

// 缓存用户信息列表
var cache_user_info_list = [];

// 当前活跃回话
var current_conversation = null;

var start_contact = "";

var alert_off = false;
var sound_off = false;



function user(data) {

}

function Conversation(message) {
    this.messages = [];
    this.contact = message === null ? "" : message.contact;
    this.user_info = null;

    // 向回话中追加一跳新消息
    this.add_message = function (message) {
        var now = new Date().getTime();
        if (this.messages.length > 0) {
            var last_msg = this.messages[0];
            if (last_msg.type !== "time") {
                if(now - last_msg.timeStamp > 60000) {
                    this.messages.unshift(time_message_handler());
                }
            }
        }else{
            this.messages.unshift(time_message_handler());
        }
        message.timeStamp = now;
        this.messages.unshift(message);
    };

    this.last_message = function () {
        if(this.messages.length > 0) {
            var msg = this.messages[0];
            if (msg.type === "img") {
                return "[图片]"
            }else if(msg.type === "audio") {
                return "[音频]"
            }else if(msg.type === "file") {
                return "[文件]"
            }
            return msg.data;
        }else{
            return null;
        }
    };

    this.last_message_time = function () {
        if(this.messages.length > 0) {
            var msg = this.messages[0];
            var date = new Date(msg.timeStamp);
            return date.getHours() + ":" + date.getMinutes();
        }else{
            return null;
        }
    };

    // 获取联系人信息
    this.contact_user_info = function (func) {
        if (this.messages.length > 0) {
            var msg = this.messages[0];
            for (var index=0, len = msg.ext.user_list.length; index < len; index++ ) {
                var user_info = msg.ext.user_list[index];
                if (user_info.ease_mob === this.contact) {
                    this.user_info = user_info;
                    func(user_info);
                    return null;
                }
            }
        }else{
            query_user_info(this.contact, function (user_info) {
                this.user_info = user_info;
                func(user_info);
            });
        }
    };

    // 发送一条文本消息
    this.send_text_message = function (msg_str, user_info, contact_info, func) {
        var id = conn.getUniqueId();
        var msg = new WebIM.message("txt", id);

        msg.set({
            msg: msg_str,
            to: this.contact,
            ext: {"user_list":[user_info, contact_info]},
            roomType: false,
            chatType: 'singleChat',
            success: function (id, serverMsgId) {
                var message = txt_message_handler(false, serverMsgId, this, "", "");
                func(true, message);
            },
            fail: function (id, serverMsgId) {
                var message = txt_message_handler(true, serverMsgId, this, "500", "消息发送失败!");
                func(false, message);
            }
        });

        conn.send(msg.body);
    };
    
    this.send_file_message = function (type, file, user_info, func) {
        var id = conn.getUniqueId();
        var msg = new WebIM.message(type, id);
        msg.set({
            apiUrl: WebIM.config.apiURL,
            file: file,
            to: this.contact,
            ext: {"user_list":[user_info, current_conversation.user_info]},
            roomType: false,
            chatType: 'singleChat',
            onFileUploadError: function () {      // 消息上传失败
                console.log('onFileUploadError');
            },
            onFileUploadComplete: function () {
                console.log('onFileUploadComplete');
            },
            success: function (id, serverMsgId) {
                var message = file_message_response_handler(false, serverMsgId, this, "", "");
                func(true, message);
            },
            fail: function (id, serverMsgId) {
                var message = file_message_response_handler(true, serverMsgId, this, "500", "");
                func(false, message);
            },
            flashUpload: WebIM.flashUpload
        });
        console.log(msg);
        conn.send(msg.body);
    }
}

// 开启连接
var conn = new WebIM.connection({
    https: WebIM.config.https,
    url: WebIM.config.xmppURL,
    isAutoLogin: WebIM.config.isAutoLogin,
    isMultiLoginSessions: WebIM.config.isMultiLoginSessions
});

// 添加监听函数
conn.listen({
    onOpened: login_success,                        //连接成功
    onClosed: logout_success,                       //断开连接成功
    onTextMessage: receive_text_message,            //接收到文本消息
    onEmojiMessage: receive_emoji_message,          //接收到表情消息
    onPictureMessage: receive_pic_message,          //接收到图片消息
    onCmdMessage: receive_cmd_message,              //接收到透传消息
    onAudioMessage: receive_audio_message,          //接收到音频消息
    onLocationMessage: receive_location_message,    //接收到位置消息
    onFileMessage: receive_file_message,            //接收到文件消息
    onVideoMessage: receive_video_message,          //接收到视频消息
    onPresence: function (message) {},              //处理“广播”或“发布-订阅”消息，如联系人订阅请求、处理群组、聊天室被踢解散等消息
    onRoster: function ( message ) {},              //处理好友申请
    onInviteMessage: function ( message ) {},       //处理群组邀请
    onOnline: function () {},                       //本机网络连接成功
    onOffline: function () {},                      //本机网络掉线
    onError: receive_error_message,                 //失败回调
    onBlacklistUpdate: function (list) {console.log(list);},  // 查询黑名单，将好友拉黑，将好友从黑名单移除都会回调这个函数，list则是黑名单现有的所有好友信息
    onReceivedMessage: function(message){},         //收到消息送达客户端回执
    onDeliveredMessage: function(message){},        //收到消息送达服务器回执
    onReadMessage: function(message){},             //收到消息已读回执
    onCreateGroup: function(message){},             //创建群组成功回执（需调用createGroupNew）
    onMutedMessage: function(message){}             //如果用户在A群组被禁言，在A群发消息会走这个回调并且消息不会传递给群其它成员
});


// 用户名/密码登录
function login_ease_mob_im(user_name, password) {
    var options = {
        apiUrl: WebIM.config.apiURL,
        user: user_name,
        pwd: password,
        appKey: WebIM.config.appkey
    };
    conn.open(options);
    current_user_id = user_name;
    show_friends_detail(current_user_id);
}

// 环信退出
function logout_ease_mob_im() {
    conn.close();
}

// 连接成功回调
function login_success() {
}

// 断开连接回调
function logout_success(error) {
    // 异常断开之后，需要退出当前账号
    console.log(error);
    //login_ease_mob_im(current_user_id, current_user_id);
}

// 接收到文本消息
function receive_text_message(message) {
    play_message_audio();
    // 接收到消息后，需要讲消息追加到回话中
    add_message_to_conversation(message);
}


// 接收到表情消息
function receive_emoji_message(message) {

}

// 接收到图片消息
function receive_pic_message(message) {
    console.log("图片消息:",message);
    play_message_audio();
    // 修改图片类型，EaseMob没有做区分
    message.type = "img";
    add_message_to_conversation(message);
}

// 接收到透传消息
function receive_cmd_message(message) {
    
}

// 接收到音频消息
function receive_audio_message(message) {
    console.log(message);
    play_message_audio();
    message.type = "audio";
    add_message_to_conversation(message);
}

// 接收到地理位置消息
function receive_location_message(message) {
    
}

// 接收到文件消息
function receive_file_message(message) {
    console.log("接收到文件消息");
    console.log(message);
    play_message_audio();
    message.type = "file";
    add_message_to_conversation(message);
}

// 接收到视频消息
function receive_video_message(message) {
    
}

// 接收到失败消息
function receive_error_message(message) {
    console.log(message);
}

function query_friend_list(func) {
    if (friend_list.length > 0) {
        func();
    }else{
        conn.getRoster({
            success: function (roster) {
                var friends = [];
                $.each(roster, function (index, ros) {
                    if (ros.subscription === "both" || ros.subscription === "to") {
                        friends.push(ros);
                    }
                });
                $.each(friends, function (index, ros) {
                    query_user_info(ros.name, function (user_info) {
                        friend_list.push(user_info);
                        if (friend_list.length === friends.length) {
                            func();
                            return null;
                        }
                    });
                });
            }
        });
    }
}

// 新添加一条消息到回话列表中
function add_message_to_conversation(message) {
    // 对象添加属性
    message.contact = (message.from === current_user_id) ? message.to : message.from;

    var conversation = query_conversation_by_from(message.contact);
    if (conversation === null) {
        // 新建一条会话，并插入到会话列表中
        conversation = new Conversation(message);
        conversation.add_message(message);
        conversation.contact_user_info(function () {
            conversation_list.unshift(conversation);
            // 新增一条会话
            insert_conversation(conversation);
        });
    }else{
        conversation.add_message(message);
        // 会话中新增一条消息
        insert_message_for_conversation(conversation);
    }
}

// 查询form用户的回话
function query_conversation_by_from(contact) {
    var checked_conversation = null;
    // 检查该消息的发送者在会话列表中是否存在
    $.each(conversation_list, function (index, conversation) {
        if (conversation.contact === contact) {
            checked_conversation = conversation;
            return false;
        }
    });
    return checked_conversation;
}


// 处理消息解析
function txt_message_handler(error, id, send_msg, errorCode, errorText) {
    var msg = {
        id: id,
        type: "chat",
        from: current_user_id,
        to: send_msg.to,
        data: send_msg.body.msg,
        ext: send_msg.ext,
        error: error,
        errorCode: errorCode,
        errorText: errorText
    };
    return msg;
}

function file_message_response_handler(error, id, send_msg, errorCode, errorText) {
    console.log(send_msg);
    var msg = {
        id: id,
        type: send_msg.body.type,
        from: current_user_id,
        to: send_msg.to,
        url: send_msg.body.url,
        secret: send_msg.body.secret,
        ext: send_msg.ext,
        filename: send_msg.filename,
        error: error,
        errorCode: errorCode,
        errorText: errorText
    };
    return msg;
}

function time_message_handler() {
    var time_stamp = new Date().getTime();
    var msg = {
        id: time_stamp,
        type: "time",
        from: "",
        to: "",
        data: "",
        timeStamp: time_stamp,
        ext: {},
        error: "",
        errorCode: "",
        errorText: ""
    };
    return msg
}

function query_user_info_from_message(message, ease_mob) {
    for(var index=0, len = message.ext.user_list.length; index < len; index++) {
        var user_info = message.ext.user_list[index];
        if (user_info.ease_mob === ease_mob) {
            return user_info;
        }
    }
    return null;
}

/*=================  Util ===========*/
// 播放收到消息的音效
function play_message_audio() {
    // 判断是否播放音效
    if (alert_off) {
        return;
    }

    var audio = document.getElementById("audio-msg-play");
    audio.play();
}

// TODO: 内存缓存设计 1.hash_key->value 2.内存回收 3.命中率 参考：Memcached
function query_user_info(ease_mob, func) {
    // 1.查找缓存
    for (var i=0, len=cache_user_info_list.length; i < len; i++) {
        var user = cache_user_info_list[i];
        if (user.ease_mob.toString() === ease_mob.toString()) {
            func(user);
            return null;
        }
    }

    // 2.服务器异步查询
    request_user_ease_mob_info(ease_mob, function (data) {
        cache_user_info_list.unshift(data);
        func(data);
    });
}

function insert_user_info(user_info) {
    for (var i=0, len=cache_user_info_list.length; i < len; i++) {
        var user = cache_user_info_list[i];
        if (user.id.toString() === user_info.id.toString()) {
            return;
        }
    }
    cache_user_info_list.unshift(user_info);
}


