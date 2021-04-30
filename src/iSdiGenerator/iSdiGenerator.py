#!/usr/bin/python3

################################################################################
# iSdiGenerator.py
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
from SdiArgumentsChecker import SdiArgumentsChecker, Action
from SdiInterfaceParser import SdiInterfaceParser
from SdiErrorsCollector import SdiErrorsCollector

################################################################################
# main
################################################################################
if("__main__" == __name__):
    inputArguments = {}

    if(Action.E_ACTION_GENERATE == SdiArgumentsChecker.Check(inputArguments)):

        interfaceParser = SdiInterfaceParser(inputArguments["sdiFileName"])
        errorsCollector = SdiErrorsCollector()

        if(True == interfaceParser.checkSyntax(errorsCollector)):
            interfaceParser.build(inputArguments["outputDirectory"])
        else:
            errorsCollector.printErrors()
            
    elif(Action.E_ACTION_IMPORT_SDI_LIB == SdiArgumentsChecker.Check(
                                                               inputArguments)):
        print("import")
    else:
        SdiArgumentsChecker.PrintSynopsis()
        