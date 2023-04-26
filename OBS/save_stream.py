import wx
import wx.html2 as html2

class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title='White Board')
        self.webview = html2.WebView.New(self)
        self.webview.LoadURL('http://localhost:8000/screenShare/')

        # 设置窗口大小
        self.SetClientSize((800, 600))  # 设置客户区域大小

        # 将 WebView 添加到 sizer 中
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.webview, 1, wx.EXPAND)
        self.SetSizer(sizer)

if __name__ == '__main__':
    app = wx.App()
    window = MainWindow()
    window.Show()
    app.MainLoop()