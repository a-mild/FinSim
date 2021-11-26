import re

import ipyvuetify as v
import traitlets

from blinker import signal
from traitlets import observe

value_updated = signal("value-updated")

#TODO: regex stimmt nicht ganz
class InterestPicker(v.VuetifyTemplate):
    template_file = "./src/components/traces/controls/interestpicker-template.vue"

    valid_regex = re.compile(r"\d{1,3}(\.\d{0,5})?")
    use_interest = traitlets.Bool(False).tag(sync=True)
    v_model = traitlets.Unicode("0").tag(sync=True)
    label = traitlets.Unicode("Interest [% p.A.]").tag(sync=True)


    def __init__(self, paramname: str, **kwargs):
        self.paramname = paramname
        super().__init__(**kwargs)

    @property
    def valid_input(self):
        if self.v_model:
            return bool(re.match(self.valid_regex, self.v_model))
        else:
            return False

    @observe("use_interest")
    def vue_on_change(self, data=None):
        if not self.valid_input:
            return
        value_updated.send(self.paramname, value=self.get_value())

    def get_value(self) -> float:
        if self.use_interest:
            return float(self.v_model)
        else:
            return 0


