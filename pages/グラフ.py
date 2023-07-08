import streamlit as st
import pygwalker as pyg
import streamlit.components.v1 as components
from pandas import DataFrame
import os
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")


data_all = st.sidebar.file_uploader(
    label="※4.グラフ化したいExcelデータ",
    type=["xlsx"],
    accept_multiple_files=True,
)

# アップロードされたExcelファイルがある場合のみ処理を実行
if data_all:
    # データフレームのリストを作成
    dfs = []
    for data in data_all:
        df = pd.read_excel(data)
        dfs.append(df)

    # データフレームを連結
    concatenated_df = pd.concat(dfs)
    df_unique = concatenated_df.drop_duplicates()

    # pyg_html = pyg.walk(df_unique, return_html=True)

    # components.html(pyg_html, height=1000, scrolling=True)

    vis_spec = """[{"visId":"gw_FfSU","name":"Chart 1","encodings":{"dimensions":[{"dragId":"gw_L_SV","fid":"aW5kZXhfMA==","name":"index","semanticType":"ordinal","analyticType":"dimension"},{"dragId":"gw_NmE5","fid":"ZGF0ZV8x","name":"date","semanticType":"temporal","analyticType":"dimension"},{"dragId":"gw_nGHj","fid":"6aCG55WqXzI=","name":"順番","semanticType":"ordinal","analyticType":"dimension"},{"dragId":"gw_8qyP","fid":"6KiI5Zmo5ZCNXzM=","name":"計器名","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_YLOH","fid":"5bu654mp5ZCNXzU=","name":"建物名","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_HMgp","fid":"6ZqOXzY=","name":"階","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_lXBi","fid":"6YOo5bGL5ZCNXzc=","name":"部屋名","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_EMKz","fid":"bWF4X2FuZ2xlXzk=","name":"max_angle","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_Wiiq","fid":"bWluX2FuZ2xlXzEw","name":"min_angle","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_-i_3","fid":"bWF4X3ByZXNzdXJlXzEx","name":"max_pressure","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_mzOm","fid":"bWluX3ByZXNzdXJlXzEy","name":"min_pressure","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_XWPP","fid":"5pel5LuYXzEz","name":"日付","semanticType":"temporal","analyticType":"dimension"},{"dragId":"gw_NBEO","fid":"5pmC5Yi7XzE0","name":"時刻","semanticType":"nominal","analyticType":"dimension"}],"measures":[{"dragId":"gw_no2K","fid":"5pWw5YCkXzQ=","name":"数値","analyticType":"measure","semanticType":"ordinal","aggName":"sum"},{"dragId":"gw_Wv95","fid":"6KeS5bqmXzg=","name":"角度","analyticType":"measure","semanticType":"ordinal","aggName":"sum"},{"dragId":"gw_count_fid","fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}}],"rows":[{"dragId":"gw_TRw6","fid":"6YOo5bGL5ZCNXzc=","name":"部屋名","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_cK1m","fid":"5pWw5YCkXzQ=","name":"数値","analyticType":"measure","semanticType":"ordinal","aggName":"max"}],"columns":[{"dragId":"gw_GDkY","fid":"5pel5LuYXzEz","name":"日付","semanticType":"temporal","analyticType":"dimension"}],"color":[{"dragId":"gw__QZA","fid":"6KiI5Zmo5ZCNXzM=","name":"計器名","semanticType":"nominal","analyticType":"dimension"}],"opacity":[],"size":[],"shape":[],"radius":[],"theta":[],"details":[],"filters":[],"text":[]},"config":{"defaultAggregated":true,"geoms":["line"],"stack":"stack","showActions":false,"interactiveScale":false,"sorted":"none","zeroScale":true,"size":{"mode":"fixed","width":672,"height":260},"format":{}}}]"""
    pyg_html = pyg.walk(df_unique, spec=vis_spec, return_html=True)

    components.html(pyg_html, height=1000, scrolling=True)
