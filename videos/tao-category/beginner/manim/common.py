# -*- coding: utf-8 -*-
"""Shared look & timing for the 道可道 video. Rendered on WHITE; paper texture is multiplied in at mux time."""
import json, os, re, math, random
from contextlib import contextmanager
import numpy as np
from manim import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS = 30
config.background_color = WHITE

INK = "#1c1a17"
INK2 = "#4a453e"
INK3 = "#8a8378"
WASH = "#e9e5dc"
WASH2 = "#d8d2c5"
SEAL = "#b3282d"       # the single red accent: the seal
TYPE_C = "#2d4a5a"     # indigo ink for type names
STR_C = "#6b4a2b"

QUOTE_FONT = "Ma Shan Zheng"
BODY_FONT = "LXGW WenKai"
CODE_FONT = "IBM Plex Mono"

LEAD = 0.30     # visuals lead audio by this much inside a beat
TAIL = 0.65     # pause after each beat's audio

CJK_RE = re.compile(r"([\u3000-\u303f\u3400-\u9fff\uff00-\uffef\u2014\u2026]+)")


def body(s, size=34, color=INK, weight=NORMAL, font=BODY_FONT, **kw):
    return Text(s, font=font, font_size=size, color=color, weight=weight, **kw)


def mono(s, size=28, color=INK, **kw):
    return Text(s, font=CODE_FONT, font_size=size, color=color, **kw)


def mixed(s, size=30, color=INK):
    """Mixed CJK (WenKai) + Latin (Plex Mono) single line, via markup."""
    return MarkupText(_markup_mixed(s, color), font=CODE_FONT, font_size=size, color=color)


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _markup_mixed(s, color=None):
    out = []
    for part in CJK_RE.split(s):
        if not part:
            continue
        if CJK_RE.fullmatch(part):
            out.append(f'<span font_family="{BODY_FONT}">{_esc(part)}</span>')
        else:
            out.append(_esc(part))
    return "".join(out)


# ---------------------------------------------------------------- Haskell code
KEYWORDS = {"module", "where", "import", "newtype", "data", "type", "forall", "deriving",
            "instance", "let", "in", "case", "of", "class", "qualified"}
TOKEN_RE = re.compile(r'("(?:[^"\\]|\\.)*")|(--.*$)|([A-Za-z_][A-Za-z0-9_\']*)|(\s+)|(.)')


def hs_markup(line):
    out = []
    for m in TOKEN_RE.finditer(line):
        st, com, ident, ws, other = m.groups()
        if st:
            out.append(f'<span foreground="{STR_C}">{_markup_mixed(st)}</span>')
        elif com:
            out.append(f'<span foreground="{INK3}">{_markup_mixed(com)}</span>')
        elif ident:
            if ident in KEYWORDS:
                out.append(f'<span foreground="{INK}" font_weight="bold">{ident}</span>')
            elif ident[0].isupper():
                out.append(f'<span foreground="{TYPE_C}">{ident}</span>')
            else:
                out.append(f'<span foreground="{INK}">{_esc(ident)}</span>')
        elif ws:
            out.append(ws)
        else:
            out.append(f'<span foreground="{INK}">{_markup_mixed(other)}</span>')
    return "".join(out)


def load_snip(name):
    hs = os.path.join(ROOT, "haskell", "src")
    for fn in sorted(os.listdir(hs)):
        lines = open(os.path.join(hs, fn), encoding="utf-8").read().split("\n")
        for i, l in enumerate(lines):
            if l.strip() == f"-- {{{{snip:{name}}}}}":
                j = i + 1
                while lines[j].strip() != "-- {{/snip}}":
                    j += 1
                return lines[i + 1:j]
    raise KeyError(name)


