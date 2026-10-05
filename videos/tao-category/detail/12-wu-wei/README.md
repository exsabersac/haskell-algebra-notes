# 进阶深讲 12 · 无为而无不为（系列终章）

道可道进阶深讲系列第 12 集（终章）：可表函子、米田引理、Haskell Yoneda/forall、Kan 扩张 Ran/Lan；赎回进阶 07 的「道可道」米田预告。成片约 **09:10**。

- `script.md` — 解说稿（含章节时间、代码摘录、DaoFP/CTFP 引用、数学校对备注）
- `haskell/` — cabal 包 `tao-category-wu-wei`（GHC 9.14 `-Wall`；包名无纯数字连字符段）
- `manim/` — 宣纸风 Manim 管线（tts → scenes → assemble → finalize → make_docs）
- `final/youtube.md` — 标题/说明/章节/标签草案
- `final/tao-category-detail-12.srt` — 中文字幕
- `final/thumbnail.png` — 1280×720 缩略图
- `final/preview-frames/` — 预览帧

成片 MP4 不进仓库；本地路径见制作目录 `/workspace/tao-category-video-detail/12-wu-wei/final/`。

## 本地构建

```bash
cd haskell && cabal build && cabal run tao-category-wu-wei
```

```bash
# 需已有 .venv（manim / edge-tts）与字体
cd manim
python tts.py
python paper.py ../build/paper.png
# 逐镜：manim -qh --fps 30 --media_dir ../build/hq/SID scenes.py SID
#   SID ∈ S0Title S1Hook S2Representable S3Yoneda S4Haskell S5Kan S6Close
python assemble.py hq
bash finalize.sh
python make_docs.py
```

## 参考

- DaoFP ch.2 Composition（Identity = wu wei）；ch.9 The Yoneda Lemma；ch.20 Kan Extensions
- CTFP 2.5 The Yoneda Lemma；2.6 Yoneda Embedding；3.11 Kan Extensions
- 《道德经》第三十七章
