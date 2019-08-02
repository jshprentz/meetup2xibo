"""A careful environment, which checks for key and JSON conversion errors."""

from .exceptions import JsonConversionError, MissingEnvVarError
import collections
import json


class CarefulEnvironment(collections.abc.Mapping):

    """An read-only environment wrapper, which checks for key and JSON
    conversion errors."""

    def __init__(self, env_vars):
        """Initialize with environment variables, a mapping of keys to
        values."""
        self._env_vars = env_vars

    def __getitem__(self, key):
        """Return the environment variable value with the named key."""
        try:
            return self._env_vars[key]
        except KeyError as err:
            message = "Missing environment variable {}".format(key)
            raise MissingEnvVarError(message) from err

    def __iter__(self):
        """Return an iterator over the environment variable keys."""
        return iter(self._env_vars)

    def __len__(self):
        """Return the length of thw wrapped environment."""
        return len(self._env_vars)

    def json(self, key):
        """Return the deserialized JSON value from the environment variable
        named key.  If the data being deserialized is not a valid JSON
        document, a JsonConversionError reporting the context description will
        be raised."""
        try:
            return json.loads(self[key])
        except json.JSONDecodeError as err:
            message = self.json_conversion_message(
                    key, err.msg, err.lineno, err.colno, err.doc)
            raise JsonConversionError(message) from err

    @staticmethod
    def json_conversion_message(
            key, err_msg, line_num, column_num, json_doc):
        """Return a message describing a JSON conversion error at a numbered
        line and column within the JSON document retrieved from the named
        environment variable."""
        json_lines = json_doc.splitlines()
        if len(json_lines) >= line_num:
            error_line = json_lines[line_num - 1]
            truncated_line = error_line[0:column_num - 1]
            detabbed_line = truncated_line.expandtabs()
            char_count = len(detabbed_line)
            pointer_line = char_count * " " + "^"
            context_lines = '\n'.join(json_lines[:line_num][-3:]).expandtabs()
            error_location = "line {:d}:\n{}\n{}" \
                .format(line_num, context_lines, pointer_line)
        else:
            error_location = "line {:d} column {:d}" \
                .format(line_num, column_num)
        return "In JSON environment variable {}: {} at {}" \
            .format(key, err_msg, error_location)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
