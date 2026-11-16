# Court Notes｜籃球戰術拆解室

給業餘球友閱讀的靜態戰術筆記。以互動五人半場圖，逐步介紹擋拆、傳切與手遞手，並提供分類搜尋、戰術比較、角色站位、判讀提示與來源。

## 專案規則
先讀 [AGENTS.md](AGENTS.md)。本專案有意依課堂要求，先建立規則，再製作內容與頁面，最後按相同規則新增單元。網頁本身不呼叫LLM；AI是開發協作者，AGENTS.md是讓協作者接續工作的規則，並非瀏覽器會執行的程式。

## 使用
- 線上版本：由本次對話提供的預覽連結開啟。私人預覽不能替代老師可公開開啟的作業網址。
- 本機：直接以瀏覽器開啟 `dist/index.html` 即可。戰術資料已內嵌，不需要伺服器、API金鑰或第三方套件。
- 首頁有戰術切換、逐步／播放／暫停／重播、關鍵字與分類篩選、加入／移出比較；每個戰術有獨立頁面。

## 檔案與新增方法
- `content/<slug>.md`：先寫內容稿。
- `data/plays.json`：戰術權威資料；新增一筆即會加入目錄和比較選項。
- `templates/`：兩種頁面模板。`src/assets/`：共用CSS與JS。
- `scripts/build.py`：產生網站到dist。`scripts/check.py`：檢查資料、圖解及連結。
- `evidence/extension.md`：實際新增手遞手單元的紀錄，避免只宣稱規則可用。

新增戰術前，請讓AI讀AGENTS.md及現有內容稿，核對教材後新增內容與資料，執行：

```sh
python3 scripts/build.py
python3 scripts/check.py
```

再用瀏覽器確認圖、文字與操作一致。若要產生GitHub可直接上傳的完整檔案包：

```sh
python3 scripts/export.py
```

## GitHub Pages繳交流程
1. 在自己的GitHub建立公開儲存庫，建議名稱 `basketball-playbook`。
2. 解壓 `Basketball_Playbook_Project.zip`。將裡面的檔案與資料夾直接上傳到儲存庫根目錄；不要只上傳ZIP，也不要再套一層資料夾。
3. 確認儲存庫根目錄有 `index.html` 與 `AGENTS.md`。
4. Settings → Pages → Source：Deploy from a branch → Branch：main → Folder：/(root) → Save。
5. 等部署成功，使用GitHub Pages實際顯示的網址，測試首頁、三個單元及比較功能。
6. 繳交Repository、公開網站、AGENTS.md三種連結及SUBMISSION.md中的介紹。未上傳前，檔案中的網址空格不是已完成的連結。

以後修改原始碼並重建時，網站產出在dist/。執行export.py後重新上傳最新檔案，或將dist/內容同步到GitHub發布根目錄。

## 來源與合理範圍
- 擋拆原理：FIBA／WABC Level 1，2.2.10，持球掩護選項。
- 傳切原理：Jr. NBA Rookie Practice Plan 5，Give & Go Drill。
- 手遞手原理：Jr. NBA Starter Practice Plan 9，Pass & Cut Decision Game。
完整連結與支持範圍列於各單元及data/plays.json。本站圖解、五人站位、時序、判讀與利弊比較為原創教學整理，沒有真實比賽軌跡、勝率或得分保證。

專案規則組織方式參考：
- https://github.com/diveai-lab/diveai-lessons/blob/main/CLAUDE.md
- https://github.com/diveai-lab/diveai-lessons/blob/main/README.md
課程示範參考：https://github.com/22Fatcorgi/AI-Demo
不沿用老師的吉祥物、品牌素材或專屬協作環境設定。
