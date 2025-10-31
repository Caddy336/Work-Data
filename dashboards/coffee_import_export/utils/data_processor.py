"""
咖啡进出口数据处理工具
"""
import pandas as pd
import numpy as np


def clean_quantity_value(value):
    """清理数量数据并转换为吨"""
    if pd.isna(value):
        return 0
    if isinstance(value, str):
        value = value.replace(',', '').strip()
        try:
            return float(value) / 1000  # kg 转 吨
        except:
            return 0
    try:
        return float(value) / 1000
    except:
        return 0


def categorize_country(partner):
    """将贸易伙伴归类"""
    if pd.isna(partner):
        return 'Others'
    partner = str(partner).strip()
    
    if partner == 'Brazil' or 'brazil' in partner.lower():
        return 'Brazil'
    elif partner == 'Viet Nam' or partner == 'Vietnam' or 'vietnam' in partner.lower():
        return 'Vietnam'
    elif partner == 'Colombia' or 'colombia' in partner.lower():
        return 'Colombia'
    elif partner == 'Uganda' or 'uganda' in partner.lower():
        return 'Uganda'
    elif partner == 'Ethiopia' or 'ethiopia' in partner.lower():
        return 'Ethiopia'
    elif partner == 'Indonesia' or 'indonesia' in partner.lower():
        return 'Indonesia'
    elif partner in ['Costa Rica', 'Honduras', 'Guatemala'] or any(x in partner.lower() for x in ['costa rica', 'honduras', 'guatemala']):
        return 'Central America'
    else:
        return 'Others'


def process_import_data(import_data):
    """处理进口数据"""
    # 识别列
    date_cols = [col for col in import_data.columns if 'date' in col.lower() or 'time' in col.lower() or 'period' in col.lower()]
    country_cols = [col for col in import_data.columns if 'country' in col.lower() or 'partner' in col.lower() or 'region' in col.lower()]
    
    # 处理日期
    if date_cols:
        date_col = date_cols[0]
        import_data['date'] = pd.to_datetime(import_data[date_col], errors='coerce')
        import_data['year'] = import_data['date'].dt.year
        import_data['month'] = import_data['date'].dt.month
    
    # 处理国家
    if country_cols:
        country_col = country_cols[0]
        import_data['Trading_partner'] = import_data[country_col]
    
    # 处理数量（从kg转为吨）
    quantity_col = 'Import (kg)'
    if quantity_col in import_data.columns:
        import_data['Quantity_tons'] = import_data[quantity_col].apply(clean_quantity_value)
    
    # 国家分类
    import_data['Country_Category'] = import_data['Trading_partner'].apply(categorize_country)
    
    return import_data


def process_export_data(export_data):
    """处理出口数据"""
    # 处理日期
    export_date_cols = [col for col in export_data.columns if 'date' in col.lower() or 'time' in col.lower() or 'period' in col.lower() or 'month' in col.lower()]
    
    if export_date_cols:
        export_date_col = export_date_cols[0]
        export_data['date'] = pd.to_datetime(export_data[export_date_col], errors='coerce')
        export_data['year'] = export_data['date'].dt.year
        export_data['month'] = export_data['date'].dt.month
    
    # 国家列映射
    country_mapping = {}
    for col in export_data.columns:
        col_str = str(col)
        if col == 'Columbia_Kg':
            country_mapping[col] = 'Colombia'
        elif 'brazil' in col_str.lower():
            country_mapping[col] = 'Brazil'
        elif 'vietnam' in col_str.lower() or 'viet nam' in col_str.lower():
            country_mapping[col] = 'Vietnam'
        elif 'uganda' in col_str.lower():
            country_mapping[col] = 'Uganda'
    
    # 转换为长表格式
    long_data_list = []
    for col, country in country_mapping.items():
        if col in export_data.columns:
            country_data = export_data[['year', 'month', col]].copy()
            country_data['Origin_Country'] = country
            country_data['Export_Quantity_tons'] = country_data[col].apply(clean_quantity_value)
            country_data = country_data[['year', 'month', 'Origin_Country', 'Export_Quantity_tons']]
            long_data_list.append(country_data)
    
    if long_data_list:
        export_data_long = pd.concat(long_data_list, ignore_index=True)
        export_data_long = export_data_long.dropna(subset=['year', 'month'])
        return export_data_long
    else:
        return pd.DataFrame()


def create_forecast_data(export_data_long, import_data):
    """创建预测数据"""
    if len(export_data_long) == 0:
        return pd.DataFrame()
    
    delay_mapping = {
        'Brazil': 2,
        'Colombia': 2,
        'Vietnam': 1,
        'Uganda': 2
    }
    
    def calculate_forecast_month(row):
        """计算预测到达月份"""
        delay = delay_mapping.get(row['Origin_Country'], 2)
        export_date = pd.Timestamp(year=int(row['year']), month=int(row['month']), day=1)
        forecast_date = export_date + pd.DateOffset(months=delay)
        return forecast_date.year, forecast_date.month
    
    def map_export_country(country):
        """映射出口国家到进口国家分类"""
        mapping = {
            'Brazil': 'Brazil',
            'Colombia': 'Colombia',
            'Vietnam': 'Vietnam',
            'Uganda': 'Uganda'
        }
        return mapping.get(country, 'Others')
    
    forecast_data = export_data_long.copy()
    forecast_results = forecast_data.apply(calculate_forecast_month, axis=1)
    forecast_data['forecast_year'] = [r[0] for r in forecast_results]
    forecast_data['forecast_month'] = [r[1] for r in forecast_results]
    forecast_data['Country_Category'] = forecast_data['Origin_Country'].apply(map_export_country)
    forecast_data = forecast_data.rename(columns={'Export_Quantity_tons': 'Forecast_Quantity_tons'})
    
    # 获取实际进口数据的最晚日期
    if 'year' in import_data.columns and 'month' in import_data.columns:
        max_import_year = import_data['year'].max()
        max_import_month = import_data[import_data['year'] == max_import_year]['month'].max()
        cutoff_date = pd.Timestamp(year=int(max_import_year), month=int(max_import_month), day=1)
        
        def should_keep_forecast(row):
            """判断预测数据是否应该保留（只保留未来的预测）"""
            forecast_date = pd.Timestamp(year=int(row['forecast_year']), month=int(row['forecast_month']), day=1)
            return forecast_date > cutoff_date
        
        forecast_data = forecast_data[forecast_data.apply(should_keep_forecast, axis=1)].copy()
    
    return forecast_data
