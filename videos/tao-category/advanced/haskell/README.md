# tao-category (Haskell code for the video)

One module per segment; every on-screen snippet is delimited by `-- {{snip:NAME}}` … `-- {{/snip}}`
and is extracted verbatim by `manim/common.py:load_snip`.

| Module | Segment | Snippets |
|---|---|---|
| `Seg1Dao` | 一 道可道 | `s1` |
| `Seg2YouWu` | 二 有无相生 | `s2wu`, `s2you`, `s2b`, `s2c` |
| `Seg3Fix` | 三 道生一 | `s3a`, `s3b`, `s3c` |
| `Seg4Hylo` | 四 反者道之动 | `s4a`, `s4b` |
| `Seg5Adjunction` | 五 知其雄，守其雌 | `s5a`, `s5b`, `s5c`, `s5d` |
| `Seg6Yoneda` | 六 无为而无不为 | `s6a`, `s6b` |

Build & run (tested with GHC 9.14.1, cabal 3.16.1, `-Wall`, zero warnings):

    cabal build && cabal run tao-category
    # or, without cabal:
    runghc -isrc app/Main.hs

Naming follows Milewski (DaoFP ch.11/12/10/16/17/9/20; CTFP 3.8/3.2/3.6/3.7/2.5/3.11):
`Fix`/`unFix`, `Algebra`/`Coalgebra`, `cata`/`ana`/`hylo`, `unit = curry id`, `counit = uncurry id`,
`data Store s c = St (s -> c) s`, `Ran`.
