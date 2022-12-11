创建新的分支
在新分支下创建和提交
然后删除主分支
修改当前分支名字为主分支名字
将当前分支强行推上去

```bash
git checkout --orphan clean_log
git add .
git commit -m "add"
git branch -D master
git branch -m master
git push -f origin master
```