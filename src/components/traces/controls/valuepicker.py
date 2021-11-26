import re

import ipyvuetify as v
import traitlets

from blinker import signal


value_updated = signal("value-updated")


class ValuePicker(v.VuetifyTemplate):
    template_file = "./src/components/traces/controls/valuepicker-template.vue"

    valid_regex = re.compile(r"([1-9]{1}[0-9]{0,2}(\,\d{3})*(\.\d{0,2})?|[1-9]{1}\d*(\.\d{0,2})?|0(\.\d{0,2})?|(\.\d{1,2}))$|^([1-9]{1}\d{0,2}(\,\d{3})*(\.\d{0,2})?|[1-9]{1}\d*(\.\d{0,2})?|0(\.\d{0,2})?|(\.\d{1,2}))$|^\(\$?([1-9]{1}\d{0,2}(\,\d{3})*(\.\d{0,2})?|[1-9]{1}\d*(\.\d{0,2})?|0(\.\d{0,2})?|(\.\d{1,2}))\)")
    v_model = traitlets.Unicode("0").tag(sync=True)
    label = traitlets.Unicode("Value").tag(sync=True)

    def __init__(self, paramname: str, **kwargs):
        self.paramname = paramname
        super().__init__(**kwargs)

    @property
    def valid_input(self) -> bool:
        if self.v_model:
            return bool(re.match(self.valid_regex, self.v_model))
        else:
            return False

    def vue_on_change(self, event=None) -> None:
        if not self.valid_input:
            return
        value_updated.send(self.paramname, value=self.get_value())

    def get_value(self) -> float:
        return float(self.v_model.replace(",", ""))
