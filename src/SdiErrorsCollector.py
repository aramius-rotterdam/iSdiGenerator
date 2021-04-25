################################################################################
# SdiErrorsCollector.py
# 
# Copyright 2016 ArAmIuS de Rotterdam <bchowa@gmail.com>
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
    E_ERRNO_SDI_FILE_EXPECTED = 4,
    E_ERRNO_PRAGMA_MALFORMED = 5,
    E_ERRNO_INCLUDE_NOT_EXPECTED = 6,
    E_ERRNO_PRAGMA_NOT_EXPECTED = 7,
    E_ERRNO_OPENNING_BRACKET_NOT_EXPECTED = 8,
    E_ERRNO_CLOSING_BRACKET_EXPECTED = 9,
    E_ERRNO_TYPEDEF_MALFORMED = 10,
    E_ERRNO_TYPEDEF_DUPLICATE = 11,
    E_ERRNO_DATA_TYPE_NOT_EXIST = 12,
    E_ERRNO_TYPEDEF_NOT_EXIST = 13

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
            Errno.E_ERRNO_SDI_FILE_EXPECTED: "A SDI file was expected.",
            Errno.E_ERRNO_PRAGMA_MALFORMED: 
                                         "The directive 'pragma' is malformed.",
            Errno.E_ERRNO_INCLUDE_NOT_EXPECTED: 
                                     "The directive 'include' was not expected",
            Errno.E_ERRNO_PRAGMA_NOT_EXPECTED: 
                                      "The directive 'pragma' was not expected",
            Errno.E_ERRNO_OPENNING_BRACKET_NOT_EXPECTED: 
                                                   "It was not expected a '{'.",
            Errno.E_ERRNO_CLOSING_BRACKET_EXPECTED: "It was expected a '};'.",
            Errno.E_ERRNO_TYPEDEF_MALFORMED: 
                                          "The type's definition is malformed.",
            Errno.E_ERRNO_TYPEDEF_DUPLICATE: 
                                          "The type's definition is duplicate.",
            Errno.E_ERRNO_DATA_TYPE_NOT_EXIST: "The data type does not exist.",
            Errno.E_ERRNO_TYPEDEF_NOT_EXIST: 
                                        "The type's definition does not exist."
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