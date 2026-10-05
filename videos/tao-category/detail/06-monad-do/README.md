# 深讲 06 · Monad 与 do 记法

道可道深讲系列第 6 集（入门深讲收束）：bind、鱼子、定律；do；Maybe / List。成片约 **08:08**。

- `script.md` — 解说稿（含章节时间、代码摘录、DaoFP/CTFP 引用）
- `haskell/` — cabal 包 `tao-category-monad`（GHC 9.14 `-Wall`；包名无纯数字连字符段）
- `manim/` — 宣纸风 Manim 管线（tts → scenes → assemble → finalize）
- `final/youtube.md` — 标题/说明/章节/标签草案
- `final/tao-category-detail-06.srt` — 中文字幕
- `final/thumbnail.png` — 1280×720 缩略图
- `final/preview-frames/` — 预览帧

成片 MP4 不进仓库；本地路径见制作目录 `/workspace/tao-category-video-detail/06-monad-do/final/`。

## 本地构建

```bash
cd haskell && cabal build && cabal run tao-category-monad
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

- DaoFP ch.15 Monads
- CTFP 3.4–3.6 Monads
