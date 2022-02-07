"""
TODO:
"""

from importlib import metadata


class TestPlugin:
    """
    TODO
    """

    def test_generator(self):
        """
        TODO
        """
        entries = metadata.entry_points()
        plugin_entries = entries["cppython.generator"]
        assert len(plugin_entries) > 1

    def test_interface(self):
        """
        TODO
        """
        entries = metadata.entry_points()
        plugin_entries = entries["cppython.interface"]
        assert len(plugin_entries) > 1
