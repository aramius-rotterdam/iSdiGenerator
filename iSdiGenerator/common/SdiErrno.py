################################################################################
# SdiErrno.py
# 
# Copyright (c) 2021 ArAmIuS de Rotterdam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#
#
################################################################################

################################################################################
# imports
################################################################################
from enum import Enum

################################################################################
# Class SdiErrno
################################################################################
class SdiErrno(Enum):
    E_ERRNO_NONE = 0
    E_ERRNO_UNKNOWN_SYNTAX = 1
    E_ERRNO_DIRECTIVE_NOT_EXIST = 2
    E_ERRNO_INCLUDE_MALFORMED = 3
    E_ERRNO_INCLUDE_RECURSION = 4
    E_ERRNO_INCLUDE_DUPLICATED = 5
    E_ERRNO_INCLUDE_NOT_EXPECTED = 6
    E_ERRNO_SDI_FILE_EXPECTED = 7
    E_ERRNO_SDI_FILE_NOT_EXIST = 8
    E_ERRNO_SDI_FILE_INCLUDED_MALFORMED = 9
    E_ERRNO_SDI_FILE_INTERFACE_DUPLICATED = 10
    E_ERRNO_PRAGMA_MALFORMED = 11
    E_ERRNO_PRAGMA_NOT_VALID = 12
    E_ERRNO_PRAGMA_NOT_EXPECTED = 13
    E_ERRNO_TYPEDEF_MALFORMED = 14
    E_ERRNO_TYPEDEF_DUPLICATED = 15
    E_ERRNO_TYPEDEF_NOT_EXIST = 16
    E_ERRNO_DATA_TYPE_NOT_EXIST = 17
    E_ERRNO_OPENNING_BRACKET_NOT_EXPECTED = 18
    E_ERRNO_CLOSING_BRACKET_EXPECTED = 19
    E_ERRNO_CLOSING_BRACKET_NOT_EXPECTED = 20
    E_ERRNO_STRUCT_DUPLICATED = 21
    E_ERRNO_STRUCT_PROPERTY_NAME_MALFORMED = 22
    E_ERRNO_STRUCT_PROPERTY_DUPLICATED = 23
    E_ERRNO_INTERFACE_PROPERTIES_SYNTAX_DUPLICATED = 24
    E_ERRNO_INTERFACE_PROPERTY_NAME_MALFORMED = 25
    E_ERRNO_INTERFACE_PROPERTY_DUPLICATED = 26