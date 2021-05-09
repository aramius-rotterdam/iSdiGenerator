################################################################################
# main.py
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
from iSdiGenerator.common.SdiAppAction import SdiAppAction
from iSdiGenerator.common.SdiArgumentsChecker import SdiArgumentsChecker
from iSdiGenerator.common.SdiErrorsCollector import SdiErrorsCollector
from iSdiGenerator.parser.SdiInterfaceParser import SdiInterfaceParser
from xdg.BaseDirectory import xdg_data_dirs
import os

################################################################################
# __importLibSdi
################################################################################
def __importLibSdi(outputDirectory):
    libSdiPath = xdg_data_dirs[2] + "isdigenerator/libsdi/"
    os.system("cp " + libSdiPath + "*.hpp " + outputDirectory + "/")

################################################################################
# main
################################################################################
def main():
    if("iSdiGenerator.main" == __name__):
        inputArguments = {}

        if(SdiAppAction.E_APP_ACTION_GENERATE == SdiArgumentsChecker.Check(
                                                               inputArguments)):

            interfaceParser = SdiInterfaceParser(inputArguments["sdiFileName"])
            errorsCollector = SdiErrorsCollector()

            if(True == interfaceParser.checkSyntax(errorsCollector)):
                interfaceParser.build(inputArguments["outputDirectory"])
            else:
                errorsCollector.printErrors()
                exit(2)
            
        elif(SdiAppAction.E_APP_ACTION_IMPORT_SDI_LIB == SdiArgumentsChecker.Check(
                                                               inputArguments)):
            __importLibSdi(inputArguments["outputDirectory"])
        else:
            SdiArgumentsChecker.PrintSynopsis()
        