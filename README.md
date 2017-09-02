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
 python send_active_email.py<br>
```
       

2. Python2.x环境下的文本搜索使用了Sphinx(coreseek)搜索,具体安装教程参见
```
# 启动Sphinx
/usr/local/coreseek/bin/searchd -c /usr/local/coreseek/etc/sphinx.conf

# 停止Sphinx
/usr/local/coreseek/bin/searchd -c /usr/local/coreseek/etc/sphinx.conf --stop

# 索引生成脚本
/usr/local/coreseek/bin/indexer -c /usr/local/coreseek/etc/sphinx.conf --all --rotate
```

3.Sphinx配置文件参考
```
source blog_article
{
        type                                    = mysql

        sql_host                                = localhost
        sql_user                                = root
        sql_pass                                = wudong
        sql_db                                  = b_blog
        sql_port                                = 3306  # optional, default is 3306
        # 确保中文有效
        sql_query_pre                           = SET NAMES utf8
        #sql_query_pre                          = SET SESSION query_cache_type=OFF
        sql_query                               = SELECT id,id as aid, user_id, title, content, updated_time FROM blog_article where status = '1'

        sql_attr_uint                           = aid
        sql_attr_timestamp                      = updated_time
        # 确保中文有效
        sql_query_info_pre                      = SET NAMES utf8
        sql_query_info                          = SELECT * FROM blog_article WHERE id=$id
}

# 索引， 当有数据源后，从数据源处构建索引。 索引实际上就是相当于一个字典检索。
# 有了整本字典内容以后，才会有字典检索
index article
{
        source                                  = blog_article
        path                                    = /usr/local/coreseek/var/data/article
        docinfo                                 = extern
        charset_dictpath                        = /usr/local/mmseg/etc/
        # 确保中文有效
        charset_type                            = zh_cn.utf-8
        min_infix_len                           = 2
}

indexer
{
        mem_limit                               = 32M
}

# 提供搜索查询服务。一般以deamon的形式运行在后台
searchd
{
        port                                    = 9312
        log                                     = /usr/local/coreseek/var/log/searchd.log
        query_log                               = /usr/local/coreseek/var/log/query.log
        read_timeout                            = 5
        max_children                            = 30
        pid_file                                = /usr/local/coreseek/var/log/searchd.pid
        max_matches                             = 1000
        seamless_rotate                         = 1
        preopen_indexes                         = 0
        unlink_old                              = 1
}
```

3. Python3.x环境下的文本搜索使用了Whoosh+Jieba 
```
# Whoosh 初始索引脚本 使用了Djano的context
# path: pony/app/scripts/whoose_script_init_index.py
python manage.py runscript whoosh_script_init_index

# whoosh 更新索引脚本

```
# TODO
5. 群聊功能
6. 聊天表情消息升级使用字符替换

# Chat Update

# Contributions
