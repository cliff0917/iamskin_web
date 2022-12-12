# iamskin

## 環境安裝
```
git clone https://github.com/cliff0917/iamskin.git
conda create -y -n iamskin python=3.7
conda activate iamskin
cd iamskin
pip install -r requirements.txt
python app.py
```

## 可能遇到的問題
* oserror: [errno 98] address already in use

  使用以下指令
  ```
  sudo lsof -t -i tcp:8080 | xargs kill -9
  ```
