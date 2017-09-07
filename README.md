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
9. django-extensions

# Info
1. 项目中的邮箱发送使用了RabbitMQ异步执行，所以需要自行安装RabbitMQ
```
 # 运行消费者脚本 
 python manage.py runscript send_active_email
```
       

2. Python2.x环境下的文本搜索使用了Sphinx(coreseek)搜索,具体安装教程参见
```
# 定时生成Sphinx索引脚本
* 3 * * * /bin/bash /usr/local/coreseek/script/build_index.sh > /dev/null 2>&1
```

```
# 启动Sphinx start_sphinx.sh
/usr/local/coreseek/bin/searchd -c /usr/local/coreseek/etc/sphinx.conf

# 停止Sphinx stop_sphinx.sh
/usr/local/coreseek/bin/searchd -c /usr/local/coreseek/etc/sphinx.conf --stop

# 索引生成脚本 build_index.sh
/usr/local/coreseek/bin/indexer -c /usr/local/coreseek/etc/sphinx.conf --all --rotate
```

3. Sphinx配置文件参考
[https://github.com/Eastwu5788/pony/blob/master/sphinx.conf](https://github.com/Eastwu5788/pony/blob/master/sphinx.conf)

4. Python3.x环境下的文本搜索使用了Whoosh+Jieba 
```
# Whoosh 初始索引脚本 使用了Djano的context
python manage.py runscript whoosh_script_init_index

# 使用Crontab定时重建索引 每天凌晨3点重建索引
* 3 * * * /usr/bin/python36 /path/pony/manage.py runscript whoosh_script_init_index > /dev/null 2>&1

# Whoosh 索引测试脚本
python36 manage.py runscript whoosh_script_test

# whoosh 增量更新索引脚本

```
# TODO
5. 群聊功能
6. 聊天表情消息升级使用字符替换

# Chat Update

# Contributions
