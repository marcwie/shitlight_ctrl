from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import time
import urwid

import random

try:
    import shytlight
except ImportError:
    import shytlight_simulator as shytlight

import shitlight_patterns



class CheckButton(urwid.CheckBox):
  """ CheckButton combines CheckBox with Button behaviour"""
  signals = ["change","click"]
  def __init__(self,*args,**kwargs):
    super(CheckButton,self).__init__(*args,**kwargs)

  def keypress(self, size, key):
    if key == " ":
      self.toggle_state()
    elif self._command_map[key] != urwid.ACTIVATE:
      return key
    else:
      self._emit('click')

  def mouse_event(self, size, event, button, x, y, focus):
    if not urwid.util.is_mouse_press(event):
      return False

    if button == 1:
      self._emit('click')

    if button == 2:
      self.toggle_state()
    return True



class CtrlView(urwid.WidgetPlaceholder):
    logo1 = '''          ___           ___                              
          /  /\         /__/\        ___           ___    
         /  /:/_        \  \:\      /  /\         /  /\   
        /  /:/ /\        \__\:\    /  /:/        /  /:/   
       /  /:/ /::\   ___ /  /::\  /__/::\       /  /:/    
      /__/:/ /:/\:\ /__/\  /:/\:\ \__\/\:\__   /  /::\    
      \  \:\/:/~/:/ \  \:\/:/__\/    \  \:\/\ /__/:/\:\   
       \  \::/ /:/   \  \::/          \__\::/ \__\/  \:\  
        \__\/ /:/     \  \:\          /__/:/       \  \:\\ 
          /__/:/       \  \:\         \__\/         \__\/ 
          \__\/         \__\/                             '''
     

    logo2 = '''                                                 ___     
                                                 /\__\    
                      ___           ___         /:/ _/_   
                     /\__\         /\__\       /:/ /\__\  
      ___     ___   /:/__/        /:/  /      /:/ /:/ _/_ 
     /\  \   /\__\ /::\  \       /:/__/      /:/_/:/ /\__\\
     \:\  \ /:/  / \/\:\  \__   /::\  \      \:\/:/ /:/  /
      \:\  /:/  /   ~~\:\/\__\ /:/\:\  \      \::/_/:/  / 
       \:\/:/  /       \::/  / \/__\:\  \      \:\/:/  /  
        \::/  /        /:/  /       \:\__\      \::/  /   
         \/__/         \/__/         \/__/       \/__/    
                                                      '''


    def __init__(self, controller):
        self.controller = controller
        self.splash = True
        self.start_time = None
        self.offset = 0
        self.palette = [
            ('banner', '', '', '', '#ffa', '#60d'),
            ('streak', '', '', '', 'g50', '#60a'),
            ('inside', '', '', '', 'g38', '#808'),
            ('outside', '', '', '', 'g27', '#a06'),
            ('bg', '', '', '', 'g7', '#d06'),
            ('button normal','light gray', 'black', 'standout'),
            ('button select','white',      'dark gray'),
            ('button active', 'yellow', 'black', 'standout'),
            ('pg normal',    'white',      'black', 'standout'),
            ('pg complete',  'white',      'dark magenta'),
            ('pg smooth', 'dark magenta','black'),
            ('input normal', 'light gray', 'dark gray'),
            ('input select', 'white', 'dark gray'),
            ('menu_button','light gray', 'black', 'standout'),
            ('menu_button_focus','white',      'dark gray')]





        
        
        self.max_box_levels = 4
        self.box_level = 0
        urwid.WidgetPlaceholder.__init__(self, self.splash_window())


    def splash_window(self):
        w = urwid.SolidFill()
        w = urwid.AttrMap(w, 'bg')
        w.original_widget = urwid.Filler(urwid.Pile([]))
        ## splash screen
        div = urwid.Divider()
        outside = urwid.AttrMap(div, 'outside')
        inside = urwid.AttrMap(div, 'inside')
        txt = urwid.Text(('banner', self.logo1+'\n'+ self.logo2), align='center')
        credits = urwid.Text(('banner', 'v2.0 (2017)'), align='center')
        streak = urwid.AttrMap(txt, 'streak')
        txt2 = urwid.Text(('bg', 'press any key, kumpel'), align='center')
        pile = w.base_widget # .base_widget skips the decorations
        for item in [outside, inside, streak, credits, inside, outside, txt2]:
            pile.contents.append((item, pile.options()))
        return w

    def overlay_logic(self, fg, bg, level, height=20):
        return urwid.Overlay(fg,
            bg,
            align='center', width=('relative', 60),
            valign='middle', height=height,
            left=level * 3,
            right=(self.max_box_levels - level - 1) * 3,
            top=level * 2,
            bottom=(self.max_box_levels - level - 1) * 2)

    def main_window(self):
        self.splash = False
        self.main_content = self.main_menu()
        self.bg = urwid.WidgetPlaceholder(urwid.SolidFill(u'S'))
        self.main = self.overlay_logic(urwid.LineBox(self.main_content),self.bg, self.box_level)
        self.box_level += 1

        return self.main

    def open_box(self, box, height=40):
        self.original_widget = self.overlay_logic(urwid.LineBox(box),self.original_widget,self.box_level, height)
        self.box_level += 1

    def go_back(self):
        if self.box_level > 1:
            self.original_widget = self.original_widget.contents[0][0]
            self.box_level -= 1
