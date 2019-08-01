"""An application that sets up logging prior to other initialization."""


class LoggingApplication:

    """An application that sets up logging prior to other initialization."""

    def __init__(self, logging_context, enter_logging_application_scope):
        """Initialize with a logging context and a logging application scope
        entrance function """
        self.logging_context = logging_context
        self.enter_logging_application_scope = enter_logging_application_scope

    def run(self):
        """Initialize and run the application within a logging context."""
        with self.logging_context:
            processor = self.enter_logging_application_scope()
            processor.run()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
