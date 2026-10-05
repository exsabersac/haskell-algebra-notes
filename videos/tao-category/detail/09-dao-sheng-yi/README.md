# 进阶深讲 09 · 道生一

道可道进阶深讲系列第 9 集：F-代数与代数同态、初始代数与 cata、兰贝克引理与不动点、Fix 的来历、Adámek 余极限与 Church 编码。成片约 **11:17**。

- `script.md` — 解说稿（含章节时间、代码摘录、DaoFP/CTFP 引用、数学校对备注）
- `haskell/` — cabal 包 `tao-category-dao-sheng-yi`（GHC 9.14 `-Wall`；包名无纯数字连字符段）
- `manim/` — 宣纸风 Manim 管线（tts → scenes → assemble → finalize → make_docs）
- `final/youtube.md` — 标题/说明/章节/标签草案
- `final/tao-category-detail-09.srt` — 中文字幕
- `final/thumbnail.png` — 1280×720 缩略图
- `final/preview-frames/` — 预览帧

成片 MP4 不进仓库；本地路径见制作目录 `/workspace/tao-category-video-detail/09-dao-sheng-yi/final/`。

## 本地构建

```bash
cd haskell && cabal build && cabal run tao-category-dao-sheng-yi
```

```bash
# 需已有 .venv（manim / edge-tts）与字体
cd manim
python tts.py
python paper.py ../build/paper.png
# 逐镜：manim -qh --fps 30 --media_dir ../build/hq/SID scenes.py SID
#   SID ∈ S0Title S1Hook S2Algebras S3Initial S4Lambek S5Fix S6Colimit S7Haskell S8Next
python assemble.py hq
bash finalize.sh
python make_docs.py
```

## 参考

- DaoFP ch.7 Recursion；ch.11 Algebras（Initial algebra / Lambek's Lemma and Fixed Points / Catamorphisms / Initial Algebra from Universality / Initial Algebra as a Colimit）
- CTFP 3.8 F-Algebras
