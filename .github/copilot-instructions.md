## 快速指南 — 为 AI 编码代理定制的要点

以下说明面向需要快速上手本仓库的自动化编码代理（Copilot / AI pair）。保持简洁、可执行、并引用仓库内的具体文件/路径。

项目结构
```
.
├── main.py                      # 主入口（启动仪表盘/检查配置/测试连接）
├── README.md                    # 项目说明
├── requirements.txt             # Python 依赖
├── archive/                     # 归档历史数据
├── scripts/                     # 工具脚本（测试、检查、设置）
├── dashboards/                  # Web 应用
│   └── coffee_import_export/    # 咖啡进口仪表盘（自包含）
└── src/                         # 核心代码库
    ├── data_processing/         # 数据处理模块
    └── visualization/           # 可视化与数据加载
```

核心架构
- 主要语言：Python
- 主入口：`main.py` — 统一启动/检查/测试
- 数据处理层：`src/data_processing/postgresql_loader.py` — PostgreSQL 集成
- 可视化层：`src/visualization/nutstore_loader.py` — 坚果云 WebDAV 加载器
- 仪表盘：`dashboards/coffee_import_export/` — 自包含的 Streamlit 应用

重要工作流
- 环境设置：`pip install -r requirements.txt`
- 启动应用：`python main.py`
- 检查配置：`python main.py --check`
- 测试连接：`python main.py --test`

项目约定
- 历史数据在 `archive/`
- 外部凭据：不硬编码；使用环境变量或参数传入
- Streamlit secrets：`dashboards/coffee_import_export/.streamlit/secrets.toml`（嵌套格式 `[nutstore]`）

常见示例
```py
# 从坚果云读取咖啡数据
from src.visualization.nutstore_loader import load_coffee_data
dfs = load_coffee_data(email='you@example.com', app_password='app_pwd')

# PostgreSQL 连接
from src.data_processing.postgresql_loader import PostgreSQLLoader
loader = PostgreSQLLoader(host='db', database='db', user='u', password='p')
```

编辑约定
- 仪表盘独立性：`dashboards/coffee_import_export/` 与 `src/` 解耦
- 配置变更时同步更新 `README.md`
- 新增凭据使用环境变量

参考文件优先级
1. `main.py`, `README.md`
2. `src/visualization/nutstore_loader.py`
3. `dashboards/coffee_import_export/app_enhanced.py`
4. `dashboards/coffee_import_export/DEPLOYMENT.md`
