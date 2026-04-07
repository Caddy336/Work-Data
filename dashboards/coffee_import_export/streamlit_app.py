"""
咖啡进口数据可视化 - 诊断版本
"""
import streamlit as st

st.set_page_config(page_title="咖啡进口数据", page_icon="☕", layout="wide")
st.title("☕ 应用启动成功!")
st.write("如果你能看到这个页面，说明基础环境正常。")

# 测试依赖
status = []

try:
    import pandas as pd
    status.append("✅ pandas")
except Exception as e:
    status.append(f"❌ pandas: {e}")

try:
    import numpy as np
    status.append("✅ numpy")
except Exception as e:
    status.append(f"❌ numpy: {e}")

try:
    import plotly.graph_objects as go
    status.append("✅ plotly")
except Exception as e:
    status.append(f"❌ plotly: {e}")

try:
    from webdav3.client import Client
    status.append("✅ webdav3")
except Exception as e:
    status.append(f"❌ webdav3: {e}")

try:
    import openpyxl
    status.append("✅ openpyxl")
except Exception as e:
    status.append(f"❌ openpyxl: {e}")

st.subheader("依赖检查")
for s in status:
    st.write(s)

# 测试 secrets
st.subheader("Secrets 检查")
try:
    if 'nutstore' in st.secrets:
        st.write("✅ nutstore secrets 已配置")
        st.write(f"Email: {st.secrets['nutstore']['email'][:5]}...")
    else:
        st.write("⚠️ 未找到 nutstore 配置")
except Exception as e:
    st.write(f"❌ Secrets 错误: {e}")

st.info("诊断完成")
