import json
from io import StringIO

import traitlets
from blinker import signal

import ipywidgets as widgets
import ipyvuetify as v
from IPython.core.display import display

from src.model import Model

from ipywidgets import Output
from IPython.display import HTML, clear_output
from base64 import b64encode

"""
download stolen from https://github.com/voila-dashboards/voila/issues/711
"""


class AppBar(v.VuetifyTemplate):
    template_file = "./src/components/appbar-template.vue"

    #drawer_opened = traitlets.Bool(default_value=True).tag(sync=True)
    loaded_filename = traitlets.Unicode(default_value="No file loaded").tag(sync=True)
    file_upload_widget = traitlets.Any(widgets.FileUpload(
        description="",
        multiple=False
    )).tag(sync=True, **widgets.widget_serialization)
    file_download_dummy_outputwidget = traitlets.Any(Output()).tag(sync=True, **widgets.widget_serialization)
    file = traitlets.Any().tag(sync=True)

    def __init__(self, model: Model):
        super().__init__()
        self.model = model
        self.file_upload_widget.observe(self.upload_traces, "value")

    def vue_toggle_drawer(self, data):
        sig = signal("toggle-drawer")
        sig.send()

    def vue_reset_all(self, data=None):
        self.model.reset_all()

    def upload_traces(self, change):
        res = {filename: f["content"] for filename, f in self.file_upload_widget.value.items()}
        filename, content = res.popitem()
        self.loaded_filename = f"loaded file: {filename!r}"
        self.model.from_json(content)

    def trigger_file_download(self, text: str, filename: str, kind: str = 'text/json'):
        # see https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs for details
        content_b64 = b64encode(text.encode()).decode()
        data_url = f'data:{kind};charset=utf-8;base64,{content_b64}'
        js_code = f"""
            var a = document.createElement('a');
            a.setAttribute('download', '{filename}');
            a.setAttribute('href', '{data_url}');
            a.click()
        """
        with self.file_download_dummy_outputwidget:
            clear_output()
            display(HTML(f'<script>{js_code}</script>'))

    def vue_save_traces(self):
        """Save the state of all traces to a .json file"""
        json_str = self.model.to_json()
        self.trigger_file_download(json_str, 'pensionsimulator.json', kind='text/json')
