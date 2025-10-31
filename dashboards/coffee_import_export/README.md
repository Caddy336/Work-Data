# ☕ 咖啡进出口数据分析项目# ☕ 咖啡进口数据可视化仪表板



## 📋 项目概述这是一个基于 Streamlit 的交互式 Web 应用，用于可视化和分析中国咖啡进口数据。



这是一个基于 Streamlit 的交互式咖啡进出口数据可视化分析应用，支持从坚果云实时同步数据或使用本地数据文件。## 📋 功能特性



## 📁 项目结构### 🎯 核心功能

- **实时数据加载**: 从坚果云直接加载最新的 Excel 数据

```- **交互式可视化**: 使用 Plotly 创建动态、可交互的图表

coffee_import_export/- **多维度分析**: 

├── app_enhanced.py              # 主应用程序（Streamlit）  - 总体趋势分析

├── coffee_visualization.ipynb   # Jupyter 数据分析笔记本  - 月度进口数据

├── start_app.sh                 # 应用启动脚本  - 累计进口数据

├── README.md                    # 项目说明文档  - 国家对比分析

├── .streamlit/                  # Streamlit 配置目录  - 原始数据查看和导出

│   └── secrets.toml            # 坚果云凭据配置（需自行创建）

├── utils/                       # 工具模块（可复用）### 📊 可视化内容

│   ├── __init__.py             # 模块初始化1. **总体趋势图**: 展示整体进口趋势和移动平均线

│   ├── config.py               # 配置常量和样式2. **月度九宫格图**: 按国家分类的月度进口数据对比

│   ├── data_loader.py          # 数据加载器（坚果云/本地）3. **累计九宫格图**: 各国家的累计进口量趋势

│   └── data_processor.py       # 数据处理工具4. **国家对比图**: 横向柱状图对比各国总进口量

└── data/                        # 数据目录5. **年度分布图**: 堆叠柱状图显示各年份国家分布

    └── raw/                     # 原始数据文件6. **数据表格**: 可筛选、排序、导出的原始数据表

```

### 🎨 界面特点

## 🚀 快速开始- 响应式布局，适配各种屏幕尺寸

- 现代化 UI 设计

### 1. 环境准备- 丰富的交互控件

- 实时数据筛选和更新

```bash

# 返回项目根目录## 🚀 快速开始

cd ../../..

### 1. 环境准备

# 创建虚拟环境（如果还没有）

python -m venv venv确保已安装 Python 3.8+，然后安装依赖：



# 激活虚拟环境```bash

source venv/bin/activate  # macOS/Linux# 回到项目根目录

cd /Users/caddyzhang/Documents/X_Codes/Caddy\'s\ data

# 安装依赖

pip install -r requirements.txt# 安装依赖

```pip install -r requirements.txt

```

### 2. 配置坚果云（可选）

### 2. 配置凭证

如果要从坚果云同步数据，需要配置凭据：

凭证已配置在 `.streamlit/secrets.toml` 文件中：

```bash

# 创建配置文件```toml

mkdir -p dashboards/coffee_import_export/.streamlitnutstore_email = "your_email@example.com"

```nutstore_app_password = "your_app_password"

```

创建 `.streamlit/secrets.toml` 文件并添加：

### 3. 运行应用

```toml

nutstore_email = "your_email@example.com"```bash

nutstore_app_password = "your_app_password"# 进入仪表板目录

```cd dashboards/coffee_import_export



### 3. 启动应用# 启动 Streamlit 应用

streamlit run app.py

```bash```

cd dashboards/coffee_import_export

chmod +x start_app.sh应用将在浏览器中自动打开，默认地址为 `http://localhost:8501`

./start_app.sh

```### 4. 使用应用



或直接运行：1. **选择数据源**: 在侧边栏选择"从坚果云加载"或"使用本地CSV文件"

2. **查看概览**: 主页显示关键指标和数据概览

```bash3. **切换标签页**: 使用顶部标签页切换不同的分析视图

streamlit run app_enhanced.py4. **交互筛选**: 使用各种控件筛选和自定义图表

```5. **导出数据**: 在"数据表格"标签页可以导出筛选后的数据



应用将在浏览器中打开：`http://localhost:8501`## 📁 文件结构



## 📊 功能特性```

coffee_import_export/

### 主应用 (app_enhanced.py)├── app.py                          # Streamlit 主应用

├── coffee_visualization.ipynb      # Jupyter Notebook 分析

- **数据源灵活切换**：支持坚果云实时同步或本地 CSV 文件├── README.md                       # 项目说明文档

- **多维度分析**：├── .streamlit/

  - 📊 数据概览：关键指标、年度趋势│   └── secrets.toml               # 坚果云凭证配置

  - 📈 月度九宫格：各国月度进口量对比├── data/                          # 数据文件夹（如需）

  - 📉 累计九宫格：累计进口量趋势├── monthly_import_data.csv        # 月度数据（导出）

  - 🔍 详细分析：深度数据挖掘├── cumulative_import_data.csv     # 累计数据（导出）

  - 🌍 国家对比：多国家横向对比├── total_by_country.csv           # 国家总计（导出）

- **智能预测**：基于出口数据的运输延迟预测├── monthly_import_by_country.png  # 月度图表（导出）

