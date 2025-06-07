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

# 方案1：使用Modal容器服务（推荐）
@app.cls(
    image=image,
    scaledown_window=3600,  # 3600s后才缩容，实际上保持长期运行
)
@modal.concurrent(max_inputs=1)  # 允许1个并发请求
class BackgroundService:
    # 使用Modal的新式参数声明，移除__init__
    process: subprocess.Popen = None
    start_time: datetime = None
        
    @modal.method()
    def start_service(self):
        """启动后台服务"""
        if self.process and self.process.poll() is None:
            return "Service already running"
            
        os.chdir("/workspace")
        self.start_time = datetime.now()  # 在这里初始化时间
        print(f"🟢 Starting background service at {self.start_time}")
        
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
            if self.start_time:
                uptime = datetime.now() - self.start_time
                return f"Service running for {uptime}, PID: {self.process.pid}"
            else:
                return f"Service running, PID: {self.process.pid}"
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

# 方案2：无限循环带重启机制
@app.function(
    image=image,
    timeout=None,  # 无超时限制
    retries=0  # 禁用自动重试，我们自己处理
)
def run_persistent_task():
    """运行持久化任务"""
    restart_count = 0
    max_restarts = 100  # 最大重启次数限制
    
    while restart_count < max_restarts:
        try:
            os.chdir("/workspace")
            print(f"🟢 Starting task (attempt {restart_count + 1}) at {datetime.now()}")
            
            # 启动主进程
            process = subprocess.Popen(
                [sys.executable, "app.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # 监控进程输出
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {output.strip()}")
            
            # 进程退出处理
            return_code = process.returncode
            
            if return_code == 0:
                print("✅ Task completed successfully")
                break
            else:
                print(f"❌ Task failed with code {return_code}")
                stderr = process.stderr.read()
                if stderr:
                    print(f"Error output: {stderr}")
                
                restart_count += 1
                if restart_count < max_restarts:
                    wait_time = min(60 * restart_count, 300)  # 指数退避，最多5分钟
                    print(f"🔄 Restarting in {wait_time} seconds...")
                    time.sleep(wait_time)
                
        except KeyboardInterrupt:
            print("🛑 Received interrupt signal")
            if 'process' in locals():
                process.terminate()
            break
            
        except Exception as e:
            print(f"🔴 Unexpected error: {e}")
            restart_count += 1
            if restart_count < max_restarts:
                time.sleep(60)
    
    print(f"🏁 Task ended after {restart_count} restarts")

# 方案3：使用定时健康检查
@app.function(
    image=image,
    schedule=modal.Cron("*/5 * * * *")  # 每5分钟检查一次
)
def health_check():
    """定时健康检查和重启"""
    try:
        # 这里可以添加健康检查逻辑
        # 比如检查日志文件、网络连接等
        service = BackgroundService()
        status = service.check_status.remote()
        print(f"Health check: {status}")
        
        # 如果服务停止，自动重启
        if "stopped" in status.lower():
            print("🔄 Auto-restarting stopped service")
            service.restart_service.remote()
            
    except Exception as e:
        print(f"Health check failed: {e}")

# 启动脚本
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["service", "persistent", "deploy"], 
                       default="deploy", help="运行模式")
    args = parser.parse_args()
    
    if args.mode == "service":
        # 启动容器服务
        print("🚀 Starting container service...")
        service = BackgroundService()
        result = service.start_service.remote()
        print(result)
        
    elif args.mode == "persistent":
        # 运行持久化任务
        print("🚀 Starting persistent task...")
        run_persistent_task.remote()
        
    else:
        # 部署应用
        print("🚀 Deploying application...")
        app.deploy("background-task-deployment")
