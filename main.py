#!/usr/bin/env python3
"""
咖啡数据分析项目主入口

启动方式：
    python main.py              # 启动 Streamlit 仪表盘
    python main.py --check      # 检查配置
    python main.py --test       # 测试坚果云连接
"""

import sys
import subprocess
from pathlib import Path


def start_dashboard():
    """启动 Streamlit 仪表盘"""
    app_path = Path(__file__).parent / "dashboards/coffee_import_export/app_enhanced.py"
    
    if not app_path.exists():
        print(f"❌ 找不到仪表盘应用: {app_path}")
        sys.exit(1)
    
    print("☕ 启动咖啡进口数据分析应用...")
    print("📊 功能特点：")
    print("  ✅ 坚果云实时数据 + 本地 CSV")
    print("  ✅ 月度九宫格可视化")
    print("  ✅ 累计九宫格可视化")
    print("  ✅ 预测功能")
    print()
    print("🚀 应用将在浏览器中打开: http://localhost:8501")
    print("💡 按 Ctrl+C 或运行 'python main.py --stop' 停止服务")
    print()
    
    subprocess.run(["streamlit", "run", str(app_path)])


def stop_dashboard():
    """停止 Streamlit 仪表盘"""
    import os
    try:
        # 获取占用 8501 端口的进程
        result = subprocess.run(
            ["lsof", "-ti:8501"], 
            capture_output=True, 
            text=True
        )
        pids = result.stdout.strip().split('\n')
        
        if pids and pids[0]:
            for pid in pids:
                if pid:
                    os.kill(int(pid), signal.SIGKILL)
            print("✅ 已停止仪表盘服务 (端口 8501)")
        else:
            print("ℹ️ 没有运行中的仪表盘服务")
    except Exception as e:
        print(f"❌ 停止失败: {e}")


def check_config():
    """检查配置"""
    script_path = Path(__file__).parent / "scripts/check_config.py"
    subprocess.run([sys.executable, str(script_path)])


def test_nutstore():
    """测试坚果云连接"""
    script_path = Path(__file__).parent / "scripts/test_nutstore.py"
    subprocess.run([sys.executable, str(script_path)])


def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ("--check", "-c"):
            check_config()
        elif arg in ("--test", "-t"):
            test_nutstore()
        elif arg in ("--stop", "-s"):
            stop_dashboard()
        elif arg in ("--help", "-h"):
            print(__doc__)
        else:
            print(f"❌ 未知参数: {arg}")
            print(__doc__)
            sys.exit(1)
    else:
        start_dashboard()


if __name__ == "__main__":
    main()
