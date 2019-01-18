# Linux Shell Cookbook

## Commonly Used Commands

### wc
wc gives a "**word count**" on a file or I/O stream.

* wc -w gives only the word count.
* wc -l gives only the line count.
* wc -c gives only the byte count.
* wc -m gives only the character count.

### cut
A tool for **extracting fields from files**. It is similar to the `print $N` command set in `awk`, but more limited. It may be simpler to use cut in a script than `awk`. Particularly important are the -d (delimiter) and -f (field specifier) options.

List all the users in /etc/passwd:
```
cut -d: -f1 /etc/passwd
```

### awk
AWK is a field-oriented pattern processing language with a C-style syntax. AWK was created at Bell Labs in the 1970s, and **its name is derived from the family names of its authors** – Alfred Aho, Peter Weinberger, and Brian Kernighan.

`awk 'patten {action}' file`

`awk` command is used to handle fields in one line. Analize every line in the file, and if the line match the patten, then do the action. pattern field is optional. `$0` indicates the whole line. The first field is `$1`.

`awk -Fchar '{action}'`

Seperate the line into different fileds by single char. No blank is between -F and char.

```
awk '$2 > 23 {print $1, $3, $4} file.txt'
awk -F: '{print $1}' file.txt
```

### sed
a non-interactive text file editor. Non-interactive "**stream editor**".

`'[position line]r source.txt' target.txt`

Find the line from target.txt through position line, and then read all lines from source.txt, at last put all lines after the line position in target.txt.

### uniq
Uniq command is helpful to remove or detect duplicate entries in a file.

```
uniq <file>
```

Count Number of Occurrences using -c option

```
uniq -c <file>
```

## Tips
### 取得当前正在执行的脚本的绝对路径

```
#!/bin/bash
basepath=$(cd `dirname $0`; pwd)
echo $basepath
```
