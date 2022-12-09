import pandas as pd
import numpy as np
import streamlit as st
import json
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import plotly.express as px



df_place = pd.read_csv('data/jeju_all_df.csv')
cnt_food = pd.read_csv('data/cnt_food.csv')
cnt_hansik = pd.read_csv('data/cnt_hansik.csv')
cnt_coffe = pd.read_csv('data/cnt_coffe.csv')
df_place2 = pd.read_csv('data/df_place_tmp.csv')
df_cash= pd.read_csv('data/df_cash.csv')
df_call = pd.read_csv('data/df_call.csv')
df_card = pd.read_csv('data/df_card.csv')
df_jeju_geo = pd.read_csv('data/df_jeju_geo.csv')
with open('data/jeju_geo_tmp.json',encoding='utf-8') as f:
	jeju_geo = json.load(f)
 
df_card['분석년월'] = df_card['분석년월'].astype('str')
df_card['수치'] = 1
 
#  page setting
st.set_page_config(page_title='제주도 음식 데이터 대시보드', layout='wide', page_icon='🥯')
st.title('JEJU FOOD DEMO')

st.header('0.Overview')
center = [33.41, 126.552]
m = folium.Map(location=center, zoom_start=10)
folium.Choropleth(
    geo_data=jeju_geo,
    data=df_jeju_geo,
    columns=('EMD_KOR_NM','제주도민매출금액비율'),
    key_on='feature.properties.EMD_KOR_NM',
    fill_color='YlGnBu'
).add_to(m)
marker_cluster = MarkerCluster().add_to(m)
for i in range(len(df_place)):
    folium.Marker(
        location = [df_place['Latitude'][i], df_place['Longitude'][i]],
        icon=folium.Icon(color = 'lightgreen',icon = 'bookmark', prefix='fa'),
        tooltip = f"""<p><b>가게명</b>: {df_place['가게명'][i]}<br>
                  <b>음식분야</b>: {df_place['음식 분야'][i]}<br>
                  <b>주소</b>: {df_place['주소'][i]}<br>"""
    ).add_to(marker_cluster)


st_map = st_folium(m, width = 1200)



st.header('1.지역별 수치')
st.subheader('지역,월단위 수치')
fig=px.bar(data_frame=df_card,x='행정동명',y='수치', color='분석월', 
           color_continuous_scale='ylgnbu',)
fig.update_layout(go.Layout(title={'text':'지역별 월단위 수치', 
                                'font':{'color':'#393E46', 'size':30}}, # 타이틀
                        xaxis={'title': {'text': '행정동명'}, # x축 라벨 추가, 그리드 숨김
                                'gridwidth':1, 'showgrid':False},
                        yaxis={'title': {'text': '수'}, # y축 라벨 추가
                                'gridwidth':1}, # grid line style은 바꿀수 없다.
                        legend ={'borderwidth':2, # 범례 테두리 두께
                                    'bordercolor':'black', # 범례 테두리 색
                                    'bgcolor':'#faf7af', # 범례 배경색
                                    'font':{'color':'black'} # 범례 글자 색
                                },
                        plot_bgcolor='white', # 차트 안쪽 배경색
                        font = {'color':'#393E46'} # 전체 글자(폰트) 색상
                    ),width=1000)
st.plotly_chart(fig)

st.subheader('시군구별')
st.sidebar.header('지역선택')
si_select = st.sidebar.selectbox('시선택', df_card['시군구명'].unique())
if si_select == '서귀포시':
    si_1 = df_card[df_card['시군구명']=='서귀포시'].groupby(['상호명'])[['제주도민매출금액비율','제주도민매출수비율','외지인매출금액비율','외지인매출수비율','전체매출금액비율','전체매출수비율']].sum()
    st.dataframe(si_1)
else:
    si_2 = df_card[df_card['시군구명']=='제주시'].groupby(['상호명'])[['제주도민매출금액비율','제주도민매출수비율','외지인매출금액비율','외지인매출수비율','전체매출금액비율','전체매출수비율']].sum()
    st.dataframe(si_2)


st.header('2.상담키워드')
st.sidebar.header('상담 건수')
weekdata = df_call['접수요일'].value_counts()
weeks = ['Monday','Tuesday','Wednesday','Thursday',"Friday","Saturday","Sunday"]
weekdata = weekdata.agg(weeks) 
weekdata = weekdata.to_frame().reset_index()
weekdata.columns= ['요일','상담건수']

monthdata = df_call['접수월'].value_counts()
monthdata = monthdata.to_frame().reset_index()
monthdata.columns= ['월','상담건수']

dt_range =  st.sidebar.radio(label = '월/요일', options=['월','요일'], index=0)
if dt_range== '요일':
    colors = ["#F7A4A4"] * 7
    fig = go.Figure(data=[go.Bar(x = weekdata['요일'], y=weekdata['상담건수'],marker_color = colors)])
    fig.update_layout(go.Layout(title={'text':'요일별 상담건수', 
                                   'font':{'color':'#393E46', 'size':30}}, # 타이틀
                            xaxis={'title': {'text': '월'}, # x축 라벨 추가, 그리드 숨김
                                   'gridwidth':1, 'showgrid':False},
                            yaxis={'title': {'text': '상담건수'}, # y축 라벨 추가
                                   'gridwidth':1}, # grid line style은 바꿀수 없다.
                            legend ={'borderwidth':2, # 범례 테두리 두께
                                     'bordercolor':'black', # 범례 테두리 색
                                     'bgcolor':'#faf7af', # 범례 배경색
                                     'font':{'color':'black'} # 범례 글자 색
                                    },
                            plot_bgcolor='white', # 차트 안쪽 배경색
                            font = {'color':'#393E46'} # 전체 글자(폰트) 색상
                        ),width=1000)
    st.plotly_chart(fig)
else:
    colors = ["#F7A4A4"] * 12
    fig = go.Figure(data=[go.Bar(x = monthdata['월'], y=monthdata['상담건수'],marker_color = colors)])
    fig.update_layout(go.Layout(title={'text':'월별 상담건수', 
                                   'font':{'color':'#393E46', 'size':30}}, # 타이틀
                            xaxis={'title': {'text': '월'}, # x축 라벨 추가, 그리드 숨김
                                   'gridwidth':1, 'showgrid':False},
                            yaxis={'title': {'text': '상담건수'}, # y축 라벨 추가
                                   'gridwidth':1}, # grid line style은 바꿀수 없다.
                            legend ={'borderwidth':2, # 범례 테두리 두께
                                     'bordercolor':'black', # 범례 테두리 색
                                     'bgcolor':'#faf7af', # 범례 배경색
                                     'font':{'color':'black'} # 범례 글자 색
                                    },
                            plot_bgcolor='white', # 차트 안쪽 배경색
                            font = {'color':'#393E46'} # 전체 글자(폰트) 색상
                        ),width=1000)
    st.plotly_chart(fig)