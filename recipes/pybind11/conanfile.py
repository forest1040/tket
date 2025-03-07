# Copyright 2019-2022 Cambridge Quantum Computing
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from conans import ConanFile, tools, CMake
import os
import sys


class PyBind11Conan(ConanFile):
    name = "pybind11"
    version = "2.10.1"
    description = "Seamless operability between C++11 and Python"
    topics = "conan", "pybind11", "python", "binding"
    homepage = "https://github.com/pybind/pybind11"
    license = "BSD-3-Clause"
    exports_sources = "CMakeLists.txt"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    no_copy_source = True

    _source_subfolder = "source_subfolder"

    _cmake = None

    def source(self):
        tools.get(
            f"https://github.com/pybind/pybind11/archive/refs/tags/v{self.version}.tar.gz"
        )
        os.rename("{}-{}".format(self.name, self.version), self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["PYBIND11_INSTALL"] = True
        self._cmake.definitions["PYBIND11_TEST"] = False
        self._cmake.definitions[
            "PYBIND11_CMAKECONFIG_INSTALL_DIR"
        ] = "lib/cmake/pybind11"

        # Use pybind11's CMakeLists.txt directly. Otherwise,
        # PYBIND11_MASTER_PROJECT is set to FALSE and the installation does not
        # generate pybind11Targets.cmake. Without that the generated package
        # config cannot be used successfully. We want to use the generated
        # package config as this starting in version 2.6.0 onwards defines the
        # pybind11::headers target that is required to make full use of all
        # installed cmake files.
        self._cmake.configure(
            source_dir=os.path.join(self.source_folder, self._source_subfolder),
            defs={"PYTHON_EXECUTABLE": sys.executable},
        )
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", src=self._source_subfolder, dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()
        lib_folder = os.path.join(self.package_folder, "lib", "cmake", "pybind11")
        os.rename(
            os.path.join(lib_folder, "pybind11Config.cmake"),
            os.path.join(lib_folder, "pybind11Install.cmake"),
        )
        os.unlink(os.path.join(lib_folder, "pybind11ConfigVersion.cmake"))

    def package_id(self):
        self.info.header_only()

    def package_info(self):
        self.cpp_info.includedirs.append(
            os.path.join(self.package_folder, "include", "pybind11")
        )

        cmake_base_path = os.path.join("lib", "cmake", "pybind11")
        self.cpp_info.builddirs = [cmake_base_path]

        def get_path(filename):
            return os.path.join(cmake_base_path, filename)

        self.cpp_info.build_modules = [
            get_path("FindPythonLibsNew.cmake"),
            get_path("pybind11Install.cmake"),
        ]
