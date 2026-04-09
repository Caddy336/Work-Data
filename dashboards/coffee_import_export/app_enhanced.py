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
import io
import warnings
warnings.filterwarnings('ignore')

# 添加当前目录到路径（确保云端部署时能找到 utils 模块）
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# 导入自定义工具模块
from utils.config import COLOR_MAP, COUNTRIES, CUSTOM_CSS
from utils.data_loader import load_from_nutstore, load_csv_data
from utils.data_processor import (
    process_import_data, 
    process_export_data, 
    create_forecast_data
)

# 页面配置
st.set_page_config(
    page_title="☕ 咖啡进口数据分析",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 应用自定义CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def fig_to_png_bytes(fig, width=1600, height=1000, scale=2):
    """将 Plotly 图表转换为 PNG 字节数据"""
    try:
        img_bytes = fig.to_image(format="png", width=width, height=height, scale=scale)
        return img_bytes
    except Exception as e:
        st.warning(f"图片生成失败: {str(e)}")
        return None


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
    # 显示所有历史年份（最近5年）
    historical_years = [y for y in years if y < latest_year and y >= latest_year - 5]
    
    # 年份颜色映射（与 notebook 保持一致）
    year_color_map = {
        2021: '#1f77b4',  # 蓝色
        2022: '#ff7f0e',  # 橙色
        2023: '#2ca02c',  # 绿色
        2024: '#17becf',  # 青色
        2025: '#9467bd',  # 紫色
    }
    
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
        
        # 绘制历史年份线图 - 每年使用固定颜色
        for year in historical_years:
            year_data = monthly_pivot[monthly_pivot['year'] == year].sort_values('month')
            if len(year_data) > 0:
                year_color = year_color_map.get(int(year), '#7f7f7f')
                fig.add_trace(
                    go.Scatter(
                        x=year_data['month'],
                        y=year_data[country],
                        mode='lines+markers',
                        name=f'{int(year)}',
                        line=dict(width=2, color=year_color),
                        marker=dict(color=year_color, size=5),
                        opacity=0.5,
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
                    textangle=0,
                    textfont=dict(size=7),
                    cliponaxis=False,
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
                        textangle=0,
                        textfont=dict(size=6, color='gray'),
                        cliponaxis=False,
                        hovertemplate='<b>预测: %{y:,.0f} 吨</b><extra></extra>'
                    ),
                    row=row, col=col
                )
    
    # 月份名称
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # 更新坐标轴格式
    # X轴：显示月份名称
    fig.update_xaxes(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=month_names,
        range=[0.5, 12.5]
    )
    
    # Y轴：只在最左侧列（col=1）显示标题
    for i in range(1, 4):  # 3行
        fig.update_yaxes(
            title_text="Import Quantity (Tons)" if i == 2 else "",  # 只在中间行显示
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
        hovermode='closest'
    )
    
    return fig

def create_single_monthly_chart(monthly_pivot, forecast_monthly, selected_year, country):
    """创建单个国家的月度图表"""
    years = sorted(monthly_pivot['year'].unique())
    latest_year = max(years)
    historical_years = [y for y in years if y < latest_year and y >= latest_year - 5]
    
    year_color_map = {
        2021: '#1f77b4',
        2022: '#ff7f0e',
        2023: '#2ca02c',
        2024: '#17becf',
        2025: '#9467bd',
    }
    
    fig = go.Figure()
    
    if country not in monthly_pivot.columns:
        return fig
    
    # 绘制历史年份线图
    for year in historical_years:
        year_data = monthly_pivot[monthly_pivot['year'] == year].sort_values('month')
        if len(year_data) > 0:
            year_color = year_color_map.get(int(year), '#7f7f7f')
            fig.add_trace(
                go.Scatter(
                    x=year_data['month'],
                    y=year_data[country],
                    mode='lines+markers',
                    name=f'{int(year)}',
                    line=dict(width=2, color=year_color),
                    marker=dict(color=year_color, size=6),
                    opacity=0.5,
                    hovertemplate='<b>%{y:,.0f} 吨</b><extra></extra>'
                )
            )
    
    # 绘制选中年份柱状图
    selected_data = monthly_pivot[monthly_pivot['year'] == selected_year].sort_values('month')
    if len(selected_data) > 0:
        text_labels = [f'{val:,.0f}' if val >= 1000 else f'{val:.0f}' 
                      for val in selected_data[country]]
        country_color = COLOR_MAP.get(country, '#95a5a6')
        
        fig.add_trace(
            go.Bar(
                x=selected_data['month'],
                y=selected_data[country],
                name=f'{int(selected_year)} (Actual)',
                marker_color=country_color,
                opacity=0.8,
                text=text_labels,
                textposition='outside',
                textangle=0,
                textfont=dict(size=16, color='#333'),
                cliponaxis=False,
                hovertemplate='<b>%{y:,.0f} 吨</b><extra></extra>'
            )
        )
    
    # 添加预测值
    if country != 'Total' and len(forecast_monthly) > 0:
        forecast_country = forecast_monthly[
            (forecast_monthly['Country_Category'] == country) & 
            (forecast_monthly['forecast_year'] == selected_year)
        ].sort_values('forecast_month')
        
        if len(forecast_country) > 0:
            forecast_col = 'Forecast_Quantity_tons' if 'Forecast_Quantity_tons' in forecast_country.columns else 'Forecast_tons'
            month_col = 'forecast_month' if 'forecast_month' in forecast_country.columns else 'month'
            forecast_text = [f'{val:,.0f}' if val >= 1000 else f'{val:.0f}' 
                            for val in forecast_country[forecast_col]]
            
            fig.add_trace(
                go.Bar(
                    x=forecast_country[month_col],
                    y=forecast_country[forecast_col],
                    name=f'{int(selected_year)} (Forecast)',
                    marker=dict(color=COLOR_MAP.get(country, '#95a5a6'), opacity=0.3, pattern_shape="/"),
                    text=forecast_text,
                    textposition='outside',
                    textangle=0,
                    textfont=dict(size=14, color='gray'),
                    cliponaxis=False,
                    hovertemplate='<b>预测: %{y:,.0f} 吨</b><extra></extra>'
                )
            )
    
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    fig.update_layout(
        title=dict(text=f"<b>{country}</b> - 月度进口量", font=dict(size=28)),
        height=550,
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=month_names,
            range=[0.5, 12.5],
            title=dict(text="月份", font=dict(size=16))
        ),
        yaxis=dict(
            title=dict(text="进口量 (吨)", font=dict(size=16)),
            tickformat=",",
            tickfont=dict(size=14),
            separatethousands=True
        ),
        showlegend=True,
        hovermode='closest',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=14))
    )
    
    return fig