#        elif self.box_level == 1:
#            self.box_level = 0
#            self.original_widget = self.main_window()


    def main_menu(self):
        pattern = self.controller.get_current_pattern()
        # header element:
        widget_header = [urwid.Text("SHITLIGHT CONTROLL",align="center"), urwid.Divider(u"\u2015",0,1)]
        # current Pattern:
        if pattern is None:
            current = "(None)"
        elif hasattr(pattern,name):
            current = pattern.name
        else:
            current = type(pattern).__name__
        self.w_current_pattern = urwid.Text("Current Pattern: " + current)
        self.w_current_palette = urwid.Text("Current Palette: (free)")
        widget_current = [self.w_current_pattern, self.w_current_palette , urwid.Divider(u"\u2015",1,1)]
        # beatdetection
        self.beat_detection_menu_content = self.beat_detection_menu()
        widget_beatdetection = [self.sub_menu("Beat Detection",self.beat_detection_menu_content)]
        # pattern selection
        self.pattern_selection_menu_content = self.pattern_menu()
        widget_patternselect = [self.sub_menu("Select Pattern",self.pattern_selection_menu_content)]
        # palette selection
        self.palette_selection_menu_content = self.palette_menu()
        widget_paletteselect = [self.sub_menu("Select Palete",self.palette_selection_menu_content)]

        self.quit_button = urwid.Button("Quit")
        urwid.connect_signal(self.quit_button, 'click', self.on_quit)
        footer = [urwid.Divider(u"\u2015",5,0), urwid.Padding(self.quit_button,align="center",width=8)]
        L = widget_header+widget_current+widget_beatdetection+widget_patternselect+widget_paletteselect + footer
        # add all
        return urwid.ListBox(urwid.SimpleFocusListWalker(L))

    def sub_menu(self,caption, content,menu_caption=None):
        if menu_caption is None:
            menu_caption=caption
        contents, height = self.menu(menu_caption, content)
        def open_menu(button):
            return self.open_box(contents,height)
        return self.menu_button([caption, u'...'], open_menu)


    def menu_button(self,caption, callback):
        button = urwid.Button(caption)
        urwid.connect_signal(button, 'click', callback)
        return urwid.AttrMap(button, 'menu_button', 'menu_button_focus')        

    def menu(self,title, content):
        body = [urwid.Text(title,align="center"), urwid.Divider(u"\u2015")]
        body.extend(content)
        height = len(content) + 2 + 2 +2 # content + border, header, footer
        def close_menu(button):
            return self.go_back()
        back = urwid.Button("back")
        urwid.connect_signal(back, 'click', close_menu)
        body.extend([urwid.Divider(u"\u2015"),
            urwid.Padding(urwid.AttrWrap(back, 'menu_button', 'menu_button_focus'),align="center",width=8)])
        return urwid.ListBox(urwid.SimpleListWalker(body)), height

    def div(self):
        return urwid.Divider(u"\u2015")

    def radio_button(self, g, l, fn):
        w = urwid.RadioButton(g, l, "first True", on_state_change=fn)
        w = urwid.AttrWrap(w, 'button normal', 'button select')
        return w

    def on_mode_button(self, button, state):
        if state:
            self.controller.set_beatsync(self.beatmode_names.index(button.get_label()))

    def on_bpmmode_button(self, button, state):
        if state:
            self.controller.set_bpmfix(self.bpmmode_names.index(button.get_label()))

    def on_fix_bpm(self, w, new_value):
        self.controller.set_fix_bpm_value(int(new_value))

    def beat_detection_menu(self):
        self.beatmode_names = ["No Detection", "Detect BPM", "Detect Beats"]
        self.bpmmode_names = ["Use detected BPM", "Fix detection to BPM", "Use fixed BPM"]
        # Declare Widgets
        self.w_beatdetection_state = urwid.Text("Status: (unknown)")
        self.w_beatdetection_bpm = urwid.Text("BPM: 120")
        #self.w_beatdetection_fix = self.sub_menu("Fix BPM", [urwid.Text("Coming Soon")])
        self.w_beatdetection_vu_meter = urwid.ProgressBar("pg normal", "pg complete", 0, 100, None)
        self.w_beatdetection_modes = []
        group = []
        for m in self.beatmode_names:
            rb = self.radio_button( group, m, self.on_mode_button )
            self.w_beatdetection_modes.append( rb )
        self.w_bpm_modes = []
        ngroup = []
        for m in self.bpmmode_names:
            rb = self.radio_button( ngroup, m, self.on_bpmmode_button )
            self.w_bpm_modes.append( rb )

        self.w_beatdetection_fix = urwid.IntEdit(('',"Fixed BPM: "),default=120)
        fix_widget = [urwid.AttrMap(self.w_beatdetection_fix, 'input normal', 'input select')]
        urwid.connect_signal(self.w_beatdetection_fix, 'change', self.on_fix_bpm)


        return [urwid.Divider(),
                self.w_beatdetection_state, 
                urwid.Divider(),
                self.div(),
                self.w_beatdetection_bpm,
                urwid.GridFlow([urwid.Text("Volume:"), self.w_beatdetection_vu_meter],15,2,0,"left"),
                self.div(),
                urwid.Text("Select Detection Mode:", align="center")] + self.w_beatdetection_modes + [self.div(), urwid.Text("Select BPM Mode (not Implemented):", align="center")] + self.w_bpm_modes + fix_widget
                
        
        
    def palette_menu(self):
        return [urwid.Text("See you 2018, Kumpel")]

    def on_pattern_mode_button(self, button, state):
        if state:
            self.controller.set_pattern_mode(self.pattern_mode_names.index(button.get_label()))

    def on_pattern_timer(self, w, new_value):
        self.controller.set_timer(int(new_value))

    def on_select_pattern(self, button, cl):
        self.controller.select_pattern(cl)
        self.update()

    def on_toggle_pattern(self, button, state, cl):
        self.controller.toggle_pattern(cl, state)
        self.update()

    def pattern_menu(self):
        group = []
        self.pattern_mode_names = ["Loop Single Pattern", "Select Random Pattern"]
        self.w_pattern_mode_menu = []
        for m in self.pattern_mode_names:
            rb = self.radio_button( group, m, self.on_pattern_mode_button )
            self.w_pattern_mode_menu.append( rb )
        self.pattern_timer_widget = urwid.IntEdit(('',"Pattern Timer [s]: "),default=60)
        timer_widget = urwid.AttrMap(self.pattern_timer_widget, 'input normal', 'input select')
        urwid.connect_signal(self.pattern_timer_widget, 'change', self.on_pattern_timer)
        explain = urwid.Text("ENTER: change pattern, SPACE: (un)select", align="center")
        self.pattern_selection = []
        for c, v in self.controller.get_patterns():
            button = CheckButton(c[0],v,False, self.on_toggle_pattern, c[1])
            urwid.connect_signal(button, 'click', self.on_select_pattern, c[1])
            self.pattern_selection.append(urwid.AttrMap(button, 'button normal', 'button select'))
        return  [urwid.Text("Select Play Mode:", align="center")] + self.w_pattern_mode_menu + [timer_widget, self.div(), explain, self.div()] + self.pattern_selection

    def update_pattern_menu(self):
        for d, w in zip(self.controller.get_patterns(), self.pattern_selection):
            at_map = ({'button normal':'button active'} if d[1] else {'button active':'button normal'})
            w.set_attr_map(at_map)


    def update_beatdetection_menu(self):
        self.w_beatdetection_state.set_text("Status: %s" % self.controller.get_analysis_state())
        self.w_beatdetection_bpm.set_text("BPM: %.1f" % self.controller.get_bpm())
        vol = self.controller.get_volume()
        if vol < 1: vol=1
        if vol > 100: vol=100
        self.w_beatdetection_vu_meter.set_completion(vol)



    def keypress(self, size, key):
        if key in ('q', 'Q'):
            self.controller.quit()
        elif key == 'esc' and self.box_level > 1:
            self.go_back()          
        elif key[0] != 'mouse press' and self.splash == True:
            self.original_widget = self.main_window()
        else:
            return super(CtrlView, self).keypress(size, key)

    def update(self):
        self.w_current_pattern.set_text("Current Pattern: " + self.controller.get_pattern_name(self.controller.get_current_pattern()))
        self.update_pattern_menu()
        self.update_beatdetection_menu()


    def on_quit(self, button):
        self.controller.quit()
    





