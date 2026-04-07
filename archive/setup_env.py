import os

#获取当前工作目录
current_path=os.getcwd()
print(f"当前工作目录是：{current_path}")

#初始化需求工作路径，把路径定义成变量，方便以后修改
base_dir=current_path

#创建新的文件夹，如果文件夹已经存在，则提示用户
folder=["logs","data"]
for i in folder:
    new_dir=os.path.join(base_dir, i)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
        print(f"路径不存在，已创建新文件夹：{new_dir}")
    else:
        print(f"文件夹已存在：{new_dir}")

#检查文件权限，判断是否有权限访问某个文件
test_dir="/etc/hosts"
if os.access(test_dir,os.R_OK):
    print(f"此文件有权限阅读：{test_dir}")
else:
    print(f"权限不足，无法查看文件：{test_dir}")
    