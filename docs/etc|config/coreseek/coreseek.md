CoreSeek的配置
====

在建立书站的时候，需要用到搜索，于是想配置一个搜索引擎，发现开源的coreseek有php接口而且是Sphinx的中文版（添加了中文分词，用了mmseg）。

###CoreSeek快速安装：
    
    ##下载coreseek：coreseek 3.2.14：点击下载、coreseek 4.0.1：点击下载、coreseek 4.1：点击下载
    $ wget http://www.coreseek.cn/uploads/csft/3.2/coreseek-3.2.14.tar.gz
    $ 或者 http://www.coreseek.cn/uploads/csft/4.0/coreseek-4.0.1-beta.tar.gz
    $ 或者 http://www.coreseek.cn/uploads/csft/4.0/coreseek-4.1-beta.tar.gz
    $ tar xzvf coreseek-3.2.14.tar.gz 或者 coreseek-4.0.1-beta.tar.gz 或者 coreseek-4.1-beta.tar.gz
    $ cd coreseek-3.2.14 或者 coreseek-4.0.1-beta 或者 coreseek-4.1-beta
    
    ##前提：需提前安装操作系统基础开发库及mysql依赖库以支持mysql数据源和xml数据源
    ##安装mmseg
    $ cd mmseg-3.2.14
    $ ./bootstrap    #输出的warning信息可以忽略，如果出现error则需要解决
    $ ./configure --prefix=/usr/local/mmseg3
    $ make && make install
    $ cd ..
    
    ##安装coreseek
    $ cd csft-3.2.14 或者 cd csft-4.0.1 或者 cd csft-4.1
    $ sh buildconf.sh    #输出的warning信息可以忽略，如果出现error则需要解决
    $ ./configure --prefix=/usr/local/coreseek  --without-unixodbc --with-mmseg --with-mmseg-includes=/usr/local/mmseg3/include/mmseg/ --with-mmseg-libs=/usr/local/mmseg3/lib/ --with-mysql    ##如果提示mysql问题，可以查看MySQL数据源安装说明
    $ make && make install
    $ cd ..

    ##测试mmseg分词，coreseek搜索（需要预先设置好字符集为zh_CN.UTF-8，确保正确显示中文）
    $ cd testpack
    $ cat var/test/test.xml    #此时应该正确显示中文
    $ /usr/local/mmseg3/bin/mmseg -d /usr/local/mmseg3/etc var/test/test.xml
    $ /usr/local/coreseek/bin/indexer -c etc/csft.conf --all
    $ /usr/local/coreseek/bin/search -c etc/csft.conf 网络搜索

具体可以看[官网](http://www.coreseek.cn/products-install/install_on_bsd_linux/)

###CoreSeek的配置文件：

有例子，可以对照自己的需求配置，贴一下自己的。
    #MySQL数据源配置，详情请查看：http://www.coreseek.cn/products-install/mysql/
    #请先将var/test/documents.sql导入数据库，并配置好以下的MySQL用户密码数据库
    
    #源定义
    source mysql
    {
        type                    = mysql
    
        sql_host                = localhost
        sql_user                = ****
        sql_pass                = ********
        sql_db                  = PHPLibrary
        sql_port                = 3306
        sql_query_pre           = SET NAMES utf8
    
        sql_query               = SELECT bno, category, title, press, year, author, price, briefcontent, labels, ISBN FROM book
                                                                  #sql_query第一列id需为整数
                                                                  #title、content作为字符串/文本字段，被全文索引
                                
        #sql_attr_uint          = group_id           #从SQL读取到的值必须为整数
        #sql_attr_timestamp     = date_added #从SQL读取到的值必须为整数，作为时间属性
    
        sql_query_info_pre      = SET NAMES utf8                                        #命令行查询时，设置正确的字符集
        sql_query_info          = SELECT * FROM documents WHERE id=$id #命令行查询时，从数据库读取原始数据信息
    }
    
    #index定义
    index mysql
    {
        source            = mysql                           #对应的source名称
        path              = var/data/mysql                  #请修改为实际使用的绝对路径，例如：/usr/local/coreseek/var/...
        docinfo           = extern
        mlock             = 0
        morphology        = none
        min_word_len      = 1
        html_strip        = 0
    
        #中文分词配置，详情请查看：http://www.coreseek.cn/products-install/coreseek_mmseg/
        charset_dictpath  = /usr/local/mmseg3/etc/           #BSD、Linux环境下设置，/符号结尾
        #charset_dictpath = etc/                             #Windows环境下设置，/符号结尾，最好给出绝对路径，例如：C:/usr/local/coreseek/etc/...
        charset_type      = zh_cn.utf-8
    }
    
    #全局index定义
    indexer
    {
        mem_limit         = 128M
    }
    
    #searchd服务定义
    searchd
    {
        listen            = 9312
        read_timeout      = 5
        max_children      = 30
        max_matches       = 1000
        seamless_rotate   = 0
        preopen_indexes   = 0
        unlink_old        = 1
        pid_file          = var/log/searchd_mysql.pid           #请修改为实际使用的绝对路径，例如：/usr/local/coreseek/var/...
        log               = var/log/searchd_mysql.log           #请修改为实际使用的绝对路径，例如：/usr/local/coreseek/var/...
        query_log         = var/log/query_mysql.log             #请修改为实际使用的绝对路径，例如：/usr/local/coreseek/var/...
        binlog_path       =                                     #关闭binlog日志
        compat_sphinxql_magics = 0  
    }
    
###CoreSeek的使用：
    
    $ cd /var/www/PHPLibrary/coreseek
    $ /usr/local/coreseek/bin/searchd -c etc/csft_mysql.conf // 打开引擎

