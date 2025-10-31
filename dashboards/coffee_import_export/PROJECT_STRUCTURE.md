# 咖啡进出口数据分析项目 - 文件结构说明

## 📁 整理后的项目结构

```
coffee_import_export/
├── README.md                    # 📖 项目主文档
├── app_enhanced.py              # 🚀 主应用程序（Streamlit Web App）
├── coffee_visualization.ipynb   # 📊 数据分析笔记本（Jupyter）
├── start_app.sh                 # ⚡ 应用启动脚本
│
├── .streamlit/                  # ⚙️ Streamlit 配置
│   └── secrets.toml            # 🔐 坚果云凭据（需自行创建）
│
├── utils/                       # 🛠️ 可复用工具模块
│   ├── __init__.py             # 模块初始化
│   ├── config.py               # 配置常量（颜色、国家、样式等）
│   ├── data_loader.py          # 数据加载器（坚果云/本地CSV）
│   └── data_processor.py       # 数据处理工具（清洗、分类、预测）
│
└── data/                        # 📂 数据目录
    └── raw/                     # 原始数据文件
```

## 🗂️ 核心文件说明

### 1. `app_enhanced.py` - 主应用程序
**用途**: Streamlit Web 应用的入口文件  
**包含功能**:
- 数据加载和缓存管理
- 5 个分析 Tab：数据概览、月度九宫格、累计九宫格、详细分析、国家对比
- 交互式控制面板（侧边栏）
- Plotly 图表渲染

**依赖模块**:
```python
from utils.config import COLOR_MAP, COUNTRIES, CUSTOM_CSS
from utils.data_loader import load_from_nutstore, load_csv_data
from utils.data_processor import process_import_data, process_export_data, create_forecast_data
```

### 2. `coffee_visualization.ipynb` - 数据分析笔记本
**用途**: 探索性数据分析和原型开发  
**适用场景**:
- 数据探索和清洗
- 新图表原型开发
- 数据质量检查
- 算法验证

### 3. `utils/` - 工具模块（可复用）

#### `utils/config.py`
定义全局配置和常量：
- `COLOR_MAP`: 国家对应的颜色映射
- `COUNTRIES`: 国家列表（按优先级排序）
- `CUSTOM_CSS`: Streamlit 自定义样式
- `NUTSTORE_CONFIG`: 坚果云路径配置
- `SHIPPING_DELAY`: 运输延迟映射

#### `utils/data_loader.py`
数据加载相关功能：
- `NutStoreLoader`: 坚果云 WebDAV 加载器类
- `load_from_nutstore()`: 从坚果云加载 Excel 数据
- `load_csv_data()`: 从本地 CSV 加载数据（备用）

#### `utils/data_processor.py`
数据处理工具函数：
- `clean_quantity_value()`: 清洗数量数据并转换单位（kg → 吨）
- `categorize_country()`: 将贸易伙伴归类到标准国家名称
- `process_import_data()`: 处理进口数据（日期、国家、数量）
- `process_export_data()`: 处理出口数据并转换为长表格式
- `create_forecast_data()`: 基于出口数据和运输延迟创建预测

## 🚀 使用方式

### 启动 Web 应用
```bash
cd dashboards/coffee_import_export
./start_app.sh
```

### 使用 Jupyter 笔记本
```bash
cd dashboards/coffee_import_export
jupyter notebook coffee_visualization.ipynb
```

### 在其他项目中复用模块
```python
import sys
sys.path.insert(0, 'path/to/dashboards/coffee_import_export')

from utils.data_processor import categorize_country, process_import_data
from utils.config import COLOR_MAP

# 使用工具函数
country = categorize_country('Viet Nam')  # 返回 'Vietnam'
color = COLOR_MAP['Brazil']  # 返回 '#e74c3c'
```

## 📋 已删除的冗余文件

以下文件已被删除以简化项目结构：

| 文件名 | 原因 | 替代方案 |
|--------|------|----------|
| `app.py` | 旧版本，功能已集成到 app_enhanced.py | 使用 app_enhanced.py |
| `app_simple.py` | 简化版本，不再需要 | 使用 app_enhanced.py |
| `start_app_enhanced.sh` | 重命名为 start_app.sh | 使用 start_app.sh |
| `*.csv` (临时文件) | 应用生成的缓存文件 | 应用运行时自动生成 |
| `*.png` (临时图片) | 应用生成的图片文件 | 应用运行时自动生成 |
| `README_ENHANCED.md` | 冗余文档 | 合并到 README.md |
| `VERSION_COMPARISON.md` | 版本对比文档，不再需要 | README.md 包含最新信息 |
| `NUTSTORE_FIX.md` | 临时修复说明 | 问题已修复，集成到代码 |

## 🔄 模块依赖关系

```
app_enhanced.py
    ├── utils/config.py (配置)
    ├── utils/data_loader.py (数据加载)
    │   └── Streamlit secrets
    └── utils/data_processor.py (数据处理)
        └── utils/config.py (配置常量)

coffee_visualization.ipynb
    └── 可选导入 utils/* 模块
```

## ✨ 优势

### 1. **模块化设计**
- 工具函数独立到 `utils/` 目录
- 易于测试和维护
- 可在其他项目中复用

### 2. **清晰的职责分离**
- `app_enhanced.py`: UI 和交互逻辑
- `utils/data_loader.py`: 数据获取
- `utils/data_processor.py`: 数据转换
- `utils/config.py`: 配置管理

### 3. **灵活的数据源**
- 支持坚果云实时同步
- 支持本地 CSV 备用方案
- 自动回退机制

### 4. **易于扩展**
- 添加新的国家：修改 `utils/config.py`
- 添加新的处理逻辑：扩展 `utils/data_processor.py`
- 添加新的数据源：扩展 `utils/data_loader.py`

## 📚 下一步改进建议

1. **添加单元测试**
   ```
   tests/
   ├── test_data_loader.py
   ├── test_data_processor.py
   └── test_config.py
   ```

2. **配置文件外部化**
   - 将更多配置移到 `config.yaml` 或 `.env` 文件

3. **日志系统**
   - 添加结构化日志记录
   - 记录数据加载和处理过程

4. **错误处理增强**
   - 更细粒度的异常处理
   - 用户友好的错误提示

---

**整理完成时间**: 2025-10-31  
**整理人**: AI Assistant
