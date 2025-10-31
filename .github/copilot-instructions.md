## 快速指南 — 为 AI 编码代理定制的要点

以下说明面向需要快速上手本仓库的自动化编码代理（Copilot / AI pair）。保持简洁、可执行、并引用仓库内的具体文件/路径。

核心架构（大局观）
- 主要语言：Python。主要代码在 `src/` 下。
- 数据处理层：`src/data_processing/`
  - `data_loader.py`：抽象基类 `DataLoader`，并提供 `CSVLoader`、`ExcelLoader`。
  - `postgresql_loader.py`：用于与 PostgreSQL 集成的 `PostgreSQLLoader`（使用 SQLAlchemy）。
  - `data_integrator.py`：`DataIntegrator` 用于把多个 DataLoader 的数据合并（通过指定 join keys）。
  - `table_relations.py`：使用 SQLAlchemy inspect + networkx 来发现表关系并生成 join 查询。
- 可视化与外部数据：`src/visualization/`
  - `nutstore_loader.py`：通过 WebDAV 从坚果云（NutStore）下载并读取 Excel，提供 `load_coffee_data(email, app_password)` 快速函数。
  - `config.py`：存放项目常量（路径、sheet 配置、列名关键字、缓存和日志配置）。
- 仪表盘：`dashboards/coffee_import_export/` 包含 Streamlit 应用（`app.py`/`app_simple.py`/`app_enhanced.py`）和启动脚本（`start_app.sh`, `start_app_enhanced.sh`）。

重要工作流（可直接运行）
- 环境：
  - python -m venv venv
  - source venv/bin/activate
  - pip install -r requirements.txt
- 快速交互式调试：打开 `notebooks/workspace_setup.ipynb` 来完成环境/路径设置（仓库 README 也有简要步骤）。
- 启动仪表盘：运行 `dashboards/coffee_import_export/start_app.sh` 或 `start_app_enhanced.sh`（脚本会启动对应的 Streamlit 应用）。

项目约定与注意事项（项目特有）
- 数据目录约定：
  - 原始数据：`data/raw/`
  - 中间文件：`data/interim/`
  - 处理后数据：`data/processed/`
- 列名检测：`src/visualization/config.py` 中定义了一系列关键词（`numeric_cols_keywords`, `country_col_keywords`, `date_col_keywords`, `product_col_keywords`）。自动映射/识别列名时优先使用这些关键词。
- 外部凭据：坚果云（NutStore）和 PostgreSQL 的凭据不会在仓库中硬编码。不要写入凭证到代码；示例函数 `load_coffee_data(email, app_password)` 接受凭据参数。
- SQL 与关系分析：`TableRelationManager` 使用数据库的外键和 networkx 来生成 join 查询；修改 SQL 生成逻辑时请参考 `src/data_processing/table_relations.py` 的 `generate_join_query` 实现。

常见示例（可直接复制到交互式会话）
- 从坚果云读取咖啡数据：
```py
from src.visualization.nutstore_loader import load_coffee_data
dfs = load_coffee_data(email='you@example.com', app_password='app_pwd')
print(dfs.keys())
```
- 用 PostgreSQLLoader 列出表：
```py
from src.data_processing.postgresql_loader import PostgreSQLLoader
loader = PostgreSQLLoader(host='db', database='db', user='u', password='p')
print(loader.list_tables())
```
- 使用 DataIntegrator 合并数据源：
```py
from src.data_processing.data_integrator import DataIntegrator
# 假设有两个 DataLoader 实例 dl1, dl2 已创建并可以返回 DataFrame
di = DataIntegrator()
di.add_data_source('a', dl1)
di.add_data_source('b', dl2)
df = di.integrate_data({'a':'date','b':'date'}, how='left')
```

编辑/贡献约定（AI 代理需要遵守）
- 保持接口稳定：尽量不改变 `DataLoader` 抽象方法签名（`load`, `preprocess`, `get_data`）。
- 当改动会影响数据目录或配置（`config/` 或 `src/visualization/config.py`）时，同时更新 `README.md` 或相关 notebook。
- 配置和凭据：新增凭据使用环境变量或参数传入；不要在仓库中新增硬编码密码。

边界与失败模式（简短说明）
- 数据缺失：`DataIntegrator.integrate_data` 假定第一个 join key 对应基础表；若基础表为空会抛出异常。
- 远程下载失败：`NutStoreLoader` 的下载会抛出 IOError/ConnectionError，请在自动化脚本中捕获并做重试或告警。

参考文件（阅读优先级）
- 根 README: `README.md`
- 数据层: `src/data_processing/data_loader.py`, `postgresql_loader.py`, `data_integrator.py`, `table_relations.py`
- 可视化/外部: `src/visualization/config.py`, `src/visualization/nutstore_loader.py`
- 仪表盘与启动: `dashboards/coffee_import_export/app.py`, `start_app.sh`, `start_app_enhanced.sh`

如果你觉得某一部分不够详细，请告诉我想要更深的方向（例如：数据预处理规范、常见列映射样例，或添加具体单元测试模板），我会据此迭代此文件。
