#!/usr/bin/env python
#coding=utf-8

#Auther: zhouyanjiang
#Date: 2015-04-29

import wx.lib.agw.flatmenu as FM
from wx.lib.agw.artmanager import ArtManager, RendererBase, DCSaver
from wx.lib.agw.fmresources import ControlFocus, ControlPressed
from wx.lib.agw.fmresources import FM_OPT_SHOW_CUSTOMIZE, FM_OPT_SHOW_TOOLBAR, FM_OPT_MINIBAR
from wx.lib.wordwrap import wordwrap
import os
import sys
import commands
import MySQLdb
import wx
import getpass
import xlrd
import xlwt
import time
reload(sys)
sys.setdefaultencoding("utf8")

NO_OUT = ">/dev/null 2>&1"
MYSQLPARA = ["192.168.9.193","root","root","swwb"]
USER = getpass.getuser()
REMEMBER_ACCOUNT_FILE = "/home/%s/.swwb_remember_account"%USER
AUTOMATIC_LOGIN_FILE  = "/home/%s/.swwb_automatic_login"%USER
LANG_CODE = {
    "af":u"南非语","am":u"阿姆哈拉语","ar":u"阿拉伯语","az":u"阿塞拜疆语","be":u"白俄罗斯语","bg":u"保加利亚语","bn":u"孟加拉语",
    "bs":u"波斯尼亚语","ca":u"加泰罗尼亚语","cs":u"捷克","da":u"丹麦","de":u"德语","el":u"希腊","en":u"英语","es":u"西班牙语",
    "et":u"爱沙尼亚语","fa":u"波斯语","fi":u"芬兰语","fr":u"法语","hr":u"克罗地亚语","he":u"希伯来语","hi":u"印地语","hu":u"匈牙利语",
    "hy":u"亚美尼亚语","in":u"印尼语","it":u"意大利语","iw":u"希伯来语","ja":u"日语","ka":u"格鲁吉亚语","kk":u"哈萨克斯坦语","km":u"柬埔寨",
    "ko":u"朝鲜语","lo":u"老挝语","lt":u"立陶宛语","lv":u"拉脱维亚语","mk":u"马其顿语","mn":u"蒙古语","ms":u"马来语","my":u"缅甸语",
    "nb":u"挪威语","ne":u"尼泊尔语","nl":u"荷兰语","pl":u"波兰语","pt":u"葡萄牙语","rm":u"罗曼什语","ro":u"罗马尼亚语","ru":u"俄语",
    "si":u"僧加罗语","sk":u"斯洛伐克语","sl":u"斯洛文尼亚语","sr":u"塞尔维亚语","sv":u"瑞典语","sw":u"斯瓦希里语","th":u"泰语","tl":u"菲律宾语",
    "tr":u"土耳其语","uk":u"乌克兰语","ur":u"乌尔都语","vi":u"越南语","zh":u"中文","zu":u"祖鲁语",}

COUT_CODE = {
    "AT":u"奥地利","AU":u"澳大利亚","AM":u"亚美尼亚","AZ":u"阿塞拜疆","BA":u"波斯尼亚","BD":u"孟加拉国","BE":u"比利时","BG":u"保加利亚",
    "BR":u"巴西","BY":u"白俄罗斯","CA":u"加拿大","CH":u"瑞士","CN":u"中国","CZ":u"捷克","DE":u"德国","DK":u"丹麦","EE":u"爱沙尼亚",
    "EG":u"埃及","ES":u"西班牙","ET":u"埃塞俄比亚","FI":u"芬兰","FR":u"法国","GE":u"格鲁吉亚","GB":u"英国","GR":u"希腊","HK":u"香港",
    "HR":u"克罗地亚","HU":u"匈牙利","ID":u"印尼","IE":u"爱尔兰","IL":u"以色列","IN":u"印度","IR":u"伊朗","IT":u"意大利","JP":u"日本",
    "KH":u"柬埔寨","KR":u"韩国","KZ":u"哈撒克斯塔","LA":u"老挝","LI":u"列支登士敦","LK":u"斯里兰卡","LT":u"立陶宛","LV":u"拉脱维亚",
    "MK":u"马其顿","MM":u"缅甸","MN":u"蒙古","MY":u"马来西亚","NL":u"荷兰","NO":u"挪威","NP":u"尼泊尔","NZ":u"新西兰","PH":u"菲律宾",
    "PK":u"巴基斯坦","PL":u"波兰","PT":u"葡萄牙","RO":u"罗马尼亚","RS":u"塞尔维亚","RU":u"俄罗斯","SE":u"瑞典","SG":u"新加坡","SI":u"斯洛文尼亚",
    "SK":u"斯洛伐克","TH":u"泰国","TR":u"土耳其","TW":u"台湾","TZ":u"坦桑尼亚","UA":u"乌克兰","US":u"美国","VN":u"越南","ZA":u"南非","ZG":u"缅甸",}

def myget(cmd):return commands.getoutput(cmd)
def mysuccess():myprint('m', 'Successed!')
def mysys(cmd):os.system('%s %s' % (cmd, NO_OUT))
def connect_db():return MySQLdb.connect(host=MYSQLPARA[0],user=MYSQLPARA[1],passwd=MYSQLPARA[2],db=MYSQLPARA[3]).cursor()
def gen_date():return time.strftime('%Y-%m-%d')
def gen_time():return time.strftime('%H:%M:%S')
def myprint(mode, message):print "===%s %s===%s: %s"%(gen_date(),gen_time(),mode,message)
def file2lines(filename):return open(filename).readlines()
def file2string(filename):return ''.join([i.strip() for i in open(filename).readlines()])
def rmquote(a):return a[1:-1] if a.startswith("'") and a.endswith("'") or a.startswith('"') and a.endswith('"') else a

def lists_to_file(LIST, filename):
    f = open(filename, 'wb')
    for one in LIST:
        one = one + '\n'
        f.write(one.encode('utf-8'))
    f.close()


