#!/usr/bin/env python3
"""Builds index.html for pittner/vision-board-for-students.

A single-purpose page for the seasonal "vision board for students / classroom" intent
(teachers plan January goal-setting lessons in December): one printable A4 student worksheet
with a QR code to the free phone maker, a 45-minute lesson plan, questions to read aloud,
a parent note, a supply list and FAQ.

Needs `segno` for the QR code (pip install segno). Run: python3 build.py
"""
import html as _html
import json
import pathlib
from urllib.parse import urlencode

import segno

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://pittner.github.io/vision-board-for-students/"
SRC = "ghpages_classroom"
CAMPAIGN = "classroom_kit_2027"
PAYPAL_CID = "Ae-xjt-swINgDhNcLWajKo9dP2_1J9HPULAWafFQcmUmkZCZ6N1Kzy56GXo1YXIpUO4kjlsuSunMSTaQ"

SERIF = "Georgia, Times New Roman, serif"
SANS = "Helvetica Neue, Helvetica, Arial, sans-serif"
ACC = "#6D28D9"
MUTED = "#6B7280"
RULE = "#D4D4D8"

# The four boxes on the worksheet: heading, one-line prompt printed under it.
BOXES = [
    ("At school", "What do I want to be able to do by June?"),
    ("For me", "What would make me proud of myself?"),
    ("With people I care about", "Who do I want to help, or spend more time with?"),
    ("Something new", "What do I want to try or learn for the first time?"),
]

# Printed QR goes to the phone maker; utm_medium=print keeps paper scans apart from page clicks.
QR_URL = ("https://visionboard.bemooore.com/free-vision-board-maker/?"
          + urlencode({"mode": "wallpaper", "utm_source": "classroom_qr", "utm_medium": "print", "utm_campaign": CAMPAIGN}))


def link(path, **extra):
    q = dict(extra)
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com" + path + "?" + urlencode(q)


TOOL = link("/free-vision-board-maker/", mode="wallpaper")
WALL_2027 = link("/2027-vision-board-wallpaper/")
HOME = link("/")

AGENDA = [
    ("0:00", "Warm-up, 5 min. Every student writes one word for 2027 in the top box and keeps it private for now."),
    ("0:05", "Think, 10 min. Read the questions below aloud, one box at a time. Students write one sentence per box before they draw anything."),
    ("0:15", "Make, 20 min. Draw, or cut and glue magazine pictures, in each box. Rule: every picture needs a reason the student can say in one sentence."),
    ("0:35", "Proof and first step, 5 min. Fill in \"I'll know it worked when\" in each box and one first step with a date at the bottom."),
    ("0:40", "Share, 5 min. In pairs, one minute each: the word, one picture and the first step."),
]

QUESTIONS = [
    ("At school", [
        "Which subject do I want to feel more confident in by June?",
        "What is one thing I can't do yet that I want to be able to do?",
        "What would my teacher notice if I had a great 2027?",
    ]),
    ("For me", [
        "What would make me proud of myself at the end of 2027?",
        "Which habit do I want to start, or stop?",
        "What does a really good day look like for me?",
    ]),
    ("With people I care about", [
        "Who do I want to spend more time with?",
        "Who could I help this year, and how?",
        "What kind of friend do I want to be?",
    ]),
    ("Something new", [
        "What have I always wanted to try?",
        "What would I learn if nobody graded it?",
        "Where would I like to go, even just once?",
    ]),
]

PARENT_NOTE = """Dear parents and carers,

This week our class made vision boards for 2027. Each student filled in one sheet: a word for the year, four goals (school, themselves, people they care about, something new), how they will know each goal worked, and one first step with a date.

The sheet is coming home today. Ask your child to tell you about one picture and their first step, and when they plan to take it.

If your child wants a version on a phone or tablet, the QR code at the bottom of the sheet opens a free page where they can type their goal and first step and save it as a lock screen. No account is needed and nothing is uploaded.

Thank you,
[teacher name]"""

