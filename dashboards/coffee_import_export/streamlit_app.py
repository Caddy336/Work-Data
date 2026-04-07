"""
☕ 咖啡进口数据可视化 Web 应用（单文件版本 - 用于云端部署）
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ================== 配置常量 ==================

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

COUNTRIES = [
    'Total', 'Brazil', 'Vietnam', 'Colombia', 'Uganda', 
    'Ethiopia', 'Central America', 'Indonesia', 'Others'
]

CUSTOM_CSS = """
<style>
    .main-title {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 0.2rem;
        margin-top: 0;
    }
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 0;
        max-width: 100%;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { height: 36px; padding: 0 12px; font-size: 0.85rem; }
</style>
"""

# ================== 数据加载器 ==================

class NutStoreLoader:
    def __init__(self, email: str, app_password: str, hostname: str = "https://dav.jianguoyun.com/dav/"):
        self.email = email
        self.app_password = app_password
        self.hostname = hostname
        self.client = None
        self._setup_client()
    
    def _setup_client(self):
        try:
            from webdav3.client import Client
            options = {
                'webdav_hostname': self.hostname,
                'webdav_login': self.email,
                'webdav_password': self.app_password
            }
            self.client = Client(options)
        except ImportError:
            raise ImportError("需要安装 webdavclient3")
    
    def download_file(self, remote_path: str, local_path: str) -> str:
        import os
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        self.client.download_sync(remote_path=remote_path, local_path=local_path)
        return local_path
    
    def load_excel(self, remote_path: str, sheet_names=None):
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            local_path = tmp_file.name
        
        try:
            self.download_file(remote_path, local_path)
            excel_file = pd.ExcelFile(local_path)
            
            if sheet_names is None:
                sheet_names = excel_file.sheet_names
            
            data_dict = {}
            for sheet_name in sheet_names:
                if sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(local_path, sheet_name=sheet_name)
                    data_dict[sheet_name] = df
            
            return data_dict
        finally:
            if os.path.exists(local_path):
                os.remove(local_path)
    
    def check_connection(self) -> bool:
        try:
            self.client.list()
            return True
        except:
            return False


def load_from_nutstore():
    try:
        if hasattr(st, 'secrets') and 'nutstore' in st.secrets:
            email = st.secrets['nutstore']['email']
            app_password = st.secrets['nutstore']['app_password']
        else:
            return None, "未配置坚果云凭证"
        
        loader = NutStoreLoader(email=email, app_password=app_password)
        
        if not loader.check_connection():
            return None, "无法连接到坚果云"
        
        remote_path = "Gondwana/04_Coffee Business 咖啡业务/03 行情报告/10 Import and Price Track/Supply_Demand BS.xlsx"
        sheet_names = ['China_Import', 'Original_Export']
        
        data_sheets = loader.load_excel(remote_path=remote_path, sheet_names=sheet_names)
        
        import_data = data_sheets['China_Import'].copy()
        export_data = data_sheets['Original_Export'].copy()
        
        return (import_data, export_data), None
        
    except Exception as e:
        return None, f"加载失败: {str(e)}"


# ================== 数据处理 ==================

def clean_quantity_value(value):
    if pd.isna(value):
        return 0
    if isinstance(value, str):
        value = value.replace(',', '').strip()
        try:
            return float(value) / 1000
        except:
            return 0
    try:
        return float(value) / 1000
    except:
        return 0


def categorize_country(partner):
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
    date_cols = [col for col in import_data.columns if 'date' in col.lower() or 'time' in col.lower() or 'period' in col.lower()]
    country_cols = [col for col in import_data.columns if 'country' in col.lower() or 'partner' in col.lower() or 'region' in col.lower()]
    
    if date_cols:
        date_col = date_cols[0]
        import_data['date'] = pd.to_datetime(import_data[date_col], errors='coerce')
        import_data['year'] = import_data['date'].dt.year
        import_data['month'] = import_data['date'].dt.month
    
    if country_cols:
        country_col = country_cols[0]
        import_data['Trading_partner'] = import_data[country_col]
    
    quantity_col = 'Import (kg)'
    if quantity_col in import_data.columns:
        import_data['Quantity_tons'] = import_data[quantity_col].apply(clean_quantity_value)
    
    import_data['Country_Category'] = import_data['Trading_partner'].apply(categorize_country)
    
    return import_data


def process_export_data(export_data):
    export_date_cols = [col for col in export_data.columns if 'date' in col.lower() or 'time' in col.lower() or 'period' in col.lower() or 'month' in col.lower()]
    
    if export_date_cols:
        export_date_col = export_date_cols[0]
        export_data['date'] = pd.to_datetime(export_data[export_date_col], errors='coerce')
        export_data['year'] = export_data['date'].dt.year
        export_data['month'] = export_data['date'].dt.month
    
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
    if len(export_data_long) == 0:
        return pd.DataFrame()
    
    delay_mapping = {'Brazil': 2, 'Colombia': 2, 'Vietnam': 1, 'Uganda': 2}
    
    def calculate_forecast_month(row):
        delay = delay_mapping.get(row['Origin_Country'], 2)
        export_date = pd.Timestamp(year=int(row['year']), month=int(row['month']), day=1)
        forecast_date = export_date + pd.DateOffset(months=delay)
        return forecast_date.year, forecast_date.month
    
    def map_export_country(country):
        mapping = {'Brazil': 'Brazil', 'Colombia': 'Colombia', 'Vietnam': 'Vietnam', 'Uganda': 'Uganda'}
        return mapping.get(country, 'Others')
    
    forecast_data = export_data_long.copy()
    forecast_results = forecast_data.apply(calculate_forecast_month, axis=1)
    forecast_data['forecast_year'] = [r[0] for r in forecast_results]
    forecast_data['forecast_month'] = [r[1] for r in forecast_results]
    forecast_data['Country_Category'] = forecast_data['Origin_Country'].apply(map_export_country)
    forecast_data = forecast_data.rename(columns={'Export_Quantity_tons': 'Forecast_Quantity_tons'})
    
    if 'year' in import_data.columns and 'month' in import_data.columns:
        max_import_year = import_data['year'].max()
        max_import_month = import_data[import_data['year'] == max_import_year]['month'].max()
        cutoff_date = pd.Timestamp(year=int(max_import_year), month=int(max_import_month), day=1)
        
        def should_keep_forecast(row):
            forecast_date = pd.Timestamp(year=int(row['forecast_year']), month=int(row['forecast_month']), day=1)
            return forecast_date > cutoff_date
        
        forecast_data = forecast_data[forecast_data.apply(should_keep_forecast, axis=1)].copy()
    
    return forecast_data


# ================== 页面配置 ==================

st.set_page_config(
    page_title="☕ 咖啡进口数据分析",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ================== 数据加载 ==================

@st.cache_data(ttl=3600)
def load_and_process_data(use_nutstore=True):
    if use_nutstore:
        data, error = load_from_nutstore()
        if data is None:
            st.warning(f"⚠️ 从坚果云加载失败: {error}")
            return None, None, None, None
        
        import_data, export_data = data
        
        import_data = process_import_data(import_data)
        export_data_long = process_export_data(export_data)
        forecast_monthly = create_forecast_data(export_data_long, import_data)
        
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
        
        monthly_pivot['Total'] = monthly_pivot[[c for c in COUNTRIES if c in monthly_pivot.columns]].sum(axis=1)
        
        cumulative_data = []
        years = sorted(monthly_pivot['year'].unique())
        for year in years:
            year_data = monthly_pivot[monthly_pivot['year'] == year].sort_values('month').copy()
            for country in COUNTRIES:
                if country in year_data.columns:
                    year_data[f'{country}_cumsum'] = year_data[country].cumsum()
            cumulative_data.append(year_data)
        
        cumulative_pivot = pd.concat(cumulative_data, ignore_index=True)
        total_by_country = import_data.groupby('Country_Category')['Quantity_tons'].sum().sort_values(ascending=False)
        
        return monthly_pivot, cumulative_pivot, total_by_country, forecast_monthly
    else:
        return None, None, None, None


# ================== 可视化函数 ==================

def create_monthly_grid_chart(monthly_pivot, forecast_monthly, selected_year):
    years = sorted(monthly_pivot['year'].unique())
    latest_year = max(years)
    historical_years = [y for y in years if y < latest_year and y >= latest_year - 5]
    
    year_color_map = {2021: '#1f77b4', 2022: '#ff7f0e', 2023: '#2ca02c', 2024: '#17becf', 2025: '#9467bd'}
    
    fig = make_subplots(rows=3, cols=3, subplot_titles=COUNTRIES, vertical_spacing=0.12, horizontal_spacing=0.08)
    
    for idx, country in enumerate(COUNTRIES):
        row = idx // 3 + 1
        col = idx % 3 + 1
        
        if country not in monthly_pivot.columns:
            continue
        
        for year in historical_years:
            year_data = monthly_pivot[monthly_pivot['year'] == year].sort_values('month')
            if len(year_data) > 0:
                year_color = year_color_map.get(int(year), '#7f7f7f')
                fig.add_trace(
                    go.Scatter(x=year_data['month'], y=year_data[country], mode='lines+markers',
                        name=f'{int(year)}', line=dict(width=2, color=year_color),
                        marker=dict(color=year_color, size=5), opacity=0.5,
                        showlegend=(idx == 0), legendgroup=f'year_{int(year)}',
                        hovertemplate='<b>%{y:,.0f} 吨</b><extra></extra>'),
                    row=row, col=col)
        
        selected_data = monthly_pivot[monthly_pivot['year'] == selected_year].sort_values('month')
        if len(selected_data) > 0:
            text_labels = [f'{val:,.0f}' if val >= 1000 else f'{val:.0f}' for val in selected_data[country]]
            country_color = COLOR_MAP.get(country, '#95a5a6')
            
            fig.add_trace(
                go.Bar(x=selected_data['month'], y=selected_data[country],
                    name=f'{int(selected_year)} (Actual)', marker_color=country_color, opacity=0.8,
                    showlegend=(idx == 0), legendgroup='actual', text=text_labels,
                    textposition='outside', textangle=0, textfont=dict(size=7), cliponaxis=False,
                    hovertemplate='<b>%{y:,.0f} 吨</b><extra></extra>'),
                row=row, col=col)
        
        if country != 'Total' and len(forecast_monthly) > 0:
            forecast_country = forecast_monthly[
                (forecast_monthly['Country_Category'] == country) & 
                (forecast_monthly['forecast_year'] == selected_year)
            ].sort_values('forecast_month')
            
            if len(forecast_country) > 0:
                forecast_col = 'Forecast_Quantity_tons' if 'Forecast_Quantity_tons' in forecast_country.columns else 'Forecast_tons'
                forecast_text = [f'{val:,.0f}' if val >= 1000 else f'{val:.0f}' for val in forecast_country[forecast_col]]
                
                fig.add_trace(
                    go.Bar(x=forecast_country['forecast_month'], y=forecast_country[forecast_col],
                        name=f'{int(selected_year)} (Forecast)',
                        marker=dict(color=COLOR_MAP.get(country, '#95a5a6'), opacity=0.3, pattern_shape="/"),
                        showlegend=(idx == 0), legendgroup='forecast', text=forecast_text,
                        textposition='outside', textangle=0, textfont=dict(size=6, color='gray'),
                        cliponaxis=False, hovertemplate='<b>预测: %{y:,.0f} 吨</b><extra></extra>'),
                    row=row, col=col)
    
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    fig.update_xaxes(tickmode='array', tickvals=list(range(1, 13)), ticktext=month_names, range=[0.5, 12.5])
    
    for i in range(1, 4):
        fig.update_yaxes(title_text="Import Quantity (Tons)" if i == 2 else "", tickformat=",", row=i, col=1)
        for j in range(2, 4):
            fig.update_yaxes(tickformat=",", row=i, col=j)
    
    fig.update_layout(height=1000, showlegend=True, hovermode='closest')
    return fig


def create_cumulative_grid_chart(cumulative_pivot, forecast_monthly, selected_year):
    years = sorted(cumulative_pivot['year'].unique())
    latest_year = max(years)
    historical_years = [y for y in years if y < latest_year and y >= latest_year - 5]
    
    year_color_map = {2021: '#1f77b4', 2022: '#ff7f0e', 2023: '#2ca02c', 2024: '#17becf', 2025: '#9467bd'}
    
    fig = make_subplots(rows=3, cols=3, subplot_titles=COUNTRIES, vertical_spacing=0.12, horizontal_spacing=0.08)
    
    for idx, country in enumerate(COUNTRIES):
        row = idx // 3 + 1
        col = idx % 3 + 1
        
        cumsum_col = f'{country}_cumsum'
        if cumsum_col not in cumulative_pivot.columns:
            continue
        
        for year in historical_years:
            year_data = cumulative_pivot[cumulative_pivot['year'] == year].sort_values('month')
            if len(year_data) > 0:
                year_color = year_color_map.get(int(year), '#7f7f7f')
                fig.add_trace(
                    go.Scatter(x=year_data['month'], y=year_data[cumsum_col], mode='lines+markers',
                        name=f'{int(year)}', line=dict(width=2, color=year_color),
                        marker=dict(color=year_color, size=5), opacity=0.5,
                        showlegend=(idx == 0), legendgroup=f'year_{int(year)}',
                        hovertemplate='<b>%{y:,.0f} 吨</b><extra></extra>'),
                    row=row, col=col)
        
        selected_data = cumulative_pivot[cumulative_pivot['year'] == selected_year].sort_values('month')
        if len(selected_data) > 0:
            country_color = COLOR_MAP.get(country, '#95a5a6')
            text_labels = [f'{val:,.0f}' for val in selected_data[cumsum_col]]
            
            fig.add_trace(
                go.Scatter(x=selected_data['month'], y=selected_data[cumsum_col], mode='lines+markers+text',
                    name=f'{int(selected_year)} (Actual)', line=dict(color=country_color, width=3),
                    marker=dict(size=8, color=country_color), opacity=0.9,
                    showlegend=(idx == 0), legendgroup='actual', text=text_labels,
                    textposition='top center', textfont=dict(size=8),
                    hovertemplate='<b>%{y:,.0f} 吨</b><extra></extra>'),
                row=row, col=col)
    
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    fig.update_xaxes(tickmode='array', tickvals=list(range(1, 13)), ticktext=month_names, range=[0.5, 12.5])
    
    for i in range(1, 4):
        fig.update_yaxes(title_text="Cumulative Import (Tons)" if i == 2 else "", tickformat=",", row=i, col=1)
        for j in range(2, 4):
            fig.update_yaxes(tickformat=",", row=i, col=j)
    
    fig.update_layout(height=1000, showlegend=True, hovermode='closest')
    return fig


# ================== 主应用 ==================

def main():
    st.markdown('<div class="main-title">☕ 中国咖啡进口数据分析</div>', unsafe_allow_html=True)
    
    if 'use_nutstore' not in st.session_state:
        st.session_state.use_nutstore = True
    
    with st.spinner('📥 正在加载数据...'):
        monthly_data, cumulative_data, total_data, forecast_data = load_and_process_data(st.session_state.use_nutstore)
    
    if monthly_data is None:
        st.error("❌ 无法加载数据")
        st.info("💡 请在 Streamlit Cloud 的 Secrets 中配置坚果云凭证")
        st.code("""
