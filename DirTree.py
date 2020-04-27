"""
DirTree.py
版本：v1.0
最后更新时间：2020 04,27
状态：烂尾
"""


# 登入需要的库
import os
import sys
# 如果是win系统，导入第三方库psutil获取所有硬盘名称
# 没有这个库则pip安装
if sys.platform.lower()[:3] == "win":
    try:
        import psutil
    except ModuleNotFoundError:
        print("安装所缺库，稍等......")
        os.system("pip3 install psutil -i https://mirrors.ustc.edu.cn/pypi/web/simple/")
        print("安装完成")
        import psutil


class DirTree:
    def __init__(self):
        # 判断用户操作系统
        # 根据操作系统获取文件路径分隔符(\和/)
        # win系统获取所有盘符，linux获取/目录下文件，如：/home
        if sys.platform.lower() == "linux":
            self.OperatingSystem = "linux"
            self.PathSpilt = "/"
            self.RootFile = ["/"+i for i in os.listdir("/")]
        elif sys.platform.lower()[:3] == "win":
            self.OperatingSystem = "win"
            self.PathSpilt = "\\"
            self.RootFile = sorted([driver.device for driver in psutil.disk_partitions(True)])
        # 用字典来代表目录树
        self.tree = {i: {} for i in self.RootFile}
        # 文件/文件夹状态 open/close
        self.FileStatus = {}
        # 文件/文件夹编号
        self.FileNumber = {}

    # 清除控制台
    def clear(self):
        os.system("clear") if self.OperatingSystem == "linux" else os.system("cls")

    # 设置文件状态
    def SetFileStatus(self, files):
        # 默认所有文件状态为close
        for file in files:
            if self.FileStatus.get(file) is None:
                self.FileStatus[file] = "close"
            if files.get(file) != {}:
                self.SetFileStatus(files[file])

    # 设置文件编码
    def SetFileNumber(self, files):
        numbers = 1
        for file in files:
            if self.FileNumber.get(file) is None:
                while numbers in self.FileNumber.values():
                    numbers += 1
                self.FileNumber[file] = numbers
            if files.get(file) != {}:
                self.SetFileNumber(files[file])
            # numbers += 1

    def print_tree(self, tree, n=0):
        # 每次调用print_tree更新一次文件状态和编码
        self.SetFileStatus(tree)
        self.SetFileNumber(tree)
        # 递归遍历tree所有键，也就是文件
        for key in tree.keys():
            # 键的状态是close用▶表示, open用▼表示，前提是键是文件夹
            if os.path.isdir(key) is True:
                status = "▶" if self.FileStatus.get(key) == "close" else "▼"
            else:
                status = " "
            number = self.FileNumber.get(key)
            if self.OperatingSystem == "win":
                # 如果是win系统并且分割符只有两个，说明tree里只有盘符，filename等于键，也就是盘符
                if len(key.split(self.PathSpilt)) == 2:
                    filename = key
                # 否则是key分隔后最后一个
                else:
                    filename = key.split(self.PathSpilt)[-1]
            else:
                filename = key.split(self.PathSpilt)[-1]

            # 输出： 文件状态(status) 编号(number) 名字(filename)
            print(f'{"  "*n}{status}   {number}. {filename}')
            # 如果还有文件则进行递归
            if tree[key] != {}:
                self.print_tree(tree[key], n+1)

    # 打开/关闭文件夹
    def OpenFolder(self, foldernumber):
        # 先把self.FileNumber键值调换，然后通过键获取文件夹路径
        folder = {self.FileNumber.get(f): f for f in self.FileNumber.keys()}.get(int(foldernumber))
        # 判断特殊情况并取消打开
        if folder is None:
            self.clear()
            print("没有这个文件夹")
        elif os.path.isdir(folder) is False:
            self.clear()
            print("暂不支持打开非文件夹")
        # 没有特殊情况则打开/关闭文件夹，并把文件夹下文件添加/删除在self.tree里
        else:
            if self.FileStatus.get(folder) == "close":
                self.FileStatus[folder] = "open"
                for i in os.listdir(folder):
                    self.tree[folder][i] = {}
                self.clear()
            elif self.FileStatus.get(folder) == "open":
                self.FileStatus[folder] = "close"
                self.FileNumber = {}
                for i in os.listdir(folder):
                    self.tree[folder] = {}
                self.clear()
        # print(self.FileNumber)

    def main(self):
        self.clear()
        while 1:
            self.print_tree(self.tree)
            self.OpenFolder(input())


DirTree().main()
