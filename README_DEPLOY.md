# 中国咖啡进出口数据分析

这个仓库包含用于分析中国咖啡进出口贸易数据的工具和应用程序。

## 📊 主要项目

### 咖啡进出口仪表盘
交互式 Web 应用，可视化中国咖啡豆进出口数据。

📂 **位置**: `dashboards/coffee_import_export/`  
📖 **文档**: [查看部署文档](dashboards/coffee_import_export/DEPLOYMENT.md)  
🚀 **在线体验**: [访问应用](https://your-app-url.streamlit.app)

**主要功能**:
- 📊 月度/累计数据九宫格可视化
- 🎨 国家专属配色方案
- ☁️ 坚果云实时数据同步
- 🔮 趋势预测分析

## 🚀 快速开始

### 环境设置

```bash
# 克隆仓库
git clone https://github.com/Caddy336/Work-Data.git
cd Work-Data

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 运行仪表盘

```bash
cd dashboards/coffee_import_export
streamlit run app_enhanced.py
```

## 📁 项目结构

```
Work-Data/
├── dashboards/
│   └── coffee_import_export/      # Streamlit 仪表盘应用
│       ├── app_enhanced.py        # 主应用
│       ├── utils/                 # 工具模块
│       ├── .streamlit/            # Streamlit 配置
│       └── DEPLOYMENT.md          # 部署指南
├── src/
│   ├── data_processing/           # 数据处理模块
│   │   ├── data_loader.py         # 数据加载器基类
│   │   ├── data_integrator.py     # 数据整合工具
│   │   ├── postgresql_loader.py   # PostgreSQL 连接
│   │   └── table_relations.py     # 表关系分析
│   └── visualization/             # 可视化工具
│       ├── config.py              # 全局配置
│       └── nutstore_loader.py     # 坚果云加载器
├── data/                          # 数据目录（已忽略）
├── notebooks/                     # Jupyter 笔记本
├── config/                        # 配置文件
├── requirements.txt               # Python 依赖
└── README.md                      # 本文件
```

## 🛠️ 技术栈

- **Python 3.8+**
- **Streamlit** - Web 应用框架
- **Pandas** - 数据处理
- **Plotly** - 交互式可视化
- **SQLAlchemy** - 数据库 ORM
- **WebDAV** - 云存储集成

## 📊 数据处理架构

### 核心组件

1. **DataLoader** (`src/data_processing/data_loader.py`)
   - 抽象基类，支持 CSV、Excel 等格式
   - 标准化的数据加载接口

2. **PostgreSQLLoader** (`src/data_processing/postgresql_loader.py`)
   - 数据库连接和查询
   - 支持 SQLAlchemy ORM

3. **DataIntegrator** (`src/data_processing/data_integrator.py`)
   - 多数据源整合
   - 支持灵活的 join 操作

4. **NutStoreLoader** (`src/visualization/nutstore_loader.py`)
   - 坚果云 WebDAV 集成
   - Excel 文件自动下载和解析

## 🚢 部署

### Streamlit Cloud（推荐）

1. 推送代码到 GitHub
2. 访问 [share.streamlit.io](https://share.streamlit.io)
3. 连接仓库并选择 `dashboards/coffee_import_export/app_enhanced.py`
4. 配置 Secrets（坚果云凭据）
5. 部署

详细步骤请查看 [DEPLOYMENT.md](dashboards/coffee_import_export/DEPLOYMENT.md)

### Docker（可选）

```bash
# 构建镜像
docker build -t coffee-dashboard .

# 运行容器
docker run -p 8501:8501 coffee-dashboard
```

## 📝 配置说明

### 坚果云配置

创建 `.streamlit/secrets.toml`：
```toml
[nutstore]
email = "your_email@example.com"
app_password = "your_app_password"
```

### 数据库配置（可选）

在 `config/data_config.json` 中配置 PostgreSQL 连接：
```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "database": "coffee_data",
    "user": "username",
    "password": "password"
  }
}
```

## 🔒 安全注意事项

⚠️ **不要提交敏感数据**

已在 `.gitignore` 中排除：
- `.streamlit/secrets.toml` - 坚果云凭据
- `data/raw/*` - 原始数据文件
- `data/processed/*` - 处理后的数据
- `config/*` - 包含密码的配置文件

## 📖 文档

- [部署指南](dashboards/coffee_import_export/DEPLOYMENT.md) - Streamlit Cloud 部署详细步骤
- [项目结构](dashboards/coffee_import_export/PROJECT_STRUCTURE.md) - 代码组织说明
- [Git 指南](docs/git_github_guide.md) - Git 使用教程

## 🤝 贡献

欢迎贡献代码！请：
1. Fork 本仓库
2. 创建特性分支
3. 提交 Pull Request

## 📄 许可

MIT License

## 👤 作者

**Caddy Zhang**
- GitHub: [@Caddy336](https://github.com/Caddy336)

---

⭐ 觉得有用？给个 Star 吧！
