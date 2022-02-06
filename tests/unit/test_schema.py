"""
TODO:
"""
import pytest

from cppython.plugins.test.data import (
    default_metadata,
    default_pep621,
    default_pyproject,
)


class TestSchema:
    """
    TODO
    """

    @pytest.mark.parametrize("metadata", [default_metadata])
    def test_metadata(self, metadata):
        """
        TODO
        """

    @pytest.mark.parametrize("pep621", [default_pep621])
    def test_pep621(self, pep621):
        """
        TODO
        """

    @pytest.mark.parametrize("pyproject", [default_pyproject])
    def test_pyproject(self, pyproject):
        """
        TODO
        """
