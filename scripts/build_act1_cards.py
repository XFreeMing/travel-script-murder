"""Build the act-one player PDF from the reviewed card manuscript."""
from pathlib import Path
import math
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/pilots/dongfang-weicheng-act1-cards.md'
OUTPUT = ROOT / 'output/pdf/dongfang-weicheng-act1-cards.pdf'
FONT = 'ActOneChinese'
pdfmetrics.registerFont(TTFont(FONT, 'C:/Windows/Fonts/simhei.ttf'))
W, H = A4
INK = colors.HexColor('#203C43')
ACCENT = colors.HexColor('#256F76')
MUTED = colors.HexColor('#54686C')
PALE = colors.HexColor('#F2F7F5')
WARM = colors.HexColor('#F7F3E8')
BORDER = colors.HexColor('#B8C7C5')

manuscript = SOURCE.read_text(encoding='utf-8')
cards = {}
for match in re.finditer(r'^## (K[1-6]) (.*?)\n(.*?)(?=^## |\Z)', manuscript, re.M | re.S):
    cards[match[1]] = re.findall(r'^> ?(.*)$', match[3], re.M)
assert set(cards) == {f'K{i}' for i in range(1, 7)}
house_data = re.findall(r'^\| (左边|中间|右边) \| (圆形|方形) \| ([12]) \| [ABC] \|$', manuscript, re.M)
assert house_data == [('左边', '圆形', '1'), ('中间', '方形', '2'), ('右边', '圆形', '2')]
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
c.setTitle('卫城小小守灯人 - 第一幕玩家卡片 0.2.1')
c.setAuthor('travel-script-murder')
c.setSubject('原创亲子纸面试玩；角色卡、文字联、位置图签和共用屋图')


def text(x, top, value, size=17, color=INK):
    c.setFillColor(color)
    c.setFont(FONT, size)
    c.drawString(x, H - top - size * .82, value)


def lines(x, top, values, size=17, leading=25, max_width=472):
    y = top
    for value in values:
        if not value:
            y += leading * .45
            continue
        row = ''
        for char in value:
            if row and pdfmetrics.stringWidth(row + char, FONT, size) > max_width:
                text(x, y, row, size)
                y += leading
                row = char
            else:
                row += char
        if row:
            text(x, y, row, size)
            y += leading
    return y


def box(x, top, width, height, fill=colors.white, stroke=BORDER, radius=12):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(1)
    c.roundRect(x, H-top-height, width, height, radius, fill=1, stroke=1)


def cut(top):
    c.saveState()
    c.setStrokeColor(BORDER)
    c.setDash(4, 4)
    c.line(36, H-top, W-36, H-top)
    c.restoreState()


def header(page, title, subtitle):
    text(36, 27, title, 20, INK)
    text(36, 55, subtitle, 10.5, MUTED)
    text(36, 807, '原创虚构 / 纸面试玩 / 0.2.1 / 非景区路线', 9.5, MUTED)
    text(W-72, 807, f'{page} / 3', 10, MUTED)


def lantern(cx, top, scale=1):
    """The same three-wave object mark appears on every item record."""
    c.saveState()
    c.translate(cx, H-top)
    c.scale(scale, scale)
    c.setStrokeColor(INK)
    c.setLineWidth(2)
    c.setFillColor(WARM)
    c.roundRect(-25, -64, 50, 58, 14, stroke=1, fill=1)
    c.setFillColor(PALE)
    c.roundRect(-17, -7, 34, 9, 3, stroke=1, fill=1)
    c.line(-11, 3, -11, 12)
    c.line(-11, 12, 11, 12)
    c.line(11, 12, 11, 3)
    for yy in (-37, -45, -53):
        path = c.beginPath()
        path.moveTo(-18, yy)
        for xx in range(-17, 19):
            path.lineTo(xx, yy + 2.2 * math.sin((xx + 18) / 36 * 2 * math.pi))
        c.drawPath(path)
    c.line(0, -64, 0, -77)
    c.line(-6, -72, 0, -78)
    c.line(6, -72, 0, -78)
    c.restoreState()


def star(cx, top, radius, fill=INK):
    points = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        rr = radius if i % 2 == 0 else radius * .43
        points.append((cx + rr * math.cos(angle), H-top + rr * math.sin(angle)))
    p = c.beginPath()
    p.moveTo(*points[0])
    for point in points[1:]:
        p.lineTo(*point)
    p.close()
    c.setFillColor(fill)
    c.setStrokeColor(INK)
    c.setLineWidth(1.3)
    c.drawPath(p, fill=1, stroke=1)


