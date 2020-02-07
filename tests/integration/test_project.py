from .common import test_project

class TestProjects():

    def test_correct_project(self, test_project):

        with test_project:
            SynodicPlugin().poetry_new()
