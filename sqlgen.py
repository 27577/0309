import subprocess

# 设置目标目录
target_directory = "queries"
# 循环22次，为每个文件生成对应的命令
for i in range(1, 23):  # 假设你有22个这样的命令，从1到22
    command = f"qgen -d {i} >d{i}.sql"
    # 在指定的目录中执行命令
    subprocess.run(command, shell=True, check=True, cwd=target_directory)
