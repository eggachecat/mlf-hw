hw1
======
#介紹
-------
hw1 的代码 <br>
實驗結果在[all_output](all_output/)文件夾下 <br>

#預安裝
-------
[Python 3.5.1](https://www.python.org/) <br>
[numpy](https://github.com/numpy/numpy)	<br>
[matplotlib](https://github.com/matplotlib/matplotlib) <br>


#测试
-------

```
	cd current-folder
	python test.py
```

#执行
-------

```
	python main.py -p pid -f fun [-o output] [-v]
或者
	python main.py -a [-o output] [-v]

其中:

-v 顯示當前的cycle數量
-a 對所有題目跑測試並且畫出坪旅途
-p[--problem]: 题号
-f[--function]： "exp" => 跑測試 or "dig" => 畫出頻率圖
-o[--output] 目標輸出文件夾
```
#project文件說明
-----
## hw1pla.py
實作pla算法

## hw1pocket.py
實作pocket-pla算法<br>
pocket-pla繼承自pla

## hw1io.py
1. 
負責將原始資料變成標準資料<br>
其中每一筆標準資料形式如下:
```
	{
		"input": x, 
		"truth": y
	}
```
2.
負責將每次實驗結果記錄在sqlite中<br>
sqlite的結構查看[資料庫結構](#資料庫結構) <br>

3.
負責保存histogram到指定目錄下

## hw1exp.py
負責呼叫上面py中的函數、可以自定義參數，搭成一個完整實驗實例<br>
如：調用多少次、什麼時候halt、記錄number_of_uopdates等等

## hw1problems.py
按照題意變成符合題意的實驗，使用特定的參數來呼叫hw1exp的實驗

## main.py
負責處理使用命令行傳遞參數來的，并呼叫hw1problems中的題目對應的實驗

## test.py
題目的測試，呼叫main.py的命令行範例，可直接執行

#資料庫結構
-------
	exp_id	| perception_structure | numer_of_updates | err_rate | alpha | exp_category
	--------|----------------------|------------|-------------|---------------
		id  | perception的矩陣 | halt之前有多少次update | 錯誤率 | 學習速率 | 實驗類別 