SUPPLIES = [
    "One printed worksheet per student (A4 or US Letter, black and white is fine)",
    "Colored pencils or markers, enough for every table",
    "Optional: 10-15 old magazines per class, scissors and glue sticks",
    "Optional: a few spare sheets for students who want to start over",
]

AGES = [
    ("Grades 3-5 (age 8-11)", "Draw instead of writing in the boxes, and pick the word for 2027 together from a list on the board. Skip the proof line or say it out loud."),
    ("Grades 6-8 (age 11-14)", "Use the sheet as it is. The proof line is where most of them need help: ask \"what would you see or hear if it worked?\""),
    ("Grades 9-12 (age 14-18)", "Ask for a number or a date in every proof line. Keep the sheets and hand them back at the end of the semester."),
]

FAQ = [
    ("How do you do a vision board activity in the classroom?",
     "Give every student one printed worksheet and run it in one 45-minute period: 5 minutes for a word for 2027, "
     "10 minutes of writing one sentence per box while you read questions aloud, 20 minutes of drawing or gluing pictures, "
     "5 minutes for the proof lines and a first step with a date, and 5 minutes of sharing in pairs."),
    ("What should students put on a vision board?",
     "One goal for school, one for themselves, one about people they care about and one new thing to try, each with a picture "
     "and a sentence that says how they will know it worked. Finish with one first step and a date."),
    ("How long does a classroom vision board take?",
     "One class period of about 45 minutes with this worksheet. A full poster board with magazines usually takes two periods."),
    ("What age is this vision board worksheet for?",
     "Grades 3 to 12 (about age 8 to 18). Younger students draw instead of writing; older students add numbers and dates to every proof line."),
    ("Do students need magazines?",
     "No. The worksheet works with colored pencils alone. Magazines, scissors and glue are optional."),
    ("Can students make a digital vision board?",
     "Yes. The QR code on the sheet opens a free maker that runs in the browser: students type a goal and a first step and save a "
     "1080x1920 lock-screen image. There is no account and nothing is uploaded."),
    ("Is this classroom kit free?",
     "Yes. The worksheet, lesson plan, questions and parent note are free and MIT licensed. No signup, no e-mail."),
]


def wrap(text, width):
    lines, cur = [], ""
    for w in text.split(" "):
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def t(x, y, s, size, fill="#111827", family=SANS, anchor=None, extra=""):
    a = f' text-anchor="{anchor}"' if anchor else ""
    return (f'<text x="{x:g}" y="{y:g}"{a} font-family="{family}" font-size="{size:g}" fill="{fill}"{extra}>'
            f'{_html.escape(s)}</text>')


