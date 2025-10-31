"""
配置常量和样式定义
"""

# 国家颜色映射
COLOR_MAP = {
    'Total': '#2c3e50',
    'Brazil': '#e74c3c',
    'Vietnam': '#3498db',
    'Colombia': '#2ecc71',
    'Uganda': '#f39c12',
    'Ethiopia': '#9b59b6',
    'Central America': '#1abc9c',
    'Indonesia': '#e67e22',
    'Others': '#95a5a6'
}

# 国家列表（按优先级排序）
COUNTRIES = [
    'Total', 'Brazil', 'Vietnam', 'Colombia', 'Uganda', 
    'Ethiopia', 'Central America', 'Indonesia', 'Others'
]

# 自定义CSS样式
CUSTOM_CSS = """
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-title {
        font-size: 1.5rem;
        color: #34495e;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3498db;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
"""

# 坚果云配置
NUTSTORE_CONFIG = {
    'remote_path': 'Gondwana/04_Coffee Business 咖啡业务/03 行情报告/10 Import and Price Track/Supply_Demand BS.xlsx',
    'sheet_names': ['China_Import', 'Original_Export']
}

# 运输延迟映射（月数）
SHIPPING_DELAY = {
    'Brazil': 2,
    'Colombia': 2,
    'Vietnam': 1,
    'Uganda': 2
}
