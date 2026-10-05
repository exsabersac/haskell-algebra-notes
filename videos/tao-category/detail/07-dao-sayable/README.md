# 进阶深讲 07 · 道可道

道可道进阶深讲系列第 7 集（进阶篇开篇）：对象不可道，箭头可道；Yoneda 一句。成片约 **08:32**。

- `script.md` — 解说稿（含章节时间、代码摘录、DaoFP/CTFP 引用）
- `haskell/` — cabal 包 `tao-category-dao-sayable`（GHC 9.14 `-Wall`；包名无纯数字连字符段）
- `manim/` — 宣纸风 Manim 管线（tts → scenes → assemble → finalize）
- `final/youtube.md` — 标题/说明/章节/标签草案
- `final/tao-category-detail-07.srt` — 中文字幕
- `final/thumbnail.png` — 1280×720 缩略图
- `final/preview-frames/` — 预览帧

成片 MP4 不进仓库；本地路径见制作目录 `/workspace/tao-category-video-detail/07-dao-sayable/final/`。

## 本地构建

```bash
cd haskell && cabal build && cabal run tao-category-dao-sayable
```

```bash
# 需已有 .venv（manim / edge-tts）与字体
cd manim
python tts.py
# 逐镜：manim -qh --fps 30 --media_dir ../build/hq/SID scenes.py SID
python assemble.py hq
bash finalize.sh
python make_docs.py
```

## 参考

- DaoFP ch.1 Clean Slate；ch.3 Isomorphism
- CTFP 1.1–1.2
