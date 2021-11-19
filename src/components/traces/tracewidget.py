from uuid import UUID

import ipyvuetify as v
import ipywidgets as w
import traitlets

from blinker import signal

delete_trace = signal("delete-trace")
value_updated = signal("value-updated")
update_trace = signal("update-trace")


class TraceWidget(v.VuetifyTemplate):
    template_file = "./src/components/traces/tracewidget-template.vue"

    name = traitlets.Unicode().tag(sync=True)
    controls = traitlets.List().tag(sync=True, **w.widget_serialization)

    def __init__(self, side: str, uuid: UUID, name: str, controls):
        self.side = side
        self.uuid = uuid
        self.name = name
        self.controls = controls
        # connect the signals
        for c in self.controls:
            value_updated.connect(self.update_params, sender=c, weak=False)
        super().__init__()

    @property
    def params(self):
        return {c.paramname: c.get_value() for c in self.controls}

    # TODO
    def change_tracename(self, data=None):
        return

    def vue_delete_trace(self, data=None):
        delete_trace.send(self.side, uuid=self.uuid)

    def update_params(self, sender):
        update_trace.send(self.uuid, params=self.params)
