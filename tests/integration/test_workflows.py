from cppoetry.core import CPPoetryAPI


class TestWorkflow:
    def test_validation_workflow(self, tmp_workspace):
        CPPoetryAPI(tmp_workspace.path, tmp_workspace.metadata).validate()

    def test_development_workflow(self, tmp_workspace):

        CPPoetryAPI(tmp_workspace.path, tmp_workspace.metadata).install()
