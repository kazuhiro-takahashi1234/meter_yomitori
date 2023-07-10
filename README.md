# meter_yomitori
<br> 
https://longterm.kikagaku.ai/<br>
こちらのキカガクAI人材育成長期コースで学んだ自走期間アプリの作成で作らせていただきました。<br> 

アナログメーターの自動読み取りについて興味がありましたのでテスト的に作成しました。 <br> 
ロボットを業務でテスト的に活用しているので、自分自身の練習のために作成してみました。<br> 
とはいってもロボットは本業ではなく突発的な仕事ではあるのですが…<br>
(私自身は3年前までエクセルすらまともに扱ったことがない人間です)<br>
1枚の画像に対し1つの計器での読み取りはよくありますが、 <br> 
複数の計器があっても読み取りをするために作成。 <br> 
また、固定カメラではなく、首振りカメラや、ロボットが自動巡回して自動撮影するときに、 <br> 
撮影位置がぶれるので、それを補正するためにQRコードで読み取りしたい <br> 
アナログメーターの場所を特定し、処理を行っています。 <br>
ちなみにメーターの画像にあるQRコードは携帯でも簡単に読み込めます。  <br>
なるべくQRコードの容量を減らすことで読み取りをしやすくしました。 <br>

streamlit上での動作<br> 
https://meteryomitori-c1eqrn18jnl.streamlit.app/ <br> 
<br> 
1.テンプレートファイル(Excel)をアップロード<br> 
ここにexcel_templateをアップロード(アナログメーターと紐づける情報が入っています)<br> <br> 

2.検針画像フォルダをアップロード<br> 
meter_QRcodeフォルダをアップロード（アナログメーターの画像が入っています。）<br> <br> 

3.上記の1と2が完了したら数値データをエクセルでダウンロードできます。<br> <br> 

4.subではダウンロードしたグラフ化したいエクセルデータをアップロードしてください。<br> 
DL_excel_dataには3日分のデータが入っています。(2日目のみ数値を簡単にいじっています)<br> <br> <br> 

今回はアナログメーターで作成しましたが、ナナセグ、レベル計などがあると思います。<br> 
それらに関しても同時に自動読み取りを行うことも必要になると思います。<br> 
また、グラフを自動的に表示しましたが、閾値の設定、異常値の算出などを過去の情報から出すことも今後の目標としてあります。<br> 

https://arkouji.cocolog-nifty.com/blog/2021/09/post-2c82af.html<br> 
針を読み取るコードはここから使わせていただきました！とても感謝しています。
