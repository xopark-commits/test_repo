import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="영업 데이터 분석 대시보드", layout="wide")

# 데이터 불러오기
@st.cache_data
def load_data():
    # 동일 폴더 내의 csv 읽기
    df = pd.read_csv("clean_sales_data.csv")
    # 날짜 데이터 변환 (필요 시)
    df['주문일자'] = pd.to_datetime(df['주문일자'])
    return df

try:
    df = load_data()

    # --- 사이드바: 도시 필터링 ---
    st.sidebar.header("🔍 필터 설정")
    cities = ["전체"] + sorted(df['도시'].unique().tolist())
    selected_city = st.sidebar.selectbox("도시를 선택하세요", cities)

    # 데이터 필터링
    if selected_city != "전체":
        filtered_df = df[df['도시'] == selected_city]
    else:
        filtered_df = df

    # --- 메인 화면 ---
    st.title("🚀 Sales Data Dashboard")
    st.markdown(f"**현재 선택된 도시:** `{selected_city}`")

    # 1. 데이터 개요
    col1, col2 = st.columns([1, 3])
    with col1:
        st.subheader("📋 데이터 요약")
        st.write(f"전체 행 수: {filtered_df.shape[0]}")
        st.write(f"전체 열 수: {filtered_df.shape[1]}")
    
    with col2:
        st.subheader("👀 데이터 미리보기")
        st.dataframe(filtered_df.head(5), use_container_width=True)

    st.divider()

    # 2. 도시별 매출 합계 (전체 데이터 기준 시각화가 의미 있으므로 필터 영향 받게 설정)
    st.subheader("📍 도시별 매출 합계")
    city_sales = filtered_df.groupby('도시')['주문금액'].sum().reset_index().sort_values(by='주문금액', ascending=False)
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.table(city_sales)
    with col_c2:
        fig_city = px.bar(city_sales, x='도시', y='주문금액', color='도시', title="도시별 매출 분포")
        st.plotly_chart(fig_city, use_container_width=True)

    # 3. 상품별 매출 TOP 10
    st.subheader("🏆 상품별 매출 TOP 10")
    top_products = filtered_df.groupby('상품명')['주문금액'].sum().nlargest(10).reset_index()
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.dataframe(top_products, use_container_width=True)
    with col_p2:
        fig_prod = px.bar(top_products, x='주문금액', y='상품명', orientation='h', 
                          title="상위 10개 상품 매출", color='주문금액', color_continuous_scale='Viridis')
        # 높은 매출이 위로 오도록 정렬
        fig_prod.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_prod, use_container_width=True)

    # 4. 결제방식별 매출 비율
    st.subheader("💳 결제방식별 매출 비중")
    pay_dist = filtered_df.groupby('결제방식')['주문금액'].sum().reset_index()
    fig_pie = px.pie(pay_dist, values='주문금액', names='결제방식', hole=0.4,
                     title="결제 수단별 점유율", color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

except FileNotFoundError:
    st.error("파일을 찾을 수 없습니다. 'clean_sales_data.csv' 파일이 같은 폴더에 있는지 확인해주세요.")