# ☕ 中国咖啡进出口数据分析仪表盘

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

实时展示中国咖啡豆进出口数据的交互式分析仪表盘，支持多维度数据可视化和趋势预测。

## 🌟 功能特性

- **📊 月度九宫格分析**：展示9个主要咖啡来源国的月度进口量对比
- **📈 累计九宫格分析**：显示各国年度累计进口量趋势
- **🎨 智能配色**：国家专属颜色识别，历史数据灰度区分
- **☁️ 云端同步**：支持从坚果云实时加载最新数据
- **🔮 趋势预测**：基于历史数据的智能预测功能

## 🚀 在线体验

访问部署好的应用：[在线演示](https://your-app-url.streamlit.app)

## 💻 本地运行

### 环境要求
- Python 3.8+
- pip

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/Caddy336/Work-Data.git
cd Work-Data/dashboards/coffee_import_export
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置坚果云凭据（可选）**

如果需要从坚果云加载数据：
```bash
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# 编辑 secrets.toml 填入你的坚果云邮箱和应用密码
```

获取坚果云应用密码：
- 登录 [坚果云网页版](https://www.jianguoyun.com/)
- 账户信息 → 安全选项 → 第三方应用管理
- 添加应用，生成应用密码

4. **启动应用**
```bash
streamlit run app_enhanced.py
```

应用将在浏览器中打开 `http://localhost:8501`

## 📦 项目结构

```
dashboards/coffee_import_export/
├── app_enhanced.py              # 主应用文件
├── requirements.txt             # Python 依赖
├── utils/                       # 工具模块
│   ├── config.py               # 配置常量
│   ├── data_loader.py          # 数据加载器
│   └── data_processor.py       # 数据处理器
├── .streamlit/
│   ├── config.toml             # Streamlit 配置
│   └── secrets.toml.example    # 凭据配置示例
└── DEPLOYMENT.md               # 本文件
```

## 🔧 技术栈

- **前端框架**：Streamlit
- **数据处理**：Pandas
- **数据可视化**：Plotly
- **云存储**：坚果云 WebDAV
- **数据库**：PostgreSQL (可选)

## 📊 数据源

- **坚果云**：实时同步的 Excel 数据文件
- **本地 CSV**：备用数据源

主要数据维度：
- 9个主要咖啡来源国/地区
- 2020-2025年月度进口数据
- 重量（吨）和金额（美元）

## 🎨 可视化特性

### 配色方案
- **国家专属色**：每个国家固定颜色，便于识别
  - 🇧🇷 巴西：红色
  - 🇻🇳 越南：蓝色
  - 🇨🇴 哥伦比亚：绿色
  - 🇺🇬 乌干达：橙色
  - 🇪🇹 埃塞俄比亚：紫色
  - 🌎 中美洲：青色
  - 🇮🇩 印度尼西亚：深橙
  - 🌍 总计：深蓝灰
  - 📊 其他：灰色

- **时间维度**：历史年份使用灰度色系区分

### 交互功能
- 悬停显示详细数据
- 图表缩放和平移
- 数据标签自动格式化（千分位分隔符）

## 🚢 部署到 Streamlit Cloud

### 步骤详解

1. **准备 GitHub 仓库**
   - 确保代码已推送到 GitHub
   - 确认 `.gitignore` 包含敏感文件

2. **访问 Streamlit Cloud**
   - 打开 [share.streamlit.io](https://share.streamlit.io)
   - 使用 GitHub 账号登录

3. **创建新应用**
   - 点击 "New app"
   - 选择仓库：`Caddy336/Work-Data`
   - 设置路径：`dashboards/coffee_import_export/app_enhanced.py`
   - App URL：自定义你的应用域名

4. **配置 Secrets**
   
   在 Advanced settings → Secrets 中添加：
   ```toml
   [nutstore]
   email = "your_email@example.com"
   app_password = "your_app_password"
   ```

5. **部署**
   - 点击 "Deploy!"
   - 等待构建完成（约2-3分钟）
   - 应用将自动启动并生成访问链接

### 自动更新
- 每次推送到 GitHub main 分支
- Streamlit Cloud 会自动重新部署应用

## 📝 使用说明

### 切换数据源
- 左侧边栏默认勾选"从坚果云加载数据"
- 取消勾选则使用本地 CSV 文件（如果有）

### 查看不同维度
- **月度九宫格**：查看每月进口量波动
- **累计九宫格**：观察全年累计趋势

### 数据刷新
- 点击"🔄 刷新数据"按钮重新加载最新数据
- 缓存时间：1小时（可在代码中调整）

## ⚙️ 高级配置

### 修改缓存时间
编辑 `app_enhanced.py`：
```python
@st.cache_data(ttl=3600)  # 3600秒 = 1小时
def load_and_process_data(use_nutstore=True):
    ...
```

### 自定义国家颜色
编辑 `utils/config.py`：
```python
COLOR_MAP = {
    'Brazil': '#e74c3c',  # 修改为你想要的颜色
    ...
}
```

### 调整图表布局
在 `app_enhanced.py` 中找到 `make_subplots()` 函数调用，调整：
- `rows`：行数
- `cols`：列数
- `vertical_spacing`：垂直间距
- `horizontal_spacing`：水平间距

## 🐛 常见问题

**Q: 坚果云连接失败？**
A: 检查以下几点：
- Secrets 配置是否正确
- 应用密码是否有效
- 网络连接是否正常
- 坚果云 WebDAV 路径是否正确

**Q: 图表显示不全？**
A: 尝试：
- 刷新浏览器
- 清除缓存后重新加载
- 调整浏览器窗口大小

**Q: 数据更新不及时？**
A: 
- 点击"🔄 刷新数据"按钮
- 或等待缓存过期（默认1小时）

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

贡献指南：
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可

MIT License - 详见 [LICENSE](LICENSE) 文件

## 👤 作者

**Caddy Zhang**
- GitHub: [@Caddy336](https://github.com/Caddy336)

## 🙏 致谢

- [Streamlit](https://streamlit.io/) - 强大的 Web 应用框架
- [Plotly](https://plotly.com/) - 交互式可视化库
- [坚果云](https://www.jianguoyun.com/) - 云存储服务

---

⭐ 如果这个项目对你有帮助，欢迎点个 Star！
