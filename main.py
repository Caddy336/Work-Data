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
    print()
    
    subprocess.run(["streamlit", "run", str(app_path)])


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