def create_single_cumulative_chart(cumulative_pivot, forecast_monthly, selected_year, country):
    """创建单个国家的累计图表"""
    years = sorted(cumulative_pivot['year'].unique())
    latest_year = max(years)
    historical_years = [y for y in years if y < latest_year and y >= latest_year - 5]
    
    year_color_map = {
        2021: '#1f77b4',
        2022: '#ff7f0e',
        2023: '#2ca02c',
        2024: '#17becf',
        2025: '#9467bd',
    }
    
    fig = go.Figure()
    
    cumsum_col = f'{country}_cumsum'
    if cumsum_col not in cumulative_pivot.columns:
        return fig
    
    # 绘制历史年份
    for year in historical_years:
        year_data = cumulative_pivot[cumulative_pivot['year'] == year].sort_values('month')
        if len(year_data) > 0:
            year_color = year_color_map.get(int(year), '#7f7f7f')
            fig.add_trace(
                go.Scatter(
                    x=year_data['month'],
                    y=year_data[cumsum_col],
                    mode='lines+markers',
                    name=f'{int(year)}',
                    line=dict(width=2, color=year_color),
                    marker=dict(color=year_color, size=6),
                    opacity=0.5,
                    hovertemplate='<b>%{y:,.0f} 吨</b><extra></extra>'
                )
            )
    
    # 绘制选中年份实际数据
    selected_data = cumulative_pivot[cumulative_pivot['year'] == selected_year].sort_values('month')
    if len(selected_data) > 0:
        country_color = COLOR_MAP.get(country, '#95a5a6')
        text_labels = [f'{val:,.0f}' for val in selected_data[cumsum_col]]
        
        fig.add_trace(
            go.Scatter(
                x=selected_data['month'],
                y=selected_data[cumsum_col],
                mode='lines+markers+text',
                name=f'{int(selected_year)} (Actual)',
                line=dict(color=country_color, width=4),
                marker=dict(size=12, color=country_color),
                opacity=0.9,
                text=text_labels,
                textposition='top center',
                textfont=dict(size=15, color='#333'),
                hovertemplate='<b>%{y:,.0f} 吨</b><extra></extra>'
            )
        )
    
    # 添加预测累计数据
    if country in ['Brazil', 'Vietnam', 'Colombia', 'Uganda'] and len(forecast_monthly) > 0:
        forecast_country = forecast_monthly[
            (forecast_monthly['Country_Category'] == country) & 
            (forecast_monthly['year'] == selected_year)
        ].sort_values('month')
        
        if len(forecast_country) > 0:
            country_color = COLOR_MAP.get(country, '#95a5a6')
            
            if len(selected_data) > 0:
                base_cumsum = selected_data[cumsum_col].iloc[-1]
                last_actual_month = selected_data['month'].iloc[-1]
            else:
                base_cumsum = 0
                last_actual_month = 0
            
            forecast_country = forecast_country[forecast_country['month'] > last_actual_month]
            
            if len(forecast_country) > 0:
                forecast_col = 'Forecast_Quantity_tons' if 'Forecast_Quantity_tons' in forecast_country.columns else 'Forecast_tons'
                forecast_cumsum = base_cumsum + forecast_country[forecast_col].cumsum()
                forecast_text = [f'{val:,.0f}' for val in forecast_cumsum]
                
                fig.add_trace(
                    go.Scatter(
                        x=forecast_country['month'],
                        y=forecast_cumsum,
                        mode='lines+markers+text',
                        name=f'{int(selected_year)} (Forecast)',
                        line=dict(color=country_color, width=3, dash='dash'),
                        marker=dict(size=10, color=country_color, symbol='square'),
                        opacity=0.5,
                        text=forecast_text,
                        textposition='top center',
                        textfont=dict(size=13, color='gray'),
                        hovertemplate='<b>预测: %{y:,.0f} 吨</b><extra></extra>'
                    )
                )
    
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    fig.update_layout(
        title=dict(text=f"<b>{country}</b> - 累计进口量", font=dict(size=28)),
        height=550,
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=month_names,
            range=[0.5, 12.5],
            title=dict(text="月份", font=dict(size=16))
        ),
        yaxis=dict(
            title=dict(text="累计进口量 (吨)", font=dict(size=16)),
            tickformat=",",
            tickfont=dict(size=14),
            separatethousands=True
        ),
        showlegend=True,
        hovermode='closest',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=14))
    )
    
    return fig


