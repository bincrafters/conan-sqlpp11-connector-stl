#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


# d1efault_options = {'shared': False, 'fPIC': True}


class sqlpp11Conan(ConanFile):
    name = "sqlpp11-connector-stl"
    version = "0.5"
    description = "An experimental SQL connector for containers and streams of the C++ Standard Library."
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/bincrafters/conan-sqlpp11-connector-stl"
    homepage = "https://github.com/rbock/sqlpp11-connector-stl"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "BSD 2-Clause"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    requires = "sqlpp11/0.57@bincrafters/stable"
    short_paths = True

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version),
                  sha256="05bd4fda37baeb5d802976d290f1c388abb46c7ec7ddcd72390e96fd51c324e4")
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

        # error C2039: 'logical_and': is not a member of 'std'
        tools.replace_in_file(os.path.join(self._source_subfolder, 'tests', 'SampleTest.cpp'),
                              '#include <iostream>',
                              '#include <iostream>\n#include <functional>')

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_TESTS"] = False
        cmake.definitions['HinnantDate_ROOT_DIR'] = self.deps_cpp_info['date'].include_paths[0]
        cmake.definitions['SQLPP11_INCLUDE_DIR'] = self.deps_cpp_info['sqlpp11'].include_paths[0]
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["sqlpp11-connector-stl"]
