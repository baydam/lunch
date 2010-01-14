#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Lunch
# Copyright (C) 2009 Société des arts technologiques (SAT)
# http://www.sat.qc.ca
# All rights reserved.
#
# This file is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Lunch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Lunch.  If not, see <http://www.gnu.org/licenses/>.

from twisted.internet import gtk2reactor
gtk2reactor.install() # has to be done before importing reactor
from twisted.internet import reactor
from twisted.internet import defer
import gtk
import sys
import os

class LunchApp(object):
    """
    Simple GTK2 GUI for Lunch Master.
    
    Defines the main window
    """
    def __init__(self, master=None):
        self.master = master
        # Window and framework
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Lunch")
        self.window.connect("destroy", self.destroy)

        # Box for multiple widgets
        self.box1 = gtk.VBox(False, 0)
        self.window.add(self.box1)

        # Buttons
        self.hboxes = {}
        self.title_labels = {}
        self.state_labels = {}
        self.start_buttons = {}
        
        self.commands = master.get_all_commands()
        for i in range(len(self.commands)):
            command = self.commands[i]
            self.hboxes[i] = gtk.HBox(False, 0)
            self.box1.pack_start(self.hboxes[i], True, True, 0)

            self.title_labels[i] = gtk.Label("%s" % (command.identifier))
            self.hboxes[i].pack_start(self.title_labels[i], True, True, 0)
            self.title_labels[i].set_width_chars(20)
            self.title_labels[i].show()

            self.state_labels[i] = gtk.Label("%s" % (command.state))
            self.hboxes[i].pack_start(self.state_labels[i], True, True, 0)
            self.state_labels[i].set_width_chars(20)
            self.state_labels[i].show()
            
            #self.start_buttons[i] = gtk.Button("Stop")
            #self.hboxes[i].pack_start(self.start_buttons[i], True, True, 0)
            #self.start_buttons[i].connect("clicked", self.on_start_clicked, i)
            #self.start_buttons[i].show()
            
            self.hboxes[i].show()

        #self.stopall_button = gtk.Button("Stop All")
        #self.stopall_button.connect("clicked", self.on_stopall_clicked)
        #self.box1.pack_start(self.stopall_button, True, True, 0)
        #self.stopall_button.show()

        self.quitbutton = gtk.Button("Quit")
        self.quitbutton.connect("clicked", self.destroy)
        self.box1.pack_start(self.quitbutton, True, True, 0)
        self.quitbutton.show()
        
        # Show the box
        self.box1.show()

        # Show the window
        self.window.show()

    def on_start_clicked(self, widget, info): # index as info
        #print "Button %s was pressed" % (info)
        print("Toggle start/stop %d" % (info))

    def on_stopall_clicked(self, widget): # index as info
        print("Stop All")

    def on_command_status_changed(self, command, new_state):
        """
        Called when the child_state_changed_signal of the command is triggered.
        @param command L{Command} 
        @param new_state str
        """
        for i in range(len(self.commands)):
            if command is self.commands[i]:
                txt = new_state
                self.state_labels[i].set_label(txt)
        print("Command %s changed its state to %s" % (command.identifier, new_state))

    def destroy(self, widget, data=None):
        """
        Destroy method causes appliaction to exit
        when main window closed
        """
        print("Destroying the window.")
        gtk.main_quit()
        print("reactor.stop()")
        reactor.stop()

    def main(self):
        """
        All PyGTK applications need a main method - event loop
        """
        gtk.main()

def start_gui(lunch_master):
    """
    Starts the GTK GUI
    :rettype: L{LunchApp}
    """
    app = LunchApp(lunch_master)
    #self.slave_state_changed_signal = sig.Signal()
    if hasattr(lunch_master, "child_state_changed_signal"):
        lunch_master.child_state_changed_signal.connect(app.on_command_status_changed)
    reactor.callLater(0, app.main)
    return app

if __name__ == "__main__":
    class Command(object):
        def __init__(self):
            self.state = "RUNNING"
            self.identifier = "/usr/bin/hello"
            
    class DummyMaster(object):
        def get_all_commands(self):
            """
            @rettype: list
            """
            data = []
            for i in range(10):
                data.append(Command())
            return data

    dummy_master = DummyMaster()
    start_gui(dummy_master)
    reactor.run()
