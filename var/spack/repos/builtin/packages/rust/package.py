# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rust(Package):
    """The rust programming language toolchain"""

    homepage = "http://www.rust-lang.org"
    git      = "https://github.com/rust-lang/rust.git"
    url = "https://github.com/rust-lang/rust/archive/1.39.0.tar.gz"

    version('develop', branch='master')
    version('1.39.0', md5='f3ca7fcd83e45d92d7cd8c93777b56f3')
    
    version('1.34.0', tag='1.34.0')
    version('1.32.0', tag='1.32.0')
    version('1.31.1', tag='1.31.1')
    version('1.31.0', tag='1.31.0')  # "Rust 2018" edition
    version('1.30.1', tag='1.30.1')
    

    extendable = True

    # Rust
    depends_on("llvm")
    depends_on("curl")
    depends_on("git")
    depends_on("cmake")
    depends_on("binutils")
    depends_on("python@:2.8")
    #depends_on("python", when="@1.35.0:")

    # Cargo
    depends_on("openssl")

    phases = ['configure', 'install']

    def setup_build_environment(self, env):
        # No idea why the python package doesn't do this
        env.append_path("PYTHONPATH",
            join_path(self.spec['python'].prefix, self.spec['python'].package.python_lib_dir))

    def setup_run_environment(self, env):
        # No idea why the python package doesn't do this
        env.append_path("PYTHONPATH",
            join_path(self.spec['python'].prefix, self.spec['python'].package.python_lib_dir))

    def configure(self, spec, prefix):
        configure_args = [
          '--prefix=%s' % prefix,
          '--llvm-root=' + spec['llvm'].prefix,
          # Workaround for "FileCheck does not exist" error
          '--disable-codegen-tests',
          # Includes Cargo in the build
          # https://github.com/rust-lang/cargo/issues/3772#issuecomment-283109482
          '--enable-extended',
          # Prevent build from writing bash completion into system path
          '--sysconfdir=%s' % join_path(prefix, 'etc/')
          ]

        configure(*configure_args)

        # Build system defaults to searching in the same path as Spack's
        # compiler wrappers which causes the build to fail
        filter_file(
            '#ar = "ar"',
            'ar = "%s"' % join_path(spec['binutils'].prefix.bin, 'ar'),
            'config.toml')

    def install(self, spec, prefix):
        make()
        make("install")
