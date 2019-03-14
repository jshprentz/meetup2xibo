"""Summarizes meetup2xibo logs, reporting meeting changes."""


class LogSummarizer:

    """Summarizes meetup2xibo logs, reporting meeting changes."""

    def __init__(
            self, input_stream, output_stream, summary, log_parser,
            renderer):
        """Initialize with input and output streams, an empty summary, a
        log parser, and a renderer."""
        self.input_stream = input_stream
        self.output_stream = output_stream
        self.summary = summary
        self.log_parser = log_parser
        self.renderer = renderer

    def run(self):
        """Summarize the logs."""
        log_text = self.input_stream.read()
        parser = self.log_parser(log_text)
        parser.log_lines(self.summary)
        rendered_summary = self.renderer.render(self.summary)
        self.output_stream.write(rendered_summary)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
