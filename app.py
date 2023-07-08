import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO
import pandas as pd
import openpyxl
from pyzbar.pyzbar import decode
from pandas import DataFrame
import os
import cv2
import statistics
import io
from datetime import datetime
import pygwalker as pyg
import streamlit.components.v1 as components


# ページの構成をカスタマイズ
st.set_page_config(layout="wide")


# tab1, tab2 = st.tabs(["日常巡回写真", "全データグラフ"])

template_file = st.sidebar.file_uploader(
    "1.テンプレートファイル(Excel)をアップロード", type=["xlsx"], accept_multiple_files=False
)


uploaded_files = st.sidebar.file_uploader(
    "2.検針画像フォルダをアップロード", type=["jpg", "png"], accept_multiple_files=True
)

new_data = pd.DataFrame(columns=["date", "順番", "角度"])


# アップロード画像を読み込み後に、QRコード位置情報取得、画像の処理。
if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        # ここで画像の処理を実行する
        st.image(image, caption=uploaded_file.name, use_column_width=True)

        data = DataFrame(decode(image))

        data["x"] = data.rect.apply(lambda r: r.left)
        data["y"] = data.rect.apply(lambda r: r.top)
        data["w"] = data.rect.apply(lambda r: r.width)
        data["h"] = data.rect.apply(lambda r: r.height)

        # data列を','で分割して、新しい列にそれぞれのデータを割り当てる
        data[["順番"]] = pd.DataFrame(
            data["data"].apply(lambda x: x.decode("utf-8").split(":")).to_list()
        )
        data = data.sort_values("順番")

        file_name = uploaded_file.name
        date_string = file_name.split("_")[0]
        date = datetime.strptime(date_string, "%Y%m%d")
        formatted_date = date.strftime("%Y-%m-%d")
        st.write("日付:", formatted_date)

        for index, row in data.iterrows():
            x = row["x"]
            y = row["y"]
            w = row["w"]
            h = row["h"]
            zyunban = row["順番"]
            img = image.crop((x - w * 0.5, y + h + 20, x + 1.5 * w, y + 3 * h))
            # img.save(f"{a}.jpg")
            cropped_image_np = np.array(img)
            img = cv2.cvtColor(cropped_image_np, cv2.COLOR_RGB2BGR)
            # height, width, channels = img.shape[:3]
            height, width, channels = img.shape[:3]
            # 二値化

            threshold = 100

            ret, img_thresh = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

            # エッジ画像へ変換(ハフ変換で直線を求めるため)

            edges = cv2.Canny(img_thresh, 50, 200, apertureSize=3)

            # cv2.imwrite('houghlines2.jpg',edges)

            # cv2.imwrite('houghlines1.jpg',img_thresh)

            # 自動的に直線が2本となるパラメータを検出

            # minn：何点の点が並んでいたら、直線を引くか？のパラメーター値

            for m in range(10, 161, 1):
                lines = cv2.HoughLines(edges, 1, np.pi / 180, m)

                if lines is None:
                    break

                # print(len(lines))

                if len(lines) == 2:
                    minn = m

            # print('minn = ', minn)

            lines = cv2.HoughLines(edges, 1, np.pi / 180, minn)

            theta_t = []  # 原点から直線に向かって下した法線と、水平線との角度 (ラジアン) を格納する配列

            aa = []  # 直線の傾きを格納する配列

            bb = []  # 直線の切片を格納する配列

            i = 0

            for i in range(len(lines)):
                for rho, theta in lines[i]:
                    # print('rho = ', rho)

                    # print('theta = ', theta)

                    theta_t.append(theta)

                    a = np.cos(theta)

                    b = np.sin(theta)

                    x0 = a * rho

                    y0 = b * rho

                    x1 = int(x0 + 1000 * (-b))

                    y1 = int(y0 + 1000 * (a))

                    x2 = int(x0 - 1000 * (-b))

                    y2 = int(y0 - 1000 * (a))

                    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

                    # 2点を通る直線の式は、y = (y2-y1)/(x2-x1)x - (y2-y1)/(x2-x1)x1 + y1

                    # 傾き a = (y2-y1)/(x2-x1) 、 b = y1 - (y2-y1)/(x2-x1)x1

                    a0 = (y2 - y1) / (x2 - x1)

                    b0 = y1 - (y2 - y1) / (x2 - x1) * x1

                    aa.append(a0)

                    bb.append(b0)

            # 針が画像の左上、左下、右上、右下 のどこにいるかを、2直線の交点の位置で判断し、角度の式を変更

            # なお、針の中心は画像の中心にあるとして、計算

            # 交点の式は、((b[1] - b[0]) / (a[0] - a[1]) , (a[0] * b[1] - b[0] * a[1]) / (a[0] - a[1]) )

            x_t = (bb[1] - bb[0]) / (aa[0] - aa[1])

            y_t = (aa[0] * bb[1] - bb[0] * aa[1]) / (aa[0] - aa[1])

            if x_t < width / 2:  # 針が左上か左下にいるとき
                theta_hor = statistics.mean(theta_t) * 180 / np.pi

            else:  # 針が右上か右下にいるとき
                theta_hor = 270 - (90 - statistics.mean(theta_t) * 180 / np.pi)

            # print(theta_hor)

            # cv2.imwrite('meter_line.jpg', img)

            # あらかじめ設定された最大角度と最小角度
            # max_angle = 315  # 単位：度
            # min_angle = 44  # 単位：度

            # 最大圧力と最小圧力
            # max_pressure = 200  # 単位：MPa
            # min_pressure = 0  # 単位：MPa

            # 写真から計算された針の位置の角度
            needle_angle = theta_hor  # 単位：度
            # print("針の角度は、{:.1f}°です。".format(needle_angle))
            # 針の位置の角度から、圧力計の針が指している圧力を計算する
            # pressure = (needle_angle - min_angle) / (max_angle - min_angle) * \
            #    (max_pressure - min_pressure) + min_pressure

            # 結果を出力する
            # print("圧力計の針が指している数値は、{:.0f} です。".format(pressure))
            data.at[index, "角度"] = needle_angle
            # 空のデータフレームに追加
            new_row = pd.DataFrame(
                [[date, zyunban, needle_angle]], columns=["date", "順番", "角度"]
            )
            # 新しい行を空のデータフレームに追加
            new_data = pd.concat([new_data, new_row], ignore_index=True)

    # アップロードされたテンプレートファイルと作成したデータフレームを結合
    template = pd.read_excel(template_file)
    new_data["順番"] = new_data["順番"].astype(str)
    template["順番"] = template["順番"].astype(str)

    merged_df = pd.merge(new_data, template, on="順番")
    merged_df["数値"] = (
        (merged_df["角度"] - merged_df["min_angle"])
        / (merged_df["max_angle"] - merged_df["min_angle"])
        * (merged_df["max_pressure"] - merged_df["min_pressure"])
    )
    merged_df["日付"] = merged_df["date"].dt.date
    merged_df["時刻"] = merged_df["date"].dt.time
    merged_df["数値"] = merged_df["数値"].round(1)
    merged_df = merged_df.reindex(
        columns=[
            "date",
            "順番",
            "計器名",
            "数値",
            "建物名",
            "階",
            "部屋名",
            "角度",
            "max_angle",
            "min_angle",
            "max_pressure",
            "min_pressure",
            "日付",
            "時刻",
        ]
    )
    st.write(merged_df, width=800, height=200)
    merged_df.to_excel(buf := BytesIO(), index=False)

    st.sidebar.text("3.数値データダウンロード")

    st.sidebar.download_button(
        "Download",
        buf.getvalue(),
        f"{formatted_date}.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
