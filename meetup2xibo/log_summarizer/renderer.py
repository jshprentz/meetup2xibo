"""Renders the log summary in HTML."""

from jinja2 import Environment, PackageLoader, select_autoescape
from email.message import EmailMessage
from email.headerregistry import Address


class Renderer:

    """Renders the combined email headers and log summary."""

    def __init__(self, email_renderer, summary_renderer):
        """Initialize with renderers for email and log summaries."""
        self.email_renderer = email_renderer
        self.summary_renderer = summary_renderer

    def render(self, summary):
        """Render an email message containing the log file summary as a
        string."""
        html_summary = self.summary_renderer.render(summary)
        if self.email_renderer.can_render():
            return self.email_renderer.render(html_summary, None)
        else:
            return html_summary


class EmailRenderer:

    """Renders an email message containing summary HTML content."""

    def __init__(self, email_to, email_subject):
        """Initialize with an email "To" address and subject."""
        self.email_to = email_to
        self.email_subject = email_subject

    def can_render(self):
        """Return true it an email message can be rendered; false otherwise."""
        return bool(self.email_to)

    def render(self, summary_html, csv_data):
        """Render an email reporting summary information and possibly some csv
        data."""
        msg = self.make_message()
        msg.set_content(summary_html, subtype="html")
        if csv_data:    
            msg.add_attachment(csv_data, subtype="csv")
        return str(msg)

    def make_message(self):
        """Make and return an email addressed to "To" recipients and with the
        supplied subject."""
        msg = EmailMessage()
        msg['Subject'] = self.email_subject
        msg['To'] = self.address_list()
        return msg

    def address_list(self):
        """Return a list of "To" email addresses."""
        return tuple(
                Address(addr_spec=address)
                for address in self.email_to.split())


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