- **交互式可视化**：基于 Plotly 的动态图表├── cumulative_import_by_country.png # 累计图表（导出）

└── total_import_by_country.png    # 总计图表（导出）

### 数据分析笔记本 (coffee_visualization.ipynb)```



- 探索性数据分析 (EDA)## 🛠️ 技术栈

- 数据清洗和预处理示例

- 自定义可视化开发- **Python 3.8+**: 主要编程语言

- **Streamlit**: Web 应用框架

## 🛠️ 模块复用- **Plotly**: 交互式图表库

- **Pandas**: 数据处理

### 数据加载模块 (`utils/data_loader.py`)- **NumPy**: 数值计算

- **WebDAV**: 坚果云数据访问

```python

from utils.data_loader import NutStoreLoader, load_csv_data## 📊 数据源



# 从坚果云加载- **来源**: 坚果云 - `Supply_Demand BS.xlsx`

loader = NutStoreLoader(email='your@email.com', app_password='pwd')- **路径**: `Gondwana/04_Coffee Business 咖啡业务/03 行情报告/10 Import and Price Track/`

data_sheets = loader.load_excel(remote_path='path/to/file.xlsx')- **工作表**: 

  - `China_Import`: 中国进口数据

# 从本地 CSV 加载  - `Original_Export`: 原产国出口数据

data, error = load_csv_data()- **更新频率**: 手动更新

```

## 🎯 使用场景

### 数据处理模块 (`utils/data_processor.py`)

1. **业务分析**: 分析咖啡进口趋势，支持商业决策

```python2. **数据报告**: 生成可视化报告，展示给管理层

from utils.data_processor import (3. **趋势预测**: 基于历史数据预测未来进口趋势

    process_import_data,4. **市场洞察**: 了解主要进口来源国的变化趋势

    process_export_data,

    create_forecast_data,## 🔧 自定义和扩展

    categorize_country

)### 添加新的可视化



# 处理进口数据在 `app.py` 中添加新的绘图函数：

processed_import = process_import_data(raw_import_data)

```python

# 创建预测数据def create_your_chart(data):

forecast = create_forecast_data(export_data, import_data)    fig = go.Figure()

```    # 添加你的图表逻辑

    return fig

### 配置模块 (`utils/config.py`)```



```python### 修改颜色方案

from utils.config import COLOR_MAP, COUNTRIES, SHIPPING_DELAY

修改 `COLOR_MAP` 字典：

# 使用预定义的颜色映射

color = COLOR_MAP['Brazil']  # '#e74c3c'```python

COLOR_MAP = {

# 获取运输延迟配置    'Brazil': '#your_color',

delay = SHIPPING_DELAY['Vietnam']  # 1 month    'Vietnam': '#your_color',

```    # ...

}

## 📝 数据格式要求```



### 进口数据 (China_Import)### 添加新的数据处理逻辑



| 列名 | 说明 | 示例 |在数据处理函数部分添加你的逻辑。

|------|------|------|

| date/Period | 日期 | 2024-01-01 |## � 更新日志

| Trading_partner | 贸易伙伴 | Brazil |

| Import (kg) | 进口数量（千克） | 1500000 |### v1.0.0 (2025-10-30)

- ✨ 初始版本发布

### 出口数据 (Original_Export)- 📊 完整的数据可视化功能

- 🔄 支持从坚果云实时加载数据

| 列名 | 说明 | 示例 |- 📈 5个主要分析标签页

|------|------|------|- 💾 数据导出功能

| Month | 月份 | 2024-01 |

| Brazil_Kg | 巴西出口量（千克） | 2000000 |## 🤝 贡献

| Vietnam_Kg | 越南出口量（千克） | 1000000 |

| ... | 其他国家 | ... |如需改进或添加新功能，请：

1. Fork 本项目

## 🔧 常见问题2. 创建特性分支

3. 提交变更

### 1. 坚果云连接失败4. 推送到分支

5. 创建 Pull Request

- 检查网络连接

- 确认 `.streamlit/secrets.toml` 配置正确## 📧 联系方式

- 验证应用密码（不是登录密码）

- **邮箱**: caddy.zhang@starstream.com.cn

### 2. 模块导入错误- **项目**: Gondwana Coffee Business Analytics



```bash## 📜 许可证

# 确保在正确的目录运行

cd dashboards/coffee_import_export本项目仅供内部使用。



# 或在 app_enhanced.py 中已添加路径---

```

**注意**: 请妥善保管坚果云凭证，不要将 `.streamlit/secrets.toml` 文件提交到公开仓库。

### 3. 依赖缺失

```bash
pip install streamlit pandas plotly webdavclient3
```

## 📚 技术栈

- **Web 框架**：Streamlit
- **数据处理**：Pandas, NumPy
- **可视化**：Plotly
- **云存储**：WebDAV (坚果云)
- **笔记本**：Jupyter

## 🎯 下一步开发

- [ ] 添加数据导出功能
- [ ] 集成更多数据源（PostgreSQL 等）
- [ ] 增加预测模型（时间序列分析）
- [ ] 添加数据质量检查报告
- [ ] 支持多语言界面

## 📄 许可证

本项目仅供内部使用。

## 👥 贡献

如需贡献或报告问题，请联系项目维护者。

---

**最后更新**: 2025-10-31  
**版本**: 2.0 (Enhanced)
