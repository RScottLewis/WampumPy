from kivy.app import App
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from wampum.util import fee_levels
from wampum_gui.kivy.i18n import _

Builder.load_string('''
<BumpFeeDialog@Popup>
    title: _('Bump fee')
    size_hint: 0.8, 0.8
    pos_hint: {'top':0.9}
    BoxLayout:
        orientation: 'vertical'
        padding: '10dp'

        GridLayout:
            height: self.minimum_height
            size_hint_y: None
            cols: 1
            spacing: '10dp'
            BoxLabel:
                id: old_fee
                text: _('Current Fee')
                value: ''
            BoxLabel:
                id: new_fee
                text: _('New Fee')
                value: ''
        Label:
            id: tooltip
            text: ''
            size_hint_y: None
        Slider:
            id: slider
            range: 0, 4
            step: 1
            on_value: root.on_slider(self.value)
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, 0.2
            Label:
                text: _('Final')
            CheckBox:
                id: final_cb
        Widget:
            size_hint: 1, 1
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, 0.5
            Button:
                text: 'Cancel'
                size_hint: 0.5, None
                height: '48dp'
                on_release: root.dismiss()
            Button:
                text: 'OK'
                size_hint: 0.5, None
                height: '48dp'
                on_release:
                    root.dismiss()
                    root.on_ok()
''')

class BumpFeeDialog(Factory.Popup):

    def __init__(self, app, fee, size, callback):
        Factory.Popup.__init__(self)
        self.app = app
        self.init_fee = fee
        self.tx_size = size
        self.callback = callback
        self.config = app.wampum_config
        self.fee_step = self.config.max_fee_rate() / 10
        self.dynfees = self.config.get('dynamic_fees', True) and self.app.network
        self.ids.old_fee.value = self.app.format_amount_and_units(self.init_fee)
        self.update_slider()
        self.update_text()

    def update_text(self):
        value = int(self.ids.slider.value)
        self.ids.new_fee.value = self.app.format_amount_and_units(self.get_fee())
        if self.dynfees:
            value = int(self.ids.slider.value)
            self.ids.tooltip.text = fee_levels[value]

    def update_slider(self):
        slider = self.ids.slider
        if self.dynfees:
            slider.range = (0, 4)
            slider.step = 1
            slider.value = 3
        else:
            slider.range = (1, 10)
            slider.step = 1
            rate = self.init_fee*1000//self.tx_size
            slider.value = min( rate * 2 // self.fee_step, 10)

    def get_fee(self):
        value = int(self.ids.slider.value)
        if self.dynfees:
            if self.config.has_fee_estimates():
                dynfee = self.config.dynfee(value)
                return int(dynfee * self.tx_size // 1000)
        else:
            return int(value*self.fee_step * self.tx_size // 1000)

    def on_ok(self):
        new_fee = self.get_fee()
        is_final = self.ids.final_cb.active
        self.callback(self.init_fee, new_fee, is_final)

    def on_slider(self, value):
        self.update_text()

    def on_checkbox(self, b):
        self.dynfees = b
        self.update_text()
