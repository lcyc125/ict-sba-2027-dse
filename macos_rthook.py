# macos_rthook.py — macOS 版啟動時用（PyInstaller --runtime-hook）
# .app 從 Finder 開啟時，工作目錄係 /（唯讀），排行榜 leaderboard.json 會寫唔到
# 所以將工作目錄改去用家資料夾，令 save_score() 可以正常寫入
import os
os.chdir(os.path.expanduser("~"))
