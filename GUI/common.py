#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import time
import commands
import getopt
import getpass
from ftplib import FTP
import urllib
import urllib2
import re
import xlwt
import xlrd
import smtplib
from email.mime.text import MIMEText
from email.header import Header
X = 20
Y = 20
Y2 = 430
BUTTON_SIZE = (60, 26)
ID_FILE_SET = 10001
ID_FILE_UPD = 10002
ID_FILE_CLO = 10003
ID_CODE_DOW = 20001
ID_CODE_BUI = 20002
ID_CODE_GOB = 20003
ID_CODE_LOG = 20004
ID_STR_EXP = 30001
ID_STR_FIL = 30002
ID_STR_IMP = 30003
ID_SCM_GIT = 40001
ID_SCM_BRA = 40002
ID_SCM_ACC = 40003
ID_REQ_GIT = 50001
ID_REQ_BRA = 50002
ID_REQ_REL = 50003
ID_HELP_ABO = 60001
NO_OUT = '>/dev/null 2>&1'

MACRO_LISTS = [
    "WT_PRODUCTION_VERSION",
    "WT_INNER_VERSION",
    "WT_CMCC_VERSION",
    "WT_CTA_VERSION",
    "WT_BUILD_NUMBER",
    "MTK_BUILD_VERNO",]

LANG_CODE = {
    "af":u"南非语",
    "am":u"阿姆哈拉语",
    "ar":u"阿拉伯语",
    "az":u"阿塞拜疆语",
    "be":u"白俄罗斯语",
    "bg":u"保加利亚语",
    "bn":u"孟加拉语",
    "bs":u"波斯尼亚语",
    "ca":u"加泰罗尼亚语",
    "cs":u"捷克",
    "da":u"丹麦",
    "de":u"德语",
    "el":u"希腊",
    "en":u"英语",
    "es":u"西班牙语",
    "et":u"爱沙尼亚语",
    "fa":u"波斯语",
    "fi":u"芬兰语",
    "fr":u"法语",
    "hr":u"克罗地亚语",
    "he":u"希伯来语",
    "hi":u"印地语",
    "hu":u"匈牙利语",
    "hy":u"亚美尼亚语",
    "in":u"印尼语",
    "it":u"意大利语",
    "iw":u"希伯来语",
    "ja":u"日语",
    "ka":u"格鲁吉亚语",
    "kk":u"哈萨克斯坦语",
    "km":u"柬埔寨",
    "ko":u"朝鲜语",
    "lo":u"老挝语",
    "lt":u"立陶宛语",
    "lv":u"拉脱维亚语",
    "mk":u"马其顿语",
    "mn":u"蒙古语",
    "ms":u"马来语",
    "my":u"缅甸语",
    "nb":u"挪威语",
    "ne":u"尼泊尔语",
    "nl":u"荷兰语",
    "pl":u"波兰语",
    "pt":u"葡萄牙语",
    "rm":u"罗曼什语",
    "ro":u"罗马尼亚语",
    "ru":u"俄语",
    "si":u"僧加罗语",
    "sk":u"斯洛伐克语",
    "sl":u"斯洛文尼亚语",
    "sr":u"塞尔维亚语",
    "sv":u"瑞典语",
    "sw":u"斯瓦希里语",
    "th":u"泰语",
    "tl":u"菲律宾语",
    "tr":u"土耳其语",
    "uk":u"乌克兰语",
    "ur":u"乌尔都语",
    "vi":u"越南语",
    "zh":u"中文",
    "zu":u"祖鲁语",}

