<?php

# mBlog v0.4.0 - Copyright 2012 Lachlan Main <lachlan.main@gmail.com>
# Licensed under the GPL version 3 <http://www.gnu.org/licenses/gpl-3.0.html>

require_once 'markdown.php';
require_once 'microtpl.php';

$title = 'Whatever1992'; # title of your blog
$root = __DIR__ . '/docs/';  # directory with html files


$tpl = new MicroTpl();
$dir = isset($_GET['dir']) ? $_GET['dir'] : null;

if (!is_dir($root . $dir) || strstr($dir, '..'))
  $tpl->error = true;
else{
  foreach(scandir($root . $dir, SCANDIR_SORT_DESCENDING) as $item){
    if (in_array($item, array('.', '..')))
      continue;
    if (is_file($root . $dir . $item)){
      $ext = strtolower(preg_filter('/^.*\.([^\.]+)$/', '\1', $item));
      if (in_array($ext, array('md', 'html', 'mkd'))){
        $text = file_get_contents($root . $dir . $item);

        //如果是 'md' or 'mkd' 就用Markdown
        if (($ext == 'md') || ($ext == 'mkd'))
          $text = Markdown($text,  $dir);
        $tpl->texts[] = array('text' => $text);
      }
    }
    else
      $tpl->dirs[] = array('dir' => $item, 'dirLink' => $dir . $item);
  }
}


//添加返回上层的导航
$formdir = substr($dir,0,-1);

if (strrpos($formdir, "/") != false){
  $formdir =  substr($formdir,0,strrpos($formdir, "/")+1);
  // echo $formdir;
}
else{
  $formdir = "";
}


$tpl->title = $title;
$tpl->dir = $dir;



$tpl->formdir = $formdir;

ob_start();

?>

<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{title}</title>
    <link href="style.css" rel="stylesheet">
    <link rel="shortcut icon" href="/whateverblog/img/favicon2.ico" type="image/x-icon" />
  </head>


  <body>
    <!--header>{title} /{dir}</header!-->
    <header>{title}</header>

    <nav>
      <!-- 左边的导航 -->
      <ul>
        <li><a href="./" style="font-size:15px; color:#ff9900">首页</a></li>

        <li><a href="./?dir={formdir}" style="font-size:14px; color:#ff9900">上一页</a></li>
        {@dirs}
        <li><a href="./?dir={dirLink}/" style="font-size:14px; color:#ff9900">{dir}</a></li>
        {/dirs}
      </ul>
    </nav>

    <!--右边的markdown-->
    {@texts}
      <article>{&text}</article>
    {/texts}



    {?error}
      <article><h1>Error</h1><p>The page you are looking for is not here.</p></article>
    {/error}


<br/>
<br/>
    <div id="copyright">Copyright &copy; 2012-2013 whatever's blog Network Association. Email: linyiyu1992@gmail.com</div>

  </body>
</html>


<?php $tpl->render(ob_get_clean()); ?>