def gen_language_class(DIR):
    lists = []
    path = DIR+"/frameworks/base/core/res/res"
    cmd = "find %s -name values*"%path
    for one in myget(cmd).split():
        one = one.split("/")[-1]
        if "-" in one:
            if len(one.split("-")) == 2:
                language = one.split("-")[1]
                if len(language) != 2:
                    language = ""
                country = ""
            elif len(one.split("-")) == 3 and "-r" in one:
                language = one.split("-")[1]
                country = one.split("-")[2][1:]
            else:
                language = country = ""
            if language != "":
                if country == "":
                    lists.append(language)
                else:
                    lists.append(language+"_"+country)
    return lists

def gen_paths(DIR):
    print DIR
    cmd = "find . -type d "
    ignores = file2lines("%s/misc/paths.ignore"%PWD)
    for one in ignores:
        if not one.startswith("#") and one != "":
            cmd = cmd + '! -path "*%s*" '%one[:-1]
    cmd = cmd + "-name values"
    return myget(cmd)

class SCMHanFrame(wx.Frame):
    def __init__(self,user):
        wx.Frame.__init__(self,None,-1,"Handle",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -2])
        self.statusbar.SetStatusText("Wingtech Communications, Shanghai,P.R.C.", 0)
        self.statusbar.SetStatusText("Welcome,  %s!"%user, 1)
        self.user = user
        X = 20
        Y = 430
        BUTTON_SIZE = (60, 26)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,"Back",(X,Y),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnRun,wx.Button(panel,-1,"Run",(X+480,Y),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        WorkbenchFrame(self.user).Show()

    def OnRun(self,e):
        pass

class Import(wx.Frame):
    def __init__(self,lists):
        wx.Frame.__init__(self,None,-1,"Settings",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.CreateStatusBar()
        X = 50
        Y = 30
        self.Listleft = lists
        self.Left  = wx.ListBox(panel,-1,(X,Y),(200,360),self.Listleft,wx.LB_SINGLE)
        self.Right = wx.ListBox(panel,-1,(X+300,Y),(200,360),"",wx.LB_SINGLE)
        self.Bind(wx.EVT_BUTTON,self.OnL2R,wx.Button(panel,-1,"=>",(X+225,Y+160),(50,26)))
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,"Back",(X,Y+400),(60,30)))
        self.Bind(wx.EVT_BUTTON,self.OnDelete,wx.Button(panel,-1,"Delet",(X+300,Y+400),(60,30)))
        self.Bind(wx.EVT_BUTTON,self.OnSave,wx.Button(panel,-1,"Save",(X+450,Y+400),(60,30)))

    def OnL2R(self,event):
        lists = []
        for one in range(self.Right.GetCount()):
            lists.append(self.Right.GetString(one))
        if self.Left.GetStringSelection() in lists:
            pass
        else:
            lists.append(self.Left.GetStringSelection())
        self.Right.Set(lists)

    def OnDelete(self,event):
        self.Right.Delete(self.Right.GetSelection())

    def OnBack(self,event):
        self.Close()

    def OnSave(self,event):
        lists = []
        for one in range(self.Right.GetCount()):
            lists.append(self.Right.GetString(one))
        lists_to_file(lists,"%s/misc/.import_languages_need"%PWD)
        self.SetStatusText("Save successed!")
        self.Close()


class Export(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"Settings",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.CreateStatusBar()
        self.SetStatusText("Choose the items you want from left to right!")
        X = 50
        Y = 30
        self.Listleft = []
        listtmp = file2lines("%s/misc/.languages"%PWD)
        for one in listtmp:
            self.Listleft.append(one[:-1])
        self.Left  = wx.ListBox(panel,-1,(X,Y),(200,360),self.Listleft,wx.LB_SINGLE)
        self.Right = wx.ListBox(panel,-1,(X+300,Y),(200,360),"",wx.LB_SINGLE)
        self.Bind(wx.EVT_BUTTON,self.OnL2R,wx.Button(panel,-1,"=>",(X+225,Y+160),(50,26)))
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,"Back",(X,Y+400),(60,30)))
        self.Bind(wx.EVT_BUTTON,self.OnDelete,wx.Button(panel,-1,"Delet",(X+300,Y+400),(60,30)))
        self.Bind(wx.EVT_BUTTON,self.OnSave,wx.Button(panel,-1,"Save",(X+450,Y+400),(60,30)))

    def OnL2R(self,event):
        lists = []
        for one in range(self.Right.GetCount()):
            lists.append(self.Right.GetString(one))
        if self.Left.GetStringSelection() in lists:
            pass
        else:
            lists.append(self.Left.GetStringSelection())
        self.Right.Set(lists)

    def OnDelete(self,event):
        self.Right.Delete(self.Right.GetSelection())

    def OnBack(self,event):
        self.Close()

    def OnSave(self,event):
        lists = []
        for one in range(self.Right.GetCount()):
            lists.append(self.Right.GetString(one))
        lists_to_file(lists,"%s/misc/.languages_need"%PWD)
        self.SetStatusText("Save successed!")
        self.Close()