def create_cumulative_grid_chart(cumulative_pivot, forecast_monthly, selected_year):
    """创建累计九宫格图表"""
    years = sorted(cumulative_pivot['year'].unique())
    latest_year = max(years)
    # 显示所有历史年份（最近5年）
    historical_years = [y for y in years if y < latest_year and y >= latest_year - 5]
    
    # 年份颜色映射（与 notebook 保持一致）
    year_color_map = {
        2021: '#1f77b4',  # 蓝色
        2022: '#ff7f0e',  # 橙色
        2023: '#2ca02c',  # 绿色
        2024: '#17becf',  # 青色
        2025: '#9467bd',  # 紫色
    }
    
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
        
        # 绘制历史年份 - 每年使用固定颜色（细线）
        for year in historical_years:
            year_data = cumulative_pivot[cumulative_pivot['year'] == year].sort_values('month')
            if len(year_data) > 0:
                year_color = year_color_map.get(int(year), '#7f7f7f')
                fig.add_trace(
                    go.Scatter(
                        x=year_data['month'],
                        y=year_data[cumsum_col],
                        mode='lines+markers',
                        name=f'{int(year)}',
                        line=dict(width=2, color=year_color),
                        marker=dict(color=year_color, size=5),
                        opacity=0.5,
                        showlegend=(idx == 0),
                        legendgroup=f'year_{int(year)}',
                        hovertemplate='<b>%{y:,.0f} 吨</b><extra></extra>'
                    ),
                    row=row, col=col
                )
        
        # 绘制选中年份实际数据（粗实线）- 使用国家颜色
        selected_data = cumulative_pivot[cumulative_pivot['year'] == selected_year].sort_values('month')
        if len(selected_data) > 0:
            country_color = COLOR_MAP.get(country, '#95a5a6')
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
        
        # 添加预测累计数据（虚线）- 只对有预测的国家
        if country in ['Brazil', 'Vietnam', 'Colombia', 'Uganda'] and len(forecast_monthly) > 0:
            # 计算预测累计值
            forecast_country = forecast_monthly[
                (forecast_monthly['Country_Category'] == country) & 
                (forecast_monthly['year'] == selected_year)
            ].sort_values('month')
            
            if len(forecast_country) > 0:
                country_color = COLOR_MAP.get(country, '#95a5a6')
                
                # 获取最后一个实际数据的累计值作为基础
                if len(selected_data) > 0:
                    base_cumsum = selected_data[cumsum_col].iloc[-1]
                    last_actual_month = selected_data['month'].iloc[-1]
                else:
                    base_cumsum = 0
                    last_actual_month = 0
                
                # 只取预测月份大于最后实际月份的数据
                forecast_country = forecast_country[forecast_country['month'] > last_actual_month]
                
                if len(forecast_country) > 0:
                    forecast_col = 'Forecast_Quantity_tons' if 'Forecast_Quantity_tons' in forecast_country.columns else 'Forecast_tons'
                    
                    # 计算预测累计值
                    forecast_cumsum = base_cumsum + forecast_country[forecast_col].cumsum()
                    forecast_text = [f'{val:,.0f}' for val in forecast_cumsum]
                    
                    fig.add_trace(
                        go.Scatter(
                            x=forecast_country['month'],
                            y=forecast_cumsum,
                            mode='lines+markers+text',
                            name=f'{int(selected_year)} (Forecast)',
                            line=dict(color=country_color, width=2.5, dash='dash'),
                            marker=dict(size=7, color=country_color, symbol='square'),
                            opacity=0.5,
                            showlegend=(idx == 0),
                            legendgroup='forecast',
                            text=forecast_text,
                            textposition='top center',
                            textfont=dict(size=7, color='gray'),
                            hovertemplate='<b>预测: %{y:,.0f} 吨</b><extra></extra>'
                        ),
                        row=row, col=col
                    )
    
    # 月份名称
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # 更新坐标轴格式
    # X轴：显示月份名称
    fig.update_xaxes(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=month_names,
        range=[0.5, 12.5]
    )
    
    # Y轴：只在最左侧列（col=1）显示标题
    for i in range(1, 4):  # 3行
        fig.update_yaxes(
            title_text="Cumulative Import (Tons)" if i == 2 else "",  # 只在中间行显示
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
        hovermode='closest'
    )
    
    return fig

