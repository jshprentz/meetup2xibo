"""Test rendering a log file summary."""

from meetup2xibo.log_summarizer.renderer import Renderer, make_jinja2_env
from meetup2xibo.log_summarizer.start_counter import StartCounter
import pytest

@pytest.fixture
def jinja2_env():
    """Return a Jinja2 environment for rendering."""
    return make_jinja2_env(__package__)

@pytest.fixture
def start_counter():
    """Return a start counter."""
    return StartCounter()

def test_jinja2_env(jinja2_env):
    """Test the Jinja2 environment by rendering hello world."""
    template = jinja2_env.get_template('hello_world.txt')
    assert template.render() == "Hello World"

def test_render_start_counter(jinja2_env, start_counter):
    """Test rendering a start counter."""
    start_counter.count("Foo 1.0.0")
    start_counter.count("Bar 2.0.0")
    start_counter.count("Foo 1.0.0")
    template = jinja2_env.get_template('counts.txt')
    expected_rendering = """
Bar 2.0.0: 1

Foo 1.0.0: 2
"""
    assert template.render(counters = start_counter.counts()) == expected_rendering

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
