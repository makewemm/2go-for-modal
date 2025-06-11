import modal
import subprocess
import sys
import os
from pathlib import Path

app = modal.App(name="books-app")

# 构建镜像
image = (
    modal.Image.debian_slim()
    .apt_install("curl", "git")
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path="/workspace")
)

# 定义需要的环境变量 - 在Modal网站上设置这些secrets
# 方法1: 使用Modal Secrets (推荐)
@app.function(
    image=image,
    timeout=86400,
    secrets=[
        modal.Secret.from_name("custom-secret"),  # 在Modal网站创建名为"app-secrets"的secret
        # modal.Secret.from_name("database-secrets"),  # 可以添加多个secrets
    ],
    cpu=1.0,
    memory=1024,
)
def run_app_with_secrets():
    """使用Modal Secrets运行应用"""
    os.chdir("/workspace")
    
    # Modal会自动将secrets注入到环境变量中
    print("🟢 Environment variables loaded from Modal Secrets")
    print("🟢 Starting app.py with environment variables...")
    
    # 打印部分环境变量（仅用于调试，生产环境中应移除）
    env_vars = [key for key in os.environ.keys() if not key.startswith('_')]
   # print(f"📋 Available environment variables: {len(env_vars)} total")
    
    # 检查app.py是否存在
    if not Path("app.py").exists():
        print("🔴 Error: app.py not found in /workspace")
        return
    
    # 运行app.py，环境变量会自动传递
    process = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True,
        env=os.environ.copy()  # 显式传递环境变量
    )
    
    # 实时打印标准输出
    try:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
    except KeyboardInterrupt:
        print("🟡 Received interrupt signal, terminating process...")
        process.terminate()
        process.wait()
        return
    
    # 检查进程退出状态
    if process.returncode != 0:
        error = process.stderr.read()
        print(f"🔴 Process failed with code {process.returncode}")
        if error:
            print(f"🔴 Error output: {error}")
        raise modal.exception.ExecutionError("Script execution failed")
    else:
        print("✅ app.py completed successfully")

if __name__ == "__main__":
    print("🚀 Deploying application...")
    
    # 选择要部署的函数
    # 推荐使用secrets方式
    print("📋 Available deployment options:")
    print("1. run_app_with_secrets (recommended)")
    
    app.deploy("production-deployment")
