"""
可视化配置文件
"""
import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 坚果云 WebDAV 配置
NUTSTORE_CONFIG = {
    'hostname': 'https://dav.jianguoyun.com/dav/',
    'remote_path': 'Gondwana/04_Coffee Business 咖啡业务/03 行情报告/10 Import and Price Track/Supply_Demand BS.xlsx',
    'local_path': str(PROJECT_ROOT / 'data' / 'raw' / 'supply_demand.xlsx')
}

# Sheet 配置
SHEET_CONFIG = {
    'demand': {
        'name': 'Demand_Factsheet',
        'type': 'wide',  # 宽表
        'description': '需求概况数据',
        'color': '#1f77b4'
    },
    'import': {
        'name': 'China_Import',
        'type': 'long',  # 长表
        'description': '中国进口数据',
        'color': '#ff7f0e'
    },
    'export': {
        'name': 'China_Export',
        'type': 'long',  # 长表
        'description': '中国出口数据',
        'color': '#2ca02c'
    }
}

# Streamlit 页面配置
PAGE_CONFIG = {
    'page_title': '咖啡进出口数据可视化',
    'page_icon': '☕',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# 数据处理配置
DATA_CONFIG = {
    # 日期格式列表
    'date_formats': ['%Y-%m-%d', '%Y/%m/%d', '%Y-%m', '%Y/%m', '%Y%m%d'],
    
    # 数值列关键词
    'numeric_cols_keywords': [
        'value', 'amount', 'quantity', 'volume', 'price', 'total',
        '数量', '金额', '价格', '总额', '数值'
    ],
    
    # 国家/地区列关键词
    'country_col_keywords': [
        'country', 'region', 'nation', 'area',
        '国家', '地区', '产地', '来源'
    ],
    
    # 日期列关键词
    'date_col_keywords': [
        'date', 'time', 'period', 'year', 'month',
        '日期', '时间', '期间', '年份', '月份'
    ],
    
    # 产品/品类列关键词
    'product_col_keywords': [
        'product', 'item', 'category', 'type',
        '产品', '品类', '类型', '商品'
    ]
}

# 图表配置
CHART_CONFIG = {
    'theme': 'plotly_white',
    'colors': [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ],
    'height': 500,
    'margin': {'l': 50, 'r': 50, 't': 50, 'b': 50}
}

# 缓存配置
CACHE_CONFIG = {
    'ttl': 3600,  # 缓存时间（秒）
    'max_entries': 10
}

# 日志配置
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
