# 将下面的 Python 代码保存到 Packages/User 目录下
# （可以通过点击 Preferences -> Browse Packages 进入 Packages 目录，然后再进入 User 目录）
# 并命名为 remove_comments.py。

# 使用时用 Ctrl+` 打开控制台，然后输入下面一行命令即可
# view.run_command('remove_comments')

import sublime_plugin
class RemoveCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        comments = self.view.find_by_selector('comment')
        for region in reversed(comments):
            self.view.erase(edit, region)