class CodeBlock(VGroup):
    """Monospace code, one MarkupText per line on a shared baseline grid; supports wash highlight."""

    def __init__(self, lines, size=26, line_h=None, **kw):
        super().__init__(**kw)
        if isinstance(lines, str):
            lines = load_snip(lines)
        self.src = lines
        self.lh = line_h or size * 0.0215   # units per line
        self.anchor = Dot([0, 0, 0], radius=0.001, fill_opacity=0, stroke_opacity=0)
        self.lines = []
        for i, l in enumerate(lines):
            y = -i * self.lh
            if not l.strip():
                self.lines.append(VGroup())
                continue
            t = MarkupText("|" + hs_markup(l), font=CODE_FONT, font_size=size)
            pipe = t[0]
            t.shift([-pipe.get_left()[0], y - pipe.get_center()[1], 0])
            t.remove(pipe)
            self.lines.append(t)
        self.text = VGroup(*[l for l in self.lines if len(l)])
        self.add(self.anchor, self.text)
        self.hl = None

    def place(self, x, y):
        """Put the left edge of the code at x and line 0's centre line at y."""
        self.shift([x - self.anchor.get_x(), y - self.anchor.get_y(), 0])
        return self

    def ly(self, i):
        return self.anchor.get_y() - i * self.lh

    def line_box(self, i, j=None, pad=0.14):
        j = i if j is None else j
        y_top = self.ly(i) + self.lh * 0.5
        y_bot = self.ly(j) - self.lh * 0.5
        left = self.anchor.get_x() - pad
        right = self.text.get_right()[0] + pad
        return Rectangle(width=right - left, height=y_top - y_bot, stroke_width=0,
                         fill_color=WASH2, fill_opacity=0.6).move_to([(left + right) / 2, (y_top + y_bot) / 2, 0])

    def focus(self, i, j=None, dim=True):
        """Animation: wash-highlight lines i..j (inclusive), dim the rest."""
        j = i if j is None else j
        box = self.line_box(i, j)
        anims = []
        if self.hl is None:
            self.hl = box
            self.add_to_back(self.hl)
            anims.append(FadeIn(self.hl))
        else:
            anims.append(Transform(self.hl, box))
        if dim:
            for k, l in enumerate(self.lines):
                if len(l):
                    anims.append(l.animate.set_opacity(1.0 if i <= k <= j else 0.32))
        return AnimationGroup(*anims)

    def unfocus(self):
        anims = [l.animate.set_opacity(1.0) for l in self.lines if len(l)]
        if self.hl is not None:
            anims.append(FadeOut(self.hl))
        return AnimationGroup(*anims)

    def drop_hl(self):
        if self.hl is not None:
            self.remove(self.hl)
            self.hl = None

    def write(self):
        return LaggedStart(*[FadeIn(l, shift=RIGHT * 0.12) for l in self.lines if len(l)], lag_ratio=0.15)


def make_code(name, size=26, line_h=None):
    return CodeBlock(name, size=size, line_h=line_h)


# ---------------------------------------------------------------- ink objects
def seal(size=0.9, chars="知白守黑"):
    """Square red seal; right column read top-down first (知白), then left (守黑)."""
    sq = RoundedRectangle(corner_radius=size * 0.08, width=size, height=size,
                          fill_color=SEAL, fill_opacity=0.92, stroke_color=SEAL, stroke_width=1.5)
    cs = size * 0.40
    g = VGroup(sq)
    pos = [(0.22, 0.22), (0.22, -0.22), (-0.22, 0.22), (-0.22, -0.22)]
    for ch, (dx, dy) in zip(chars, pos):
        t = Text(ch, font=QUOTE_FONT, font_size=100, color="#fbf6ee")
        t.scale_to_fit_height(cs)
        t.move_to(sq.get_center() + np.array([dx * size, dy * size, 0]))
        g.add(t)
    return g


