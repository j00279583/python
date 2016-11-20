#_*_ coding:utf-8 _*_
import wx
import re
import MySQLdb as Agent_Db

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,id = -1,title = 'Telephone book')
        panel = wx.Panel(self,-1)
        self.button1 = wx.Button(panel, -1, "Submit", pos=(250,250))
        self.Bind(wx.EVT_BUTTON, self.OnClick1, self.button1)
        self.button1.SetDefault()

        self.button2 = wx.Button(panel,-1,"Connect Mysql",pos = (250,300))
        self.Bind(wx.EVT_BUTTON,self.OnClick2,self.button2)
        self.button2.SetDefault()

        self.button3 = wx.Button(panel, -1, "Search People", pos=(250, 350))
        self.Bind(wx.EVT_BUTTON, self.OnClick3, self.button3)
        self.button3.SetDefault()

        staTicText1 = wx.StaticText(panel,-1,"Name:",pos=(15,25))
        self.basicText1 = wx.TextCtrl(panel,-1," ",pos=(85,25),size =(100,20),style = wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER,self.OnInputText1,self.basicText1);

        staTicText2 = wx.StaticText(panel, -1, "Address:", pos=(15, 75))
        self.basicText2 = wx.TextCtrl(panel, -1, "", pos=(85, 75), size=(100, 20),style = wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnInputText2, self.basicText2);

        staTicText3 = wx.StaticText(panel, -1, "PhoneNum:", pos=(15, 125))
        self.basicText3 = wx.TextCtrl(panel, -1, "", pos=(85, 125), size=(100, 20),style = wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnInputText3, self.basicText3)

        staTicText4 = wx.StaticText(panel, -1, "PeopleName:", pos=(0, 355))
        self.basicText4 = wx.TextCtrl(panel, -1, " ", pos=(85, 350), size=(100, 30))

        self.cur = ''
        self.MessageList = []
        self.string1 = ''
        self.string2 = ''
        self.string3 = ''

    def OnClick1(self,event):
        self.OnInputText1(None)
        self.OnInputText2(None)
        self.OnInputText3(None)

        self.Agent_OperateMysql(self.cur,self.con)

        return True

    def OnClick2(self,event):
        self.ret = self.Agent_Connet_Mysql()
        if self.ret == True:
            wx.MessageBox("connet success", "Notice")
        else:
            wx.MessageBox("connnect faile", "Waring")
        return True

    def OnClick3(self, event):
        self.string4 = self.basicText4.GetValue()
        print self.string4
        self.CovertStr4 = self.string4.encode("ascii")
        self.Agent_GetDataByMysql(self.cur,self.con)

        return True

    def Agent_CheckMessAge(self):
        if len(self.MessageList) != 3:
            wx.MessageBox("Please input the message!","Waring")
            print self.MessageList[0]
            print self.MessageList[1]
            print self.MessageList[2]
            return  False
        return True

    def Agent_Connet_Mysql(self):
        try:
            con = Agent_Db.connect(host='localhost', user='root', passwd='root', db='cusemysql')
            if con != '':
                pass
            self.cur = con.cursor()
            self.con = con

            return True
        except Agent_Db.Error,msg:
            print "MySQL Error %d, %s" %(msg.args[0],msg.args[1])
            return False
    def Agent_OperateMysql(self,cursor,con):
        if True ==self.Agent_CheckMessAge():
            cursor.execute("CREATE TABLE IF NOT EXISTS TELPHONE(PeopleName VARCHAR(25) PRIMARY KEY , \
                           Addr VARCHAR(25),TelephoneNum VARCHAR(11))")
            try:
                statement = """INSERT INTO TELPHONE(PeopleName,Addr,TelephoneNum) VALUES (%s,%s,%s)"""
                parama = str(self.CovertStr1),str(self.CovertStr2),str(self.CovertStr3)
                cursor.execute(statement,parama)
                con.commit()
            except Agent_Db.Error,msg:
                wx.MessageBox("MySQL Error %d, %s" %(msg.args[0],msg.args[1]), "Waring")
                pass
            self.Agent_Clear()

    def Agent_GetDataByMysql(self, cursor, con):
        string1 = str(self.CovertStr4)
        print string1
        parama = '%string1%'
        stament = """SELECT * FROM TELPHONE WHERE  PeopleName  LIKE '%s'""" %(parama)
        command = cursor.execute(stament)
        self.DataList  = cursor.fetchall()
        if len(self.DataList) == 0:
            print "NoPeople"
            return False
        for i in self.DataList:
            print i
        return True

    def OnInputText1(self,event):
        if self.string1 == '':
            self.string1 = self.basicText1.GetValue()
            self.CovertStr1 = self.string1.encode("ascii")
            try:
                if type(self.CovertStr1) == str:
                    print  self.string1
                    self.MessageList.append(self.CovertStr1)
            except:
                wx.MessageBox("Warning", "Please Input Name again!")
                self.basicText1.Clear()
                self.string1 =''
                return False
            return  True

    def OnInputText2(self,event):
        if self.string2 == '':
            self.string2 = self.basicText2.GetValue()
            self.CovertStr2 = self.string2.encode("ascii")
            try:
                if type(self.CovertStr2) == str:
                    print  self.string2
                    self.MessageList.append(self.CovertStr2)
            except:
                self.basicText2.Clear()
                wx.MessageBox("Warning", "Please Input Addr again!")
                self.string1 = ''
                return False
            return  True

    def OnInputText3(self,event):
        if self.string3 == '':
            self.string3 = self.basicText3.GetValue()
            self.CovertStr3 = self.string3.encode("ascii")
            if len(self.CovertStr3) != 11:
                wx.MessageBox("Warning", "Please Input PhoneNum again!")
                self.basicText3.Clear()
                self.string3 = ''
                return False
            try:
                if type(self.CovertStr3) == str:
                    print  self.string3
                    self.MessageList.append(self.CovertStr3)
            except:
                wx.MessageBox("Warning", "Please Input PhoneNum again!")
                self.basicText3.Clear()
                self.string3 = ''
                return False
            return  True
    def Agent_Clear(self):
        self.basicText1.Clear()
        self.basicText2.Clear()
        self.basicText3.Clear()
        self.MessageList = []
        self.string1 = ''
        self.string2 = ''
        self.string3 = ''
        return True
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop();