COUT_CODE = {
    "AT":u"奥地利",
    "AU":u"澳大利亚",
    "AM":u"亚美尼亚",
    "AZ":u"阿塞拜疆",
    "BA":u"波斯尼亚",
    "BD":u"孟加拉国",
    "BE":u"比利时",
    "BG":u"保加利亚",
    "BR":u"巴西",
    "BY":u"白俄罗斯",
    "CA":u"加拿大",
    "CH":u"瑞士",
    "CN":u"中国",
    "CZ":u"捷克",
    "DE":u"德国",
    "DK":u"丹麦",
    "EE":u"爱沙尼亚",
    "EG":u"埃及",
    "ES":u"西班牙",
    "ET":u"埃塞俄比亚",
    "FI":u"芬兰",
    "FR":u"法国",
    "GE":u"格鲁吉亚",
    "GB":u"英国",
    "GR":u"希腊",
    "HK":u"香港",
    "HR":u"克罗地亚",
    "HU":u"匈牙利",
    "ID":u"印尼",
    "IE":u"爱尔兰",
    "IL":u"以色列",
    "IN":u"印度",  
    "IR":u"伊朗",
    "IT":u"意大利",
    "JP":u"日本",
    "KH":u"柬埔寨",
    "KR":u"韩国",
    "KZ":u"哈撒克斯塔",
    "LA":u"老挝",
    "LI":u"列支登士敦",
    "LK":u"斯里兰卡",
    "LT":u"立陶宛",
    "LV":u"拉脱维亚",
    "MK":u"马其顿",
    "MM":u"缅甸",
    "MN":u"蒙古",
    "MY":u"马来西亚",
    "NL":u"荷兰",
    "NO":u"挪威",
    "NP":u"尼泊尔",
    "NZ":u"新西兰",
    "PH":u"菲律宾",
    "PK":u"巴基斯坦",
    "PL":u"波兰",
    "PT":u"葡萄牙",
    "RO":u"罗马尼亚",
    "RS":u"塞尔维亚",
    "RU":u"俄罗斯",
    "SE":u"瑞典",
    "SG":u"新加坡",
    "SI":u"斯洛文尼亚",
    "SK":u"斯洛伐克",
    "TH":u"泰国",
    "TR":u"土耳其",
    "TW":u"台湾",
    "TZ":u"坦桑尼亚",
    "UA":u"乌克兰",
    "US":u"美国",
    "VN":u"越南",
    "ZA":u"南非",
    "ZG":u"缅甸",}

def gen_date():
    return time.strftime('%Y-%m-%d')


def gen_time():
    return time.strftime('%H:%M:%S')


def wt_print(mode, message):
    date = gen_date()
    time1 = gen_time()
    mark = '==='
    prelog = mark + date + ' ' + time1 + mark
    if mode == 'm':
        print prelog + 'LOG: ' + message
    elif mode == 'w':
        print prelog + 'WARNING: ' + message
    elif mode == 'e':
        print prelog + 'ERROR: ' + message
        sys.exit(-1)


def wt_successed():
    wt_print('m', 'Successed!')


def wt_sys(cmd):
    os.system('%s %s' % (cmd, NO_OUT))


def wt_get(cmd):
    return commands.getstatusoutput(cmd)[1]


def wt_remkd(path):
    wt_sys('rm -rf %s' % path)
    wt_sys('mkdir -p %s' % path)


def wt_mkdir(path):
    if not os.path.exists(path):
        wt_sys('mkdir -p %s' % path)


def gen_lines(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    return lines


def lists_to_file(LIST, filename):
    f = open(filename, 'wb')
    for one in LIST:
        one = one + '\n'
        f.write(one.encode('utf-8'))
    f.close()


def translate_by_google(STR, CODE):
    values = {
        'hi': CODE,
        'ie': 'UTF-8',
        'text': STR,
        'langpair': 'en|%s' % CODE }
    url = 'http://translate.google.cn/'
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    browser = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)'
    req.add_header('User-Agent', browser)
    response = urllib2.urlopen(req)
    html = response.read()
    p = re.compile('(?<=TRANSLATED_TEXT=).*?;')
    m = p.search(html)
    out = m.group(0).strip(';')
    return out

def remove_quote(STR):
    if STR.startswith('"') and STR.endswith('"'):
        return STR[1:-1]
    elif STR.startswith("'") and STR.endswith("'"):
        return STR[1:-1]
    else:
        return STR


def send_mail(subject,message,receiver):
    sender = 'zhouyanjiang@wingtech.com'
    smtpserver = 'smtp.wingtech.com'
    username = 'zhouyanjiang'
    password = '880715zyj'
    msg = MIMEText(message,'html','utf-8')  
    msg['Subject'] = Header(subject, 'utf-8')
    smtp = smtplib.SMTP()
    smtp.connect('smtp.wingtech.com')
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
