"""Renders the log summary in HTML."""

from jinja2 import Environment, PackageLoader, select_autoescape
from email.utils import formatdate


class Renderer:

    """Renders the combined email headers and log summary."""

    def __init__(self, email_header_renderer, summary_renderer):
        """Initialize with renderers for email headers and log summaries."""
        self.email_header_renderer = email_header_renderer
        self.summary_renderer = summary_renderer

    def render(self, summary):
        """Render the email headers and log file summary as a string."""
        return self.email_header_renderer.render() \
            + self.summary_renderer.render(summary)


class EmailHeaderRenderer:

    """Renders the email headers."""

    def __init__(self, jinja2_env, template_name, email_to, email_subject):
        """Initialize with a Jinja2 environment and a template name."""
        self.jinja2_env = jinja2_env
        self.template_name = template_name
        self.email_to = email_to
        self.email_subject = email_subject

    def render(self):
        """Render the email headers as a string."""
        template = self.jinja2_env.get_template(self.template_name)
        now_formatted = formatdate(localtime=True)
        return template.render(
                email_to=self.email_to,
                email_subject=self.email_subject,
                email_date=now_formatted
                )


class SummaryRenderer:

    """Renders the log summary in HTML."""

    def __init__(self, jinja2_env, template_name):
        """Initialize with a Jinja2 environment and a template name."""
        self.jinja2_env = jinja2_env
        self.template_name = template_name

    def render(self, summary):
        """Render the log file summary as a string."""
        template = self.jinja2_env.get_template(self.template_name)
        return template.render(
                counters=summary.counter.counts(),
                cruds=summary.crud_lister.sorted_event_cruds()
                )


def make_jinja2_env(package):
    """Make a Jinja2 environment for a Python package."""
    return Environment(
            loader=PackageLoader(package, 'templates'),
            autoescape=select_autoescape(['html'])
            )


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
