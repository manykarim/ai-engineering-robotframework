"""Pre-run modifier: stops a run before its first test when the shop settings cannot work.

Robot Framework reports a failing variable file and then runs the tests anyway,
so the check lives here. When the settings are unusable, the top suite's setup
becomes ``Fatal Error`` with the explanation: no test runs, the message is the
first thing on the console, and the exit status is non-zero.
"""
from robot.api import SuiteVisitor

from shop.config import load


class preflight(SuiteVisitor):  # noqa: N801 - Robot Framework expects the module's name
    def start_suite(self, suite):
        if suite.parent is not None:
            return
        problem = load().problem
        if problem:
            suite.setup.config(name="BuiltIn.Fatal Error", args=[problem])
