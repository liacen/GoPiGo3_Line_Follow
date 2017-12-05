## 使い方


###GPG_line_followをgitでクローンする
- `git clone https://gitea.nelsia.net/nelsia/GoPiGo3_LineFollower.git`

  
###srcフォルダ内にあるline_threshold_set.pyを実行
- GPG_line_followを保存したフォルダに行く
- `sudo python line_threshold_set.py` をTerminalで実行
- ラインセンサーの全てを白い部分に乗せて [Enter]
- 現在の値で良ければ'y'を入力して [Enter]
- ラインセンサーの全てを黒い部分に乗せて [Enter]
- 現在の値で良ければ'y'を入力して [Enter]
   

###ライントレースを起動
- `sudo python line_follow.py`


####正常に動作すればこれでライントレースするはず