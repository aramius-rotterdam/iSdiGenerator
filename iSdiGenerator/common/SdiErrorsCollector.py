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
from termcolor import cprint
from iSdiGenerator.common.SdiErrno import SdiErrno

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
            SdiErrno.E_ERRNO_UNKNOWN_SYNTAX: "Unknown syntax.",
            SdiErrno.E_ERRNO_DIRECTIVE_NOT_EXIST: 
                                                "The directive does not exist.",
            SdiErrno.E_ERRNO_INCLUDE_MALFORMED: 
                                        "The directive 'include' is malformed.",
            SdiErrno.E_ERRNO_INCLUDE_RECURSION:
                                      "The included file provokes a recursion.",
            SdiErrno.E_ERRNO_INCLUDE_DUPLICATED: 
                                              "The included file is duplicated",
            SdiErrno.E_ERRNO_INCLUDE_NOT_EXPECTED: 
                                     "The directive 'include' was not expected",
            SdiErrno.E_ERRNO_SDI_FILE_EXPECTED: "A SDI file was expected.",
            SdiErrno.E_ERRNO_SDI_FILE_NOT_EXIST: "The SDI file does not exist.",
            SdiErrno.E_ERRNO_SDI_FILE_INCLUDED_MALFORMED: 
                                        "The included SDI files are malformed.",
            SdiErrno.E_ERRNO_SDI_FILE_INTERFACE_DUPLICATED:
                                 "The interface from a SDI file is duplicated.",
            SdiErrno.E_ERRNO_PRAGMA_MALFORMED: 
                                         "The directive 'pragma' is malformed.",
            SdiErrno.E_ERRNO_PRAGMA_NOT_VALID:
                          "The type's definition is not valid for this pragma.",
            SdiErrno.E_ERRNO_PRAGMA_NOT_EXPECTED: 
                                      "The directive 'pragma' was not expected",
            SdiErrno.E_ERRNO_TYPEDEF_MALFORMED: 
                                          "The type's definition is malformed.",
            SdiErrno.E_ERRNO_TYPEDEF_DUPLICATED: 
                                         "The type's definition is duplicated.",
            SdiErrno.E_ERRNO_TYPEDEF_NOT_EXIST: 
                                        "The type's definition does not exist.",
            SdiErrno.E_ERRNO_DATA_TYPE_NOT_EXIST: 
                                                "The data type does not exist.",
            SdiErrno.E_ERRNO_OPENNING_BRACKET_NOT_EXPECTED: 
                                                   "It was not expected a '{'.",
            SdiErrno.E_ERRNO_CLOSING_BRACKET_EXPECTED: 
                                                      "It was expected a '};'.",
            SdiErrno.E_ERRNO_CLOSING_BRACKET_NOT_EXPECTED: 
                                                  "It was not expected a '};'.",
            SdiErrno.E_ERRNO_STRUCT_DUPLICATED: "The struct is duplicated.",
            SdiErrno.E_ERRNO_STRUCT_PROPERTY_NAME_MALFORMED:
                "The struct's property name is malformed. It was expected the prefix 'm_' in its name",
            SdiErrno.E_ERRNO_STRUCT_PROPERTY_DUPLICATED: 
                                         "The struct's property is duplicated.",
            SdiErrno.E_ERRNO_INTERFACE_PROPERTIES_SYNTAX_DUPLICATED:
                          "The syntax of interface's properties is duplicated.",
            SdiErrno.E_ERRNO_INTERFACE_PROPERTY_NAME_MALFORMED:
                "The interface's property name is malformed. It was expected the prefix 'm_' in its name",
            SdiErrno.E_ERRNO_INTERFACE_PROPERTY_DUPLICATED:
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