import modal
import subprocess
import sys
import os

app = modal.App(name="persistent-app-v2")  # 修改应用名避免冲突

# 构建镜像（使用最新API）
image = (
    modal.Image.debian_slim()
    .apt_install("curl")  # 安装curl
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path="/workspace")  # 复制本地代码到镜像
)

@app.function(
    image=image,
    timeout=86400  # 运行最长一天
)
def run_app():
    """运行主应用程序"""
    os.chdir("/workspace")
    print("🟢 Starting app.py...")

    process = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    # 实时打印标准输出
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())

    # 如果进程退出码非0，打印错误信息
    if process.returncode != 0:
        error = process.stderr.read()
        print(f"🔴 Process failed with code {process.returncode}: {error}")
        raise modal.exception.ExecutionError("Script execution failed")

if __name__ == "__main__":
    # 只做部署，不自动运行
    print("🚀 Deploying application...")
    app.deploy("production-deployment")
