"""
TODO:
"""

from importlib.metadata import entry_points


class TestPlugin:
    """
    TODO
    """

    def test_generator(self):
        """
        TODO
        """
        plugin_entries = entry_points(group="cppython.generator_plugins")
        assert len(plugin_entries) > 0
