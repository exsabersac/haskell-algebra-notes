# 进阶深讲 10 · 反者道之动

道可道进阶深讲系列第 10 集：余代数与同态、终余代数与 ana、μF/νF 与阻抗失配、hylo 融合。成片约 **10:26**。

- `script.md` — 解说稿（含章节时间、代码摘录、DaoFP/CTFP 引用、数学校对备注）
- `haskell/` — cabal 包 `tao-category-fan-zhe`（GHC 9.14 `-Wall`；包名无纯数字连字符段）
- `manim/` — 宣纸风 Manim 管线（tts → scenes → assemble → finalize → make_docs）
- `final/youtube.md` — 标题/说明/章节/标签草案
- `final/tao-category-detail-10.srt` — 中文字幕
- `final/thumbnail.png` — 1280×720 缩略图
- `final/preview-frames/` — 预览帧

成片 MP4 不进仓库；本地路径见制作目录 `/workspace/tao-category-video-detail/10-fan-zhe/final/`。

## 本地构建

```bash
cd haskell && cabal build && cabal run tao-category-fan-zhe
```

```bash
# 需已有 .venv（manim / edge-tts）与字体
cd manim
python tts.py
python paper.py ../build/paper.png
# 逐镜：manim -qh --fps 30 --media_dir ../build/hq/SID scenes.py SID
#   SID ∈ S0Title S1Hook S2Coalgebras S3Terminal S4Flip S5MuNu S6Hylo S7Haskell S8Next
python assemble.py hq
bash finalize.sh
python make_docs.py
```

## 参考

- DaoFP ch.12 Coalgebras（Anamorphisms / Infinite data structures / Hylomorphisms / The impedance mismatch）
- CTFP 3.8 F-Algebras（Coalgebras）