# Page 1: two independently cut role cards; neither contains clue answers.
header(1, '卫城小小守灯人 · 第一幕', '角色卡 / 沿虚线剪开 / 可由引导者朗读')
box(36, 82, W-72, 314, PALE)
text(58, 101, '孩子先拿', 11, ACCENT)
text(58, 126, '见习守灯人', 25)
end = lines(58, 177, cards['K1'], size=17.5, leading=25, max_width=W-116)
assert end <= 384, ('K1 overflow', end)
cut(414)
box(36, 433, W-72, 345, WARM)
text(58, 452, '家长先拿', 11, ACCENT)
text(58, 477, '灯会联络员', 25)
end = lines(58, 529, cards['K2'], size=17.2, leading=26, max_width=W-116)
assert end <= 764, ('K2 overflow', end)
c.showPage()

# Page 2: text and symbol are deliberately on separate cut cards.
header(2, '两份材料，分别先拿', '沿虚线剪开 / 上半给家长 / 下半放进“搬运夹”给孩子')
box(36, 82, W-72, 333, WARM)
text(58, 99, '家长线索 · 组织者收到的文字联', 11, ACCENT)
text(58, 125, cards['K4'][0], 23)
lantern(W-88, 152, .65)
end = lines(58, 163, cards['K4'][1:7], size=16, leading=25, max_width=W-116)
assert end <= 316, ('K4 overflow', end)
box(52, 331, W-104, 64, colors.white, BORDER, 7)
text(65, 343, cards['K4'][7], 12, MUTED)
text(65, 366, cards['K4'][8], 15.5)
cut(435)
box(36, 453, W-72, 325, PALE)
text(58, 469, '孩子线索 · 打开搬运夹后取得', 11, ACCENT)
text(58, 496, '搬运夹里的图签', 23)
text(58, 538, cards['K5'][0], 17)
lantern(W-88, 527, .65)
text(58, 576, cards['K5'][1], 15, MUTED)
assert cards['K5'][2] == '★ ★'
star(W/2 - 48, 636, 30)
star(W/2 + 48, 636, 30)
text(58, 704, cards['K5'][3], 13, MUTED)
end = lines(58, 738, cards['K5'][4:], size=15, leading=22, max_width=W-116)
assert end <= 767, ('K5 overflow', end)
c.showPage()

# Page 3: public task and map, with no answer numbers or highlight.
header(3, '一家人一起看', '公共委托 + 三屋图 / 整页保留 / 用手指选屋即可')
box(36, 82, W-72, 308, PALE)
lantern(83, 123, .8)
text(128, 106, '请找到迎归灯', 24)
text(128, 143, '本次要找：灯身带三条波纹的这盏灯', 14.5, MUTED)
end = lines(58, 216, cards['K3'], size=16.5, leading=25, max_width=W-116)
assert end <= 378, ('K3 overflow', end)
text(36, 422, '三间暂存屋', 22)
lines(36, 459, cards['K6'], size=16, leading=25, max_width=W-72)

for center, (_, window, count) in zip((123, W/2, W-123), house_data):
    c.setStrokeColor(INK)
    c.setFillColor(WARM)
    c.setLineWidth(1.8)
    c.rect(center-64, H-748, 128, 171, fill=1, stroke=1)
    roof = c.beginPath()
    roof.moveTo(center-74, H-577)
    roof.lineTo(center, H-535)
    roof.lineTo(center+74, H-577)
    roof.close()
    c.setFillColor(PALE)
    c.drawPath(roof, fill=1, stroke=1)
    c.setFillColor(colors.white)
    if window == '圆形':
        c.circle(center, H-615, 18, fill=1, stroke=1)
    else:
        c.rect(center-18, H-633, 36, 36, fill=1, stroke=1)
    c.roundRect(center-26, H-748, 52, 78, 3, fill=1, stroke=1)
    if count == '1':
        star(center, 696, 10)
    else:
        star(center-12, 696, 10)
        star(center+12, 696, 10)
    c.circle(center+16, H-730, 1.7, fill=1, stroke=1)

text(36, 773, '这些小屋是故事图卡，不代表景区里的真实建筑。', 10.5, MUTED)
c.save()

reader = PdfReader(str(OUTPUT))
assert len(reader.pages) == 3
page_text = [page.extract_text() for page in reader.pages]
assert all('0.2.1' in value for value in page_text)
assert '圆形' in page_text[1] and '阿舟' in page_text[1]
assert '防雨' not in ''.join(page_text) and '检修' not in ''.join(page_text)
assert '圆形' not in page_text[0] and '两颗星' not in page_text[0]
assert all(page['/Resources'].get('/Font') for page in reader.pages)
print(f'Created {OUTPUT}; {len(reader.pages)} pages; text checks passed.')
