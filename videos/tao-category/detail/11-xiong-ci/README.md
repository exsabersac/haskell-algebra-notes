# 进阶深讲 11 · 知其雄，守其雌

道可道进阶深讲系列第 11 集：伴随作为 hom 集自然同构、单位/余单位与三角恒等式、R∘L → State、L∘R → Store、lens 作为 Store 余代数。成片约 **11:51**。

- `script.md` — 解说稿（含章节时间、代码摘录、DaoFP/CTFP 引用、数学校对备注）
- `haskell/` — cabal 包 `tao-category-xiong-ci`（GHC 9.14 `-Wall`；包名无纯数字连字符段）
- `manim/` — 宣纸风 Manim 管线（tts → scenes → assemble → finalize → make_docs）
- `final/youtube.md` — 标题/说明/章节/标签草案
- `final/tao-category-detail-11.srt` — 中文字幕
- `final/thumbnail.png` — 1280×720 缩略图
- `final/preview-frames/` — 预览帧

成片 MP4 不进仓库；本地路径见制作目录 `/workspace/tao-category-video-detail/11-xiong-ci/final/`。

## 本地构建

```bash
cd haskell && cabal build && cabal run tao-category-xiong-ci
```

```bash
# 需已有 .venv（manim / edge-tts）与字体
cd manim
python tts.py
python paper.py ../build/paper.png
# 逐镜：manim -qh --fps 30 --media_dir ../build/hq/SID scenes.py SID
#   SID ∈ S0Title S1Hook S2Adjunction S3UnitCounit S4State S5Store S6XiongCi S7Haskell S8Next
python assemble.py hq
bash finalize.sh
python make_docs.py
```

## 参考

- DaoFP ch.10 Adjunctions；ch.16 Monads from Adjunctions；ch.17 Comonads from Adjunctions
- CTFP 3.2 Adjunctions；3.6 Monads Categorically；3.7 The Store Comonad
- 《道德经》第二十八章
