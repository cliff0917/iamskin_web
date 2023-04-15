# iamskin

## 環境配置
- Ubuntu
- Anaconda

## 建立網域
- [Linux 如何建立網域](https://cliff0917.github.io/post/Linux-%E5%BB%BA%E7%AB%8B%E7%B6%B2%E5%9F%9F/)

## 環境安裝
```
sudo apt install tmux
git clone https://github.com/cliff0917/iamskin_website.git
cd iamskin_website
source scripts/build.sh
```

## 背景執行
```
sh restart.sh
```

## 查看執行情況
```
tmux a -t web
```

## 更新 linebot 的 richmenu
- 用新的 richmenu png 覆蓋掉 `rich_menu/richmenu.png`（檔名一樣要叫 `richmenu.png`）
- 執行 `python rich_menu/richmenu.py`