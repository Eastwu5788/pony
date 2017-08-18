// 存储所有回话的列表
var conversation_list = [];

function user(data) {

}

function Conversation(message) {
    this.from = message.from;
    this.to = message.to;
    this.messages = [message];

    // 向回话中追加一跳新消息
    this.add_message = function (message) {
        this.messages.append(message);
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
}

// 环信退出
function logout_ease_mob_im() {
    conn.close();
}

// 连接成功回调
function login_success(message) {
    console.log(message)
}

// 断开连接回调
function logout_success(message) {
    
}

// 接收到文本消息
function receive_text_message(message) {
    console.log(message);
    // 接收到消息后，需要讲消息追加到回话中
    add_message_to_conversation(message);
}

// 接收到表情消息
function receive_emoji_message(message) {

}

// 接收到图片消息
function receive_pic_message(message) {
    
}

// 接收到透传消息
function receive_cmd_message(message) {
    
}

// 接收到音频消息
function receive_audio_message(message) {
    
}

// 接收到地理位置消息
function receive_location_message(message) {
    
}

// 接收到文件消息
function receive_file_message(message) {
    
}

// 接收到视频消息
function receive_video_message(message) {
    
}

// 接收到失败消息
function receive_error_message(message) {
    console.log(message);
}

// 新添加一条消息到回话列表中
function add_message_to_conversation(message) {
    var conversation = query_conversation_by_from(message.form);
    if (conversation == null) {
        // 新建一条会话，并插入到会话列表中
        conversation = new Conversation(message);
        conversation_list.unshift(conversation);
        // 新增一条会话
        insert_conversation(conversation);
    }else{
        conversation.add_message(message);
        // 会话中新增一条消息
        insert_message_for_conversation(conversation);
    }
}

// 查询form用户的回话
function query_conversation_by_from(from) {
    // 检查该消息的发送者在会话列表中是否存在
    for (var conversation in conversation_list) {
        if (conversation.from = from) {
            return conversation;
        }
    }
    return null
}