# ================== 主应用 ==================

def main():
    # 标题
    st.markdown('<div class="main-title">☕ 中国咖啡进口数据分析</div>', unsafe_allow_html=True)
    
    # 使用 session_state 保存数据源选择
    if 'use_nutstore' not in st.session_state:
        st.session_state.use_nutstore = True
    
    # 加载数据
    with st.spinner('📥 正在加载数据...'):
        monthly_data, cumulative_data, total_data, forecast_data = load_and_process_data(st.session_state.use_nutstore)
    
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
    
    years = sorted(monthly_data['year'].unique())
    selected_year = max(years)
    
    # 初始化 session_state 用于跟踪当前国家索引
    if 'monthly_country_idx' not in st.session_state:
        st.session_state.monthly_country_idx = 0
    if 'cumulative_country_idx' not in st.session_state:
        st.session_state.cumulative_country_idx = 0
    
    # 主要内容区域 - 三个Tab
    tab1, tab2, tab3 = st.tabs([
        f"📈 月度图表 ({int(selected_year)})", 
        f"📉 累计图表 ({int(selected_year)})",
        "⚙️ 设置"
    ])
    
    # Tab 1: 月度图表
    with tab1:
        # 视图模式选择
        view_mode_monthly = st.radio(
            "视图模式",
            ["🔲 九宫格视图", "📄 单张视图"],
            horizontal=True,
            key="monthly_view_mode"
        )
        
        if view_mode_monthly == "🔲 九宫格视图":
            fig = create_monthly_grid_chart(monthly_data, forecast_data, selected_year)
            st.plotly_chart(fig, use_container_width=True)
            
            # 下载按钮
            img_bytes = fig_to_png_bytes(fig, width=1800, height=1200, scale=2)
            if img_bytes:
                st.download_button(
                    label="📷 下载图片",
                    data=img_bytes,
                    file_name="monthly_import_by_country.png",
                    mime="image/png",
                    key="download_monthly_grid"
                )
        else:
            # 单张视图 - 翻页导航
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col2:
                selected_country_monthly = st.selectbox(
                    "选择国家/地区",
                    COUNTRIES,
                    index=st.session_state.monthly_country_idx,
                    key="monthly_country_select"
                )
                st.session_state.monthly_country_idx = COUNTRIES.index(selected_country_monthly)
            
            with col1:
                st.write("")  # 占位对齐
                if st.button("⬅️ 上一个", key="monthly_prev", use_container_width=True):
                    st.session_state.monthly_country_idx = (st.session_state.monthly_country_idx - 1) % len(COUNTRIES)
                    st.rerun()
            
            with col3:
                st.write("")  # 占位对齐
                if st.button("下一个 ➡️", key="monthly_next", use_container_width=True):
                    st.session_state.monthly_country_idx = (st.session_state.monthly_country_idx + 1) % len(COUNTRIES)
                    st.rerun()
            
            # 显示当前国家图表
            current_country = COUNTRIES[st.session_state.monthly_country_idx]
            fig = create_single_monthly_chart(monthly_data, forecast_data, selected_year, current_country)
            st.plotly_chart(fig, use_container_width=True)
            
            # 下载按钮
            img_bytes = fig_to_png_bytes(fig, width=1200, height=700, scale=2)
            if img_bytes:
                st.download_button(
                    label=f"📷 下载 {current_country} 图片",
                    data=img_bytes,
                    file_name=f"monthly_import_{current_country.lower().replace(' ', '_')}.png",
                    mime="image/png",
                    key="download_monthly_single"
                )
            
            # 进度指示器
            st.caption(f"📍 {st.session_state.monthly_country_idx + 1} / {len(COUNTRIES)} | 使用按钮或下拉菜单切换")
        
        st.caption("💡 线图=历史年份 | 实心柱=实际值 | 斜纹柱=预测值")
    
    # Tab 2: 累计图表
    with tab2:
        # 视图模式选择
        view_mode_cumulative = st.radio(
            "视图模式",
            ["🔲 九宫格视图", "📄 单张视图"],
            horizontal=True,
            key="cumulative_view_mode"
        )
        
        if view_mode_cumulative == "🔲 九宫格视图":
            fig = create_cumulative_grid_chart(cumulative_data, forecast_data, selected_year)
            st.plotly_chart(fig, use_container_width=True)
            
            # 下载按钮
            img_bytes = fig_to_png_bytes(fig, width=1800, height=1200, scale=2)
            if img_bytes:
                st.download_button(
                    label="📷 下载图片",
                    data=img_bytes,
                    file_name="cumulative_import_by_country.png",
                    mime="image/png",
                    key="download_cumulative_grid"
                )
        else:
            # 单张视图 - 翻页导航
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col2:
                selected_country_cumulative = st.selectbox(
                    "选择国家/地区",
                    COUNTRIES,
                    index=st.session_state.cumulative_country_idx,
                    key="cumulative_country_select"
                )
                st.session_state.cumulative_country_idx = COUNTRIES.index(selected_country_cumulative)
            
            with col1:
                st.write("")  # 占位对齐
                if st.button("⬅️ 上一个", key="cumulative_prev", use_container_width=True):
                    st.session_state.cumulative_country_idx = (st.session_state.cumulative_country_idx - 1) % len(COUNTRIES)
                    st.rerun()
            
            with col3:
                st.write("")  # 占位对齐
                if st.button("下一个 ➡️", key="cumulative_next", use_container_width=True):
                    st.session_state.cumulative_country_idx = (st.session_state.cumulative_country_idx + 1) % len(COUNTRIES)
                    st.rerun()
            
            # 显示当前国家图表
            current_country = COUNTRIES[st.session_state.cumulative_country_idx]
            fig = create_single_cumulative_chart(cumulative_data, forecast_data, selected_year, current_country)
            st.plotly_chart(fig, use_container_width=True)
            
            # 下载按钮
            img_bytes = fig_to_png_bytes(fig, width=1200, height=700, scale=2)
            if img_bytes:
                st.download_button(
                    label=f"📷 下载 {current_country} 图片",
                    data=img_bytes,
                    file_name=f"cumulative_import_{current_country.lower().replace(' ', '_')}.png",
                    mime="image/png",
                    key="download_cumulative_single"
                )
            
            # 进度指示器
            st.caption(f"📍 {st.session_state.cumulative_country_idx + 1} / {len(COUNTRIES)} | 使用按钮或下拉菜单切换")
        
        st.caption("💡 细线=历史年份 | 粗线=当前年份 | 虚线=预测")
    
    # Tab 3: 设置
    with tab3:
        st.subheader("📊 数据源设置")
        
        col1, col2 = st.columns(2)
        with col1:
            new_use_nutstore = st.checkbox("从坚果云加载数据", value=st.session_state.use_nutstore,
                                           help="取消勾选使用本地CSV文件")
            if new_use_nutstore != st.session_state.use_nutstore:
                st.session_state.use_nutstore = new_use_nutstore
                st.cache_data.clear()
                st.rerun()
        
        with col2:
            if st.button("🔄 刷新数据"):
                st.cache_data.clear()
                st.rerun()
        
        st.markdown("---")
        st.subheader("📈 数据概览")
        
        src = "坚果云" if st.session_state.use_nutstore else "本地CSV"
        forecast_count = len(forecast_data) if len(forecast_data) > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("数据源", src)
        col2.metric("时间范围", f"{int(min(years))}-{int(max(years))}")
        col3.metric("数据记录", f"{len(monthly_data)}条")
        
        if forecast_count > 0:
            st.info(f"📊 包含 {forecast_count} 条预测数据")

if __name__ == "__main__":
    main()