def line(x1, y1, x2, y2, w=0.3, color=RULE, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{color}" stroke-width="{w:g}"{d}/>'


def box(x, y, w, h):
    return (f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="2" fill="none" '
            f'stroke="{RULE}" stroke-width="0.4"/>')


def qr_svg(x, y, size):
    q = segno.make(QR_URL, error="m")
    m = q.matrix
    n = len(m) + 8  # 4-module quiet zone on each side
    cell = size / n
    parts = [f'<rect x="{x:g}" y="{y:g}" width="{size:g}" height="{size:g}" fill="#FFFFFF"/>']
    path = []
    for r, row in enumerate(m):
        for c, v in enumerate(row):
            if v:
                path.append(f"M{x + (c + 4) * cell:.3f} {y + (r + 4) * cell:.3f}h{cell:.3f}v{cell:.3f}h-{cell:.3f}z")
    parts.append(f'<path d="{"".join(path)}" fill="#111827"/>')
    return "".join(parts)


def sheet():
    o = ['<svg id="svg-sheet" class="sheet" viewBox="0 0 210 297" xmlns="http://www.w3.org/2000/svg" role="img" '
         'aria-label="Printable 2027 vision board worksheet for students, one A4 page">',
         '<rect width="210" height="297" fill="#FFFFFF"/>',
         t(12, 18, "My 2027 Vision Board", 10, family=SERIF),
         t(12, 24.5, "Write one sentence in each box first, then draw or glue a picture that shows it.", 3.7, MUTED),
         t(12, 32, "Name", 3.6, MUTED), line(22, 32.6, 112, 32.6),
         t(118, 32, "Class", 3.6, MUTED), line(128, 32.6, 160, 32.6),
         t(165, 32, "Date", 3.6, MUTED), line(174, 32.6, 198, 32.6)]
    # Word for the year
    o.append(box(12, 37, 186, 15))
    o.append(t(16, 42.5, "MY WORD FOR 2027", 3.4, ACC, extra=' letter-spacing="0.5"'))
    # Four goal boxes, 2 x 2
    bw, bh, gx, gy = 91, 74, 4, 4
    for i, (head, prompt) in enumerate(BOXES):
        col, row = i % 2, i // 2
        x, y = 12 + col * (bw + gx), 56 + row * (bh + gy)
        o.append(box(x, y, bw, bh))
        o.append(t(x + 4, y + 6.5, f"{i + 1:02d}", 3.4, ACC, extra=' letter-spacing="0.5"'))
        o.append(t(x + 11, y + 6.5, head.upper(), 3.4, ACC, extra=' letter-spacing="0.5"'))
        for j, ln in enumerate(wrap(prompt, 52)):
            o.append(t(x + 4, y + 11.5 + j * 4.2, ln, 3.3, MUTED, family=SERIF))
        o.append(line(x + 4, y + 21, x + bw - 4, y + 21))
        o.append(t(x + 4, y + 25.5, "my picture", 2.8, "#A1A1AA"))
        o.append(t(x + 4, y + bh - 9.5, "I'll know it worked when:", 3.0, MUTED))
        o.append(line(x + 4, y + bh - 3.5, x + bw - 4, y + bh - 3.5))
    # First step
    fy = 56 + 2 * (bh + gy) + 1  # 213
    o.append(box(12, fy, 186, 34))
    o.append(t(16, fy + 6.5, "MY FIRST STEP", 3.4, ACC, extra=' letter-spacing="0.5"'))
    o.append(t(16, fy + 15, "What I will do:", 3.6, MUTED)); o.append(line(42, fy + 15.6, 194, fy + 15.6))
    o.append(t(16, fy + 24, "By (date):", 3.6, MUTED)); o.append(line(34, fy + 24.6, 90, fy + 24.6))
    o.append(t(96, fy + 24, "Who can help me:", 3.6, MUTED)); o.append(line(125, fy + 24.6, 194, fy + 24.6))
    o.append(t(16, fy + 31, "Check it again on:  ____ / ____", 3.2, MUTED))
    # QR to the phone maker
    qy = fy + 38  # 251
    o.append(qr_svg(12, qy, 26))
    o.append(t(42, qy + 8, "AT HOME: MAKE IT YOUR LOCK SCREEN", 3.7, ACC, extra=' letter-spacing="0.5"'))
    o.append(t(42, qy + 14, "Scan, type your goal and first step, save it on a phone or tablet.", 3.9))
    o.append(t(42, qy + 19.5, "Free, no account, nothing uploaded.", 3.9, MUTED))
    o.append(line(12, 284, 198, 284))
    o.append(t(12, 289, "Vision Board for Students 2027 - free, MIT licensed - pittner.github.io/vision-board-for-students", 3.3, MUTED))
    o.append(t(198, 289, "visionboard.bemooore.com", 3.3, MUTED, anchor="end"))
    o.append("</svg>")
    return "".join(o)


def e(s):
    return _html.escape(s, quote=True)


def build():
    agenda = "\n".join(f"      <li><b>{e(a)}</b> {e(b)}</li>" for a, b in AGENDA)
    questions = "\n".join(
        f"    <div class=\"qgrp\"><h3>{e(h)}</h3><ul>" + "".join(f"<li>{e(q)}</li>" for q in qs) + "</ul></div>"
        for h, qs in QUESTIONS)
    supplies = "\n".join(f"    <li>{e(s)}</li>" for s in SUPPLIES)
    ages = "\n".join(f"    <li><b>{e(a)}.</b> {e(b)}</li>" for a, b in AGES)
    faq_html = "\n".join(f"  <h3>{e(q)}</h3>\n  <p>{e(a)}</p>" for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    page = TEMPLATE
    for k, v in {
        "%%SHEET%%": sheet(), "%%AGENDA%%": agenda, "%%QUESTIONS%%": questions, "%%SUPPLIES%%": supplies,
        "%%AGES%%": ages, "%%FAQ%%": faq_html, "%%LD%%": ld, "%%NOTE%%": e(PARENT_NOTE), "%%TOOL%%": e(TOOL),
        "%%WALL%%": e(WALL_2027), "%%HOME%%": e(HOME), "%%URL%%": URL, "%%SRC%%": SRC, "%%CID%%": PAYPAL_CID,
    }.items():
        page = page.replace(k, v)
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html", len(page.encode()), "bytes")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vision Board for Students 2027: Free Printable Classroom Worksheet &amp; 45-Minute Lesson</title>
<meta name="description" content="A free printable 2027 vision board worksheet for students, a 45-minute lesson plan, questions to read aloud, a parent note and age tips for grades 3-12. No signup, MIT licensed.">
<link rel="canonical" href="%%URL%%">
<meta property="og:type" content="website">
<meta property="og:title" content="Vision board for students 2027 - free printable classroom kit">
<meta property="og:description" content="One printable worksheet, a 45-minute lesson plan, questions to read aloud and a parent note for a 2027 classroom vision board. Free, no signup.">
<meta property="og:url" content="%%URL%%">
<style>
:root{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#6D28D9;--bg:#FBFAF9}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header.hero{padding:48px 0 18px}
h1{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}
.lede{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}
.meta{font-size:14px;color:var(--muted);margin:0}
.btn{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#5B21B6;color:#fff}
.main{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:28px;align-items:start;padding:12px 0 36px}
@media (max-width:760px){.main{grid-template-columns:1fr}}
.card{background:#fff;border:1px solid var(--rule);border-radius:16px;overflow:hidden}
.preview{padding:16px}
.preview svg{width:100%;height:auto;display:block;border:1px solid var(--rule);border-radius:6px}
.actions{padding:0 16px 16px;display:flex;gap:8px;flex-wrap:wrap}
.side h2{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}
.side ol{list-style:none;padding:0;margin:0 0 18px;color:#374151}
.side li{margin:0 0 10px}
.side li b{display:inline-block;min-width:3.2em;color:var(--acc);font-variant-numeric:tabular-nums}
.bar{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 14px}
section.block{padding:30px 0;border-top:1px solid var(--rule)}
section.block h2{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}
section.block>p{max-width:70ch;color:#374151}
.qs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:4px 28px}
@media (max-width:760px){.qs{grid-template-columns:1fr}}
.qgrp h3{font:600 16px/1.4 inherit;margin:14px 0 4px;color:var(--acc)}
.qgrp ul{margin:0;padding-left:20px;color:#374151}
textarea.invite{width:100%;max-width:640px;min-height:300px;border:1px solid var(--rule);border-radius:12px;padding:14px 16px;font:15px/1.55 inherit;color:#374151;background:#fff;resize:vertical}
ul.sup{max-width:70ch;color:#374151;padding-left:20px}
ul.sup li{margin:6px 0}
.after{margin:0 16px 16px;padding:16px 18px;border:1px solid var(--rule);border-left:4px solid var(--acc);border-radius:12px;background:#FAF7FF;font-size:15px;color:#374151}
.after[hidden]{display:none}
.after p{margin:0 0 10px}
.after .lbl{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:14px 0 6px}
.tip-amts{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 10px}
.tip-amt.on{background:var(--acc);border-color:var(--acc);color:#fff}
#tip-go:disabled{opacity:.7;cursor:default}
#tip-msg{margin-top:8px;font-size:13px;color:var(--muted)}
.faq h3{font:600 16px/1.4 inherit;margin:18px 0 4px}
.faq p{margin:0;color:#374151;max-width:70ch}
footer{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}
@media print{
  body{background:#fff}
  .wrap>*:not(.printzone){display:none!important}
  .printzone{display:block!important}
  .printzone svg{width:100%;height:auto;display:block;border:0}
}
@page{size:A4 portrait;margin:0}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Vision board for students: a free 2027 classroom kit</h1>
  <p class="lede">One printable worksheet per student and a lesson that fits in a single 45-minute period: a word for 2027, four goals with a picture each, how they will know it worked, and one first step with a date. Questions to read aloud, a note for parents and age tips are below. Free, no signup, no e-mail.</p>
  <p class="meta">Grades 3-12 &middot; one class period &middot; A4 and US Letter &middot; SVG and PNG download &middot; MIT licensed</p>
</header>

<div class="main">
  <article class="card" id="sheet">
    <div class="preview">%%SHEET%%</div>
    <div class="actions">
      <button class="btn primary" data-print="sheet">Print the worksheet</button>
      <button class="btn" data-svg="sheet">Download SVG</button>
      <button class="btn" data-png="sheet">Download PNG</button>
    </div>
    <div class="after" id="afterDl" hidden>
      <p><strong>Saved.</strong> The QR at the bottom of the sheet opens the free maker, so students can type their goal and first step at home and keep it as a 1080&times;1920 lock screen. No account, nothing uploaded. You can try it first yourself.</p>
      <a class="btn primary" href="%%TOOL%%" data-cta="after_dl_tool">Try the phone version</a>
      <div class="lbl">Or just say thanks</div>
      <p>This kit is free and MIT licensed, and it stays that way. If it saved you a planning period, you can send a one-off thank you. You get nothing extra for it.</p>
      <div class="tip-amts" role="group" aria-label="Amount">
        <button type="button" class="btn tip-amt" data-amt="3">&euro;3</button>
        <button type="button" class="btn tip-amt on" data-amt="5">&euro;5</button>
        <button type="button" class="btn tip-amt" data-amt="10">&euro;10</button>
      </div>
      <button type="button" class="btn" id="tip-go">Say thanks with PayPal</button>
      <div id="tip-pp" style="max-width:360px;margin-top:10px"></div>
      <div id="tip-msg">PayPal handles the payment. Nothing is loaded from PayPal until you press the button.</div>
    </div>
  </article>

  <div class="side">
    <h2>The 45-minute lesson</h2>
    <div class="bar">
      <button class="btn primary" id="pageA4" aria-pressed="true">Paper: A4</button>
      <button class="btn" id="pageLetter" aria-pressed="false">Paper: US Letter</button>
    </div>
    <ol>
%%AGENDA%%
    </ol>
    <p class="meta">Why writing comes before drawing: a student who has written one sentence per box draws a picture for a reason, and the board ends up being about their goal, not about whatever picture was easiest to find.</p>
  </div>
</div>

<section class="block">
  <h2>Questions to read aloud</h2>
  <p>Read one group per box during the 10-minute thinking part. Students answer in one sentence on the line under the box heading.</p>
  <div class="qs">
%%QUESTIONS%%
  </div>
</section>

<section class="block">
  <h2>By age</h2>
  <ul class="sup">
%%AGES%%
  </ul>
</section>

<section class="block">
  <h2>Note for parents</h2>
  <p>Paste it into your class newsletter, e-mail or app message and fill in the bracket.</p>
  <textarea class="invite" id="note" readonly>%%NOTE%%</textarea>
  <p><button class="btn primary" id="copyNote" type="button">Copy the note</button> <span class="meta" id="copyMsg"></span></p>
</section>

<section class="block">
  <h2>What you need for one class</h2>
  <ul class="sup">
%%SUPPLIES%%
  </ul>
</section>

<section class="block">
  <h2>Digital version on school devices</h2>
  <p>Students open the free maker in the browser, type the goal and first step from their worksheet and save it as a 1080&times;1920 image for a lock screen or desktop. It runs on the device, nothing is uploaded and nobody needs an account. The QR on the worksheet opens the same page.</p>
  <p><a class="btn primary" href="%%TOOL%%" data-cta="section_phone_tool">Open the free maker</a>
     <a class="btn" href="%%WALL%%" data-cta="section_wallpaper_2027">20 ready 2027 goals as wallpapers</a></p>
</section>

<section class="block faq">
  <h2>Questions</h2>
%%FAQ%%
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="%%HOME%%" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/2027-vision-board-template/">printable 2027 vision board template</a>,
  <a href="https://pittner.github.io/vision-board-party-kit/">vision board party kit</a>,
  <a href="https://pittner.github.io/vision-board-templates/">all 7 printable vision board templates</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/vision-board-for-students">source</a>
</footer>

<div class="printzone" id="printzone" style="display:none"></div>
</div>

<script type="application/ld+json">
%%LD%%
</script>

<script>
(function(){
  var EP='https://visionboard.bemooore.com/api/event.php',P='%%SRC%%',engaged=false;
  function beacon(ev,label){
    try{
      var b=JSON.stringify({event:ev,utm:P+' | '+label+' | '+location.search});
      if(navigator.sendBeacon){navigator.sendBeacon(EP,new Blob([b],{type:'text/plain'}));}
      else{fetch(EP,{method:'POST',body:b,keepalive:true,mode:'no-cors'});}
    }catch(e){}
  }
  // Every link to our site carries the button and where the visitor came from (e.g. chatgpt.com).
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){
    a.href+='&utm_content='+encodeURIComponent(a.getAttribute('data-cta'))+'&utm_term='+encodeURIComponent('via_'+src);
  });
  function engage(how){ if(engaged)return; engaged=true; beacon('page_engaged',how); }
  setTimeout(function(){engage('dwell6s');},6000);
  window.addEventListener('scroll',function(){
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  },{passive:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  });

  var ps=document.createElement('style'); document.head.appendChild(ps);
  function paper(size){
    ps.textContent='@page{size:'+size+' portrait;margin:'+(size==='A4'?'0':'6mm')+'}';
    document.getElementById('pageA4').classList.toggle('primary',size==='A4');
    document.getElementById('pageLetter').classList.toggle('primary',size!=='A4');
    document.getElementById('pageA4').setAttribute('aria-pressed',String(size==='A4'));
    document.getElementById('pageLetter').setAttribute('aria-pressed',String(size!=='A4'));
  }
  paper('A4');
  document.getElementById('pageA4').onclick=function(){paper('A4');beacon('cta_click','paper_a4');};
  document.getElementById('pageLetter').onclick=function(){paper('Letter');beacon('cta_click','paper_letter');};

  var cm=document.getElementById('copyMsg');
  document.getElementById('copyNote').onclick=function(){
    var ta=document.getElementById('note');
    beacon('cta_click','copy_parent_note');
    function done(){ cm.textContent='Copied. Paste it into your class message.'; }
    if(navigator.clipboard&&navigator.clipboard.writeText){
      navigator.clipboard.writeText(ta.value).then(done,function(){ ta.select(); document.execCommand('copy'); done(); });
    } else { ta.select(); document.execCommand('copy'); done(); }
  };

  var after=document.getElementById('afterDl');
  function showAfter(){ after.hidden=false; }

  // Voluntary thank-you, same flow as T-095/T-105/T-107/T-112: PayPal SDK loads only on click.
  var amt='5',tipLoading=false,amts=document.querySelector('.tip-amts'),go=document.getElementById('tip-go'),msg=document.getElementById('tip-msg');
  amts.addEventListener('click',function(e){
    var b=e.target.closest('.tip-amt'); if(!b)return;
    amt=b.getAttribute('data-amt');
    Array.prototype.forEach.call(amts.querySelectorAll('.tip-amt'),function(x){x.classList.toggle('on',x===b);});
  });
  go.addEventListener('click',function(){
    if(tipLoading)return; tipLoading=true; go.disabled=true; go.textContent='Loading PayPal...';
    beacon('cta_click','tip_open_'+amt);
    var s=document.createElement('script');
    s.src='https://www.paypal.com/sdk/js?client-id=%%CID%%&currency=EUR&intent=capture&components=buttons';
    s.onerror=function(){ tipLoading=false; go.disabled=false; go.textContent='Say thanks with PayPal'; msg.textContent='PayPal could not be loaded. Please try again in a moment.'; };
    s.onload=function(){
      go.style.display='none';
      window.paypal.Buttons({
        style:{layout:'vertical',label:'paypal'},
        createOrder:function(d,actions){
          return actions.order.create({
            purchase_units:[{amount:{value:amt,currency_code:'EUR'},custom_id:'tip-vb-classroom',description:'Vision board for students 2027, voluntary thank you'}],
            application_context:{brand_name:'VisionBoard',user_action:'PAY_NOW',shipping_preference:'NO_SHIPPING'}
          });
        },
        onApprove:function(d,actions){
          return actions.order.capture().then(function(){
            beacon('cta_click','tip_paid_'+amt);
            document.getElementById('tip-pp').innerHTML='<p><strong>Thank you.</strong> The payment went through.</p>';
            msg.textContent='PayPal has emailed you the receipt.';
          });
        },
        onError:function(){ msg.textContent='Something went wrong at PayPal and no money was taken. You can try again.'; }
      }).render('#tip-pp');
    };
    document.head.appendChild(s);
  });

  function svgEl(){ return document.getElementById('svg-sheet'); }
  function serialize(){
    var s=svgEl().cloneNode(true); s.removeAttribute('class'); s.removeAttribute('id');
    s.setAttribute('xmlns','http://www.w3.org/2000/svg');
    s.setAttribute('width','210mm'); s.setAttribute('height','297mm');
    return '<?xml version="1.0" encoding="UTF-8"?>\n'+new XMLSerializer().serializeToString(s);
  }
  function save(blob,name){
    var u=URL.createObjectURL(blob),a=document.createElement('a');
    a.href=u;a.download=name;document.body.appendChild(a);a.click();
    setTimeout(function(){URL.revokeObjectURL(u);a.remove();},1500);
  }
  document.addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b)return;
    if(b.hasAttribute('data-print')){
      var z=document.getElementById('printzone');
      z.innerHTML=''; z.appendChild(svgEl().cloneNode(true)); z.style.display='block';
      beacon('template_print','classroom-sheet');
      window.print();
      setTimeout(function(){z.style.display='none';z.innerHTML='';showAfter();},800);
    } else if(b.hasAttribute('data-svg')){
      save(new Blob([serialize()],{type:'image/svg+xml'}),'vision-board-worksheet-students-2027.svg');
      beacon('template_download','classroom-sheet|svg');
      showAfter();
    } else if(b.hasAttribute('data-png')){
      var img=new Image(), src='data:image/svg+xml;base64,'+btoa(unescape(encodeURIComponent(serialize())));
      img.onload=function(){
        var c=document.createElement('canvas'); c.width=1654; c.height=2339; // A4 @ 200dpi
        var x=c.getContext('2d'); x.fillStyle='#fff'; x.fillRect(0,0,c.width,c.height);
        x.drawImage(img,0,0,c.width,c.height);
        c.toBlob(function(bl){ save(bl,'vision-board-worksheet-students-2027.png'); },'image/png');
      };
      img.src=src;
      beacon('template_download','classroom-sheet|png');
      showAfter();
    }
  });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
