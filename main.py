#!/usr/bin/env python3

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, Gio, GLib, Pango
import psutil
from funct.convert import *
from funct.info import *
from widget import *

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # CSS Import
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_file(Gio.File.new_for_path('style.css'))
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # CPU
        self.label_cpu_1 = Gtk.Label(label="CPU", halign=Gtk.Align.START)
        self.cpu_progress = Gtk.DrawingArea(halign=Gtk.Align.CENTER, content_width=125, content_height=125)
        self.cpu_progress.set_draw_func(circular_progress_bar, psutil.cpu_percent())
        self.label_cpu_2 = Gtk.Label(name="text_secondary", label="Frequency", halign=Gtk.Align.START)
        self.label_cpu_3 = Gtk.Label(name="text_secondary", label="Cores", halign=Gtk.Align.START)
        self.label_cpu_4 = Gtk.Label(name="text_secondary", label="Threads", halign=Gtk.Align.START)
        self.label_cpu_5 = Gtk.Label(label=convert_frequency(psutil.cpu_freq().current), halign=Gtk.Align.END, ellipsize=Pango.EllipsizeMode.END)
        self.label_cpu_6 = Gtk.Label(label=psutil.cpu_count(logical=False), halign=Gtk.Align.END, ellipsize=Pango.EllipsizeMode.END)
        self.label_cpu_7 = Gtk.Label(label=psutil.cpu_count(), halign=Gtk.Align.END)
        self.grid_cpu = Gtk.Grid(column_spacing=25, column_homogeneous=True, row_spacing=10)
        self.grid_cpu.attach(self.label_cpu_2, 0, 0, 1, 1)
        self.grid_cpu.attach(self.label_cpu_3, 0, 1, 1, 1)
        self.grid_cpu.attach(self.label_cpu_4, 0, 2, 1, 1)
        self.grid_cpu.attach(self.label_cpu_5, 1, 0, 1, 1)
        self.grid_cpu.attach(self.label_cpu_6, 1, 1, 1, 1)
        self.grid_cpu.attach(self.label_cpu_7, 1, 2, 1, 1)
        self.box_cpu = Gtk.Box(name="box", orientation=Gtk.Orientation.VERTICAL, spacing=25)
        self.box_cpu.append(self.label_cpu_1)
        self.box_cpu.append(self.cpu_progress)
        self.box_cpu.append(self.grid_cpu)

        self.box_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=25)
        self.box_1.append(self.box_cpu)

        # Memory
        self.label_memory_1 = Gtk.Label(label="Memory", halign=Gtk.Align.START)
        self.memory_progress = Gtk.DrawingArea(halign=Gtk.Align.CENTER, content_width=125, content_height=125)
        self.memory_progress.set_draw_func(circular_progress_bar, psutil.virtual_memory().percent)
        self.label_memory_2 = Gtk.Label(name="text_secondary", label="Available", halign=Gtk.Align.START)
        self.label_memory_3 = Gtk.Label(name="text_secondary", label="Total", halign=Gtk.Align.START)
        self.label_memory_4 = Gtk.Label(label=convert_bytes(psutil.virtual_memory().available), halign=Gtk.Align.END)
        self.label_memory_5 = Gtk.Label(label=convert_bytes(psutil.virtual_memory().total), halign=Gtk.Align.END)
        self.grid_memory = Gtk.Grid(column_spacing=25, column_homogeneous=True, row_spacing=10)
        self.grid_memory.attach(self.label_memory_2, 0, 0, 1, 1)
        self.grid_memory.attach(self.label_memory_3, 0, 1, 1, 1)
        self.grid_memory.attach(self.label_memory_4, 1, 0, 1, 1)
        self.grid_memory.attach(self.label_memory_5, 1, 1, 1, 1)
        self.box_memory = Gtk.Box(name="box", orientation=Gtk.Orientation.VERTICAL, spacing=25)
        self.box_memory.append(self.label_memory_1)
        self.box_memory.append(self.memory_progress)
        self.box_memory.append(self.grid_memory)

        # Swap
        self.label_swap_1 = Gtk.Label(label="Swap", halign=Gtk.Align.START)
        self.swap_progress = Gtk.DrawingArea(halign=Gtk.Align.CENTER, content_width=80, content_height=80)
        self.swap_progress.set_draw_func(circular_progress_bar, psutil.swap_memory().percent)
        self.label_swap_2 = Gtk.Label(name="text_secondary", label="Used", halign=Gtk.Align.START)
        self.label_swap_3 = Gtk.Label(name="text_secondary", label="Total", halign=Gtk.Align.START)
        self.label_swap_4 = Gtk.Label(label=convert_bytes(psutil.swap_memory().used), halign=Gtk.Align.END, hexpand=True)
        self.label_swap_5 = Gtk.Label(label=convert_bytes(psutil.swap_memory().total), halign=Gtk.Align.END, hexpand=True)
        self.grid_swap = Gtk.Grid(column_spacing=25, row_spacing=10)
        self.grid_swap.attach(self.swap_progress, 0, 0, 1, 4)
        self.grid_swap.attach(self.label_swap_2, 1, 0, 1, 1)
        self.grid_swap.attach(self.label_swap_3, 1, 1, 1, 1)
        self.grid_swap.attach(self.label_swap_4, 2, 0, 1, 1)
        self.grid_swap.attach(self.label_swap_5, 2, 1, 1, 1)
        self.box_swap = Gtk.Box(name="box", orientation=Gtk.Orientation.VERTICAL, spacing=25)
        self.box_swap.append(self.label_swap_1)
        self.box_swap.append(self.grid_swap)

        self.box_2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=25)
        self.box_2.append(self.box_memory)
        self.box_2.append(self.box_swap)

        # Disk
        self.label_disk_1 = Gtk.Label(label="Disk", halign=Gtk.Align.START)
        self.viewport = Gtk.Viewport(margin_start=10, margin_end=10)
        self.viewport.set_child(self.disk_ui())
        self.scroll = Gtk.ScrolledWindow(propagate_natural_width=True, propagate_natural_height=True, max_content_height=350)
        self.scroll.set_child(self.viewport)
        self.box_disk = Gtk.Box(name="box", orientation=Gtk.Orientation.VERTICAL, spacing=25)
        self.box_disk.append(self.label_disk_1)
        self.box_disk.append(self.scroll)

        self.box_3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=25)
        self.box_3.append(self.box_disk)
        
        # Network
        self.label_network_1 = Gtk.Label(label="Network", halign=Gtk.Align.START)
        self.label_network_2 = Gtk.Picture.new_for_filename("icons/download.svg")
        self.label_network_2.set_can_shrink(False)
        self.label_network_3 = Gtk.Picture.new_for_filename("icons/upload.svg")
        self.label_network_3.set_can_shrink(False)
        self.label_network_4 = Gtk.Label(label="0 bytes/s", halign=Gtk.Align.START, ellipsize=Pango.EllipsizeMode.END)
        self.label_network_5 = Gtk.Label(name="text_secondary", label=convert_bytes(psutil.net_io_counters().bytes_recv), halign=Gtk.Align.START)
        self.label_network_6 = Gtk.Label(label="0 bytes/s", halign=Gtk.Align.START, ellipsize=Pango.EllipsizeMode.END)
        self.label_network_7 = Gtk.Label(name="text_secondary", label=convert_bytes(psutil.net_io_counters().bytes_sent), halign=Gtk.Align.START)
        self.label_network_8 = Gtk.Label(label="")
        self.grid_network = Gtk.Grid(column_spacing=25, row_spacing=10)
        self.grid_network.attach(self.label_network_2, 0, 0, 1, 2)
        self.grid_network.attach(self.label_network_3, 0, 3, 1, 2)
        self.grid_network.attach(self.label_network_4, 1, 0, 1, 1)
        self.grid_network.attach(self.label_network_5, 1, 1, 1, 1)
        self.grid_network.attach(self.label_network_6, 1, 3, 1, 1)
        self.grid_network.attach(self.label_network_7, 1, 4, 1, 1)
        self.grid_network.attach(self.label_network_8, 1, 2, 1, 1)
        self.box_network = Gtk.Box(name="box", orientation=Gtk.Orientation.VERTICAL, spacing=25)
        self.box_network.append(self.label_network_1)
        self.box_network.append(self.grid_network)
        global bytes_recv_old
        global bytes_sent_old
        bytes_recv_old = psutil.net_io_counters().bytes_recv
        bytes_sent_old = psutil.net_io_counters().bytes_sent

        self.box_4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=25)
        self.box_4.append(self.box_network)

        # Battery
        if psutil.sensors_battery() != None:
            self.label_battery_1 = Gtk.Label(label="Battery", halign=Gtk.Align.START)
            self.label_battery_2 = Gtk.Label(label=str(int(psutil.sensors_battery().percent))+"%", halign=Gtk.Align.START)
            self.battery_progress = Gtk.DrawingArea(hexpand=True, content_height=5)
            self.battery_progress.set_draw_func(progress_bar, int(psutil.sensors_battery().percent), True)
            self.label_battery_4 = Gtk.Label(name="text_secondary", label="", halign=Gtk.Align.END)
            if psutil.sensors_battery().percent == 100:
                self.label_battery_4.set_label("Full")

            elif psutil.sensors_battery().power_plugged == False:
                self.label_battery_4.set_label("Discharging")

            elif psutil.sensors_battery().power_plugged == True:
                self.label_battery_4.set_label("Charging")

            self.box_battery_2 = Gtk.Box(homogeneous=True, spacing=25)
            self.box_battery_2.append(self.label_battery_2)
            self.box_battery_2.append(self.label_battery_4)
            self.box_battery_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            self.box_battery_1.append(self.box_battery_2)
            self.box_battery_1.append(self.battery_progress)
            if psutil.sensors_battery().power_plugged == False:
                self.label_battery_3 = Gtk.Label(name="text_secondary", label=convert_seconds(psutil.sensors_battery().secsleft)+" Remaining", halign=Gtk.Align.START, ellipsize=Pango.EllipsizeMode.MIDDLE)
                self.box_battery_1.append(self.label_battery_3)

            elif psutil.sensors_battery().power_plugged == True:
                self.label_battery_3 = Gtk.Label(name="text_secondary", label="AC power is connected", halign=Gtk.Align.START, ellipsize=Pango.EllipsizeMode.MIDDLE)
                self.box_battery_1.append(self.label_battery_3)

            self.box_battery = Gtk.Box(name="box", orientation=Gtk.Orientation.VERTICAL, spacing=25)
            self.box_battery.append(self.label_battery_1)
            self.box_battery.append(self.box_battery_1)
            self.box_4.append(self.box_battery)

        # Info
        self.label_1 = Gtk.Label(name="text_secondary", label="Hostname", halign=Gtk.Align.START)
        self.label_2 = Gtk.Label(name="text_secondary", label="Uptime", halign=Gtk.Align.START)
        self.label_3 = Gtk.Label(name="text_secondary", label="Hardware Model", halign=Gtk.Align.START)
        self.label_4 = Gtk.Label(name="text_secondary", label="OS", halign=Gtk.Align.START)
        self.label_5 = Gtk.Label(name="text_secondary", label="Kernel", halign=Gtk.Align.START)
        self.label_6 = Gtk.Label(name="text_secondary", label="Machine", halign=Gtk.Align.START)
        self.label_7 = Gtk.Label(name="text_secondary", label="Processor", halign=Gtk.Align.START)
        self.label_8 = Gtk.Label(name="text_secondary", label="Memory", halign=Gtk.Align.START)
        self.label_9 = Gtk.Label(name="text_secondary", label="Disk Capacity", halign=Gtk.Align.START)
        self.label_10 = Gtk.Label(label=hostname(), halign=Gtk.Align.END, ellipsize=Pango.EllipsizeMode.END, hexpand=True)
        self.label_11 = Gtk.Label(label=convert_seconds(uptime()), halign=Gtk.Align.END, ellipsize=Pango.EllipsizeMode.END, hexpand=True)
        self.label_12 = Gtk.Label(label=hardware_model(), halign=Gtk.Align.END, ellipsize=Pango.EllipsizeMode.END, hexpand=True)
        self.label_13 = Gtk.Label(label=os(), halign=Gtk.Align.END, ellipsize=Pango.EllipsizeMode.END, hexpand=True)
        self.label_14 = Gtk.Label(label=kernel(), halign=Gtk.Align.END, ellipsize=Pango.EllipsizeMode.END, hexpand=True)
        self.label_15 = Gtk.Label(label=machines(), halign=Gtk.Align.END, ellipsize=Pango.EllipsizeMode.END, hexpand=True)
        self.label_16 = Gtk.Label(label=cpu_name(), halign=Gtk.Align.END, ellipsize=Pango.EllipsizeMode.END, hexpand=True)
        self.label_17 = Gtk.Label(label=convert_bytes(psutil.virtual_memory().total), halign=Gtk.Align.END, ellipsize=Pango.EllipsizeMode.END, hexpand=True)
        self.label_18 = Gtk.Label(label="2 TB", halign=Gtk.Align.END, ellipsize=Pango.EllipsizeMode.END, hexpand=True)
        self.grid_1 = Gtk.Grid(name="box", column_spacing=25, row_spacing=10)
        self.grid_1.attach(self.label_1, 0, 0, 1, 1)
        self.grid_1.attach(self.label_2, 0, 1, 1, 1)
        self.grid_1.attach(self.label_3, 0, 2, 1, 1)
        self.grid_1.attach(self.label_4, 2, 0, 1, 1)
        self.grid_1.attach(self.label_5, 2, 1, 1, 1)
        self.grid_1.attach(self.label_6, 2, 2, 1, 1)
        self.grid_1.attach(self.label_7, 4, 0, 1, 1)
        self.grid_1.attach(self.label_8, 4, 1, 1, 1)
        self.grid_1.attach(self.label_9, 4, 2, 1, 1)
        self.grid_1.attach(self.label_10, 1, 0, 1, 1)
        self.grid_1.attach(self.label_11, 1, 1, 1, 1)
        self.grid_1.attach(self.label_12, 1, 2, 1, 1)
        self.grid_1.attach(self.label_13, 3, 0, 1, 1)
        self.grid_1.attach(self.label_14, 3, 1, 1, 1)
        self.grid_1.attach(self.label_15, 3, 2, 1, 1)
        self.grid_1.attach(self.label_16, 5, 0, 1, 1)
        self.grid_1.attach(self.label_17, 5, 1, 1, 1)
        self.grid_1.attach(self.label_18, 5, 2, 1, 1)

        # Welcome
        self.label_welcome = Gtk.Label(name="text_welcome",
            label=("Welcome " + username()),
            halign=Gtk.Align.START)

        self.dashboard = Gtk.Grid(
            column_homogeneous=True,
            column_spacing=25,
            row_spacing=25,
            margin_start=40,
            margin_end=40,
            margin_top=40,
            margin_bottom=40,
            halign=Gtk.Align.CENTER)
        self.dashboard.attach(self.label_welcome, 0, 0, 4, 1)
        self.dashboard.attach(self.grid_1, 0, 1, 4, 1)
        self.dashboard.attach(self.box_1, 0, 2, 1, 1)
        self.dashboard.attach(self.box_2, 1, 2, 1, 1)
        self.dashboard.attach(self.box_3, 2, 2, 1, 1)
        self.dashboard.attach(self.box_4, 3, 2, 1, 1)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.add_titled(self.dashboard, "dashboard", "Dashboard")
        self.stack_switcher = Gtk.StackSwitcher()
        self.stack_switcher.set_stack(self.stack)

        self.header = Gtk.HeaderBar()
        self.header.props.title_widget=self.stack_switcher

        self.props.title="Sys Monitor"
        self.props.default_width=1280
        self.props.default_height=800
        self.set_titlebar(self.header)
        self.set_child(self.stack)

        self.timer()

    def disk_ui(self):
        self.box_disk_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=25)

        for part in psutil.disk_partitions():
            percent = psutil.disk_usage(part.mountpoint).percent
            use = convert_bytes(psutil.disk_usage(part.mountpoint).used) + " / " + convert_bytes(psutil.disk_usage(part.mountpoint).total) + " used"
            self.label_disk_2 = Gtk.Label(label=part.mountpoint, halign=Gtk.Align.START, ellipsize=Pango.EllipsizeMode.MIDDLE)
            self.label_disk_3 = Gtk.Label(name="text_secondary", label=use, halign=Gtk.Align.START, ellipsize=Pango.EllipsizeMode.MIDDLE)
            self.disk_progress = Gtk.DrawingArea(hexpand=True, content_height=5)
            self.disk_progress.set_draw_func(progress_bar, percent)
            self.box_disk_2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            self.box_disk_2.append(self.label_disk_2)
            self.box_disk_2.append(self.disk_progress)
            self.box_disk_2.append(self.label_disk_3)
            self.box_disk_1.append(self.box_disk_2)

            if part.mountpoint.startswith("/run/media/") == True:
                self.label_disk_2.set_label(part.mountpoint.split("/")[-1])

        return self.box_disk_1

    def realtime(self):
        self.label_11.set_label(convert_seconds(uptime()))

        self.label_cpu_5.set_label(convert_frequency(psutil.cpu_freq().current))
        self.cpu_progress.set_draw_func(circular_progress_bar, psutil.cpu_percent())

        self.label_memory_4.set_label(convert_bytes(psutil.virtual_memory().available))
        self.memory_progress.set_draw_func(circular_progress_bar, psutil.virtual_memory().percent)

        self.label_swap_4.set_label(convert_bytes(psutil.swap_memory().used))
        self.swap_progress.set_draw_func(circular_progress_bar, psutil.swap_memory().percent)
 
        self.viewport.set_child(self.disk_ui())

        if psutil.sensors_battery() != None:
            self.label_battery_2.set_label(str(int(psutil.sensors_battery().percent))+"%")
            self.battery_progress.set_draw_func(progress_bar, int(psutil.sensors_battery().percent), True)

            if psutil.sensors_battery().power_plugged == False:
                self.label_battery_3.set_label(convert_seconds(psutil.sensors_battery().secsleft)+" Remaining")

            elif psutil.sensors_battery().power_plugged == True:
                self.label_battery_3.set_label("AC power is connected")

            if psutil.sensors_battery().percent == 100:
                self.label_battery_4.set_label("Full")

            elif psutil.sensors_battery().power_plugged == False:
                self.label_battery_4.set_label("Discharging")

            elif psutil.sensors_battery().power_plugged == True:
                self.label_battery_4.set_label("Charging")

        global bytes_recv_old
        global bytes_sent_old
        bytes_recv = psutil.net_io_counters().bytes_recv
        bytes_sent = psutil.net_io_counters().bytes_sent
        self.label_network_4.set_label(convert_bytes(bytes_recv-bytes_recv_old)+"/s")
        self.label_network_5.set_label(convert_bytes(bytes_recv))
        self.label_network_6.set_label(convert_bytes(bytes_sent-bytes_sent_old)+"/s")
        self.label_network_7.set_label(convert_bytes(bytes_sent))
        bytes_recv_old =  bytes_recv
        bytes_sent_old =  bytes_sent
        
        return True

    def timer(self):
        GLib.timeout_add(1000, self.realtime)

class MyApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = MyApp(application_id='org.gtk.SysMonitor')
app.run(None)