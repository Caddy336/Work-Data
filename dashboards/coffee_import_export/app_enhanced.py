"""
☕ 咖啡进口数据可视化 Web 应用（增强版）

这个 Streamlit 应用展示中国咖啡进口数据的交互式可视化分析。
数据来源：坚果云同步或本地 CSV 文件
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path
import sys
import warnings
warnings.filterwarnings('ignore')

# 导入自定义工具模块
from utils.config import COLOR_MAP, COUNTRIES, CUSTOM_CSS
from utils.data_loader import load_from_nutstore, load_csv_data
from utils.data_processor import (
    process_import_data, 
    process_export_data, 
    create_forecast_data
)

# 添加项目路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 页面配置
st.set_page_config(
    page_title="☕ 咖啡进口数据分析",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用自定义CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)



@st.cache_data(ttl=3600)
def load_and_process_data(use_nutstore=True):
    """加载并处理数据"""
    if use_nutstore:
        data, error = load_from_nutstore()
        if data is None:
            st.warning(f"⚠️ 从坚果云加载失败: {error}，将尝试使用本地CSV文件")
            return load_csv_data()
        
        import_data, export_data = data
        
        # 处理数据
        import_data = process_import_data(import_data)
        export_data_long = process_export_data(export_data)
        forecast_monthly = create_forecast_data(export_data_long, import_data)
        
        # 创建透视表
        monthly_by_country = import_data.groupby(['year', 'month', 'Country_Category'])['Quantity_tons'].sum().reset_index()
        monthly_pivot = monthly_by_country.pivot_table(
            index=['year', 'month'], 
            columns='Country_Category', 
            values='Quantity_tons', 
            fill_value=0
        ).reset_index()
        
        # 确保所有国家列存在
        for country in COUNTRIES:
            if country not in monthly_pivot.columns:
                monthly_pivot[country] = 0
        
        monthly_pivot['Total'] = monthly_pivot[[c for c in COUNTRIES if c in monthly_pivot.columns]].sum(axis=1)
        
        # 计算累计数据
        cumulative_data = []
        years = sorted(monthly_pivot['year'].unique())
        for year in years:
            year_data = monthly_pivot[monthly_pivot['year'] == year].sort_values('month').copy()
            for country in COUNTRIES:
                if country in year_data.columns:
                    year_data[f'{country}_cumsum'] = year_data[country].cumsum()
            cumulative_data.append(year_data)
        
        cumulative_pivot = pd.concat(cumulative_data, ignore_index=True)
        
        # 计算总计
        total_by_country = import_data.groupby('Country_Category')['Quantity_tons'].sum().sort_values(ascending=False)
        
        return monthly_pivot, cumulative_pivot, total_by_country, forecast_monthly
    else:
        return load_csv_data()

def load_csv_data():
    """加载本地CSV数据"""
    try:
        current_dir = Path(__file__).parent
        
        # 检查文件是否存在
        monthly_file = current_dir / 'monthly_import_data.csv'
        if not monthly_file.exists():
            st.error(f"❌ 未找到数据文件: {monthly_file}")
            st.info("💡 请先从坚果云加载数据，或确保本地CSV文件存在")
            return None, None, None, None
        
        monthly_data = pd.read_csv(monthly_file)
        cumulative_data = pd.read_csv(current_dir / 'cumulative_import_data.csv')
        total_data = pd.read_csv(current_dir / 'total_by_country.csv', index_col=0)
        
        return monthly_data, cumulative_data, total_data['Total_Quantity_Tons'], pd.DataFrame()
    except Exception as e:
        st.error(f"❌ 加载本地数据失败: {str(e)}")
        return None, None, None, None

# ================== 可视化函数 ==================

def create_monthly_grid_chart(monthly_pivot, forecast_monthly, selected_year):
    """创建月度九宫格图表"""
    years = sorted(monthly_pivot['year'].unique())
    latest_year = max(years)
    historical_years = [y for y in years if y < latest_year and y >= latest_year - 3]  # 最近3年
    
    # 创建3x3子图
    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=COUNTRIES,
        vertical_spacing=0.12,
        horizontal_spacing=0.08
    )
    
    for idx, country in enumerate(COUNTRIES):
        row = idx // 3 + 1
        col = idx % 3 + 1
        
        if country not in monthly_pivot.columns:
            continue
        
        # 绘制历史年份线图（所有国家使用统一颜色，不同年份用不同颜色区分）
        # 使用好看的颜色系列区分不同年份
        year_colors = ["#32c3cd", "#b882dd", "#D6D024"]  # 灰色系
        for year_idx, year in enumerate(historical_years):
            year_data = monthly_pivot[monthly_pivot['year'] == year].sort_values('month')
            if len(year_data) > 0:
                year_color = year_colors[year_idx % len(year_colors)]
                fig.add_trace(
                    go.Scatter(
                        x=year_data['month'],
                        y=year_data[country],
                        mode='lines+markers',
                        name=f'{int(year)}',
                        line=dict(width=2, color=year_color),
                        marker=dict(color=year_color, size=6),
                        opacity=0.6,
                        showlegend=(idx == 0),
                        legendgroup=f'year_{int(year)}',
                        hovertemplate='<b>%{y:,.0f} 吨</b><extra></extra>'
                    ),
                    row=row, col=col
                )
        
        # 绘制选中年份柱状图（使用国家颜色）
        selected_data = monthly_pivot[monthly_pivot['year'] == selected_year].sort_values('month')
        if len(selected_data) > 0:
            # 格式化数据标签：大于1000显示千分符，否则显示整数
            text_labels = [f'{val:,.0f}' if val >= 1000 else f'{val:.0f}' 
                          for val in selected_data[country]]
            
            # 使用该国家的固定颜色
            country_color = COLOR_MAP.get(country, '#95a5a6')
            
            fig.add_trace(
                go.Bar(
                    x=selected_data['month'],
                    y=selected_data[country],
                    name=f'{int(selected_year)} (Actual)',
                    marker_color=country_color,
                    opacity=0.8,
                    showlegend=(idx == 0),
                    legendgroup='actual',
                    text=text_labels,
                    textposition='outside',
                    textfont=dict(size=9),
                    hovertemplate='<b>%{y:,.0f} 吨</b><extra></extra>'
                ),
                row=row, col=col
            )
        
        # 添加预测值
        if country != 'Total' and len(forecast_monthly) > 0:
            forecast_country = forecast_monthly[
                (forecast_monthly['Country_Category'] == country) & 
                (forecast_monthly['forecast_year'] == selected_year)
            ].sort_values('forecast_month')
            
            if len(forecast_country) > 0:
                # 获取预测数据的列名（兼容不同数据源）
                forecast_col = 'Forecast_Quantity_tons' if 'Forecast_Quantity_tons' in forecast_country.columns else 'Forecast_tons'
                month_col = 'forecast_month' if 'forecast_month' in forecast_country.columns else 'month'
                
                # 格式化预测标签
                forecast_text = [f'{val:,.0f}' if val >= 1000 else f'{val:.0f}' 
                                for val in forecast_country[forecast_col]]
                
                fig.add_trace(
                    go.Bar(
                        x=forecast_country[month_col],
                        y=forecast_country[forecast_col],
                        name=f'{int(selected_year)} (Forecast)',
                        marker=dict(
                            color=COLOR_MAP.get(country, '#95a5a6'),
                            opacity=0.3,
                            pattern_shape="/"
                        ),
                        showlegend=(idx == 0),
                        legendgroup='forecast',
                        text=forecast_text,
                        textposition='outside',
                        textfont=dict(size=8, color='gray'),
                        hovertemplate='<b>预测: %{y:,.0f} 吨</b><extra></extra>'
                    ),
                    row=row, col=col
                )
    
    # 更新坐标轴格式
    # X轴：显示1-12月
    fig.update_xaxes(
        tickmode='linear',
        tick0=1,
        dtick=1,
        range=[0.5, 12.5]
    )
    
    # Y轴：只在最左侧列（col=1）显示标题
    for i in range(1, 4):  # 3行
        fig.update_yaxes(
            title_text="进口量 (吨)" if i == 2 else "",  # 只在中间行显示
            tickformat=",",
            separatethousands=True,
            row=i, col=1
        )
        # 其他列不显示Y轴标题
        for j in range(2, 4):  # 第2、3列
            fig.update_yaxes(
                tickformat=",",
                separatethousands=True,
                row=i, col=j
            )
    
    fig.update_layout(
        height=1000,
        showlegend=True,
        title_text=f"月度咖啡进口量 - {int(selected_year)}年",
        title_x=0.5,
        hovermode='closest'
    )
    
    return fig

def create_cumulative_grid_chart(cumulative_pivot, forecast_monthly, selected_year):
    """创建累计九宫格图表"""
    years = sorted(cumulative_pivot['year'].unique())
    latest_year = max(years)
    historical_years = [y for y in years if y < latest_year and y >= latest_year - 3]
    
    # 创建3x3子图
    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=COUNTRIES,
        vertical_spacing=0.12,
        horizontal_spacing=0.08
    )
    
    for idx, country in enumerate(COUNTRIES):
        row = idx // 3 + 1
        col = idx % 3 + 1
        
        cumsum_col = f'{country}_cumsum'
        if cumsum_col not in cumulative_pivot.columns:
            continue
        
        # 绘制历史年份 - 所有国家使用统一颜色，不同年份用不同颜色区分
        year_colors = ["#32c3cd", "#b882dd", "#D6D024"]  # 灰色系
        for year_idx, year in enumerate(historical_years):
            year_data = cumulative_pivot[cumulative_pivot['year'] == year].sort_values('month')
            if len(year_data) > 0:
                year_color = year_colors[year_idx % len(year_colors)]
                fig.add_trace(
                    go.Scatter(
                        x=year_data['month'],
                        y=year_data[cumsum_col],
                        mode='lines+markers',
                        name=f'{int(year)}',
                        line=dict(width=2, color=year_color),
                        marker=dict(color=year_color, size=6),
                        opacity=0.6,
                        showlegend=(idx == 0),
                        legendgroup=f'year_{int(year)}',
                        hovertemplate='<b>%{y:,.0f} 吨</b><extra></extra>'
                    ),
                    row=row, col=col
                )
        
        # 绘制选中年份（加粗并添加数据标签）- 使用国家颜色
        selected_data = cumulative_pivot[cumulative_pivot['year'] == selected_year].sort_values('month')
        if len(selected_data) > 0:
            # 使用该国家的固定颜色
            country_color = COLOR_MAP.get(country, '#95a5a6')
            
            # 只在每个数据点上显示标签
            text_labels = [f'{val:,.0f}' for val in selected_data[cumsum_col]]
            
            fig.add_trace(
                go.Scatter(
                    x=selected_data['month'],
                    y=selected_data[cumsum_col],
                    mode='lines+markers+text',
                    name=f'{int(selected_year)} (Actual)',
                    line=dict(color=country_color, width=3),
                    marker=dict(size=8, color=country_color),
                    opacity=0.9,
                    showlegend=(idx == 0),
                    legendgroup='actual',
                    text=text_labels,
                    textposition='top center',
                    textfont=dict(size=8),
                    hovertemplate='<b>%{y:,.0f} 吨</b><extra></extra>'
                ),
                row=row, col=col
            )
    
    # 更新坐标轴格式
    # X轴：显示1-12月
    fig.update_xaxes(
        tickmode='linear',
        tick0=1,
        dtick=1,
        range=[0.5, 12.5]
    )
    
    # Y轴：只在最左侧列（col=1）显示标题
    for i in range(1, 4):  # 3行
        fig.update_yaxes(
            title_text="累计进口量 (吨)" if i == 2 else "",  # 只在中间行显示
            tickformat=",",
            separatethousands=True,
            row=i, col=1
        )
        # 其他列不显示Y轴标题
        for j in range(2, 4):  # 第2、3列
            fig.update_yaxes(
                tickformat=",",
                separatethousands=True,
                row=i, col=j
            )
    
    fig.update_layout(
        height=1000,
        showlegend=True,
        title_text=f"累计咖啡进口量 - {int(selected_year)}年",
        title_x=0.5,
        hovermode='closest'
    )
    
    return fig

# ================== 主应用 ==================

def main():
    # 标题
    st.markdown('<div class="main-title">☕ 咖啡进口数据可视化分析</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">China Coffee Import Analysis Dashboard (Enhanced)</div>', unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.image("https://em-content.zobj.net/thumbs/120/apple/354/hot-beverage_2615.png", width=100)
        st.title("📊 控制面板")
        
        st.markdown("---")
        
        # 数据源选择
        st.subheader("📥 数据源")
        use_nutstore = st.checkbox("从坚果云加载数据", value=True, 
                                   help="勾选后从坚果云实时加载，取消勾选使用本地CSV文件")
        
        if st.button("🔄 刷新数据"):
            st.cache_data.clear()
            st.rerun()
    
    # 加载数据
    with st.spinner('📥 正在加载数据...'):
        monthly_data, cumulative_data, total_data, forecast_data = load_and_process_data(use_nutstore)
    
    if monthly_data is None:
        st.error("❌ 无法加载数据")
        st.info("💡 **解决方案**：")
        st.markdown("""
        1. 如果使用坚果云：检查 `.streamlit/secrets.toml` 配置是否正确
        2. 如果使用本地文件：确保以下文件存在：
           - `monthly_import_data.csv`
           - `cumulative_import_data.csv`
           - `total_by_country.csv`
        """)
        return
    
    # 确保预测数据不为 None
    if forecast_data is None or (isinstance(forecast_data, pd.DataFrame) and len(forecast_data) == 0):
        forecast_data = pd.DataFrame()  # 使用空的 DataFrame
    
    st.success(f"✅ 数据加载成功！{'(坚果云)' if use_nutstore else '(本地CSV)'}")
    if use_nutstore and len(forecast_data) > 0:
        st.info(f"📊 包含 {len(forecast_data)} 条预测数据")
    
    # 继续侧边栏配置
    with st.sidebar:
        st.markdown("---")
        
        # 数据信息
        st.subheader("📈 数据概览")
        years = sorted(monthly_data['year'].unique())
        st.info(f"**时间范围**: {int(min(years))} - {int(max(years))}")
        st.info(f"**数据记录**: {len(monthly_data)} 条")
    
    # 自动使用最新年份
    selected_year = max(years)
    
    # 主要内容区域 - 只保留两个核心Tab
    tab1, tab2 = st.tabs([
        "📈 月度九宫格", 
        "📉 累计九宫格"
    ])
    
    # Tab 1: 月度九宫格
    with tab1:
        st.header(f"📈 月度进口量九宫格 - {int(selected_year)}年")
        st.markdown("显示各国家/地区的月度进口量，包括历史对比和预测值")
        
        fig = create_monthly_grid_chart(monthly_data, forecast_data, selected_year)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 **图表说明**: 线图表示历史年份，实心柱状图表示实际值，斜纹柱状图表示预测值")
    
    # Tab 2: 累计九宫格
    with tab2:
        st.header(f"📉 累计进口量九宫格 - {int(selected_year)}年")
        st.markdown("显示各国家/地区的累计进口量趋势")
        
        fig = create_cumulative_grid_chart(cumulative_data, forecast_data, selected_year)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 **图表说明**: 细线表示历史年份，粗线表示当前选中年份")
    
    # 页脚
    st.markdown("---")
    data_source = "☁️ 坚果云实时数据" if use_nutstore else "📁 本地CSV文件"
    st.markdown(f"""
    <div style='text-align: center; color: #95a5a6; font-size: 0.9rem;'>
        <p>☕ 咖啡进口数据可视化 | 数据来源: {data_source}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

