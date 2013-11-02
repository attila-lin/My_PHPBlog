#修改mBlog

---

曾经介绍过mBlog，是一个轻量的Blog。语言实现——php，和markdown一起使用。使用方法方便，将markdown文件放在docs目录下就好了。

实现一些要求：

+ 有返回上层目录的功能
+ markdown有添加图片功能
+ 评论功能
+ markdown的一些配置
+ 界面的一些改善



##index.php

    24  if (in_array($ext, array('md', 'html'))){  //加个'mkd'
    
    26        if ($ext == 'md')           //if (($ext == 'md') || ($ext == 'mkd'))

