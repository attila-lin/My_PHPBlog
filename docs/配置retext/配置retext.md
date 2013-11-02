#配置Retext

----

原来以为Retext是不能配置css的，正决定wine个MarkPad，同学搜到了配置方法

    cd ~/.config/ReText Project/
    
该目录下有个ReText.conf

    vim ReText.conf
    
    
    [General]
    useReST=false
    defaultExt=md
    useWebkit=true
    styleSheet=/home/whatever/.config/ReText project/github.css
    autoSave=true
    recentFileList=/home/whatevr/\x6587\x6863/test.md    
    //最后一行好像没什么用啊

然后再新建个github.css，可以点[这里](https://gist.github.com/andyferra/2554919)下载。
 
顺便被推荐一个在线编辑markdown: [dillinger](http://dillinger.io/#)

可以和dropbox连接，问题是图片和不能直接export为html。