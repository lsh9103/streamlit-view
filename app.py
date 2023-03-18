import pandas as pd
import streamlit as st
import altair as alt
from datetime import datetime

# 엑셀 파일 읽어오기
df = pd.read_excel('Outbound.xlsx', sheet_name='볼륨')

# 'date' 열을 datetime 형식으로 변환
df['date'] = pd.to_datetime(df['date'])

# '년', '월' 열 추가
df['년'] = df['date'].dt.year
df['월'] = df['date'].dt.month

# '출고수량' 열 이름 변경
df = df.rename(columns={'출고수량': 'volume'})

# '년-월' 컬럼이 없다면 다시 생성
if '년-월' not in df.columns:
    df['년-월'] = df['date'].dt.strftime('%Y-%m')

# 연도 필터
start_year = st.sidebar.slider("시작 연도를 선택하세요.", int(df['년'].min()), int(df['년'].max()), int(df['년'].min()))
end_year = st.sidebar.slider("종료 연도를 선택하세요.", int(df['년'].min()), int(df['년'].max()), int(df['년'].max()))

# 월 필터
start_month = st.sidebar.slider("시작 월을 선택하세요.", 1, 12, 1)
end_month = st.sidebar.slider("종료 월을 선택하세요.", 1, 12, 12)

start_date = pd.to_datetime(f"{start_year}-{start_month}-01")
end_date = pd.to_datetime(f"{end_year}-{end_month}-01") + pd.offsets.MonthEnd(0)
filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# 막대 그래프 생성
bar_chart = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X('년-월', title=None),
    y=alt.Y('volume', title='출고 수량'),
    color=alt.Color('년:O', title='연도'),
    tooltip=['년-월', 'volume']
).properties(
    width=800,
    height=500,
    title='Outbound Q.ty'
)

# Streamlit으로 출력
st.sidebar.write('### 기간 필터')
st.sidebar.write(f"선택된 날짜(범위): {start_date.date()} ~ {end_date.date()}")
selected_point = st.altair_chart(bar_chart, use_container_width=True)

st.write('### Volume Trande')
data_table = st.write(filtered_df[['년', '월', '핸들링 수량', '핸들링 피스', '입고수량', 'SKU', '입고 피스', 'CBM', '리턴수량', 'volume', 'Order', '출고 피스', '입출고 균형', '재고']])
