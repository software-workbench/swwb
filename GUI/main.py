#!/usr/bin/env python
# _*_ coding:utf-8 _*_

# Tool:Strings Tool for Wingtech
# Auth:zhouyanjiang(zhouyanjiang@wingtech.com)
# Version:V1.0.1
# Date:2015-01-27


#通用常量和常用的方法
from common import *

import wx
import getpass
import xlrd
import wx.lib.agw.flatmenu as FM
from wx.lib.agw.artmanager import ArtManager, RendererBase, DCSaver
from wx.lib.agw.fmresources import ControlFocus, ControlPressed
from wx.lib.agw.fmresources import FM_OPT_SHOW_CUSTOMIZE, FM_OPT_SHOW_TOOLBAR, FM_OPT_MINIBAR
from wx.lib.wordwrap import wordwrap

#获取语言集合
#从代码的frameworks/base/core/res/res路径下搜索所有values-的路径
#通过common.py中的字典加以解析
def gen_language_class(DIR):
    lists = []
    path = DIR+"/frameworks/base/core/res/res"
    cmd = "find %s -name values*"%path
    for one in wt_get(cmd).split():
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


#在语言处理的工具中使用
#遍历代码，排除黑名单, 获取路径
#黑名单在misc/paths.ignore里
#模糊路径: 例如cts =*cts*,会过滤掉路径cts, 也会过滤掉Contacts
def gen_paths(DIR):
    print DIR
    cmd = "find . -type d "
    ignores = gen_lines("%s/misc/paths.ignore"%PWD)
    for one in ignores:
        if not one.startswith("#") and one != "":
            cmd = cmd + '! -path "*%s*" '%one[:-1]
    cmd = cmd + "-name values"
    return wt_get(cmd)


class Import(wx.Frame):
    def __init__(self,lists):
        wx.Frame.__init__(self,None,-1,u"导入语言设置",size=(600,500))
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
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y+400),(60,30)))
        self.Bind(wx.EVT_BUTTON,self.OnDelete,wx.Button(panel,-1,u"删除",(X+300,Y+400),(60,30)))
        self.Bind(wx.EVT_BUTTON,self.OnSave,wx.Button(panel,-1,u"保存",(X+450,Y+400),(60,30)))

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
        wx.Frame.__init__(self,None,-1,u"导出语言设置",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.CreateStatusBar()
        self.SetStatusText(u"左侧显示的是该代码下所有支持的语言，可以选中添加到右侧一栏!")
        X = 50
        Y = 30
        self.Listleft = []
        listtmp = gen_lines("%s/misc/.languages"%PWD)
        for one in listtmp:
            self.Listleft.append(one[:-1])
        self.Left  = wx.ListBox(panel,-1,(X,Y),(200,360),self.Listleft,wx.LB_SINGLE)
        self.Right = wx.ListBox(panel,-1,(X+300,Y),(200,360),"",wx.LB_SINGLE)
        self.Bind(wx.EVT_BUTTON,self.OnL2R,wx.Button(panel,-1,"=>",(X+225,Y+160),(50,26)))
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y+400),(60,30)))
        self.Bind(wx.EVT_BUTTON,self.OnDelete,wx.Button(panel,-1,u"删除",(X+300,Y+400),(60,30)))
        self.Bind(wx.EVT_BUTTON,self.OnSave,wx.Button(panel,-1,u"保存",(X+450,Y+400),(60,30)))

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


class FileSetFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"设置",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("")

        try:
            lines = gen_lines("/home/%s/.WTTOOLCONFIG"%getpass.getuser())
        except Exception:
            lines = []

        user = mail = cc = ""
        if len(lines) != 0:
            for one in lines:
                if "user:" in one:
                    user = one.split("user:")[1].split("\n")[0]
                if "mail:" in one:
                    mail = one.split("mail:")[1].split("\n")[0]
                if "cc:" in one:
                    cc = one.split("cc:")[1].split("\n")[0]
                
        self.Label1 = wx.StaticText(panel,-1,u"默认用户",(X,Y))
        self.User = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,user,(X+70,Y-2),(440,26))
        self.Label2 = wx.StaticText(panel,-1,u"邮箱地址",(X,Y+38))
        self.Mail = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,mail,(X+70,Y+36),(440,26))
        self.Label3 = wx.StaticText(panel,-1,u"默认抄送",(X,Y+76))
        self.CC = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,cc,(X+70,Y+74),(440,26))

        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y2),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnConf,wx.Button(panel,-1,u"确定",(X+450,Y2),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        ToolFrame().Show()

    def OnConf(self,e):
        user = self.User.GetValue()
        mail = self.Mail.GetValue()
        cc = self.CC.GetValue()
        if user != "" or mail != "" or cc != "":
            os.system("echo 'user:%s' > /home/%s/.WTTOOLCONFIG"%(user,getpass.getuser()))
            os.system("echo 'mail:%s' >> /home/%s/.WTTOOLCONFIG"%(mail,getpass.getuser()))
            os.system("echo 'cc:%s' >> /home/%s/.WTTOOLCONFIG"%(cc,getpass.getuser()))
            wx.MessageBox(u"信息保存成功！",u"成功")
        else:
            wx.MessageBox(u"无法保存！请输入至少一条信息！",u"警告")


class FileUpdFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"更新",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.cur = wt_get("git log -1 --oneline").split(" ")[1]
        self.statusbar.SetStatusText(u"当前版本: %s"%self.cur)

        self.Bind(wx.EVT_BUTTON,self.OnUpdate,wx.Button(panel,-1,u"更新",(X+235,Y+180),(80,40)))
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y2),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        ToolFrame().Show()

    def OnUpdate(self,e):
        if "Connection to 192.168.7.132 closed." in wt_get("ssh -p 29418 192.168.7.132"):
            wt_sys("git pull")
            new = wt_get("git log -1 --oneline").split(" ")[1]
            self.statusbar.SetStatusText(u"版本已更新到最新，最新版本: %s"%new)
            wx.MessageBox(u"版本已更新到最新，最新版本: %s"%new,"OK")
        else:
            wx.MessageBox(u"无法连接到服务器, 请联系SCM",u"警告") 


class CodeDowFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"下载代码",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("")

        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y2),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        ToolFrame().Show()


class CodeBuiFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"编译打包",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("")

        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y2),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        ToolFrame().Show()


class CodeGobFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"回退代码",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("")

        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y2),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        ToolFrame().Show()


class CodeLogFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"生成Log",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("")

        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y2),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        ToolFrame().Show()


class StrExpFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"字串导出",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("")

        self.DIC = {}
        
        self.Label1 = wx.StaticText(panel,-1,u"代码地址",(X,Y))
        self.Dir = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,"",(X+70,Y-2),(370,26))
        self.Bind(wx.EVT_BUTTON,self.OnDirPath,wx.Button(panel,-1,u"浏览",(X+450,Y-2),(60,26)))

        self.Bind(wx.EVT_BUTTON,self.OnCheck,wx.Button(panel,-1,u"检测",(X,Y+44),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnExport_Setting,wx.Button(panel,-1,u"设置",(X+65,Y+44),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnStart,wx.Button(panel,-1,u"开始",(X+450,Y2),BUTTON_SIZE))

        self.Log = wx.ListBox(panel,-1,(X,Y+84),(510,310),"",wx.LB_SINGLE)
        lists = [
          u"导出步骤：",
          u"1.点击浏览按钮，选择代码路径",
          u"2.点击检测按钮，检测代码环境",
          u"3.点击设置按钮，选择需要导出的语言",
          u"4.点击开始按钮，执行并输出"]
        self.Log.Set(lists)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y2),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        ToolFrame().Show()

    def OnDirPath(self,event):
        dialog = wx.DirDialog(None, u'请选择代码路径:',os.getcwd(),style = wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.Dir.SetValue(dialog.GetPath())
            self.ROOT_PATH = dialog.GetPath()
        dialog.Destroy()

    def OnCheck(self,e):
        try:
            os.chdir(self.ROOT_PATH)
            self.SetStatusText(u"开始检测代码环境，请稍后...")
        except Exception,e:
            wx.MessageBox(u"请首先选择一个代码路径!",u"错误")
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
          u"语言种类数目:  %d"%total_languages,
          u"字串所在路径总数:  %d"%total_paths,
          u"",
          u"提示:",
          u"1.如果要忽略某些路径，请修改文件 paths.ignore",
          u"2.如果想要指定导出某些文件，请点击设置按钮进行选择!"]
        self.Log.Set(lists)
        self.SetStatusText(u"代码环境OK!")

    def OnExport_Setting(self,e):
        if os.path.exists("%s/misc/.languages"%PWD):
            Export().Show()
        else:
            self.SetStatusText(u"请先检测代码环境!")

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
        language = gen_lines("%s/misc/.languages_need"%PWD)
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
        wx.MessageBox(u"导出成功，点击确认到目标文件夹!","OK")
        wt_sys("nautilus %s/out"%PWD)

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
                wt_print("m","%s/%s === %s === %s"%(path,xml,name,value))
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
                    wt_print("m","%s/%s === %s === %s"%(path,xml,name,dic1[key]))
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
                    wt_print("m","%s/%s === %s === %s"%(path,xml,name,dic1[key]))
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


class StrFilFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"字串过滤",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("")

        self.Label1 = wx.StaticText(panel,-1,u"字符串表",(X,Y))
        self.Label2 = wx.StaticText(panel,-1,u"语言",(X,Y+47))
        self.Dir = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,"",(X+70,Y-2),(370,26))
        self.Bind(wx.EVT_BUTTON,self.OnSearch,wx.Button(panel,-1,u"浏览",(X+450,Y-2),(60,26)))
        self.LANG = wx.ComboBox(panel, -1, "", (X+70,Y+45),(160,26), [], wx.CB_DROPDOWN)
        self.Log = wx.ListBox(panel,-1,(X,Y+84),(510,310),"",wx.LB_SINGLE)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y2),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnStart,wx.Button(panel,-1,u"开始",(X+450,Y2),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        ToolFrame().Show()

    def OnSearch(self,e):
        dialog = wx.FileDialog(self,"请选择一个文件",os.getcwd(),style=wx.OPEN,wildcard="*.xls")
        if dialog.ShowModal() == wx.ID_OK:
            self.Dir.SetValue(dialog.GetPath())
        try:
            self.data = xlrd.open_workbook(dialog.GetPath())
            self.table = self.data.sheet_by_name('sheet1')
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
        lists.append(u"字串总个数：%d"%N)
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
                if remove_quote(self.table.row_values(one)[5]) != remove_quote(str1):
                    FLAG = False
                if remove_quote(str1).startswith("@string/"):
                    FLAG = False
                if remove_quote(str1).isdigit() == True:
                    FLAG =False
                if len(remove_quote(str1)) == 1:
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
                        lists.append(remove_quote(self.table.row_values(one+two)[local]))
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
        wx.MessageBox(u"过滤成功，点击确认按钮到目标文件夹","OK")
        wt_sys("nautilus %s/out"%PWD)


class StrImpFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"字串导入",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("")

        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y2),BUTTON_SIZE))
        self.DIC = {}
        
        self.Label1 = wx.StaticText(panel,-1,u"字串文件",(X,Y))
        self.Label2 = wx.StaticText(panel,-1,u"代码路径",(X,Y+35))
        self.Dir1 = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,"",(X+70,Y-2),(370,26))
        self.Dir2 = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,"",(X+70,Y+33),(370,26))
        self.Bind(wx.EVT_BUTTON,self.OnFilePath,wx.Button(panel,-1,u"浏览",(X+450,Y-2),(60,26)))
        self.Bind(wx.EVT_BUTTON,self.OnDirPath,wx.Button(panel,-1,u"浏览",(X+450,Y+33),(60,26)))

        self.Bind(wx.EVT_BUTTON,self.OnCheck,wx.Button(panel,-1,u"检测",(X,Y+74),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnImport_Setting,wx.Button(panel,-1,u"设置",(X+65,Y+74),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnStart,wx.Button(panel,-1,u"开始",(X+450,Y2),BUTTON_SIZE))

        self.Log = wx.ListBox(panel,-1,(X,Y+114),(510,280),"",wx.LB_SINGLE)
        lists = [
          u"导入步骤：",
          u"1.点击浏览按钮，选择字串文件",
          u"2.点击检测按钮，检测字串文件",
          u"3.点击设置按钮，选择需要导入的语言",
          u"4.点击开始按钮，导入并输出"]
        self.Log.Set(lists)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y2),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        ToolFrame().Show()

    def OnFilePath(self,event):
        dialog = wx.FileDialog(None, u'请选择字串文件:',os.getcwd(),style = wx.OPEN,wildcard = "*.xls")
        if dialog.ShowModal() == wx.ID_OK:
            self.Dir1.SetValue(dialog.GetPath())
        dialog.Destroy()

    def OnDirPath(self,event):
        dialog = wx.DirDialog(None, u'请选择代码路径:',os.getcwd(),style = wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.Dir2.SetValue(dialog.GetPath())
            self.ROOT_PATH = dialog.GetPath()
        dialog.Destroy()

    def OnBack(self,e):
        self.Close()
        ToolFrame().Show()

    def OnCheck(self,e):
        self.muls = []
        if not self.Dir1.GetValue():
            wx.MessageBox(u"请首先选择一个字串文件!",u"错误")
        try:
            os.chdir(self.ROOT_PATH)
            self.SetStatusText(u"开始检测代码环境，请稍后...")
        except Exception,e:
            wx.MessageBox(u"请首先选择一个代码路径!",u"错误")
        if os.path.exists("%s/frameworks/base"%self.ROOT_PATH):
            data = xlrd.open_workbook(self.Dir1.GetValue())
            table = data.sheets()[0]
            self.muls = table.row_values(0)[6:]
            self.SetStatusText(u"代码环境OK!")

    def OnImport_Setting(self,e):
        if self.muls:
            Import(self.muls).Show()
        else:
            self.SetStatusText(u"请先检测代码环境!")

    def OnStart(self,e):
        data = xlrd.open_workbook(self.Dir1.GetValue())
        table = data.sheets()[0]
        firstlists = table.row_values(0)
        rows = table.nrows
        for one in gen_lines("%s/misc/.import_languages_need"%PWD):
            i = 0
            for item in firstlists:
                if one == item:
                    localrow = i
                    break
                else:
                    i = i + 1
            for i in range(1,rows):
                listi = table.row_values(i)
                pathi = listi[0]
                typei = listi[1]
                namei = listi[2]
                lengi = listi[3]
                value = listi[localrow]
                i = i + 1
                if pathi == table.row_values(i-1)[0] and typei == table.row_values(i-1)[1] and namei == table.row_values(i-1)[2]:
                    pass
                else:
                    file1 = pathi.split("/values/")[0]+"/"+one+"/"+pathi.split("/values/")[1]+"tmpbak"
                    if os.path.exists(file1):
                        pass
                    else:
                        f = open(file1,"w")
                        f.write()
 
                
                
        

class ScmGitFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"建库",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("")

        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y2),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        ToolFrame().Show()


class ScmBraFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"建分支",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("")

        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y2),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        ToolFrame().Show()


class ScmAccFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"账户权限",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("")

        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y2),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        ToolFrame().Show()


class ReqGitFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"申请Git库",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("")

        mail = cc = ""
        try:
            lines = gen_lines("/home/%s/.WTTOOLCONFIG"%getpass.getuser())
        except Exception:
            lines = []
        for one in lines:
            if "mail:" in one:
                mail = one.split("mail:")[1].split("\n")[0]
            if "cc:" in one:
                cc = one.split("cc:")[1].split("\n")[0]

        self.Label1 = wx.StaticText(panel,-1,u"代码地址",(X,Y))
        self.Add = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,"",(X+70,Y-2),(440,26))
        self.Label2 = wx.StaticText(panel,-1,u"申请人",(X,Y+38))
        self.Aut = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,mail,(X+70,Y+36),(440,26))
        self.Label3 = wx.StaticText(panel,-1,u"CC",(X,Y+76))
        self.CCs = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,cc,(X+70,Y+74),(440,26))
        self.Label4 = wx.StaticText(panel,-1,u"新建库",(X,Y+114))
        self.Dir = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,"",(X+70,Y+112),(350,26))
        self.Dirs = wx.ListBox(panel,-1,(X,Y+160),(510,230),"",wx.LB_SINGLE)
        self.Bind(wx.EVT_BUTTON,self.OnAdd,wx.Button(panel,-1,u"添加",(X+450,Y+112),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y2),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnClear,wx.Button(panel,-1,u"清空",(X+80,Y2),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnDelete,wx.Button(panel,-1,u"删除",(X+160,Y2),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnReq,wx.Button(panel,-1,u"申请",(X+450,Y2),BUTTON_SIZE))

    def OnAdd(self,e):
        if self.Dir.GetValue() != "":
            self.Dirs.Append(self.Dir.GetValue())

    def OnClear(self,e):
        self.Dirs.Clear()

    def OnDelete(self,e):
        self.Dirs.Delete(self.Dirs.GetSelection())

    def OnBack(self,e):
        self.Close()
        ToolFrame().Show()

    def OnCheck():
        try:
            repoadd = self.Add.GetValue()
            wt_sys("mkdir out")
            os.chdir("out")
            wt_sys(repoadd)
            os.chdir(PWD)
        except Exception,e:
            print e

    def OnReq(self,e):
        if self.OnCheck() == True:
            print "ok"


class ReqBraFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"申请分支",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("")

        mail = cc = ""
        try:
            lines = gen_lines("/home/%s/.WTTOOLCONFIG"%getpass.getuser())
        except Exception:
            lines = []
        for one in lines:
            if "mail:" in one:
                mail = one.split("mail:")[1].split("\n")[0]
            if "cc:" in one:
                cc = one.split("cc:")[1].split("\n")[0]

        self.Label1 = wx.StaticText(panel,-1,u"基础地址",(X,Y))
        self.Base = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,"",(X+70,Y-2),(440,26))
        self.Label2 = wx.StaticText(panel,-1,u"目标名称",(X,Y+38))
        self.Remote = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,"",(X+70,Y+36),(440,26))
        self.Label3 = wx.StaticText(panel,-1,u"目标地址",(X,Y+76))
        self.New = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,"",(X+70,Y+74),(440,26))
        self.Label4 = wx.StaticText(panel,-1,u"申请人",(X,Y+114))
        self.Auth = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,mail,(X+70,Y+112),(440,26))
        self.Label5 = wx.StaticText(panel,-1,u"CC",(X,Y+152))
        self.CCS = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,cc,(X+70,Y+150),(440,26))
        self.Label6 = wx.StaticText(panel,-1,u"建立时间",(X,Y+190))
        self.Time = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,"%s %s"%(gen_date(),gen_time()),(X+70,Y+188),(440,26))

        self.Bind(wx.EVT_BUTTON,self.OnReq,wx.Button(panel,-1,u"申请",(X+450,Y2),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y2),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        ToolFrame().Show()

    def OnReq(self,e):
        pass


class ReqRelFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"申请发布版本",size=(600,500))
        panel = wx.Panel(self,-1)
        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("")

        Y1 = 33
        self.Label1 = wx.StaticText(panel,-1,u"项目名称",(X,Y))
        self.Project = wx.ComboBox(panel, -1, "", (X+70,Y-2),(380,26), ["T86518","S86518"], wx.CB_DROPDOWN)
        self.Label2 = wx.StaticText(panel,-1,u"编译模式",(X,Y+Y1))
        self.Mode = wx.ComboBox(panel, -1, "user", (X+70,Y+Y1-2),(380,26), ["user","eng","userdebug"], wx.CB_DROPDOWN)
        self.Label3 = wx.StaticText(panel,-1,u"编译时间",(X,Y+Y1*2))
        self.Old = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,"",(X+70,Y+Y1*2-2),(380,26))
        self.Label4 = wx.StaticText(panel,-1,u"差分版本",(X,Y+Y1*3))
        self.Old = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,"",(X+70,Y+Y1*3-2),(380,26))
        self.Bind(wx.EVT_BUTTON,self.OnAddOld,wx.Button(panel,-1,u"添加",(X+465,Y+Y1*3-2),BUTTON_SIZE))
        self.Label4 = wx.StaticText(panel,-1,u"宏",(X,Y+Y1*4))
        self.MacroKey = wx.ComboBox(panel, -1, "WT_INNER_VERSION", (X+70,Y+Y1*4-2),(180,26), MACRO_LISTS, wx.CB_DROPDOWN)
        self.MacroVal = wx.TextCtrl(panel,wx.TE_PROCESS_ENTER,"",(X+270,Y+Y1*4-2),(180,26))
        self.Bind(wx.EVT_BUTTON,self.OnAddMacro,wx.Button(panel,-1,u"添加",(X+465,Y+Y1*4-2),BUTTON_SIZE))
        #self.Bind(wx.EVT_TEXT,self.OnSearch,self.Project)
        self.Log = wx.ListBox(panel,-1,(X,Y+Y1*5+7),(450,227),"",wx.LB_SINGLE)
        self.Bind(wx.EVT_BUTTON,self.OnBack,wx.Button(panel,-1,u"返回",(X,Y2),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnDelete,wx.Button(panel,-1,u"删除",(X+465,Y+170),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnClear,wx.Button(panel,-1,u"清空",(X+465,Y+210),BUTTON_SIZE))
        self.Bind(wx.EVT_BUTTON,self.OnReq,wx.Button(panel,-1,u"申请",(X+465,Y2),BUTTON_SIZE))

    def OnBack(self,e):
        self.Close()
        ToolFrame().Show()

    def OnAddOld(self,e):
        olds = self.Old.GetValue().split(";")
        for one in olds:
            item = "Old Versions:%s"%one
            if self.Log.FindString(item) == -1:
                self.Log.Append("Old Versions:%s"%one)
            else:
                wx.MessageBox(u"%s 重复选择，请确认！"%item,u"警告")
        
    def OnAddMacro(self,e):
        name = self.MacroKey.GetValue()
        value = self.MacroVal.GetValue()
        if value != "":
            item = "Macro:%s=%s"%(name,value)
            if self.Log.FindString(item) == -1:
                self.Log.Append("Macro:%s=%s"%(name,value))
            else:
                wx.MessageBox(u"%s 重复定义，请确认！"%item,u"警告")

    #def OnSearch(self,e):
    #    pass

    def OnDelete(self,e):
        self.Log.Delete(self.Log.GetSelection())

    def OnClear(self,e):
        self.Log.Clear()

    def OnReq(self,e):
        pass

class ToolFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"闻泰工具集合",size=(600,500))
        panel = wx.Panel(self,-1)

        self.Center()
        self.SetBackgroundColour(wx.Color(255,255,255))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1, -1, -1])
        self.cur = wt_get("git log -1 --oneline").split(" ")[1]
        self.statusbar.SetStatusText(u"当前版本: %s"%self.cur, 0)
        self.statusbar.SetStatusText(u"日期: %s"%gen_date(), 1)
        self.statusbar.SetStatusText(u"作者: zhouyanjiang", 2)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)

        self._mb = FM.FlatMenuBar(self, wx.ID_ANY, 32, 4, options=FM_OPT_SHOW_TOOLBAR)
        fileMenu = FM.FlatMenu()
        codeMenu = FM.FlatMenu()
        buildMenu= FM.FlatMenu()
        strMenu = FM.FlatMenu()
        scmMenu  = FM.FlatMenu()
        reqMenu  = FM.FlatMenu()
        helpMenu = FM.FlatMenu()

        fileMenu.AppendItem(FM.FlatMenuItem(fileMenu, ID_FILE_SET, u"设置\tCtrl+S", wx.ITEM_NORMAL))
        fileMenu.AppendItem(FM.FlatMenuItem(fileMenu, ID_FILE_UPD, u"更新\tCtrl+U", wx.ITEM_NORMAL))
        fileMenu.AppendItem(FM.FlatMenuItem(fileMenu, ID_FILE_CLO, u"关闭\tF4", wx.ITEM_NORMAL))
        codeMenu.AppendItem(FM.FlatMenuItem(codeMenu, ID_CODE_DOW, u"下载代码\tCtrl+D", wx.ITEM_NORMAL))
        codeMenu.AppendItem(FM.FlatMenuItem(codeMenu, ID_CODE_BUI, u"编译打包\tCtrl+B", wx.ITEM_NORMAL))
        codeMenu.AppendItem(FM.FlatMenuItem(codeMenu, ID_CODE_GOB, u"回退代码\tCtrl+G", wx.ITEM_NORMAL))
        codeMenu.AppendItem(FM.FlatMenuItem(codeMenu, ID_CODE_LOG, u"生成Log\tCtrl+L", wx.ITEM_NORMAL))
        strMenu.AppendItem(FM.FlatMenuItem(strMenu, ID_STR_EXP, u"字串导出", wx.ITEM_NORMAL))
        strMenu.AppendItem(FM.FlatMenuItem(strMenu, ID_STR_FIL, u"字串过滤", wx.ITEM_NORMAL))
        strMenu.AppendItem(FM.FlatMenuItem(strMenu, ID_STR_IMP, u"字串导入", wx.ITEM_NORMAL))
        scmMenu.AppendItem(FM.FlatMenuItem(scmMenu, ID_SCM_GIT, u"建库\tAlt+1", wx.ITEM_NORMAL))
        scmMenu.AppendItem(FM.FlatMenuItem(scmMenu, ID_SCM_BRA, u"建分支\tAlt+2", wx.ITEM_NORMAL))
        scmMenu.AppendItem(FM.FlatMenuItem(scmMenu, ID_SCM_ACC, u"账户权限\tAlt+3", wx.ITEM_NORMAL))
        reqMenu.AppendItem(FM.FlatMenuItem(reqMenu, ID_REQ_GIT, u"Git库", wx.ITEM_NORMAL))
        reqMenu.AppendItem(FM.FlatMenuItem(reqMenu, ID_REQ_BRA, u"分支", wx.ITEM_NORMAL))
        reqMenu.AppendItem(FM.FlatMenuItem(reqMenu, ID_REQ_REL, u"版本发布", wx.ITEM_NORMAL))
        helpMenu.AppendItem(FM.FlatMenuItem(helpMenu, ID_HELP_ABO, u"关于\tF1", wx.ITEM_NORMAL))

        self._mb.Append(fileMenu, u"文件")
        self._mb.Append(codeMenu, u"代码")
        self._mb.Append(strMenu, u"字串")
        #self._mb.Append(scmMenu,  "SCM")
        self._mb.Append(reqMenu,  u"申请")
        self._mb.Append(helpMenu, u"帮助")
        mainSizer.Add(self._mb, -1, wx.EXPAND)
        mainSizer.Layout()

        X1 = 90

        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnFileSet, id=ID_FILE_SET)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnFileUpd, id=ID_FILE_UPD)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnFileClo, id=ID_FILE_CLO)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnCodeDow, id=ID_CODE_DOW)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnCodeBui, id=ID_CODE_BUI)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnCodeGob, id=ID_CODE_GOB)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnCodeLog, id=ID_CODE_LOG)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnStrExp, id=ID_STR_EXP)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnStrFil, id=ID_STR_FIL)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnStrImp, id=ID_STR_IMP)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnScmGit, id=ID_SCM_GIT)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnScmBra, id=ID_SCM_BRA)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnScmAcc, id=ID_SCM_ACC)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnReqGit, id=ID_REQ_GIT)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnReqBra, id=ID_REQ_BRA)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnReqRel, id=ID_REQ_REL)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnHelpAbo, id=ID_HELP_ABO)

    def OnFileSet(self,event):
        FileSetFrame().Show()
        self.Hide()

    def OnFileUpd(self,event):
        FileUpdFrame().Show()
        self.Hide()

    def OnFileClo(self,event):
        self.Close()
        sys.exit(-1) 

    def OnCodeDow(self,event):
        CodeDowFrame().Show()
        self.Hide()     

    def OnCodeBui(self,event):
        CodeBuiFrame().Show()
        self.Hide()

    def OnCodeGob(self,event):
        CodeGobFrame().Show()
        self.Hide()

    def OnCodeLog(self,event):
        CodeLogFrame().Show()
        self.Hide()

    def OnStrExp(self,event):
        StrExpFrame().Show()
        self.Hide()

    def OnStrFil(self,event):
        StrFilFrame().Show()
        self.Hide()

    def OnStrImp(self,event):
        StrImpFrame().Show()
        self.Hide()

    def OnScmGit(self,event):
        ScmGitFrame().Show()
        self.Hide()

    def OnScmBra(self,event):
        ScmBraFrame().Show()
        self.Hide()

    def OnScmAcc(self,event):
        ScmAccFrame().Show()
        self.Hide()

    def OnReqGit(self,event):
        ReqGitFrame().Show()
        self.Hide()

    def OnReqBra(self,event):
        ReqBraFrame().Show()
        self.Hide()

    def OnReqRel(self,event):
        ReqRelFrame().Show()
        self.Hide()

    def OnHelpAbo(self,event):
        info = wx.AboutDialogInfo()
        info.Name = u"闻泰工具集合"
        info.Version = wt_get("git log -1 --oneline").split(" ")[1]
        info.Copyright = "(C) 2015 Programmers and Coders Everywhere"
        info.Description = wordwrap(
            u"该工具是上海闻泰软件内部GUI工具的集合。"
            u"开发者在Linux下使用python + wxpython开发，"
            u"主要功能包括自动化编译打包，字符串处理，图片处理等一些批量处理的工具，"
            u"以及一些GIT库和分支的配置管理工具。",
            350, wx.ClientDC(self))
        info.WebSite = ("http://192.168.7.238/", "Home page")
        info.Developers = [ "zhouyanjiang",]
        licenseText = u"本工具仅适用闻泰软件内网"
        info.License = wordwrap(licenseText, 500, wx.ClientDC(self))
        wx.AboutBox(info)


if __name__ == '__main__':
    wt_sys("rm -rf ./misc/.*language* *.log")
    PWD = wt_get("pwd")
    app = wx.PySimpleApp() 
    ToolFrame().Show()
    app.MainLoop()
