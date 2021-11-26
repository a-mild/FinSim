from datetime import datetime

import ipyvuetify as v
import traitlets

from blinker import signal
from traitlets import observe

value_updated = signal("value-updated")


class DatePicker(v.VuetifyTemplate):
    template_file = "./src/components/traces/controls/datepicker-template.vue"

    v_model = traitlets.Unicode(datetime.today().strftime("%Y-%m")).tag(sync=True)

    label = traitlets.Unicode('Select date').tag(sync=True)

    menu = traitlets.Bool(False).tag(sync=True)

    def __init__(self, paramname: str, **kwargs):
        self.paramname = paramname
        super().__init__(**kwargs)

    @observe("v_model")
    def on_change(self, event=None):
        value_updated.send(self.paramname, value=self.get_value())

    def get_value(self):
        return datetime.strptime(self.v_model, "%Y-%m")
