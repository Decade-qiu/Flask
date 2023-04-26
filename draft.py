from gi.repository import Gtk, WebKit2

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_default_size(800, 600)
        self.connect('delete-event', Gtk.main_quit)

        # 创建 WebKit 控件
        self.webview = WebKit2.WebView()

        # 加载网页
        self.webview.load_uri('https://www.baidu.com')

        # 将 WebKit 控件添加到主窗口
        self.add(self.webview)

if __name__ == '__main__':
    window = MainWindow()
    window.show_all()
    Gtk.main()