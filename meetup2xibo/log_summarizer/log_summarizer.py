"""Summarizes meetup2xibo logs, reporting meeting changes."""


class LogSummarizer:

    """Summarizes meetup2xibo logs, reporting meeting changes."""

    def __init__(self, input_stream, output_stream, summary, log_parser):
        """Initialize with input and output streams, an empty summary, and a
        log parser."""
        self.input_stream = input_stream
        self.output_stream = output_stream
        self.summary = summary
        self.log_parser = log_parser

    def run(self):
        """Summarize the logs."""
        log_text = self.input_stream.read()
        parser = self.log_parser(log_text)
        parser.log_lines(self.summary)
        for name, count in self.summary.counter.counts():
            print(name, count)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
