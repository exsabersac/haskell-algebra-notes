# 道可道：道德经 × 范畴论 × Haskell（视频材料）

用六句《道德经》读范畴论与 Haskell 的系列视频材料。本目录只收 **脚本、Haskell 源码、Manim 源码、字幕、缩略图与少量预览帧**；成片 MP4 / 旁白 WAV 等大媒体 **不在仓库**（也不应被提交）。

播放列表：[YouTube Playlist](https://www.youtube.com/playlist?list=PLUNBsZjTpca0)

| 集数 | 标题 | 链接 | 状态 |
|------|------|------|------|
| 入门篇 | 道可道：用《道德经》入门范畴论与 Haskell | https://youtu.be/Rvr0Kaigv0U | 目前不公开 |
| 进阶篇 | 道可道：用《道德经》读范畴论与 Haskell（Fix / 伴随 / 米田） | https://youtu.be/MHO5Go3j49A | — |
| 深讲 01 | 类型与箭头 | https://youtu.be/7_gerVxtJ_8 （不公开） | 材料已入库 |
| 深讲 02 | Void 与 () | YouTube https://youtu.be/ZnL-qV2bxTI （不公开） | 材料已入库 |
| 深讲 03 | Maybe 与 List | YouTube https://youtu.be/7G8f5TJ0uRA （不公开） | 材料已入库 |
| 深讲 04 | 构造与折叠 | YouTube https://youtu.be/t9FMZVuRCxM （不公开） | 材料已入库 |
| 深讲 05 | Functor | YouTube https://youtu.be/2t11eDI33T0 （不公开） | 材料已入库 |

目录：

- [`beginner/`](beginner/) — 入门篇
- [`advanced/`](advanced/) — 进阶篇
- [`detail/`](detail/) — 深讲系列（逐题展开）

每集结构大致相同：`script.md`、`haskell/`、`manim/`、`final/youtube.md`、字幕 `.srt`、`thumbnail.png`、`final/preview-frames/`（若干 jpg）。

---

## 章节

### 入门篇（成片约 13:36）

来源：[`beginner/final/youtube.md`](beginner/final/youtube.md)

```
00:00 开场：六句话，带你入门
00:55 一 道可道：对象、箭头与复合
03:01 二 有无相生：Void 与单元类型
05:00 三 道生一：Maybe、列表与折叠
06:57 四 反者道之动：展开与折叠
08:49 五 知其雄，守其雌：函子与 Applicative
11:00 六 无为而无不为：单子与 do 记法
13:12 结语：看箭头 · 进阶篇见
```

### 进阶篇（成片约 14:06）

来源：[`advanced/final/youtube.md`](advanced/final/youtube.md)

```
00:00 开场：六句话，一件事
00:42 一 道可道：对象不可道，箭头可道
02:15 二 有无相生：始对象与终对象
04:13 三 道生一：初始代数、兰贝克引理与 cata
06:52 四 反者道之动：余代数、ana 与 hylo
09:20 五 知其雄，守其雌：伴随生出 State 与 Store
11:20 六 无为而无不为：米田引理与 Kan 扩张
13:44 结语：看箭头
```

### 深讲 01 · 类型与箭头（成片约 09:57）

材料：[`detail/01-types-arrows/`](detail/01-types-arrows/) · YouTube：https://youtu.be/7_gerVxtJ_8 （不公开）

来源：[`detail/01-types-arrows/final/youtube.md`](detail/01-types-arrows/final/youtube.md)

```
00:00 开场：深讲第一集
00:56 一 道可道：对象不可道，箭头可道
02:10 二 地图：点与路
03:27 三 类型是对象，函数是箭头
04:57 四 复合与结合律
06:31 五 恒等：无为的环路
07:44 六 落到 Haskell：id 与 (.)
09:15 结语：看箭头 · 下集 Void/()
```

### 深讲 02 · Void 与 ()（成片约 08:04）

材料：[`detail/02-void-unit/`](detail/02-void-unit/) · YouTube：https://youtu.be/ZnL-qV2bxTI （不公开）

来源：[`detail/02-void-unit/final/youtube.md`](detail/02-void-unit/final/youtube.md)

```
00:00 开场：深讲第二集
00:52 一 有无相生：始与终
02:06 二 Void：无出射 · 始对象
03:35 三 ()：唯一入 · 终对象
04:42 四 对偶：有无相生
05:59 五 落到 Haskell：absurd 与 const
07:23 结语：下集 Maybe / List
```

### 深讲 03 · Maybe 与 List（成片约 07:50）

材料：[`detail/03-maybe-list/`](detail/03-maybe-list/) · YouTube：https://youtu.be/7G8f5TJ0uRA （不公开）

来源：[`detail/03-maybe-list/final/youtube.md`](detail/03-maybe-list/final/youtube.md)

```
00:00 开场：深讲第三集
00:49 一 道生一：构造子
01:53 二 Maybe = 1 + A
03:16 三 List：递归
04:43 四 从无生长
06:00 五 落到 Haskell
07:13 结语：下集构造与折叠
```


### 深讲 04 · 构造与折叠（成片约 08:50）

材料：[`detail/04-fold-unfold/`](detail/04-fold-unfold/) · YouTube https://youtu.be/t9FMZVuRCxM （不公开）

来源：[`detail/04-fold-unfold/final/youtube.md`](detail/04-fold-unfold/final/youtube.md)

```
00:00 开场：深讲第四集
00:55 一 各复归其根
02:02 二 构造代数
03:38 三 折叠 cata / foldr
05:14 四 展开 ana（浅提）
06:44 五 落到 Haskell
08:09 结语：下集 Functor
```


### 深讲 05 · Functor（成片约 08:16）

材料：[`detail/05-functor/`](detail/05-functor/) · YouTube https://youtu.be/2t11eDI33T0 （不公开）

来源：[`detail/05-functor/final/youtube.md`](detail/05-functor/final/youtube.md)

```
00:00 开场：深讲第五集
00:49 一 大制不割
01:52 二 函子保形
03:22 三 fmap / 交换图
04:48 四 函子定律
06:14 五 Maybe 与 List
07:34 结语：下集 Monad
```

---

## 运行片中的 Haskell

每集是独立的 cabal 包（`base` only）。在对应目录：

```bash
cd videos/tao-category/beginner/haskell
cabal build && cabal run tao-category-beginner

cd videos/tao-category/advanced/haskell
cabal build && cabal run tao-category

cd videos/tao-category/detail/01-types-arrows/haskell
cabal build && cabal run tao-category-types-arrows

cd videos/tao-category/detail/02-void-unit/haskell
cabal build && cabal run tao-category-void-unit

cd videos/tao-category/detail/03-maybe-list/haskell
cabal build && cabal run tao-category-maybe-list

cd videos/tao-category/detail/04-fold-unfold/haskell
cabal build && cabal run tao-category-fold-unfold

cd videos/tao-category/detail/05-functor/haskell
cabal build && cabal run tao-category-functor
```

屏幕代码用 `-- {{snip:NAME}}` … `-- {{/snip}}` 标记，由 `manim/common.py:load_snip` 抽取。GHC ≥ 9、`cabal`、`-Wall`。

---

## 重新渲染（Manim + edge-tts，简要）

依赖大致为：Manim Community、`edge-tts`、`ffmpeg` / `ffprobe`、Python 3，以及脚本里用到的中英文字体（霞鹜文楷 / Ma Shan Zheng / IBM Plex Mono / EB Garamond 等）。

管线按集目录为根（`ROOT = dirname(manim/)`）：

1. **旁白**：`python manim/tts.py` — edge-tts（`zh-CN-YunxiNeural`）写入 `audio/beats/`，元数据进 `build/tts/`。
2. **场景**：对 `manim/scenes.py` 中各 `S*…` 场景跑 Manim（例如 `manim -qh manim/scenes.py S0Title`），输出进 `build/hq/<Scene>/…`。
3. **组装**：`python manim/assemble.py hq` — 拼接画面、按节拍对齐旁白、生成 SRT/ASS。
4. **成片**：`bash manim/finalize.sh` — 宣纸叠乘、烧录字幕、AAC 混音，写出 `final/*.mp4`。
5. **文档 / 缩略图**：`python manim/make_docs.py`；`manim … Thumb` / `python manim/paper.py` 等按需。

本地会生成 `.venv/`、`build/`、`audio/`、`*.mp4`、`*.wav` / `*.mp3`；这些已由本目录 [`.gitignore`](.gitignore) 排除，**不要提交**。

> **路径说明**：脚本用相对 `ROOT`（`__file__` 推导），可搬迁。个别文案里可能仍出现绝对路径 `/workspace/tao-category-video…`（例如 beginner 的 `make_docs.py` 在生成的说明文字里引用进阶篇目录）；那只是说明文字，不是密钥。Manim / TTS 脚本里 **没有** API key / token 硬编码。

---

## 参考文献

框架主要参照 Bartosz Milewski 两本书（叙述为释义改写），章节引用见各集 `final/youtube.md`：

- **DaoFP** — [*The Dao of Functional Programming*](https://github.com/BartoszMilewski/DaoFP)  
  - 入门篇：第 1、2、7、12、14、15 章等  
  - 进阶篇：第 1、2、3、7、9（Yoneda）、10（Adjunctions）、11（Algebras）、12（Coalgebras）、16、17、20（Kan）等
- **CTFP** — [*Category Theory for Programmers*](https://github.com/hmemcpy/milewski-ctfp-pdf)  
  - 入门篇：1.1、1.2、1.5、1.6、1.7、1.8、3.4、3.6、3.8 等  
  - 进阶篇：1.5、1.6、2.5–2.6 Yoneda、3.2 Adjunctions、3.6–3.7 Monads/Comonads、3.8 F-Algebras、3.11 Kan 等
- 《道德经》第一、二、二十八、三十七、四十、四十二章

---

## 媒体不在仓库

成片、无字幕版、旁白 WAV/MP3、完整预览帧序列等体积大，**刻意不纳入**本仓库。请到 YouTube 观看；本地重建请按上一节管线生成。
