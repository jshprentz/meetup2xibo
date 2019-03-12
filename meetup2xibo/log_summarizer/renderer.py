"""Renders the log summary in HTML."""

from jinja2 import Environment, PackageLoader, select_autoescape


class Renderer:

    """Renders the log summary in HTML."""

    def __init__(self, jinja2_env, template_name):
        """Initialize with a Jinja2 environment and a template name."""
        self.jinja2_env = jinja2_env
        self.template_name = template_name

    def render(self, summary):
        """Render the log file summary as a string."""
        template = self.jinja2_env.get_template(self.template_name)
        return template.render(
                counters = summary.counter.counts(),
                cruds=summary.crud_lister.sorted_event_cruds()
                )

def make_jinja2_env(package):
    """Make a Jinja2 environment for a Python package."""
    return Environment(
            loader=PackageLoader(package, 'templates'),
            autoescape=select_autoescape(['html'])
            )


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
