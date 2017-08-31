# Pony
我的个人博客源代码

# DB
[https://github.com/Eastwu5788/pony/wiki](https://github.com/Eastwu5788/pony/wiki)

# Requirements
1. Django
2. pymysql
3. MySQLClient
4. mistune
5. pillow
6. python3-memcached
7. redis
8. pika
9. django-sphinx

# Info
1. 项目中的邮箱发送使用了RabbitMQ异步执行，所以需要自行安装RabbitMQ。<br>
   添加消息的生产者脚本: message_queue.py<br>
   处理消息的消费者脚本: send_active_email.py（此脚本需要独立运行 /pony/app/modules/jobs/send_active_email.py)<br>
        运行消费者脚本: python send_active_email.py<br>

2. 项目中的文本搜索使用了Sphinx(coreseek)搜索,具体安装教程参见
[http://www.keyunq.com/server/coreseek-sphinx.html](http://www.keyunq.com/server/coreseek-sphinx.html)
 
# TODO
1. <del>RabbitMQ发送认证邮箱，解决注册时接口过慢问题<del>
2. <del>用户关注、取消关注、好友列表、粉丝列表功能<del>
3. <del>聊天中的好友搜索功能 打算使用Sphinx模糊检索用户昵称<del>
4. <del>聊天时的用户个人信息修改功能<del>
5. 群聊功能
6. 聊天表情消息升级使用字符替换
7. <del>首页样式修改，显示更多文章（右侧添加最新文章列表）<del>
8. <del>首页右侧添加阅读排行榜<del>
9. <del>用户默认头像设置 使用gravatar的头像生成算法<del>

# Chat Update

# Contributions
