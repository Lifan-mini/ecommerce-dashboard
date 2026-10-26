import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------- 页面基础设置 ----------------------
st.set_page_config(page_title="跨境广告投放复盘看板", layout="wide")
st.title("📊 跨境广告投放数据复盘看板")
st.markdown("支持上传广告CSV报表，自动计算投放核心指标")

# ---------------------- 上传文件 ----------------------
uploaded_file = st.file_uploader("上传广告报表（csv）", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    # 没有上传文件时，加载本地 ad_test.csv 测试数据
    df = pd.read_csv("ad_test.csv")
    st.info("✅ 当前使用本地测试文件 ad_test.csv")

# ---------------------- 计算指标 ----------------------
df["CTR"] = df["点击"] / df["曝光"]
df["CPC"] = df["花费"] / df["点击"]
df["CPA"] = df["花费"] / df["转化数"]
df["ROI"] = df["销售额"] / df["花费"]

# 保留4位小数方便看
df["CTR"] = df["CTR"].round(4)
df["CPC"] = df["CPC"].round(2)
df["CPA"] = df["CPA"].round(2)
df["ROI"] = df["ROI"].round(2)

# ---------------------- 汇总大盘数据 ----------------------
total_spend = df["花费"].sum()
total_sale = df["销售额"].sum()
total_conv = df["转化数"].sum()
total_click = df["点击"].sum()
total_imp = df["曝光"].sum()
total_roi = total_sale / total_spend

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("总花费", f"{total_spend:.2f}")
col2.metric("总销售额", f"{total_sale:.2f}")
col3.metric("总转化", f"{total_conv}")
col4.metric("总点击", f"{total_click}")
col5.metric("整体ROI", f"{total_roi:.2f}")

st.divider()

# ---------------------- 明细表格 ----------------------
st.subheader("📋 广告组明细 & 指标")
st.dataframe(df, width="stretch")

st.divider()

# ---------------------- 可视化图表 ----------------------
st.subheader("📈 各广告组 ROI 对比")
fig_roi = px.bar(df, x="广告组", y="ROI", color="ROI", text="ROI",
                 color_continuous_scale="RdYlGn", range_color=[1,5])
fig_roi.update_layout(yaxis_title="ROI")
st.plotly_chart(fig_roi, width="stretch")

st.subheader("💰 花费与销售额对比")
df_melt = pd.melt(df, id_vars=["广告组"], value_vars=["花费","销售额"], var_name="类型", value_name="金额")
fig_money = px.bar(df_melt, x="广告组", y="金额", color="类型", barmode="group")
st.dataframe(df, width="stretch")

# ---------------------- 简单复盘提示 ----------------------
st.divider()
st.subheader("💡 简单复盘提示")
bad = df[df["ROI"] < 1.5]["广告组"].tolist()
good = df[df["ROI"] >= 3]["广告组"].tolist()
st.markdown(f"""
- ✅ 高ROI优质广告组（ROI≥3）：{good}
- ⚠️ 低效广告组（ROI<1.5，建议观察/关停）：{bad}
""")