class StringsExpFrame(wx.Frame):
    def __init__(self,user):
        wx.Frame.__init__(self,None,-1,"Export",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -2])
        self.statusbar.SetStatusText("Wingtech Communications, Shanghai,P.R.C.", 0)
        self.statusbar.SetStatusText("Welcome,  %s!"%user, 1)
        self.user = user
        X = Y = 20
        Y2 = 430
        BUTTON_SIZE = (60, 26)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,"Back",(X,Y2),BUTTON_SIZE))

        self.DIC = {}
        self.Label1 = wx.StaticText(panel,-1,"CodePath",(X,Y))
        self.Dir = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,"",(X+70,Y-2),(370,26))
        self.Bind(wx.EVT_BUTTON,self.OnDirPath,wx.Button(panel,-1,"Browse",(X+450,Y-2),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnCheck,wx.Button(panel,-1,"Check",(X,Y+44),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnExport_Setting,wx.Button(panel,-1,"Setting",(X+65,Y+44),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnStart,wx.Button(panel,-1,"Go",(X+450,Y2),BUTTON_SIZE))
        self.Log = wx.ListBox(panel,-1,(X,Y+84),(510,310),"",wx.LB_SINGLE)
        lists = [
          "Operating Steps",
          "1.Click Browse to choose the path of code",
          "2.Click Check to generate some necessary parameters",
          "3.Click Setting to choose the languages need to export",
          "4.Click Go at last"]
        self.Log.Set(lists)

    def OnBack(self,e):
        self.Close()
        WorkbenchFrame(self.user).Show()

    def OnDirPath(self,e):
        dialog = wx.DirDialog(None, 'Choose the path of code',os.getcwd(),style = wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.Dir.SetValue(dialog.GetPath())
            self.ROOT_PATH = dialog.GetPath()
        dialog.Destroy()

    def OnCheck(self,e):
        try:
            os.chdir(self.ROOT_PATH)
            self.SetStatusText("Check env，half a moment...")
        except Exception,e:
            wx.MessageBox("Choose the path of code first!","Warning")
            return -1
        try:
            self.languages = gen_language_class(self.ROOT_PATH)
            self.paths = gen_paths(self.ROOT_PATH)
        except Exception,e:
            print e
        total_languages = len(self.languages)
        total_paths = len(self.paths)
        l = []
        for one in self.languages:
            if "_" in one:
                l.append("-r".join(one.split("_"))+":"+LANG_CODE[one.split("_")[0]]+"["+COUT_CODE[one.split("_")[1]]+"]")
            else:
                l.append(one+":"+LANG_CODE[one])
        l.sort()
        lists_to_file(l,"%s/misc/.languages"%PWD)
        lists = [
          "Total languages:  %d"%total_languages,
          "Total paths:  %d"%total_paths,
          "",
          "Tips",
          "1.If there is no need to export from some paths, please modify the file of <paths.ignore>",
          "2.If you want to appoint some languages, please click Setting!"]
        self.Log.Set(lists)
        self.SetStatusText("Everything is OK!")

    def OnExport_Setting(self,e):
        if os.path.exists("%s/misc/.languages"%PWD):
            Export().Show()
        else:
            self.SetStatusText("Check the env first!")

    def OnStart(self,event):
        if os.path.exists("%s/misc/.languages_need"%PWD):
            self.SetStatusText("Start to export strings...")
            self.OnExport()



    def OnExport(self):
        wbk = xlwt.Workbook(encoding='utf-8')
        self.sheet = wbk.add_sheet('sheet1')
        self.sheet.col(0).width = 16000
        self.sheet.col(1).width = 3000
        self.sheet.col(2).width = 9000
        self.sheet.col(3).width = 3000
        self.sheet.col(4).width = 3000
        self.sheet.col(5).width = 10000
        styleBlueBkg = xlwt.easyxf('pattern: pattern solid, fore_colour ocean_blue; font: bold on;')
        self.sheet.write(0,0,'Relative Path')
        self.sheet.write(0,1,'String Type')
        self.sheet.write(0,2,'Name')
        self.sheet.write(0,3,'Length')
        self.sheet.write(0,4,'Index')
        self.sheet.write(0,5,'values')

        self.i = 1
        self.k = 1
        self.values_all = []
        paths = self.paths
        language = file2lines("%s/misc/.languages_need"%PWD)
        for one in language:
            self.sheet.write(0,5+self.k,"values-"+one.split(":")[0])
            self.k = self.k + 1
            self.values_all.append(one.split(":")[0])
        for one in paths.split():
            if os.path.exists('%s/strings.xml'%one):
                self._export_path(one,"strings.xml")
            if os.path.exists('%s/wt_strings.xml'%one):
                self._export_path(one,"wt_strings.xml")
            if os.path.exists('%s/arrays.xml'%one):
                self._export_path(one,"arrays.xml")
            if os.path.exists('%s/mtk_strings.xml'%one):
                self._export_path(one,"mtk_strings.xml")
        wbk.save('%s/out/Export_%s_%s.xls'%(PWD,gen_date(),gen_time()))
        wx.MessageBox("Export successed!","OK")
        mysys("nautilus %s/out"%PWD)

    def _export_path(self,path,xml):
        with open('%s/%s'%(path,xml),'r') as f:
            content = ''.join([i.strip() for i in f.readlines()])
        for one in content.split("</string>"):
            if "<string " in one and 'translatable="false"' not in one:
                st = one.split("<string ")[1]
                name = st.split('"')[1].split('"')[0]
                if 'product="' in st:
                    name = name + "[product]:(%s)"%st.split('"')[3].split('"')[0]
                n = st.find(">")
                value = st[n+1:]
                myprint("m","%s/%s === %s === %s"%(path,xml,name,value))
                self.sheet.write(self.i,0,"%s/%s"%(path,xml))
                self.sheet.write(self.i,1,'string')
                self.sheet.write(self.i,2,name)
                self.sheet.write(self.i,3,'0')
                self.sheet.write(self.i,4,'0')
                self.sheet.write(self.i,5,value)
                k=1
                for two in self.values_all:
                    try:
                        with open('%s-%s/%s'%(path,two,xml),'r') as f1:
                            content1 = ''.join([i.strip() for i in f1.readlines()])
                        st1 = content1.split('"%s"'%name)[1].split("</string>")[0]
                        n1 = st1.find(">")
                        value1 = st1[n1+1:]
                    except Exception:
                        value1 = value
                    self.sheet.write(self.i,5+k,value1)
                    k=k+1
                self.i = self.i + 1

        for one in content.split("</plurals>"):
            if "<plurals " in one and 'translatable="false"' not in one:
                st = one.split("<plurals ")[1]
                name = st.split('"')[1].split('"')[0]
                if 'product="' in st:
                    name = name + "[product]:(%s)"%st.split('"')[3].split('"')[0]
                count = len(st.split("</item>"))-1
                dic1 = {}
                for one in range(count):
                    itsr = st.split("</item>")[one]
                    key1 = itsr.split("<item")[1].split('"')[1].split('"')[0]
                    n = itsr.split("<item")[1].find(">")
                    values1 = itsr.split("<item")[1][n+1:]
                    dic1.setdefault(key1,values1)
                for key in dic1.keys():
                    myprint("m","%s/%s === %s === %s"%(path,xml,name,dic1[key]))
                    self.sheet.write(self.i,0,"%s/%s"%(path,xml))
                    self.sheet.write(self.i,1,'plurals')
                    self.sheet.write(self.i,2,name)
                    self.sheet.write(self.i,3,count)
                    self.sheet.write(self.i,4,key)
                    self.sheet.write(self.i,5,dic1[key])
                    k=1
                    for two in self.values_all:
                        try:
                            with open('%s-%s/%s'%(path,two,xml),'r') as f1:
                                content1 = ''.join([i.strip() for i in f1.readlines()])
                            st1 = content1.split('"%s"'%name)[1].split("</plurals>")[0]
                            st1 = st1.split('"%s"'%key)[1].split("</item>")[0]
                            n1 = st1.find(">")
                            value1 = st1[n1+1:]
                        except Exception:
                            value1 = dic1[key]
                        self.sheet.write(self.i,5+k,value1)
                        k=k+1
                    self.i = self.i + 1

        for one in content.split("</string-array>"):
            if "<string-array " in one and 'translatable="false"' not in one:
                st = one.split("<string-array ")[1]
                name = st.split('"')[1].split('"')[0]
                if 'product="' in st:
                    name = name + "[product]:(%s)"%st.split('"')[3].split('"')[0]
                count = len(st.split("</item>"))-1
                dic1 = {}
                for one in range(count):
                    itsr = st.split("</item>")[one]
                    try:
                        n = itsr.split("<item")[1].find(">")
                        values1 = itsr.split("<item")[1][n+1:]
                        dic1.setdefault(one,values1)
                    except Exception,e:
                        print e
                for key in dic1.keys():
                    myprint("m","%s/%s === %s === %s"%(path,xml,name,dic1[key]))
                    self.sheet.write(self.i,0,"%s/%s"%(path,xml))
                    self.sheet.write(self.i,1,'arrays')
                    self.sheet.write(self.i,2,name)
                    self.sheet.write(self.i,3,count)
                    self.sheet.write(self.i,4,key)
                    self.sheet.write(self.i,5,dic1[key])
                    k=1
                    for two in self.values_all:
                        try:
                            with open('%s-%s/%s'%(path,two,xml),'r') as f1:
                                content1 = ''.join([i.strip() for i in f1.readlines()])
                            st1 = content1.split('"%s"'%name)[1].split("</string-array>")[0]
                            st1 = st1.split("</item>")[int(key)].split("<item")[1]
                            n1 = st1.find(">")
                            value1 = st1[n1+1:]
                        except Exception,e:
                            print e
                            value1 = dic1[key]
                        self.sheet.write(self.i,5+k,value1)
                        k=k+1
                    self.i = self.i + 1


class StringsFilFrame(wx.Frame):
    def __init__(self,user):
        wx.Frame.__init__(self,None,-1,"Filter",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -2])
        self.statusbar.SetStatusText("Wingtech Communications, Shanghai,P.R.C.", 0)
        self.statusbar.SetStatusText("Welcome,  %s!"%user, 1)
        self.user = user
        X = Y = 20
        Y2 = 430
        BUTTON_SIZE = (60, 26)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,"Back",(X,Y2),BUTTON_SIZE))

        self.Label1 = wx.StaticText(panel,-1,"Excel",(X,Y))
        self.Label2 = wx.StaticText(panel,-1,"Language",(X,Y+47))
        self.Dir = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,"",(X+70,Y-2),(370,26))
        self.Bind(wx.EVT_BUTTON,self.OnSearch,wx.Button(panel,-1,"Browse",(X+450,Y-2),(60,26)))
        self.LANG = wx.ComboBox(panel, -1, "", (X+70,Y+45),(160,26), [], wx.CB_DROPDOWN)
        self.Log = wx.ListBox(panel,-1,(X,Y+84),(510,310),"",wx.LB_SINGLE)
        self.Bind(wx.EVT_BUTTON,self.OnStart,wx.Button(panel,-1,"Go",(X+450,Y2),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        WorkbenchFrame(self.user).Show()

    def OnSearch(self,e):
        dialog = wx.FileDialog(self,"Choose a file",os.getcwd(),style=wx.OPEN,wildcard="*.xls")
        if dialog.ShowModal() == wx.ID_OK:
            self.Dir.SetValue(dialog.GetPath())
        try:
            self.data = xlrd.open_workbook(dialog.GetPath())
            self.table = self.data.sheet_by_index(0)
            self.LANG.Clear()
            for one in self.table.row_values(0)[7:]:
               self.LANG.Append(one)
        except Exception,e:
            print e
        dialog.Destroy()

    def gen_local(self):
        local = 7
        for one in self.table.row_values(0)[7:]:
            if one == self.LANG.GetValue():
                return local
            else:
                local = local + 1

    def OnStart(self,e):
        local = self.gen_local()
        lists = []
        N = self.table.nrows
        lists.append("Total strings：%d"%N)
        self.Log.Set(lists)
        wbk = xlwt.Workbook(encoding='utf-8')
        self.sheet = wbk.add_sheet('sheet1')
        self.sheet.col(0).width = 16000
        self.sheet.col(1).width = 3000
        self.sheet.col(2).width = 9000
        self.sheet.col(3).width = 3000
        self.sheet.col(4).width = 3000
        self.sheet.col(5).width = 10000
        self.sheet.col(6).width = 15000
        self.sheet.col(7).width = 15000
        K = 1
        for one in range(N):
            if self.table.cell(one,3).value == "Length":
                self.sheet.write(0,0,'Relative Path')
                self.sheet.write(0,1,'String Type')
                self.sheet.write(0,2,'Name')
                self.sheet.write(0,3,'Length')
                self.sheet.write(0,4,'Index')
                self.sheet.write(0,5,'values')
                self.sheet.write(0,6,'values-zh-rCN')
                self.sheet.write(0,7,self.LANG.GetValue())
            elif self.table.cell(one,3).value == "0":
                FLAG = True
                str1 = self.table.row_values(one)[local]
                if rmquote(self.table.row_values(one)[5]) != rmquote(str1):
                    FLAG = False
                if rmquote(str1).startswith("@string/"):
                    FLAG = False
                if rmquote(str1).isdigit() == True:
                    FLAG =False
                if len(rmquote(str1)) == 1:
                    FLAG = False
                if self.table.row_values(one)[5] == "":
                    FLAG = False
                if FLAG == True:
                    self.sheet.write(K,0,self.table.row_values(one)[0])
                    self.sheet.write(K,1,self.table.row_values(one)[1])
                    self.sheet.write(K,2,self.table.row_values(one)[2])
                    self.sheet.write(K,3,self.table.row_values(one)[3])
                    self.sheet.write(K,4,self.table.row_values(one)[4])
                    self.sheet.write(K,5,self.table.row_values(one)[5])
                    self.sheet.write(K,6,self.table.row_values(one)[6])
                    self.sheet.write(K,7,self.table.row_values(one)[local])
                    K = K + 1
            else:
                FLAG = True
                length1 = int(self.table.cell(one,3).value)
                if self.table.row_values(one)[2] == self.table.row_values(one-1)[2]:
                    FLAG = False
                lists = []
                for two in range(length1):
                    try:
                        lists.append(rmquote(self.table.row_values(one+two)[local]))
                    except Exception:
                        pass
                m = 0
                n = 0
                for three in lists:
                    if three.startswith("@string/"):
                        m = m + 1
                    if three.isdigit() == True:
                        n = n + 1
                if m == length1 or n == length1:
                    FLAG = False
                if FLAG == True:
                    for four in range(length1):
                        self.sheet.write(K,0,self.table.row_values(one+four)[0])
                        self.sheet.write(K,1,self.table.row_values(one+four)[1])
                        self.sheet.write(K,2,self.table.row_values(one+four)[2])
                        self.sheet.write(K,3,self.table.row_values(one+four)[3])
                        self.sheet.write(K,4,self.table.row_values(one+four)[4])
                        self.sheet.write(K,5,self.table.row_values(one+four)[5])
                        self.sheet.write(K,6,self.table.row_values(one+four)[6])
                        self.sheet.write(K,7,self.table.row_values(one+four)[local])
                        K = K + 1
        wbk.save('%s/out/Filter_%s_%s.xls'%(PWD,gen_date(),gen_time()))
        wx.MessageBox("Filter successed","OK")
        mysys("nautilus %s/out"%PWD)



class StringsImpFrame(wx.Frame):
    def __init__(self,user):
        wx.Frame.__init__(self,None,-1,"Import",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -2])
        self.statusbar.SetStatusText("Wingtech Communications, Shanghai,P.R.C.", 0)
        self.statusbar.SetStatusText("Welcome,  %s!"%user, 1)
        self.user = user
        X = Y = 20
        Y2 = 430
        BUTTON_SIZE = (60, 26)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,"Back",(X,Y2),BUTTON_SIZE))
        self.DIC = {}
        self.Label1 = wx.StaticText(panel,-1,"Excel",(X,Y))
        self.Label2 = wx.StaticText(panel,-1,"CodePath",(X,Y+35))
        self.Dir1 = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,"",(X+70,Y-2),(370,26))
        self.Dir2 = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,"",(X+70,Y+33),(370,26))
        self.Bind(wx.EVT_BUTTON,self.OnFilePath,wx.Button(panel,-1,"Browse",(X+450,Y-2),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnDirPath,wx.Button(panel,-1,"Browse",(X+450,Y+33),BUTTON_SIZE))

        self.Bind(wx.EVT_BUTTON,self.OnCheck,wx.Button(panel,-1,"Check",(X,Y+74),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnImport_Setting,wx.Button(panel,-1,"Setting",(X+65,Y+74),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnStart,wx.Button(panel,-1,"Go",(X+450,Y2),BUTTON_SIZE))

        self.Log = wx.ListBox(panel,-1,(X,Y+114),(510,280),"",wx.LB_SINGLE)
        lists = [
          "Import Steps:",
          "1.Click Browse to choose the strings file",
          "2.Click Check to check the env",
          "3.Click Setting to choose languages need to import",
          "4.Click Go at last"]
        self.Log.Set(lists)

    def OnFilePath(self,event):
        dialog = wx.FileDialog(None, 'Choose the string file:',os.getcwd(),style = wx.OPEN,wildcard = "*.xls")
        if dialog.ShowModal() == wx.ID_OK:
            self.Dir1.SetValue(dialog.GetPath())
        dialog.Destroy()

    def OnDirPath(self,event):
        dialog = wx.DirDialog(None, 'Choose the code path:',os.getcwd(),style = wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.Dir2.SetValue(dialog.GetPath())
            self.ROOT_PATH = dialog.GetPath()
        dialog.Destroy()

    def OnBack(self,e):
        self.Close()
        WorkbenchFrame(self.user).Show()

    def OnCheck(self,e):
        self.muls = []
        if not self.Dir1.GetValue():
            wx.MessageBox("Choose a string file first!","Error")
            return -1
        try:
            os.chdir(self.ROOT_PATH)
            self.SetStatusText("Check env，half a moment...")
            mysys("find . -name *.xmltmpbak|xargs rm")
        except Exception,e:
            wx.MessageBox("Choose the code path first","Error")
            return -1
        if os.path.exists("%s/frameworks/base"%self.ROOT_PATH):
            data = xlrd.open_workbook(self.Dir1.GetValue())
            table = data.sheets()[0]
            self.muls = table.row_values(0)[6:]
            self.SetStatusText("The env is OK!")

    def OnImport_Setting(self,e):
        if self.muls:
            Import(self.muls).Show()
        else:
            self.SetStatusText("Please check the env!")

    def OnStart(self,e):
        data = xlrd.open_workbook(self.Dir1.GetValue())
        table = data.sheets()[0]
        firstlists = table.row_values(0)
        rows = table.nrows
        for one in file2lines("%s/misc/.import_languages_need"%PWD):
            one = one.split("\n")[0]
            i = 0
            for item in firstlists:
                if one == item:
                    localrow = i
                    break
                else:
                    i = i + 1
            for i in range(1,rows):
                print "current row: %d"%i
                listi = table.row_values(i)
                pathi = listi[0]
                typei = listi[1]
                namei = listi[2]
                lengi = int(listi[3])
                value = listi[localrow]
                if pathi == table.row_values(i-1)[0] and typei == table.row_values(i-1)[1] and namei == table.row_values(i-1)[2]:
                    pass
                else:
                    file1 = pathi.split("/values/")[0]+"/"+one+"/"+pathi.split("/values/")[1]+"tmpbak"
                    if os.path.exists(file1):
                        pass
                    else:
                        mysys("mkdir -p %s"%file1[:file1.rfind("/")])
                        f = open(file1,"w")
                        f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources xmlns:xliff="urn:oasis:names:tc:xliff:document:1.2">\n')
                        f.close()
                    if typei == "string":
                        f = open(file1,"a")
                        if "[product]:" in namei:
                            name_value = namei.split("[product]:")[0]
                            product_value = namei.split("[product]:")[1]
                            f.write(u'    <string name="%s" product="%s">%s</string>\n'%(name_value,product_value,value))
                        else:
                            f.write(u'    <string name="%s">%s</string>\n'%(namei,value))
                        f.close()
                    if typei == "plurals":
                        f = open(file1,"a")
                        f.write(u'    <plurals name="%s">\n'%namei)
                        for j in range(lengi):
                            f.write(u'        <item quantity="%s">%s</item>\n'%(table.row_values(i+j)[4],table.row_values(i+j)[localrow]))
                        f.write(u'    </plurals>\n')
                        f.close()
                    if typei == "arrays":
                        f = open(file1,"a")
                        f.write(u'    <string-array name="%s">\n'%namei)
                        for j in range(lengi):
                            f.write(u'        <item>%s</item>\n'%(table.row_values(i+j)[localrow]))
                        f.write(u'    </string-array>\n')
                        f.close()
                i = i + 1
            lists = myget("find . -name *.xmltmpbak").split("\n")
            for two in lists:
                f = open(two,"a")
                f.write("</resources>")
                f.close()
                mysys("mv %s %s"%(two,two[:-6]))
                print "finish opt %s"%two[:-6]
            print "Finish import!"


class QueryBraFrame(wx.Frame):
    def __init__(self,user):
        wx.Frame.__init__(self,None,-1,"Branch",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -2])
        self.statusbar.SetStatusText("Wingtech Communications, Shanghai,P.R.C.", 0)
        self.statusbar.SetStatusText("Welcome,  %s!"%user, 1)
        self.user = user
        X = 20
        Y = 430
        BUTTON_SIZE = (60, 26)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,"Back",(X,Y),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnRun,wx.Button(panel,-1,"Run",(X+480,Y),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        WorkbenchFrame(self.user).Show()

    def OnRun(self,e):
        pass


class QueryMinFrame(wx.Frame):
    def __init__(self,user):
        wx.Frame.__init__(self,None,-1,"Mine",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -2])
        self.statusbar.SetStatusText("Wingtech Communications, Shanghai,P.R.C.", 0)
        self.statusbar.SetStatusText("Welcome,  %s!"%user, 1)
        self.user = user
        X = 20
        Y = 430
        BUTTON_SIZE = (60, 26)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,"Back",(X,Y),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnRun,wx.Button(panel,-1,"Run",(X+480,Y),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        WorkbenchFrame(self.user).Show()

    def OnRun(self,e):
        pass


class ApplyAutFrame(wx.Frame):
    def __init__(self,user):
        wx.Frame.__init__(self,None,-1,"Authority",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -2])
        self.statusbar.SetStatusText("Wingtech Communications, Shanghai,P.R.C.", 0)
        self.statusbar.SetStatusText("Welcome,  %s!"%user, 1)
        self.user = user
        X = 20
        Y = 430
        BUTTON_SIZE = (60, 26)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,"Back",(X,Y),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnRun,wx.Button(panel,-1,"Run",(X+480,Y),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        WorkbenchFrame(self.user).Show()

    def OnRun(self,e):
        pass


class ApplyGitFrame(wx.Frame):
    def __init__(self,user):
        wx.Frame.__init__(self,None,-1,"Git",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -2])
        self.statusbar.SetStatusText("Wingtech Communications, Shanghai,P.R.C.", 0)
        self.statusbar.SetStatusText("Welcome,  %s!"%user, 1)
        self.user = user
        X = 20
        Y = 430
        BUTTON_SIZE = (60, 26)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,"Back",(X,Y),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnRun,wx.Button(panel,-1,"Run",(X+480,Y),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        WorkbenchFrame(self.user).Show()

    def OnRun(self,e):
        pass

class ApplyBraFrame(wx.Frame):
    def __init__(self,user):
        wx.Frame.__init__(self,None,-1,"Branch",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -2])
        self.statusbar.SetStatusText("Wingtech Communications, Shanghai,P.R.C.", 0)
        self.statusbar.SetStatusText("Welcome,  %s!"%user, 1)
        self.user = user
        X = 20
        Y = 430
        BUTTON_SIZE = (60, 26)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,"Back",(X,Y),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnRun,wx.Button(panel,-1,"Run",(X+480,Y),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        WorkbenchFrame(self.user).Show()

    def OnRun(self,e):
        pass

class ApplyDaiFrame(wx.Frame):
    def __init__(self,user):
        wx.Frame.__init__(self,None,-1,"Dailybuild",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -2])
        self.statusbar.SetStatusText("Wingtech Communications, Shanghai,P.R.C.", 0)
        self.statusbar.SetStatusText("Welcome,  %s!"%user, 1)
        self.user = user
        X = 20
        Y = 430
        BUTTON_SIZE = (60, 26)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,"Back",(X,Y),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnRun,wx.Button(panel,-1,"Run",(X+480,Y),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        WorkbenchFrame(self.user).Show()

    def OnRun(self,e):
        pass

class ApplyRelFrame(wx.Frame):
    def __init__(self,user):
        wx.Frame.__init__(self,None,-1,"Release",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -2])
        self.statusbar.SetStatusText("Wingtech Communications, Shanghai,P.R.C.", 0)
        self.statusbar.SetStatusText("Welcome,  %s!"%user, 1)
        self.user = user
        X = 20
        Y = 430
        BUTTON_SIZE = (60, 26)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,"Back",(X,Y),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnRun,wx.Button(panel,-1,"Run",(X+480,Y),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        WorkbenchFrame(self.user).Show()

    def OnRun(self,e):
        pass

class FileSetFrame(wx.Frame):
    def __init__(self,user):
        wx.Frame.__init__(self,None,-1,"Settings",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -2])
        self.statusbar.SetStatusText("Wingtech Communications, Shanghai,P.R.C.", 0)
        self.statusbar.SetStatusText("Welcome,  %s!"%user, 1)
        self.user = user
        X = 20
        Y = 430
        BUTTON_SIZE = (60, 26)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,"Back",(X,Y),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnRun,wx.Button(panel,-1,"Run",(X+480,Y),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        WorkbenchFrame(self.user).Show()

    def OnRun(self,e):
        pass

class FileUpdFrame(wx.Frame):
    def __init__(self,user):
        wx.Frame.__init__(self,None,-1,"Update",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -2])
        self.statusbar.SetStatusText("Wingtech Communications, Shanghai,P.R.C.", 0)
        self.statusbar.SetStatusText("Welcome,  %s!"%user, 1)
        self.user = user
        X = 20
        Y = 430
        BUTTON_SIZE = (60, 26)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,"Back",(X,Y),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnRun,wx.Button(panel,-1,"Run",(X+480,Y),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        WorkbenchFrame(self.user).Show()

    def OnRun(self,e):
        pass

class FileAboFrame(wx.Frame):
    def __init__(self,user):
        wx.Frame.__init__(self,None,-1,"About",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -2])
        self.statusbar.SetStatusText("Wingtech Communications, Shanghai,P.R.C.", 0)
        self.statusbar.SetStatusText("Welcome,  %s!"%user, 1)
        self.user = user
        X = 20
        Y = 430
        BUTTON_SIZE = (60, 26)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,"Back",(X,Y),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnRun,wx.Button(panel,-1,"Run",(X+480,Y),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        WorkbenchFrame(self.user).Show()

    def OnRun(self,e):
        pass

class WorkbenchFrame(wx.Frame):
    def __init__(self,user):
        wx.Frame.__init__(self,None,-1,u"Workbench",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -2])
        self.statusbar.SetStatusText("Wingtech Communications, Shanghai,P.R.C.", 0)
        self.statusbar.SetStatusText("Welcome,  %s!"%user, 1)
        self.user = user
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        self._mb = FM.FlatMenuBar(self, wx.ID_ANY, 32, 4, options=FM_OPT_SHOW_TOOLBAR)
        FileMenu = FM.FlatMenu()
        ApplyMenu = FM.FlatMenu()
        QueryMenu = FM.FlatMenu()
        ToolMenu = FM.FlatMenu()
        StringsMenu = FM.FlatMenu()
        SCMMenu  = FM.FlatMenu()

        ID_FILE_SET = 10001
        ID_FILE_UPD = 10002
        ID_FILE_ABO = 10003
        ID_FILE_CLO = 10004
        FileMenu.AppendItem(FM.FlatMenuItem(FileMenu, ID_FILE_SET, "Settings", wx.ITEM_NORMAL))
        FileMenu.AppendItem(FM.FlatMenuItem(FileMenu, ID_FILE_UPD, "Update", wx.ITEM_NORMAL))
        FileMenu.AppendItem(FM.FlatMenuItem(FileMenu, ID_FILE_ABO, "About", wx.ITEM_NORMAL))
        FileMenu.AppendItem(FM.FlatMenuItem(FileMenu, ID_FILE_CLO, "Close", wx.ITEM_NORMAL))
        ID_APPLY_AUT = 20001
        ID_APPLY_GIT = 20002
        ID_APPLY_BRA = 20003
        ID_APPLY_DAI = 20004
        ID_APPLY_REL = 20005
        ApplyMenu.AppendItem(FM.FlatMenuItem(FileMenu, ID_APPLY_AUT, "Authority", wx.ITEM_NORMAL))
        ApplyMenu.AppendItem(FM.FlatMenuItem(FileMenu, ID_APPLY_GIT, "Git", wx.ITEM_NORMAL))
        ApplyMenu.AppendItem(FM.FlatMenuItem(FileMenu, ID_APPLY_BRA, "Branch", wx.ITEM_NORMAL))
        ApplyMenu.AppendItem(FM.FlatMenuItem(FileMenu, ID_APPLY_DAI, "Dailybuild", wx.ITEM_NORMAL))
        ApplyMenu.AppendItem(FM.FlatMenuItem(FileMenu, ID_APPLY_REL, "Release", wx.ITEM_NORMAL))
        ID_QUERY_BRA = 30001
        ID_QUERY_MIN = 30002
        QueryMenu.AppendItem(FM.FlatMenuItem(QueryMenu, ID_QUERY_BRA, "Branch", wx.ITEM_NORMAL))
        QueryMenu.AppendItem(FM.FlatMenuItem(QueryMenu, ID_QUERY_MIN, "Mine", wx.ITEM_NORMAL))
        ID_TOOL_STR = 40001
        ToolMenu.AppendItem(FM.FlatMenuItem(ToolMenu, ID_TOOL_STR, "Strings", "", wx.ITEM_NORMAL, StringsMenu))
        ID_STRINGS_EXP = 400011
        ID_STRINGS_FIL = 400012
        ID_STRINGS_IMP = 400013
        StringsMenu.AppendItem(FM.FlatMenuItem(StringsMenu, ID_STRINGS_EXP, "Export", "", wx.ITEM_NORMAL))
        StringsMenu.AppendItem(FM.FlatMenuItem(StringsMenu, ID_STRINGS_FIL, "Filter", "", wx.ITEM_NORMAL))
        StringsMenu.AppendItem(FM.FlatMenuItem(StringsMenu, ID_STRINGS_IMP, "Import", "", wx.ITEM_NORMAL))
        ID_SCM_HAN = 50001
        SCMMenu.AppendItem(FM.FlatMenuItem(SCMMenu, ID_SCM_HAN, "Handle", wx.ITEM_NORMAL))

        self._mb.Append(FileMenu, "File")
        self._mb.Append(ApplyMenu, "Apply")
        self._mb.Append(QueryMenu, "Query")
        self._mb.Append(ToolMenu, "Tool")
        self._mb.Append(SCMMenu, "SCM")
        mainSizer.Add(self._mb, -1, wx.EXPAND)
        mainSizer.Layout()

        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnFileSet, id=ID_FILE_SET)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnFileUpd, id=ID_FILE_UPD)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnFileAbo, id=ID_FILE_ABO)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnFileClo, id=ID_FILE_CLO)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnApplyAut, id=ID_APPLY_AUT)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnApplyGit, id=ID_APPLY_GIT)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnApplyBra, id=ID_APPLY_BRA)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnApplyDai, id=ID_APPLY_DAI)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnApplyRel, id=ID_APPLY_REL)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnQueryBra, id=ID_QUERY_BRA)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnQueryMin, id=ID_QUERY_MIN)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnStringsExp, id=ID_STRINGS_EXP)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnStringsFil, id=ID_STRINGS_FIL)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnStringsImp, id=ID_STRINGS_IMP)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnSCMHan, id=ID_SCM_HAN)

    def OnFileSet(self,e):
        FileSetFrame(self.user).Show()
        self.Hide()

    def OnFileUpd(self,e):
        FileUpdFrame(self.user).Show()
        self.Hide()

    def OnFileAbo(self,event):
        info = wx.AboutDialogInfo()
        info.Name = "Wingtech Communications, Shanghai,P.R.C."
        info.Version = "V1.0.0"
        info.Copyright = "(C) 2015 Programmers and Coders Everywhere"
        info.Description = wordwrap(
            "It's a GUI tool wrote by python and wxpython.",
            350, wx.ClientDC(self))
        info.WebSite = ("http://192.168.7.238/", "Home page")
        info.Developers = [ "zhouyanjiang",]
        licenseText = u"Wingtech Communications, Shanghai,P.R.C."
        info.License = wordwrap(licenseText, 500, wx.ClientDC(self))
        wx.AboutBox(info)

    def OnFileClo(self,e):
        self.Close()
        sys.exit(-1)

    def OnApplyAut(self,e):
        ApplyAutFrame(self.user).Show()
        self.Hide()

    def OnApplyGit(self,e):
        ApplyGitFrame(self.user).Show()
        self.Hide()

    def OnApplyBra(self,e):
        ApplyBraFrame(self.user).Show()
        self.Hide()

    def OnApplyDai(self,e):
        ApplyDaiFrame(self.user).Show()
        self.Hide()

    def OnApplyRel(self,e):
        ApplyRelFrame(self.user).Show()
        self.Hide()

    def OnQueryBra(self,e):
        QueryBraFrame(self.user).Show()
        self.Hide()

    def OnQueryMin(self,e):
        QueryMinFrame(self.user).Show()
        self.Hide()

    def OnStringsExp(self,e):
        StringsExpFrame(self.user).Show()
        self.Hide()

    def OnStringsFil(self,e):
        StringsFilFrame(self.user).Show()
        self.Hide()

    def OnStringsImp(self,e):
        StringsImpFrame(self.user).Show()
        self.Hide()

    def OnSCMHan(self,e):
        SCMHanFrame(self.user).Show()
        self.Hide()


