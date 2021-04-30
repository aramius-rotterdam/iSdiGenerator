################################################################################
# SdiErrorsCollector.py
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
from termcolor import cprint

################################################################################
# Class Errno
################################################################################
class Errno(Enum):
    E_ERRNO_NONE = 0,
    E_ERRNO_UNKNOWN_SYNTAX = 1,
    E_ERRNO_DIRECTIVE_NOT_EXIST = 2,
    E_ERRNO_INCLUDE_MALFORMED = 3,
    E_ERRNO_INCLUDE_RECURSION = 4,
    E_ERRNO_INCLUDE_DUPLICATED = 5,
    E_ERRNO_INCLUDE_NOT_EXPECTED = 6,
    E_ERRNO_SDI_FILE_EXPECTED = 7,
    E_ERRNO_SDI_FILE_NOT_EXIST = 8,
    E_ERRNO_SDI_FILE_INCLUDED_MALFORMED = 9,
    E_ERRNO_SDI_FILE_INTERFACE_DUPLICATED = 10,
    E_ERRNO_PRAGMA_MALFORMED = 11,
    E_ERRNO_PRAGMA_NOT_VALID = 12,
    E_ERRNO_PRAGMA_NOT_EXPECTED = 13,
    E_ERRNO_TYPEDEF_MALFORMED = 14,
    E_ERRNO_TYPEDEF_DUPLICATED = 15,
    E_ERRNO_TYPEDEF_NOT_EXIST = 16,
    E_ERRNO_DATA_TYPE_NOT_EXIST = 17,
    E_ERRNO_OPENNING_BRACKET_NOT_EXPECTED = 18,
    E_ERRNO_CLOSING_BRACKET_EXPECTED = 19,
    E_ERRNO_CLOSING_BRACKET_NOT_EXPECTED = 20,
    E_ERRNO_STRUCT_DUPLICATED = 21,
    E_ERRNO_STRUCT_PROPERTY_NAME_MALFORMED = 22
    E_ERRNO_STRUCT_PROPERTY_DUPLICATED = 23,
    E_ERRNO_INTERFACE_PROPERTIES_SYNTAX_DUPLICATED = 24
    E_ERRNO_INTERFACE_PROPERTY_NAME_MALFORMED = 25
    E_ERRNO_INTERFACE_PROPERTY_DUPLICATED = 26

################################################################################
# Class SdiErrorsCollector
################################################################################
class SdiErrorsCollector:
    ############################################################################
    # __init__
    ############################################################################
    def __init__(self):
        self.__errorsList = []

    ############################################################################
    # __getErrorMsg
    ############################################################################
    def __getErrorMsg(self, sdiFileName, errno, lineNumber):
        oResult = "Error in '" + sdiFileName + "'(" + str(lineNumber) + "): "
        switcher = {
            Errno.E_ERRNO_UNKNOWN_SYNTAX: "Unknown syntax.",
            Errno.E_ERRNO_DIRECTIVE_NOT_EXIST: "The directive does not exist.",
            Errno.E_ERRNO_INCLUDE_MALFORMED: 
                                        "The directive 'include' is malformed.",
            Errno.E_ERRNO_INCLUDE_RECURSION:
                                      "The included file provokes a recursion.",
            Errno.E_ERRNO_INCLUDE_DUPLICATED: "The included file is duplicated",
            Errno.E_ERRNO_INCLUDE_NOT_EXPECTED: 
                                     "The directive 'include' was not expected",
            Errno.E_ERRNO_SDI_FILE_EXPECTED: "A SDI file was expected.",
            Errno.E_ERRNO_SDI_FILE_NOT_EXIST: "The SDI file does not exist.",
            Errno.E_ERRNO_SDI_FILE_INCLUDED_MALFORMED: 
                                        "The included SDI files are malformed.",
            Errno.E_ERRNO_SDI_FILE_INTERFACE_DUPLICATED:
                                 "The interface from a SDI file is duplicated.",
            Errno.E_ERRNO_PRAGMA_MALFORMED: 
                                         "The directive 'pragma' is malformed.",
            Errno.E_ERRNO_PRAGMA_NOT_VALID:
                          "The type's definition is not valid for this pragma.",
            Errno.E_ERRNO_PRAGMA_NOT_EXPECTED: 
                                      "The directive 'pragma' was not expected",
            Errno.E_ERRNO_TYPEDEF_MALFORMED: 
                                          "The type's definition is malformed.",
            Errno.E_ERRNO_TYPEDEF_DUPLICATED: 
                                         "The type's definition is duplicated.",
            Errno.E_ERRNO_TYPEDEF_NOT_EXIST: 
                                        "The type's definition does not exist.",
            Errno.E_ERRNO_DATA_TYPE_NOT_EXIST: "The data type does not exist.",
            Errno.E_ERRNO_OPENNING_BRACKET_NOT_EXPECTED: 
                                                   "It was not expected a '{'.",
            Errno.E_ERRNO_CLOSING_BRACKET_EXPECTED: "It was expected a '};'.",
            Errno.E_ERRNO_CLOSING_BRACKET_NOT_EXPECTED: 
                                                  "It was not expected a '};'.",
            Errno.E_ERRNO_STRUCT_DUPLICATED: "The struct is duplicated.",
            Errno.E_ERRNO_STRUCT_PROPERTY_NAME_MALFORMED:
                "The struct's property name is malformed. It was expected the prefix 'm_' in its name",
            Errno.E_ERRNO_STRUCT_PROPERTY_DUPLICATED: 
                                         "The struct's property is duplicated.",
            Errno.E_ERRNO_INTERFACE_PROPERTIES_SYNTAX_DUPLICATED:
                          "The syntax of interface's properties is duplicated.",
            Errno.E_ERRNO_INTERFACE_PROPERTY_NAME_MALFORMED:
                "The interface's property name is malformed. It was expected the prefix 'm_' in its name",
            Errno.E_ERRNO_INTERFACE_PROPERTY_DUPLICATED:
                                       "The interface's property is duplicated."                                                                
        }

        oResult += switcher.get(errno, "")

        return oResult

    ############################################################################
    # addErrors
    ############################################################################
    def addError(self, sdiFileName, errno, lineNumber):
        self.__errorsList.append(self.__getErrorMsg(sdiFileName, 
                                                    errno, 
                                                    lineNumber))

    ############################################################################
    # printErrors
    ############################################################################
    def printErrors(self):
        for error in(self.__errorsList):
            cprint(error, 'red')