## Setup ##

When you want to make a new post, simply place either a html or markdown file in docs/.  Files without a .html or .md ending will not be processed; files with a .md ending will be processed with markdown before being published.

Tip: name your files based on the date like so yyyymmdd, this way mBlog will display the most recent post first.

## How it works ##

index.php lists all of the files in $directory, sorts them and then prints them.  The order of sort can be changed.

## Directories ##

You can add directories to docs/, and have posts in them.  mBlog will automatically generate a menu allowing you to browse the directory structure.
