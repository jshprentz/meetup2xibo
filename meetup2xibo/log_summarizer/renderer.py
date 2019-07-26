"""Renders the log summary in HTML."""

from jinja2 import Environment, PackageLoader, select_autoescape
from email.message import EmailMessage
from email.headerregistry import Address
from io import StringIO
import csv


class Renderer:

    """Renders the combined email headers and log summary."""

    def __init__(
            self, mappings_flag, email_renderer, summary_renderer,
            location_mapping_csv_renderer):
        """Initialize with a mappings flag to request CSV output and with
        renderers for email, log summaries, and location mapping."""
        self.mappings_flag = mappings_flag
        self.email_renderer = email_renderer
        self.summary_renderer = summary_renderer
        self.location_renderer = location_mapping_csv_renderer

    def render(self, summary):
        """Render an email message containing the log file summary as a
        string."""
        if self.email_renderer.can_render():
            return self.email_renderer.render(
                self.summary_renderer.render(summary),
                self.location_renderer.render(summary.location_mapper))
        elif self.mappings_flag:
            return self.location_renderer.render(summary.location_mapper)
        else:
            return self.summary_renderer.render(summary)


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
            msg.add_attachment(
                    csv_data,
                    subtype="csv",
                    filename="meetup_locations.csv")
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


class LocationMappingCsvRenderer:

    """Renders location mappings as comma separated values."""

    def render(self, location_mapper):
        """Render location mappings as comma separated values, if possible."""
        if location_mapper.has_mappings():
            return self.render_csv(location_mapper)
        else:
            return ""

    def render_csv(self, location_mapper):
        """Render location mappings as comma separated values."""
        with StringIO(newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            self.write_csv_header(csv_writer)
            self.write_csv_mappings(csv_writer, location_mapper.mapping_list())
            return csv_file.getvalue()

    @staticmethod
    def write_csv_header(csv_writer):
        """Write the CSV header line."""
        csv_writer.writerow(
            ["Location", "Venue", "Find Us", "Example Meetup", "Example URL"])

    def write_csv_mappings(self, csv_writer, mapping_list):
        """Write CSV lines for the location mapping log lines a list."""
        for log_line in mapping_list:
            self.write_csv_mapping(csv_writer, log_line)

    def write_csv_mapping(self, csv_writer, log_line):
        """Write a CSV line for the event location log line."""
        csv_writer.writerow([
                log_line.location,
                log_line.event.venue,
                log_line.event.find_us,
                log_line.event.name,
                log_line.event.url
                ])


class SummaryRenderer:

    """Renders the log summary in HTML."""

    def __init__(self, jinja2_env, template_name):
        """Initialize with a Jinja2 environment and a template name."""
        self.jinja2_env = jinja2_env
        self.template_name = template_name

    def render(self, summary):
        """Render the log file summary as a string."""
        crud_lister = summary.crud_lister
        conflict_reporter = summary.conflict_reporter
        template = self.jinja2_env.get_template(self.template_name)
        return template.render(
                counters=summary.counter.counts(),
                current_event_logs=crud_lister.sorted_current_event_logs(),
                past_event_logs=crud_lister.sorted_past_event_logs(),
                has_conflicts=conflict_reporter.has_conflicts(),
                checked_places=conflict_reporter.sorted_checked_places(),
                conflict_places=conflict_reporter.sorted_conflict_places()
                )


def make_jinja2_env(package):
    """Make a Jinja2 environment for a Python package."""
    return Environment(
            loader=PackageLoader(package, 'templates'),
            autoescape=select_autoescape(['html'])
            )


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
