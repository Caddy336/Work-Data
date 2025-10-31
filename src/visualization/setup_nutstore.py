#!/usr/bin/env python3
"""
坚果云配置助手
帮助用户快速配置坚果云凭证
"""
import os
from pathlib import Path


def main():
    """配置助手主函数"""
    print("\n" + "=" * 70)
    print("☕ 坚果云数据可视化配置助手")
    print("=" * 70)
    
    print("\n📋 此工具将帮助你配置坚果云凭证\n")
    
    # 获取项目根目录
    project_root = Path(__file__).parent.parent.parent
    secrets_file = project_root / ".streamlit" / "secrets.toml"
    
    # 检查文件是否存在
    if secrets_file.exists():
        print(f"⚠️  配置文件已存在: {secrets_file}")
        overwrite = input("\n是否覆盖现有配置？(y/N): ").strip().lower()
        if overwrite != 'y':
            print("\n❌ 已取消配置")
            return
    
    print("\n" + "-" * 70)
    print("📝 步骤 1: 获取坚果云应用密码")
    print("-" * 70)
    print("""
1. 访问: https://www.jianguoyun.com/
2. 登录你的账号
3. 点击右上角头像 → 账户信息
4. 选择"安全选项"标签
5. 找到"第三方应用管理"
6. 点击"添加应用密码"
7. 输入应用名称（如"Streamlit Dashboard"）
8. 复制生成的密码
""")
    
    input("按 Enter 继续...")
    
    print("\n" + "-" * 70)
    print("✏️  步骤 2: 输入凭证")
    print("-" * 70)
    
    # 获取用户输入
    email = input("\n请输入坚果云邮箱: ").strip()
    
    while not email:
        print("❌ 邮箱不能为空")
        email = input("请输入坚果云邮箱: ").strip()
    
    app_password = input("请输入坚果云应用密码: ").strip()
    
    while not app_password:
        print("❌ 应用密码不能为空")
        app_password = input("请输入坚果云应用密码: ").strip()
    
    # 生成配置文件内容
    config_content = f"""# 坚果云凭证配置
# ⚠️ 重要：此文件包含敏感信息，请勿提交到 Git 仓库！

[nutstore]
# 坚果云账号邮箱
email = "{email}"

# 坚果云应用密码（在账户设置中生成）
app_password = "{app_password}"

# WebDAV 服务器地址
hostname = "https://dav.jianguoyun.com/dav/"
"""
    
    # 确保目录存在
    secrets_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 写入配置文件
    try:
        with open(secrets_file, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print("\n" + "=" * 70)
        print("✅ 配置成功！")
        print("=" * 70)
        print(f"\n📄 配置文件已保存到: {secrets_file}")
        
        print("\n" + "-" * 70)
        print("🧪 下一步：测试连接")
        print("-" * 70)
        print("""
运行以下命令测试配置：

    python src/visualization/test_nutstore.py

如果测试通过，就可以运行可视化仪表板了：

    streamlit run dashboards/coffee_import_export/app.py
""")
        
    except Exception as e:
        print(f"\n❌ 保存配置失败: {str(e)}")
        return
    
    print("\n" + "=" * 70)
    print("🎉 配置完成！")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ 已取消配置")
    except Exception as e:
        print(f"\n\n❌ 错误: {str(e)}")
