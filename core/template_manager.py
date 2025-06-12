from pptx import Presentation

class TemplateManager:
    def __init__(self, template_dir):
        self.template_dir = template_dir

    def load_template(self, slide_type):
        path = f"{self.template_dir}/{slide_type}.pptx"
        return Presentation(path)
