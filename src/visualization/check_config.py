#!/usr/bin/env python3
"""
查看当前坚果云配置状态
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def check_config():
    """检查配置状态"""
    print("\n" + "=" * 70)
    print("🔍 坚果云配置状态检查")
    print("=" * 70 + "\n")
    
    secrets_file = project_root / ".streamlit" / "secrets.toml"
    
    # 检查配置文件是否存在
    if not secrets_file.exists():
        print("❌ 配置文件不存在")
        print(f"   路径: {secrets_file}")
        print("\n💡 运行以下命令创建配置：")
        print("   python src/visualization/setup_nutstore.py\n")
        return False
    
    print(f"✅ 配置文件存在: {secrets_file}\n")
    
    # 读取配置
    try:
        with open(secrets_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查必要的字段
        has_email = 'email' in content and 'your-email' not in content
        has_password = 'app_password' in content and 'your-app-password' not in content
        
        print("-" * 70)
        print("📋 配置内容检查")
        print("-" * 70)
        
        if has_email:
            print("✅ 邮箱已配置")
            # 尝试提取邮箱（仅显示部分）
            for line in content.split('\n'):
                if 'email' in line and '=' in line:
                    email = line.split('=')[1].strip().strip('"\'')
                    if email and 'your-email' not in email:
                        masked_email = email[0] + "***" + email[email.index('@'):] if '@' in email else "***"
                        print(f"   📧 {masked_email}")
        else:
            print("❌ 邮箱未配置")
        
        if has_password:
            print("✅ 应用密码已配置")
            print("   🔑 ********")
        else:
            print("❌ 应用密码未配置")
        
        print()
        
        if has_email and has_password:
            print("=" * 70)
            print("🎉 配置完整！")
            print("=" * 70)
            print("\n✅ 你可以进行下一步：")
            print("\n1. 测试连接：")
            print("   python src/visualization/test_nutstore.py")
            print("\n2. 运行仪表板：")
            print("   streamlit run dashboards/coffee_import_export/app.py\n")
            return True
        else:
            print("=" * 70)
            print("⚠️  配置不完整")
            print("=" * 70)
            print("\n请编辑配置文件：")
            print(f"   {secrets_file}")
            print("\n或重新运行配置助手：")
            print("   python src/visualization/setup_nutstore.py\n")
            return False
            
    except Exception as e:
        print(f"❌ 读取配置文件失败: {str(e)}\n")
        return False


def check_dependencies():
    """检查依赖安装状态"""
    print("-" * 70)
    print("📦 依赖检查")
    print("-" * 70 + "\n")
    
    dependencies = {
        'streamlit': 'Streamlit',
        'plotly': 'Plotly',
        'openpyxl': 'OpenPyXL',
        'webdav3': 'WebDAV Client'
    }
    
    all_installed = True
    
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} (未安装)")
            all_installed = False
    
    print()
    
    if not all_installed:
        print("💡 运行以下命令安装依赖：")
        print("   pip install -r requirements.txt\n")
    
    return all_installed


def main():
    """主函数"""
    has_config = check_config()
    print()
    has_deps = check_dependencies()
    
    if has_config and has_deps:
        print("=" * 70)
        print("🚀 一切就绪！可以开始使用了")
        print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
