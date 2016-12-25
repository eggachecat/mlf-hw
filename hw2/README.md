hw2
======
#介紹
-------
hw2 的代码 <br>
實驗結果在[all_output](all_output/)文件夾下 <br>
hw2_bounds.py 對應作業Q4 <br>
hw2.py 對應作業Q16-Q20 <br>

#預安裝
-------
[Python 3.5.1](https://www.python.org/) <br>
[numpy](https://github.com/numpy/numpy)	<br>
[matplotlib](https://github.com/matplotlib/matplotlib) <br>

#执行
-------

```
<!-- Q16-Q20 -->
	python hw2.py
<!-- Q4 -->
	python hw2_bounds.py
```
#project文件說明
-----
## hw2.py
將 logging.basicConfig(level=logging.INFO) 改为 logging.basicConfig(level=logging.DEBUG) 查看詳細執行過程<br>
DSA 這個 class 對應了descion stump algorithm <br>
会在output下輸出以下几张图:<br>
&nbsp;&nbsp;Q17.png: Q17中E_in的histogra<br>
&nbsp;&nbsp;Q18.png: Q18中E_out的histogram<br>
&nbsp;&nbsp;Q19.png: Q19中每個緯度的分佈<br>


## hw2_bounds.py
DSA 這個 class 對應了descion stump algorithm <br>
可以呼叫draw(start, end)來查看N在[start, end]上，各個bound的表現 <br>
輸出圖片格式為Q4_{start}-{end}.png<br>
会在output下輸出以下几张图:<br>
&nbsp;&nbsp;Q4_3-20: 各個bounds在N∈[3, 20]時候的表現
&nbsp;&nbsp;Q4_100-1000: 各個bounds在N∈[3, 20]時候的表現
&nbsp;&nbsp;Q4_1000-10000: 各個bounds在N∈[3, 20]時候的表現
&nbsp;&nbsp;Q4_10000-100000: 各個bounds在N∈[3, 20]時候的表現
