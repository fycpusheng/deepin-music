#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Hou Shaohui
# 
# Author:     Hou Shaohui <houshao55@gmail.com>
# Maintainer: Hou Shaohui <houshao55@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk
from collections import OrderedDict
from dtk.ui.new_treeview import TreeView
from dtk.ui.paned import HPaned

import utils
from widget.webcast_item import CategoryTreeItem
from widget.skin import app_theme
from widget.combo import TextPrompt
from widget.webcast_view import WebcastIconView, MultiDragWebcastView
from widget.ui_utils import draw_alpha_mask, switch_tab, set_widget_gravity
from webcast_library import WebcastDB, WebcastQuery
from widget.ui import BackButton
from helper import SignalContainer, Dispatcher
from nls import _


class WebcastsBrowser(gtk.VBox, SignalContainer):
    
    def __init__(self):
        gtk.VBox.__init__(self)
        SignalContainer.__init__(self)

        # Init categorys.
        self.get_categorys()
        
        # load data.
        self.__load_webcast_query()
        
        # Init webcastbar.
        self.__init_webcastbar()
        
        # Init iconview.
        self.metro_view = self.get_icon_view()
        self.metro_view_sw = self.metro_view.get_scrolled_window()
        
        self.page_box = gtk.VBox()
        self.page_box.add(self.metro_view_sw)
        
        
        # webcasts view
        self.webcast_view = self.get_webcast_view()
        self.webcast_view_sw = self.webcast_view.get_scrolled_window()
        
        # init listview page.
        self.init_listview_page()
        

        
        body_paned = HPaned(handle_color=app_theme.get_color("panedHandler"))
        body_paned.add1(self.webcastbar)
        body_paned.add2(self.page_box)
        self.add(body_paned)
        
        
    def get_categorys(self):    
        lang = utils.get_system_lang()
        if lang.startswith("zh"):
            self.__categorys = ["region", "genre", "composite"]
            self.current_category = "region"            
        else:    
            self.__categorys = ["region_en", "genre_en"]
            self.current_category = "region_en"            
            
        self.__category_gettexts = {
            "region" : _("Region"),
            "genre"  : _("Genre"),
            "region_en" : _("Region"),
            "genre_en"  : _("Genre"),
            "composite"  : _("Miscellaneous"),
            "finance" : _("财经"),
            "sports"  : _("体育"),
            "music"   : _("音乐"),
            "news"    : _("新闻"),
            "network" : _("网络"),
            }    
        
    def __load_webcast_query(self):    
        self.__db_query = WebcastQuery()        
        if WebcastDB.isloaded():
            self.__on_db_loaded()
        else:    
            WebcastDB.connect("loaded", lambda obj: self.__on_db_loaded())
            
    def __on_db_loaded(self):        
        self.autoconnect(self.__db_query, "added", self.__on_added_songs)
        self.autoconnect(self.__db_query, "removed", self.__on_removed_songs)
        self.autoconnect(self.__db_query, "update-songs", self.__on_update_songs)
        self.autoconnect(self.__db_query, "full-update", self.__on_full_update)
        self.__db_query.set_query()
        
    def __on_added_songs(self, db_query, songs):    
        self.reload_flag = True
    
    def __on_removed_songs(self, db_query, songs):
        self.reload_flag = True
    
    def __on_update_songs(self, db_query, songs):
        self.reload_flag = True
    
    def __on_full_update(self, db_query):
        self.load_view_data()
        
    def __init_webcastbar(self):    
        self.webcastbar = TreeView(enable_drag_drop=False, enable_multiple_select=False)
        self.webcastbar.connect("single-click-item", self.on_webcastbar_single_click_item)
        items = []
        for category in self.__categorys:
            items.append(CategoryTreeItem(self.__category_gettexts[category], category=category))
        self.webcastbar.add_items(items)
        self.webcastbar.select_items([self.webcastbar.visible_items[0]])
        self.webcastbar.set_size_request(121, -1)
        self.webcastbar.draw_mask = self.on_webcastbar_draw_mask        
        
    def on_webcastbar_draw_mask(self, cr, x, y, w, h):    
        draw_alpha_mask(cr, x, y, w, h ,"layoutRight")
        
    def on_webcastbar_single_click_item(self, widget, item, column, x, y):    
        widget = self.page_box.get_children()[0]
        if widget != self.metro_view_sw:
            switch_tab(self.page_box, self.metro_view_sw)            
        
        if self.current_category != item.category:
            self.current_category = item.category
            self.load_view_data()
        
    def init_listview_page(self):    
        self.listview_page = gtk.VBox()
        self.text_prompt = TextPrompt("Default")
        prompt_align = set_widget_gravity(self.text_prompt, 
                                          paddings=(10, 10, 0, 0))
        prompt_box = gtk.HBox()
        back_button = BackButton()
        back_button.connect("clicked", self.on_backbutton_clicked)
        back_button_align = set_widget_gravity(back_button, gravity=(0.5, 0.5, 0, 0),
                                               paddings=(0, 0, 10, 5))
        prompt_box.pack_start(back_button_align, False, True)
        prompt_box.pack_start(prompt_align, False, False)
        
        self.listview_page.pack_start(prompt_box, False, True)
        self.listview_page.pack_start(self.webcast_view_sw, True, True)
        
    def on_backbutton_clicked(self, widget):    
        switch_tab(self.page_box, self.metro_view_sw)
        
    def switch_to_listview(self, category, title):    
        self.text_prompt.set_text(title)
        self.webcast_view.clear()
        
        songs = self.__db_query.get_songs(category, title)
        self.webcast_view.add_webcasts(songs)
        switch_tab(self.page_box, self.listview_page)
        
        
    def load_view_data(self):    
        self.metro_view.clear()                    
        if self.current_category == "composite":
            child_datas = self.__db_query.get_composite_categorys()
            gettext_datas = []
            for child in child_datas:
                gettext_datas.append((self.__category_gettexts[child], child))
            self.metro_view.add_composite_items(gettext_datas)    
                
        else:    
            child_datas = self.__db_query.get_info(self.current_category)[0]
            self.metro_view.add_webcast_items(child_datas)            

        
    def get_icon_view(self):
        icon_view = WebcastIconView()
        icon_view.connect("single-click-item", self.on_iconview_single_click_item)
        icon_view.connect("double-click-item", self.on_iconview_single_click_item)
        return icon_view
    
    
    def on_iconview_single_click_item(self, widget, item, x, y):
        if item.is_composited:
            category = item.category
        else:    
            category = self.current_category
            
        title = item.title
        if item.is_composited:
            self.switch_to_listview(category, title)
        else:    
            self.switch_to_listview(category, title)
        
    def get_webcast_view(self):    
        webcast_view = MultiDragWebcastView()
        webcast_view.keymap.update({"BackSpace" : lambda : self.on_backbutton_clicked(None)})        
        return webcast_view

        
    def save(self):
        pass
