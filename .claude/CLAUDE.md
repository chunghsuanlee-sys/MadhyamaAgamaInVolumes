# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 這是什麼

《中阿含經》（T01 No.26）全 60 卷之白話譯註，依「十八品」分類，並以《例經》（經 222）之三十七道品・十一切處・十無學法為核心整理，彙整成單一 HTML：`NL_中阿含經分卷_文件彙整.html`。
HTML 格式規範：`D:\OneDrive\文件產生規範\文件整理彙整HTML規格與設計規則.md`（字型、無粗體、離線、不手動編輯 HTML 等規則都在這裡）。

本 CLAUDE.md 放在 `.claude/` 而非根目錄：產生器會把根目錄的任何檔案（含 `.gitignore` 這類點檔）當成「未分類」文件收進 HTML，只有點開頭的資料夾（`.tools`、`.claude`、`.git`）會略過。所以 `.gitignore` 放在 `.tools/`，根目錄只能有 60 卷 docx／md、`00_總覽.md`、設定檔與產出 HTML。

## 指令（PowerShell）

本機 `python` 只是 Microsoft Store 別名，請用 uv 的 Python；主控台為 cp950，需設 UTF-8：

```powershell
$env:PYTHONIOENCODING="utf-8"; $py="C:\Users\ch26669\.local\bin\python3.14.exe"
& $py .tools\docx2md.py      # docx → 同名 .md（改過 docx 才需要）
& $py .tools\extract.py      # docx → .tools\_work\txt\NN.txt
& $py .tools\syn.py          # 經號索引 idx.json＋逐經提要 syn.json（會 import index.py）
& $py .tools\build.py        # 產生 00_總覽.md、佛法核心匯整\*.md、_文件彙整設定.json
uv run --no-project --with markdown --with openpyxl --with pypdf python D:\OneDrive\文件產生規範\generate_doc_bundle.py "D:\OneDrive\Puthak\NL_中阿含經分卷"
```

順序依上；`.tools\_work\` 為中間產物（gitignore）。沒有測試；build.py 末尾的 assert（每個分組恰對到 docx＋md 兩檔、共 60 卷、222 經）即為檢查。

## 架構

- **原始資料**：`中阿含經卷第X.docx`（60 卷）。`.md` 由 docx2md.py 產生（Heading3/4/5 → `##`/`###`/`####`，numPr 段落 → `-`）；同名 docx＋md 在 HTML 中合併為一份文件，內容取 MD。
- **由 build.py 產生、勿手改**：`00_總覽.md`、`佛法核心匯整\01–06_*.md`、`_文件彙整設定.json`。要改內容請改 build.py 後重跑。
- **build.py 的資料**：
  - `PIN`：十八品表（品名、經號起訖、卷起訖、主旨、三大法門對應、代表經）。中阿含的品界線恰好落在卷界線上，所以每卷只屬一品；`SONG` 為五誦的卷範圍（依各卷卷末誦名）。
  - 經名來自 index.py 以正則抓卷內「（N）…品…經第」標題；抓不到或截斷者在 `SUT.update(...)` 手動補（71、72、143、162–164）。逐經提要缺者在 `syn.update(...)` 補寫。
  - 「道品／一切處／無學」標記：`KW` 正則在各卷文中命中後歸屬到前一個經題，再加上 `MANUAL`。
  - 設定檔：分組樣式 `中阿含經卷第X.*`、`"內嵌格式": ["md"]`（只內嵌 md，HTML 約 6 MB；內嵌 docx 時約 43 MB）、`"本機開啟連結": false`。
- **流程圖**：一律為 **UML 活動圖**記號（「act 名稱」外框、● 起點、◉ 終點、圓角框動作、實線箭頭、fork／join 粗槓、◇ 決策＋`[guard]`、泳道 partition、連接點 A/B…）。`FC_CSS`＋`chain()`（自動加起訖點）／`decision()`／`partitions()`／`fork_lanes()`／`MAIN_MAP` 在 md 內直接寫 HTML/CSS（不可用 Mermaid／CDN）。HTML 區塊內不可有空行（否則被 Markdown 拆開），前後要空行；顏色只用頁面 CSS 變數（`--accent`、`--line`…）以支援深色主題；節點文字避免「項目：內容」形式，以免被「📌 文件重點」擷取。
- **產生器** `generate_doc_bundle.py` 為多個資料夾共用，改動須維持預設行為不變，並同步更新規格書的設定表。
