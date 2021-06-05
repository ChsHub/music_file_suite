from wx import VERTICAL, TOP
from wx.lib.agw.hyperlink import HyperLinkCtrl
from wxwidgets import SimpleSizer


class TabAbout:
    def __init__(self, tab, border_size):
        with SimpleSizer(tab, VERTICAL) as sizer:
            text = HyperLinkCtrl(tab, label="https://www.youtube.com/", URL="https://www.youtube.com/")
            sizer.Add(text, flag=TOP, border=border_size)

            text = HyperLinkCtrl(tab, label="This software uses libraries from the FFmpeg project under the LGPLv2.1",
                                 URL="https://www.ffmpeg.org/")
            sizer.Add(text, flag=TOP, border=border_size)
