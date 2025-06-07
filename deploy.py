import modal
import subprocess
import sys
import os
import time
import signal
from datetime import datetime

app = modal.App(name="persistent-background-task")

# 构建镜像
image = (
    modal.Image.debian_slim()
    .apt_install("curl", "supervisor")  # 添加supervisor进程管理
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path="/workspace")
)

# 使用Modal容器服务
@app.cls(
    image=image,
    container_idle_timeout=0,  # 永不超时
    allow_concurrent_inputs=10,  # 允许并发请求
)
class BackgroundService:
    def __init__(self):
        self.process = None
        self.start_time = datetime.now()
        
    @modal.method()
    def start_service(self):
        """启动后台服务"""
        if self.process and self.process.poll() is None:
            return "Service already running"
            
        os.chdir("/workspace")
        print(f"🟢 Starting background service at {datetime.now()}")
        
        self.process = subprocess.Popen(
            [sys.executable, "app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        return f"Service started with PID: {self.process.pid}"
    
    @modal.method()
    def check_status(self):
        """检查服务状态"""
        if not self.process:
            return "Service not started"
            
        if self.process.poll() is None:
            uptime = datetime.now() - self.start_time
            return f"Service running for {uptime}, PID: {self.process.pid}"
        else:
            return f"Service stopped with exit code: {self.process.returncode}"
    
    @modal.method()
    def stop_service(self):
        """停止服务"""
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
            return "Service stopped"
        return "Service not running"
    
    @modal.method()
    def restart_service(self):
        """重启服务"""
        self.stop_service()
        time.sleep(2)
        return self.start_service()
