#!/usr/bin/env python

# Copyright (c) 2017 CNRS Author: Joseph Mirabel
#
# This file is part of hpp-gepetto-viewer. hpp-gepetto-viewer is free software:
# you can redistribute it and/or modify it under the terms of the GNU Lesser
# General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# hpp-gepetto-viewer is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Lesser Public License
# for more details.  You should have received a copy of the GNU Lesser General
# Public License along with hpp-gepetto-viewer.  If not, see
# <http://www.gnu.org/licenses/>.

macro(INSTALL_PYTHON_FILES MODULE)
  set(FIRST TRUE)
  foreach(PYFILE ${ARGV})
    if(${FIRST})
      set(FIRST FALSE)
    else()
      python_install_on_site(${MODULE} ${PYFILE})
    endif()
  endforeach()
endmacro()

install_python_files("pyhpp_gepetto" __init__.py viewer.py)
install_python_files("pyhpp_viser" __init__.py viewer.py)
