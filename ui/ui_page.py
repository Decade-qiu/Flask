# -*- coding: utf-8 -*-
import tornado.web


# 分页UI
class PageUI(tornado.web.UIModule):
    def render(self, data, q):
        return self.render_string("ui/page.html", data=data, q=q)