class CtrlController:
    def __init__(self):
        self.view = CtrlView( self )
        # use the first mode as the default
        #mode = self.get_modes()[0]
        #self.model.set_mode( mode )
        # update the view
        #self.view.on_mode_change( mode )
        #self.view.update_graph(True)           
        shytlight.init_shitlight()
        shytlight.init_analysis(b"default")


        self.patterns = shitlight_patterns.patterns
        self.pattern = None
        self.patterns_selection = []

        self.pattern_alarm = None
        self.pattern_timer = 60

        self.fixed_bpm = 120.0
        self.bpm_mode = 0



    def main(self):
        self.loop = urwid.MainLoop(self.view, self.view.palette, unhandled_input=exit_on_q)
        self.loop.screen.set_terminal_properties(colors=256)
        self.loop.set_alarm_in(1,self.animate_splash)
        self.loop.run()
        

    def animate_splash(self, loop=None, user_data=None):
        if self.view.splash:
            self.loop.set_alarm_in(1,self.animate_splash)
        else:
            self.animate()

    def animate(self, loop=None, user_data=None):
        self.view.update()
        self.loop.set_alarm_in(.1,self.animate)

    def handle_keys(self, key):
        if key in ('q', 'Q'):
            self.quit()
        elif key == 'esc' and self.view.box_level > 1:
            self.view.go_back()          
        elif key[0] != 'mouse press' and self.view.splash == True:
            self.view.original_widget = self.view.main_window()
    
    def get_volume(self):
        return int(shytlight.get_volume())

    def get_bpm(self):
        return shytlight.get_bpm()

    def get_analysis_state(self):
        state = shytlight.get_analysis_state()
        if state < 0:
            return "Analysis Stopped"
        if state == 0:
            return "Fixed BPM Mode"
        if state > 0 and state <= 10:
            return "Detect BPM Mode"
        if state > 10:
            return "Detect Beats mode"

    def set_bpmfix(self,val=0):
        pass 

    def set_fix_bpm_value(self,value=120):
        self.fixed_bpm = float(value)

    def set_beatsync(self,val=0):
        enable_int = val*10
        shytlight.beat_sync(enable_int)

    def set_timer(self, value):
        self.pattern_timer = value
        if self.pattern_alarm:
          self.update_pattern_alarm()

    def set_pattern_mode(self, mode):
        if mode == 0:
          self.loop.remove_alarm(self.pattern_alarm)
          self.pattern_alarm = None
        if mode == 1:
          self.update_pattern_alarm()

    def update_pattern_alarm(self):
        if self.pattern_alarm:
          self.loop.remove_alarm(self.pattern_alarm)
        self.pattern_alarm = self.loop.set_alarm_in(self.pattern_timer,self.select_random_pattern)


    def get_pattern_name(self, pattern):
        if pattern is None:
            return "(None)"
        elif hasattr(pattern,"identifier"):
            return pattern.identifier
        else:
            for name, cl in self.patterns:
                if isinstance(pattern,cl): return name



    def get_patterns(self):
        c = []
        for name, cl in self.patterns:
            c.append(([name, cl], isinstance(self.pattern,cl)))
        return c

    def get_current_pattern(self):
        return self.pattern

    def toggle_pattern(self, cl, state):
        if state and cl not in self.patterns_selection:
            self.patterns_selection.append(cl)
        elif cl in self.patterns_selection:
            self.patterns_selection.remove(cl)

    def stop_shitlight(self):
        if self.pattern and self.pattern.is_alive():
            self.pattern.stop()
        shytlight.clear_buffer()


    def select_pattern(self, cl):
        if self.pattern and self.pattern.is_alive:
            self.pattern.stop()
            self.pattern.join(2.) # give pattern thread chance to finish clean
            shytlight.clear_buffer()            

        self.pattern = cl()
        self.pattern.start()

    def select_random_pattern(self,loop=None, user_data=None):
        if not self.patterns_selection:
          # no pattern selected for choice, do nothing but set new alarm
          self.pattern_alarm = self.loop.set_alarm_in(self.pattern_timer,self.select_random_pattern)
          return
        if self.pattern and self.pattern.is_alive:
            self.pattern.stop()
            self.pattern.join(2.) # give pattern thread chance to finish clean
            shytlight.clear_buffer()

        cl = random.choice(self.patterns_selection)            
        self.pattern = cl()
        self.pattern.start()

        self.pattern_alarm = self.loop.set_alarm_in(self.pattern_timer,self.select_random_pattern)        


    def quit(self):
        self.stop_shitlight()
        raise urwid.ExitMainLoop()








def main():
    global control
    control = CtrlController()
    control.main()

def exit_on_q(key):
    global control
    control.handle_keys(key)
    


if '__main__'==__name__:
    main()      
