# Court Notes｜籃球戰術拆解室

把配合，變成共同語言。

Court Notes 是為業餘籃球愛好者設計的戰術學習網站。透過互動半場戰術板，將站位、跑動與傳球拆成可逐步閱讀的教學內容，協助使用者理解不同配合的目的與選擇。

## 主要功能

- **互動戰術板**：逐步查看五名球員的位置、移動方向與持球狀態，支援播放、暫停及重播。
- **戰術分類與搜尋**：依配合類型或關鍵字尋找內容。
- **多戰術比較**：對照不同戰術的目標、適合陣容、優點與風險。
- **完整教學單元**：每個戰術包含角色站位、執行步驟、防守判讀、常見錯誤及參考來源。
- **響應式版面**：依螢幕寬度調整閱讀與操作配置。

## 戰術單元

| 戰術 | 英文名稱 | 學習重點 |
|---|---|---|
| 擋拆 | Pick & Roll | 利用持球掩護，理解突破、順下與外圍接應的選擇。 |
| 傳切 | Give & Go | 傳球後持續移動，建立切入與回傳的配合。 |
| 手遞手 | Dribble Handoff | 掌握近距離交球、移動接球與後續進攻的銜接。 |

## 使用方式

以瀏覽器開啟根目錄的 `index.html`，即可瀏覽網站。

網站使用原生 HTML、CSS 與 JavaScript，戰術資料已內嵌於頁面，瀏覽時不需要後端服務、API 金鑰或額外套件。

## 專案結構

| 路徑 | 用途 |
|---|---|
| `index.html` | 網站首頁與戰術目錄。 |
| `plays/` | 各戰術的獨立教學頁面。 |
| `assets/` | 發布網站使用的樣式與互動程式。 |
| `about/` | 網站介紹與來源說明。 |
| [AGENTS.md](AGENTS.md) | 開發與內容維護規則。 |
| `content/` | 各戰術的內容稿。 |
| `data/plays.json` | 戰術資料與逐步圖解設定。 |
| `templates/` | 首頁與戰術頁的共用模板。 |
| `src/assets/` | 共用樣式與互動程式的原始檔。 |
| `scripts/` | 網站建置、檢查及匯出工具。 |
| [CHANGELOG.md](CHANGELOG.md) | 專案修改紀錄。 |

## 內容維護

新增或修改戰術前，先閱讀 [AGENTS.md](AGENTS.md)，依照既有規格整理內容稿，再更新 `data/plays.json`。

使用 Python 3 執行建置與檢查，不需要安裝第三方 Python 套件：

```sh
python3 scripts/build.py
python3 scripts/check.py
```

建置結果位於 `dist/`。確認圖文、互動與連結後，將產生的網站內容同步至發布根目錄。共用模板與樣式讓新增單元維持一致，首頁目錄與比較選項也會隨戰術資料更新。

## 參考資料

- [FIBA／WABC Level 1 Coaching Manual](https://assets.fiba.basketball/image/upload/documents-corporate-wabc-coaching-level-manuals-level-1-eng.pdf)：持球掩護與相關進攻選項。
- [Jr. NBA — Rookie Practice Plan 5](https://jr.nba.com/basketball-practice-plans/rookie/page/5/)：傳切配合。
- [Jr. NBA — Starter Practice Plan 9](https://jr.nba.com/basketball-practice-plans/starter/page/9/)：傳球後的切入與手遞手判斷。

各單元頁面另列出教材所支持的觀念。本站的五人配置、路徑與步驟時序為簡化教學安排，非真實比賽追蹤資料；戰術比較不代表得分保證或實測成功率。

