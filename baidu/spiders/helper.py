
import re

def strip_r_n(s):
    if s:
        s = s.strip()
        s = s.replace('\r', '')
        s = s.replace('\n', '')
    return s


def parse_content(c):
    if c:
        div = re.compile(r'<div id=(.*) accuse="aContent" (.*)">')
        c = div.sub("", c)
        c = c.replace('<div class="wgt-best-mask">', '')
        c = c.replace('<div class="wgt-best-showbtn">', '')
        c = c.replace('展开全部<span class="wgt-best-arrowdown"></span>', '')
        c = c.replace('<div class="wgt-answers-mask">', '')
        c = c.replace('<div class="wgt-answers-showbtn">', '')
        c = c.replace('展开全部<span class="wgt-answers-arrowdown"></span>', '')
        c = c.replace('</div>', '')
        c = c.strip()
    return c

def is_valid_date(str):
  try:
    time.strptime(str, '%Y-%m-%d')
    return True
  except:
    return False
