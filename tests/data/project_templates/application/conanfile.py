from conans import ConanFile, CMake

class synodicpoetictestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "Poco/1.9"
    generators = ["cmake_find_package", "cmake_paths"]

