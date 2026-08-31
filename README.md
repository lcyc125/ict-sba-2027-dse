# 貪食蛇大冒險 (Snake Adventure) — ICT SBA 2027 DSE

單元 C（算法與程式編寫）貪食蛇遊戲（Python + Pygame）。

## 執行方式

1. 安裝 Python 3.8 或以上，再安裝 pygame：

```bash
pip install -r requirements.txt
```

2. 執行遊戲：

```bash
python main.py
```

## 玩法

- 輸入玩家名稱（最多 8 個字元），按 Enter 開始
- 用方向鍵控制蛇移動，吃到蘋果加 10 分
- 撞牆或者撞到自己就結束遊戲
- 遊戲結束後按 Space 重新開始、按 L 查看排行榜、按 ESC 返回選單
- 開始畫面左上角的 QR code 可以用電話掃描，開啟意見問卷填寫

## 檔案

| 檔案 | 用途 |
|------|------|
| main.py | 遊戲程式碼 |
| apple.png / worm.png / background.png | 食物、蚯蚓和背景圖片 |
| point.wav | 進食音效 |
| qr_code.png | 開始畫面的意見問卷 QR code |
| leaderboard.json | 排行榜紀錄（第一次執行時自動建立） |
