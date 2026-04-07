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
    /* 主标题紧凑 */
    .main-title {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 0.2rem;
        margin-top: 0;
    }
    .sub-title {
        font-size: 0.9rem;
        color: #34495e;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 4px solid #3498db;
    }
    /* 标签页紧凑 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 36px;
        padding: 0 12px;
        font-size: 0.85rem;
    }
    /* 主内容区域紧凑 */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 0;
        max-width: 100%;
    }
    /* 减少标题间距 */
    .main h1, .main h2, .main h3 {
        margin-top: 0.3rem;
        margin-bottom: 0.3rem;
    }
    /* Tab内容紧凑 */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 0.5rem;
    }
    /* 隐藏页眉底部空白 */
    header[data-testid="stHeader"] {
        height: 2.5rem;
    }
    /* 侧边栏字体缩小 */
    [data-testid="stSidebar"] {
        font-size: 0.8rem;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li {
        font-size: 0.8rem;
    }
    [data-testid="stSidebar"] h1 {
        font-size: 1.1rem;
        margin-bottom: 0.2rem;
    }
    [data-testid="stSidebar"] h2 {
        font-size: 0.95rem;
        margin-top: 0.2rem;
        margin-bottom: 0.2rem;
    }
    [data-testid="stSidebar"] h3 {
        font-size: 0.85rem;
        margin-top: 0.2rem;
        margin-bottom: 0.2rem;
    }
    [data-testid="stSidebar"] .stAlert p {
        font-size: 0.75rem;
    }
    /* 侧边栏紧凑布局 */
    [data-testid="stSidebar"] .stAlert {
        padding: 0.3rem 0.5rem;
        margin-bottom: 0.2rem;
    }
    [data-testid="stSidebar"] .stMarkdown {
        margin-bottom: 0.1rem;
    }
    [data-testid="stSidebar"] hr {
        margin: 0.3rem 0;
    }
    [data-testid="stSidebar"] .stButton button {
        padding: 0.2rem 0.6rem;
        font-size: 0.75rem;
    }
    [data-testid="stSidebar"] .stCheckbox {
        margin-bottom: 0.1rem;
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 0.5rem;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
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
