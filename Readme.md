## WIP

# OpenROAD Wheels

Unofficial pre-built binary wheels for
[OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD), also including the
full OpenROAD binary with a Tcl interpreter.

## Requirements

* Any of:
    * macOS 15 or later  (arm64)
    * GNU/Linux with Glibc 2.27 or later (x86_64 or aarch64)
* Python 3.10 or later

## Caveats

* The OpenROAD Qt GUI is not supported.
* The OpenROAD binary requires a one-time extraction step which must be prepared
  ahead of time for read-only environments.
* We cannot guarantee more than one .post version per OpenROAD version will be
  up on PyPI at the same time due to storage requirements.

## Licensing

### Binaries

As the binary incorporates OpenSTA code, the binaries are distributed under the
GNU General Public License, v3, or any later version. See [COPYING](./COPYING)
for more info.

### Code

Copyright (c) 2018-2025, The OpenROAD Authors.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1.  Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

2.  Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

3.  Neither the name of the copyright holder nor the names of its contributors
    may be used to endorse or promote products derived from this software
    without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