class Login(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"Login",size=(300,175))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        X = Y = 20
        wx.StaticText(panel,-1,"User",(X,Y))
        wx.StaticText(panel,-1,"Passwd",(X,Y+30))
        X = 75
        default_user = default_pass = ""
        default_isremb = False
        if os.path.exists(REMEMBER_ACCOUNT_FILE):
            try:
                default_user = file2lines(REMEMBER_ACCOUNT_FILE)[0].strip()
                default_pass =  file2lines(REMEMBER_ACCOUNT_FILE)[1].strip()
                default_isremb = True
            except Exception:
                default_user = default_pass = ""
                default_isremb = False
        self.User = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,default_user,(X,Y-2),(200,26))
        self.Pass = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,default_pass,(X,Y+28),(200,26),style=wx.TE_PASSWORD)
        X = 20
        Y = 80
        self.rempassCheck=wx.CheckBox(panel,label='Remember',pos=(X,Y))
        self.rempassCheck.SetValue(default_isremb)
        self.autologCheck=wx.CheckBox(panel,label='Automatic login',pos=(X+120,Y))       
        Y = 115
        BUTTON_SIZE = (60,28)
        self.Bind(wx.EVT_BUTTON,self.OnExit,wx.Button(panel,-1,"Exit",(X,Y),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnLogin,wx.Button(panel,-1,"Login",(X+192,Y),BUTTON_SIZE))

    def OnExit(self,e):
        self.Close()

    def OnLogin(self,e):
        user = self.User.GetValue()
        if not user:
            wx.MessageBox("Please enter a username!","Warning")
            return -1
        passwd = self.Pass.GetValue()
        if not passwd:
            wx.MessageBox("Please enter the password!","Warning")
            return -1
        isauto = self.autologCheck.GetValue()
        if isauto:
            isremb = True
        else:
            isremb = self.rempassCheck.GetValue()
        try:
            cu = connect_db()
        except Exception:
            wx.MessageBox("Can not connect to the database!","Warning")
            return -1
        try:
            cu.execute("select passwd from USER where name='%s'"%user)
            db_passwd = cu.fetchall()[0][0]
        except Exception:
            wx.MessageBox("Illegal user name!","Warning")
            return -1
        if db_passwd != passwd:
            wx.MessageBox("Error password!","Warning")
            return -1
        if isremb:
            f = open(REMEMBER_ACCOUNT_FILE,"w")
            f.write("%s\n%s"%(user,passwd))
            f.close()
        else:
            mysys("rm %s"%REMEMBER_ACCOUNT_FILE)
        if isauto:
            f = open(AUTOMATIC_LOGIN_FILE,"w")
            f.close()
        self.Close()
        WorkbenchFrame(user).Show()

if __name__ == '__main__':
    mysys("rm -rf ./misc/.*language* *.log")
    PWD = myget("pwd")
    app = wx.PySimpleApp()
    if os.path.exists(AUTOMATIC_LOGIN_FILE):
        WorkbenchFrame(file2lines(REMEMBER_ACCOUNT_FILE)[0].strip()).Show()
    else:
        Login().Show()
    app.MainLoop()