def ink_blob(radius=0.8, seed=3, layers=9):
    """Ink-wash blot: a dense core plus soft, irregular, off-center halos."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    k = np.arange(1, 8)
    for L in range(layers):
        t = L / (layers - 1)                     # 0 = outer halo, 1 = core
        r0 = radius * (1.55 - 0.6 * t)
        ph = rng.uniform(0, 2 * np.pi, 7)
        amp = rng.uniform(0.03, 0.10, 7) / k ** 0.9
        th = np.linspace(0, 2 * np.pi, 160, endpoint=False)
        r = r0 * (1 + (amp[:, None] * np.sin(k[:, None] * th[None, :] + ph[:, None])).sum(0))
        off = rng.normal(0, 0.05 * radius, 2) * (1 - t)
        pts = np.stack([r * np.cos(th) + off[0], r * np.sin(th) + off[1], 0 * th], 1)
        op = 0.05 + 0.05 * t if L < layers - 1 else 0.88
        g.add(Polygon(*pts, stroke_width=0, fill_color=INK, fill_opacity=op).make_smooth())
    return g


def serif(s, size=34, color=INK2, slant=ITALIC):
    return Text(s, font="EB Garamond", font_size=size, color=color, slant=slant)


def callig(s, size=60, color=INK):
    return Text(s, font=QUOTE_FONT, font_size=size, color=color)


def dots(n, r=0.055, gap=0.2, color=INK):
    if n == 0:
        return Circle(radius=0.11, color=INK3, stroke_width=2)
    return VGroup(*[Dot(radius=r, color=color) for _ in range(n)]).arrange(RIGHT, buff=gap - 2 * r)


def enso_points(R=2.0, start=PI * 0.62, sweep=1.86 * PI, frac=1.0, seed=7, width=0.34):
    rng = np.random.default_rng(seed)
    n = 220
    s = np.linspace(0, frac, max(int(n * frac), 3))
    th = start - sweep * s
    taper = np.clip(np.minimum(s / 0.08, 1), 0, 1) ** 0.6 * np.clip((1.0 - s) / 0.35, 0.25, 1)
    noise = 1 + 0.08 * np.sin(23 * s + 1.3) + 0.05 * np.sin(57 * s + 0.4)
    w = width * taper * noise
    rad = R * (1 + 0.025 * np.sin(3 * th + 0.5))
    outer = np.stack([(rad + w / 2) * np.cos(th), (rad + w / 2) * np.sin(th), 0 * th], 1)
    inner = np.stack([(rad - w / 2) * np.cos(th), (rad - w / 2) * np.sin(th), 0 * th], 1)
    return np.concatenate([outer, inner[::-1]], 0)


def enso(R=2.0, frac=1.0, **kw):
    pts = enso_points(R=R, frac=frac, **kw)
    return Polygon(*pts, stroke_width=0, fill_color=INK, fill_opacity=0.92)


# ---------------------------------------------------------------- calligraphy quote
def split_phrases(q):
    return [p for p in re.split(r"[，。；、！？]", q) if p]


def vertical_quote(q, char_h=0.7, gap=0.08, col_gap=0.5, color=INK, max_col=8):
    """Columns right→left, one phrase per column (long phrases wrap)."""
    cols = []
    for p in split_phrases(q):
        while len(p) > max_col:
            cols.append(p[:max_col]); p = p[max_col:]
        cols.append(p)
    ref = Text("道", font=QUOTE_FONT, font_size=120)
    factor = char_h * 0.86 / ref.height
    group = VGroup()
    for ci, col in enumerate(cols):
        cg = VGroup()
        for ri, ch in enumerate(col):
            t = Text(ch, font=QUOTE_FONT, font_size=120, color=color)
            t.scale(factor)
            box = Square(side_length=char_h, stroke_opacity=0, fill_opacity=0)
            box.move_to([-(ci) * (char_h + col_gap), -ri * (char_h + gap), 0])
            t.move_to(box.get_center())
            cg.add(VGroup(box, t))
        group.add(cg)
    return group


def quote_chars(vq):
    return [cell[1] for col in vq for cell in col]


# ---------------------------------------------------------------- arrows & diagrams
def node(s, size=30, color=INK):
    return mixed(s, size=size, color=color)


def arrow(a, b, buff=0.18, color=INK, sw=3.2, dashed=False, tip=0.17, curve=0):
    p = a.get_center() if isinstance(a, Mobject) else np.array(a, dtype=float)
    q = b.get_center() if isinstance(b, Mobject) else np.array(b, dtype=float)
    d = (q - p) / (np.linalg.norm(q - p) + 1e-9)
    if isinstance(a, Mobject):
        p = _edge(a, d) + d * buff
    if isinstance(b, Mobject):
        q = _edge(b, -d) - d * buff
    if curve:
        ar = CurvedArrow(p, q, angle=curve, color=color, stroke_width=sw, tip_length=tip)
    elif dashed:
        ar = DashedLine(p, q, color=color, stroke_width=sw, dash_length=0.11, dashed_ratio=0.55)
        tri = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=0).scale(tip * 0.62)
        tri.rotate(np.arctan2(d[1], d[0]) - PI / 2).move_to(q - d * tip * 0.35)
        ar = VGroup(ar, tri)
    else:
        ar = Arrow(p, q, buff=0, color=color, stroke_width=sw, tip_length=tip, max_tip_length_to_length_ratio=0.3,
                   max_stroke_width_to_length_ratio=12)
    return ar


def _edge(m, d):
    """Point on the bounding box of m in direction d from its center."""
    c = m.get_center()
    w, h = m.width / 2 + 0.02, m.height / 2 + 0.02
    dx, dy = d[0], d[1]
    tx = w / abs(dx) if abs(dx) > 1e-6 else 1e9
    ty = h / abs(dy) if abs(dy) > 1e-6 else 1e9
    t = min(tx, ty)
    return c + np.array([dx * t, dy * t, 0])


def label(ar, s, side=UP, size=24, buff=0.12, color=INK2):
    t = mixed(s, size=size, color=color)
    mid = ar.point_from_proportion(0.5) if isinstance(ar, CurvedArrow) else ar.get_center()
    t.next_to(mid, side, buff=buff)
    return t


# ---------------------------------------------------------------- the scene base
class TaoScene(Scene):
    SID = None
    QUOTE = ""
    TITLE = ""
    CHAPTER = ""

    def setup(self):
        meta = json.load(open(os.path.join(ROOT, "build", "tts", self.SID + ".json")))
        self.durs = meta["durations"]
        self.starts = [None] * len(self.durs)
        self.ends = [None] * len(self.durs)

    def now(self):
        return self.renderer.time

    def wait_until(self, t):
        n = int(round((t - self.now()) * FPS))
        if n > 0:
            self.wait((n + 0.25) / FPS)

    def at(self, k, frac):
        """Wait until a fraction of beat k's narration has elapsed."""
        self.wait_until(self.starts[k] + frac * self.durs[k])

    def end_scene(self, rt=0.9):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=rt)
        self.hold(0.3)

    def hold(self, sec):
        self.wait_until(self.now() + sec)

    @contextmanager
    def beat(self, k, tail=TAIL, lead=LEAD):
        start = self.now()
        self.starts[k] = start + lead          # audio starts here
        yield
        end = start + lead + self.durs[k] + tail
        if self.now() > end + 0.05:
            print(f"[warn] {self.SID} beat {k} visuals overrun by {self.now() - end:.2f}s")
        self.wait_until(end)
        self.ends[k] = self.now()

    def tear_down(self):
        out = os.path.join(ROOT, "build", "timings")
        os.makedirs(out, exist_ok=True)
        json.dump(dict(id=self.SID, starts=self.starts, durs=self.durs, ends=self.ends, total=self.now()),
                  open(os.path.join(out, self.SID + ".json"), "w"), indent=1)

    # ---- recurring layout pieces
    def quote_card(self, k=0):
        """Beat k: big vertical quote centered; then shrink to the right margin column. Returns small quote."""
        q = self.QUOTE
        n_cols = len(split_phrases(q))
        ch = 0.78 if max(len(p) for p in split_phrases(q)) <= 6 else 0.66
        vq = vertical_quote(q, char_h=ch, col_gap=0.42)
        vq.move_to([0.6, 0.45, 0])
        title = body(self.TITLE, size=30, color=INK2)
        chap = body(self.CHAPTER, size=26, color=INK3)
        side = VGroup(title, chap).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        side.next_to(vq, LEFT, buff=0.9).align_to(vq, DOWN)
        s = seal(0.62).next_to(side, UP, buff=0.3).align_to(side, LEFT)
        with self.beat(k, tail=1.1):
            self.play(LaggedStart(*[FadeIn(c, scale=1.08) for c in quote_chars(vq)], lag_ratio=0.12),
                      run_time=min(2.6, self.durs[k] * 0.8))
            self.play(FadeIn(side, shift=UP * 0.1), FadeIn(s, scale=1.3), run_time=0.6)
        # shrink into a marginal column at the right edge
        small = vertical_quote(q.replace("，", "").replace("；", "").replace("。", ""), char_h=0.3, gap=0.03, max_col=99)
        small = VGroup(*quote_chars(small))
        if small.height > 6.2:
            small.scale_to_fit_height(6.2)
        small.set_color(INK2).move_to([6.62, 0, 0]).align_to([0, 3.62, 0], UP)
        small_seal = seal(0.42).next_to(small, DOWN, buff=0.18)
        big = VGroup(*quote_chars(vq))
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.play(*[Transform(a, b) for a, b in zip(quote_chars(vq), small)],
                  Transform(s, small_seal), FadeOut(chap), Transform(title, head), run_time=1.0)
        self.margin = VGroup(*quote_chars(vq), s)
        self.head = title
        return self.margin

    def clear_stage(self, keep=None, rt=0.6):
        keep = keep or []
        keep_ids = set()
        for k in [self.margin, self.head] + list(keep):
            keep_ids |= {id(m) for m in k.get_family()}
        gone = [m for m in self.mobjects if id(m) not in keep_ids]
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=rt)
