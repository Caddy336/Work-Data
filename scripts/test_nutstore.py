"""
测试坚果云连接和数据加载
运行此脚本以验证配置是否正确
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.visualization.nutstore_loader import NutStoreLoader, load_coffee_data
import os


def test_connection():
    """测试坚果云连接"""
    print("=" * 60)
    print("🧪 测试坚果云连接")
    print("=" * 60)
    
    # 从环境变量或 secrets.toml 读取凭证
    email = os.getenv("NUTSTORE_EMAIL")
    password = os.getenv("NUTSTORE_PASSWORD")
    
    if not email or not password:
        print("\n⚠️  请设置环境变量：")
        print("   export NUTSTORE_EMAIL='your-email@example.com'")
        print("   export NUTSTORE_PASSWORD='your-app-password'")
        print("\n或者直接在代码中填入（仅用于测试）：")
        
        email = input("\n请输入坚果云邮箱: ").strip()
        password = input("请输入坚果云应用密码: ").strip()
    
    try:
        # 创建加载器
        print(f"\n📧 使用账号: {email}")
        loader = NutStoreLoader(email, password)
        
        # 检查连接
        if loader.check_connection():
            print("✅ 连接成功！\n")
            return loader
        else:
            print("❌ 连接失败！\n")
            return None
            
    except Exception as e:
        print(f"❌ 错误: {str(e)}\n")
        return None


def test_list_files(loader):
    """测试列出文件"""
    print("=" * 60)
    print("📁 测试列出坚果云文件")
    print("=" * 60)
    
    try:
        # 列出根目录
        print("\n正在列出根目录文件...\n")
        files = loader.list_files()
        
        if files:
            print(f"找到 {len(files)} 个文件/文件夹：")
            for i, file in enumerate(files[:10], 1):  # 只显示前10个
                print(f"  {i}. {file}")
            
            if len(files) > 10:
                print(f"  ... 还有 {len(files) - 10} 个文件\n")
        else:
            print("未找到文件\n")
            
    except Exception as e:
        print(f"❌ 列出文件失败: {str(e)}\n")


def test_load_excel(loader):
    """测试加载 Excel 文件"""
    print("=" * 60)
    print("📊 测试加载 Excel 数据")
    print("=" * 60)
    
    remote_path = "Gondwana/04_Coffee Business 咖啡业务/03 行情报告/10 Import and Price Track/Supply_Demand BS.xlsx"
    sheet_names = ['Demand_Factsheet', 'China_Import', 'China_Export']
    
    print(f"\n文件路径: {remote_path}")
    print(f"目标 Sheet: {', '.join(sheet_names)}\n")
    
    try:
        data_dict = loader.load_excel(remote_path, sheet_names)
        
        print("\n✅ 数据加载成功！\n")
        print("=" * 60)
        print("📈 数据概览")
        print("=" * 60)
        
        for sheet_name, df in data_dict.items():
            print(f"\n📋 Sheet: {sheet_name}")
            print(f"   维度: {len(df)} 行 × {len(df.columns)} 列")
            print(f"   列名: {', '.join(df.columns.tolist()[:5])}")
            if len(df.columns) > 5:
                print(f"        ... 还有 {len(df.columns) - 5} 列")
            
            print(f"\n   前3行数据预览:")
            print(df.head(3).to_string(max_cols=5))
            print()
        
        return data_dict
        
    except Exception as e:
        print(f"❌ 加载数据失败: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("☕ 坚果云数据加载测试工具")
    print("=" * 60 + "\n")
    
    # 1. 测试连接
    loader = test_connection()
    if not loader:
        print("⚠️  连接失败，无法继续测试")
        return
    
    print()
    
    # 2. 测试列出文件
    test_list_files(loader)
    
    print()
    
    # 3. 测试加载数据
    data_dict = test_load_excel(loader)
    
    if data_dict:
        print("=" * 60)
        print("🎉 所有测试通过！")
        print("=" * 60)
        print("\n✅ 你可以开始使用可视化仪表板了")
        print("   运行命令: streamlit run dashboards/coffee_import_export/app.py\n")
    else:
        print("=" * 60)
        print("⚠️  部分测试失败")
        print("=" * 60)
        print("\n请检查：")
        print("1. 坚果云账号和应用密码是否正确")
        print("2. 文件路径是否存在")
        print("3. 网络连接是否正常\n")


if __name__ == "__main__":
    main()
