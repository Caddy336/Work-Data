# 🎯 下一步操作指南

## ✅ 已完成的配置

1. ✅ 创建了可视化模块结构
2. ✅ 安装了所有必要的依赖包
3. ✅ 创建了配置文件模板
4. ✅ 创建了测试和配置工具

## 📋 你需要做的事情

### 1. 配置坚果云凭证 ⭐ **重要**

编辑文件：`.streamlit/secrets.toml`

```toml
[nutstore]
email = "your-email@example.com"        # 替换为你的坚果云邮箱
app_password = "your-app-password-here"  # 替换为你的应用密码
```

#### 如何获取应用密码？

1. 访问 https://www.jianguoyun.com/
2. 登录 → 右上角头像 → **账户信息**
3. 选择 **安全选项** 标签
4. 找到 **第三方应用管理**
5. 点击 **添加应用密码**
6. 输入名称（如"Streamlit"）
7. **复制生成的密码**

### 2. 测试连接

配置完成后，运行测试：

```bash
python src/visualization/test_nutstore.py
```

**预期输出：**
```
✅ 成功连接到坚果云
✅ 数据加载成功！
🎉 所有测试通过！
```

### 3. 检查配置状态

随时可以运行：

```bash
python src/visualization/check_config.py
```

## 🚀 准备就绪后

一旦测试通过，就可以开发可视化仪表板了！

## 📂 项目结构

```
.
├── .streamlit/
│   ├── secrets.toml          # ⭐ 需要配置
│   └── config.toml           # ✅ 已配置
├── src/
│   └── visualization/
│       ├── __init__.py       # ✅ 已创建
│       ├── config.py         # ✅ 已创建（数据配置）
│       ├── nutstore_loader.py # ✅ 已创建（数据加载）
│       ├── setup_nutstore.py  # ✅ 配置助手
│       ├── check_config.py    # ✅ 配置检查
│       └── test_nutstore.py   # ✅ 连接测试
├── dashboards/
│   └── coffee_import_export/
│       └── README.md         # ✅ 配置指南
└── requirements.txt          # ✅ 已更新

```

## 💡 快速命令参考

```bash
# 1. 检查配置
python src/visualization/check_config.py

# 2. 重新配置（交互式）
python src/visualization/setup_nutstore.py

# 3. 测试连接
python src/visualization/test_nutstore.py

# 4. 查看详细说明
cat dashboards/coffee_import_export/README.md
```

## ⚠️ 注意事项

- `.streamlit/secrets.toml` 已添加到 `.gitignore`，不会被提交
- 应用密码 ≠ 登录密码
- 应用密码只显示一次，请妥善保存

## 📞 遇到问题？

运行配置检查查看详细信息：
```bash
python src/visualization/check_config.py
```

---

**准备好了吗？** 配置完 secrets.toml 后，运行测试脚本！🚀