[nutstore]
email = "your_email@example.com"
app_password = "your_app_password"
        """)
        return
    
    if forecast_data is None or (isinstance(forecast_data, pd.DataFrame) and len(forecast_data) == 0):
        forecast_data = pd.DataFrame()
    
    years = sorted(monthly_data['year'].unique())
    selected_year = max(years)
    
    tab1, tab2, tab3 = st.tabs([
        f"📈 月度九宫格 ({int(selected_year)})", 
        f"📉 累计九宫格 ({int(selected_year)})",
        "⚙️ 设置"
    ])
    
    with tab1:
        fig = create_monthly_grid_chart(monthly_data, forecast_data, selected_year)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("💡 线图=历史年份 | 实心柱=实际值 | 斜纹柱=预测值")
    
    with tab2:
        fig = create_cumulative_grid_chart(cumulative_data, forecast_data, selected_year)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("💡 细线=历史年份 | 粗线=当前年份")
    
    with tab3:
        st.subheader("📊 数据源设置")
        
        if st.button("🔄 刷新数据"):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.subheader("📈 数据概览")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("数据源", "坚果云")
        col2.metric("时间范围", f"{int(min(years))}-{int(max(years))}")
        col3.metric("数据记录", f"{len(monthly_data)}条")
        
        if len(forecast_data) > 0:
            st.info(f"📊 包含 {len(forecast_data)} 条预测数据")


if __name__ == "__main__":
    main()
