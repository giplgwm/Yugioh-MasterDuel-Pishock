import wx
from lose_screen_detection import at_lose_screen
from pishockpy import PishockAPI
import json

with open('config.json', 'r') as file:
    config = json.loads(file.read())

SCREEN_SCAN_INTERVAL_IN_MS = config['bot_behaviour']['screen_scan_interval_ms']
COOLDOWN = config['bot_behaviour']['scanning_cooldown_after_shocking_ms']
DETECTION_THRESHOLD = config['bot_behaviour']['detection_threshold']

scanning = False

shocks = 0
pishock = PishockAPI(config['account']['api_key'],
                     config['account']['username'],
                     config['account']['share_code'],
                     config['account']['program_name'])


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Duel Master Pishock")
        panel = wx.Panel(self)
        self.SetIcon(wx.Icon('img/icon_5.ico'))

        self.scan_btn = wx.Button(panel, label="Start Scanning")
        self.Bind(wx.EVT_BUTTON, self.button_press, self.scan_btn)

        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        strength_sizer = wx.BoxSizer(wx.VERTICAL)
        duration_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.scanner_text = wx.StaticText(panel, label="Waiting...")

        self.shock_count = wx.StaticText(panel, label=f"Shocks: {shocks}")

        self.strength_control = wx.SpinCtrl(panel)
        self.strength_control.SetRange(1, 100)
        self.duration_control = wx.SpinCtrl(panel)
        self.duration_control.SetRange(1,15)

        strength_sizer.Add(wx.StaticText(panel, label='Strength:'), 0, wx.CENTER, 5)
        strength_sizer.Add(self.strength_control, 0, wx.CENTER, 5)

        duration_sizer.Add(wx.StaticText(panel, label='Duration:'), 0, wx.CENTER, 5)
        duration_sizer.Add(self.duration_control, 0, wx.CENTER, 5)

        input_sizer.Add(strength_sizer, 0, wx.CENTER, 5)
        input_sizer.AddSpacer(80)
        input_sizer.Add(duration_sizer, 0, wx.CENTER, 5)

        sizer.AddSpacer(10)
        sizer.Add(input_sizer, 0, wx.CENTER, 5)
        sizer.AddSpacer(10)
        sizer.Add(self.scan_btn, 0, wx.EXPAND | wx.ALL, 5)
        sizer.AddSpacer(20)
        sizer.Add(self.scanner_text, 0, wx.CENTER, 5)
        sizer.AddSpacer(20)
        sizer.Add(self.shock_count, 0, wx.CENTER, 5)

        panel.SetSizer(sizer)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)

        self.restart_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_restart_timer, self.restart_timer)

        self.Show()

    def button_press(self, event):
        global scanning
        scanning = not scanning
        if scanning:
            self.scan_btn.SetLabel("Stop scanning")
            print('Scanning.')
            self.scanner_text.SetLabel("Scanning!")
            self.timer.Start(SCREEN_SCAN_INTERVAL_IN_MS)
        else:
            self.scan_btn.SetLabel("Start scanning")
            print('Scanning Stopped.')
            self.scanner_text.SetLabel("Waiting...")
            self.timer.Stop()

    def on_timer(self, event):
        global shocks
        if at_lose_screen(DETECTION_THRESHOLD):
            print('DETECTED!')
            self.timer.Stop()
            self.restart_timer.Start(COOLDOWN, oneShot=True)
            shocks += 1
            self.shock_count.SetLabel(f'Shocks: {shocks}')
            pishock.shock(self.strength_control.GetValue()/100, self.duration_control.GetValue())
            print('Shock signal sent!')

        else:
            pass

    def on_restart_timer(self, event):
        self.timer.Start(SCREEN_SCAN_INTERVAL_IN_MS)




app = wx.App()
frame = MyFrame()
frame.Show()
pishock.beep(1)
app.MainLoop()