"""
咖啡进口数据可视化 Web 应用
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import tempfile
import os
import warnings
warnings.filterwarnings('ignore')

# 页面配置
st.set_page_config(
    page_title="咖啡进口数据分析",
    page_icon="☕",
    layout="wide"
)

# 配置常量
COLOR_MAP = {
    'Total': '#2c3e50', 'Brazil': '#e74c3c', 'Vietnam': '#3498db',
    'Colombia': '#2ecc71', 'Uganda': '#f39c12', 'Ethiopia': '#9b59b6',
    'Central America': '#1abc9c', 'Indonesia': '#e67e22', 'Others': '#95a5a6'
}

COUNTRIES = ['Total', 'Brazil', 'Vietnam', 'Colombia', 'Uganda', 
             'Ethiopia', 'Central America', 'Indonesia', 'Others']

def clean_quantity_value(value):
    if pd.isna(value):
        return 0
    if isinstance(value, str):
        value = value.replace(',', '').strip()
    try:
        return float(value) / 1000
    except:
        return 0

def categorize_country(partner):
    if pd.isna(partner):
        return 'Others'
    partner = str(partner).strip().lower()
    
    if 'brazil' in partner:
        return 'Brazil'
    elif 'vietnam' in partner or 'viet nam' in partner:
        return 'Vietnam'
    elif 'colombia' in partner:
        return 'Colombia'
    elif 'uganda' in partner:
        return 'Uganda'
    elif 'ethiopia' in partner:
        return 'Ethiopia'
    elif 'indonesia' in partner:
        return 'Indonesia'
    elif any(x in partner for x in ['costa rica', 'honduras', 'guatemala']):
        return 'Central America'
    else:
        return 'Others'

def load_from_nutstore():
    try:
        if 'nutstore' not in st.secrets:
            return None, "未配置坚果云凭证"
        
        email = st.secrets['nutstore']['email']
        app_password = st.secrets['nutstore']['app_password']
        
        from webdav3.client import Client
        options = {
            'webdav_hostname': "https://dav.jianguoyun.com/dav/",
            'webdav_login': email,
            'webdav_password': app_password
        }
        client = Client(options)
        
        remote_path = "Gondwana/04_Coffee Business 咖啡业务/03 行情报告/10 Import and Price Track/Supply_Demand BS.xlsx"
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            local_path = tmp_file.name
        
        try:
            client.download_sync(remote_path=remote_path, local_path=local_path)
            import_data = pd.read_excel(local_path, sheet_name='China_Import')
            export_data = pd.read_excel(local_path, sheet_name='Original_Export')
            return (import_data, export_data), None
        finally:
            if os.path.exists(local_path):
                os.remove(local_path)
                
    except Exception as e:
        return None, str(e)

def process_data(import_data, export_data):
    date_cols = [col for col in import_data.columns if 'date' in col.lower() or 'time' in col.lower() or 'period' in col.lower()]
    if date_cols:
        import_data['date'] = pd.to_datetime(import_data[date_cols[0]], errors='coerce')
        import_data['year'] = import_data['date'].dt.year
        import_data['month'] = import_data['date'].dt.month
    
    country_cols = [col for col in import_data.columns if 'country' in col.lower() or 'partner' in col.lower()]
    if country_cols:
        import_data['Trading_partner'] = import_data[country_cols[0]]
    
    if 'Import (kg)' in import_data.columns:
        import_data['Quantity_tons'] = import_data['Import (kg)'].apply(clean_quantity_value)
    
    import_data['Country_Category'] = import_data['Trading_partner'].apply(categorize_country)
    
    monthly_by_country = import_data.groupby(['year', 'month', 'Country_Category'])['Quantity_tons'].sum().reset_index()
    monthly_pivot = monthly_by_country.pivot_table(
        index=['year', 'month'], 
        columns='Country_Category', 
        values='Quantity_tons', 
        fill_value=0
    ).reset_index()
    
    for country in COUNTRIES:
        if country not in monthly_pivot.columns:
            monthly_pivot[country] = 0
    
    monthly_pivot['Total'] = monthly_pivot[[c for c in COUNTRIES if c != 'Total' and c in monthly_pivot.columns]].sum(axis=1)
    
    cumulative_data = []
    for year in sorted(monthly_pivot['year'].unique()):
        year_data = monthly_pivot[monthly_pivot['year'] == year].sort_values('month').copy()
        for country in COUNTRIES:
            if country in year_data.columns:
                year_data[f'{country}_cumsum'] = year_data[country].cumsum()
        cumulative_data.append(year_data)
    
    cumulative_pivot = pd.concat(cumulative_data, ignore_index=True)
    return monthly_pivot, cumulative_pivot

def create_monthly_chart(monthly_pivot, selected_year):
    years = sorted(monthly_pivot['year'].unique())
    latest_year = max(years)
    historical_years = [y for y in years if y < latest_year and y >= latest_year - 4]
    
    year_colors = {2021: '#1f77b4', 2022: '#ff7f0e', 2023: '#2ca02c', 2024: '#17becf', 2025: '#9467bd', 2026: '#d62728'}
    
    fig = make_subplots(rows=3, cols=3, subplot_titles=COUNTRIES, vertical_spacing=0.12, horizontal_spacing=0.08)
    
    for idx, country in enumerate(COUNTRIES):
        row, col = idx // 3 + 1, idx % 3 + 1
        
        if country not in monthly_pivot.columns:
            continue
        
        for year in historical_years:
            year_data = monthly_pivot[monthly_pivot['year'] == year].sort_values('month')
            if len(year_data) > 0:
                fig.add_trace(
                    go.Scatter(x=year_data['month'], y=year_data[country], mode='lines+markers',
                        name=f'{int(year)}', line=dict(width=2, color=year_colors.get(int(year), '#7f7f7f')),
                        opacity=0.5, showlegend=(idx == 0), legendgroup=f'y{int(year)}'),
                    row=row, col=col)
        
        selected_data = monthly_pivot[monthly_pivot['year'] == selected_year].sort_values('month')
        if len(selected_data) > 0:
            fig.add_trace(
                go.Bar(x=selected_data['month'], y=selected_data[country],
                    name=f'{int(selected_year)}', marker_color=COLOR_MAP.get(country, '#95a5a6'),
                    opacity=0.8, showlegend=(idx == 0), legendgroup='current',
                    text=[f'{v:,.0f}' for v in selected_data[country]], textposition='outside', textfont=dict(size=7)),
                row=row, col=col)
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    fig.update_xaxes(tickmode='array', tickvals=list(range(1, 13)), ticktext=months)
    fig.update_layout(height=900, showlegend=True)
    return fig

def create_cumulative_chart(cumulative_pivot, selected_year):
    years = sorted(cumulative_pivot['year'].unique())
    latest_year = max(years)
    historical_years = [y for y in years if y < latest_year and y >= latest_year - 4]
    
    year_colors = {2021: '#1f77b4', 2022: '#ff7f0e', 2023: '#2ca02c', 2024: '#17becf', 2025: '#9467bd', 2026: '#d62728'}
    
    fig = make_subplots(rows=3, cols=3, subplot_titles=COUNTRIES, vertical_spacing=0.12, horizontal_spacing=0.08)
    
    for idx, country in enumerate(COUNTRIES):
        row, col = idx // 3 + 1, idx % 3 + 1
        cumsum_col = f'{country}_cumsum'
        
        if cumsum_col not in cumulative_pivot.columns:
            continue
        
        for year in historical_years:
            year_data = cumulative_pivot[cumulative_pivot['year'] == year].sort_values('month')
            if len(year_data) > 0:
                fig.add_trace(
                    go.Scatter(x=year_data['month'], y=year_data[cumsum_col], mode='lines+markers',
                        name=f'{int(year)}', line=dict(width=2, color=year_colors.get(int(year), '#7f7f7f')),
                        opacity=0.5, showlegend=(idx == 0), legendgroup=f'y{int(year)}'),
                    row=row, col=col)
        
        selected_data = cumulative_pivot[cumulative_pivot['year'] == selected_year].sort_values('month')
        if len(selected_data) > 0:
            fig.add_trace(
                go.Scatter(x=selected_data['month'], y=selected_data[cumsum_col], mode='lines+markers+text',
                    name=f'{int(selected_year)}', line=dict(width=3, color=COLOR_MAP.get(country, '#95a5a6')),
                    marker=dict(size=8), showlegend=(idx == 0), legendgroup='current',
                    text=[f'{v:,.0f}' for v in selected_data[cumsum_col]], textposition='top center', textfont=dict(size=7)),
                row=row, col=col)
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    fig.update_xaxes(tickmode='array', tickvals=list(range(1, 13)), ticktext=months)
    fig.update_layout(height=900, showlegend=True)
    return fig

# 主应用
st.markdown("## 中国咖啡进口数据分析")

@st.cache_data(ttl=3600)
def load_data():
    data, error = load_from_nutstore()
    if data is None:
        return None, None, error
    import_data, export_data = data
    monthly, cumulative = process_data(import_data, export_data)
    return monthly, cumulative, None

monthly_data, cumulative_data, error = load_data()

if error:
    st.error(f"数据加载失败: {error}")
    st.info("请在 Streamlit Cloud Settings -> Secrets 中配置:")
    st.code('[nutstore]\nemail = "your_email"\napp_password = "your_password"')
    st.stop()

if monthly_data is None:
    st.error("无法加载数据")
    st.stop()

years = sorted(monthly_data['year'].unique())
selected_year = max(years)

tab1, tab2 = st.tabs([f"月度 ({int(selected_year)})", f"累计 ({int(selected_year)})"])

with tab1:
    fig = create_monthly_chart(monthly_data, selected_year)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("线图=历史年份 | 柱图=当前年份")

with tab2:
    fig = create_cumulative_chart(cumulative_data, selected_year)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("细线=历史年份 | 粗线=当前年份")

st.caption(f"数据范围: {int(min(years))}-{int(max(years))} | 记录: {len(monthly_data)}条")
