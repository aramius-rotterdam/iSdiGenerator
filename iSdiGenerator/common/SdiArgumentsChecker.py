################################################################################
# SdiArgumentsChecker.py
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
import getopt, sys, os
from termcolor import colored, cprint
from iSdiGenerator.common.SdiAppAction import SdiAppAction

################################################################################
# Class SdiArgumentsChecker
################################################################################
class SdiArgumentsChecker:
    ############################################################################
    # __PrintError
    ############################################################################
    @staticmethod
    def __PrintError(errorMsg):
        print(errorMsg)
        exit(2)
        
    ############################################################################
    # PrintSynopsis 
    ############################################################################
    @staticmethod
    def PrintSynopsis():
        space = " "
        usageText = colored("Usage:" + space, attrs=["bold"])
        orText = colored(3 * space + "or: ", attrs=["bold"])
        usageExample1 = "iSdiGenerator [OPTION]... [-i] DIRECTORY"
        usageExample2 = "iSdiGenerator [OPTION]... [-g] SDI_FILE DIRECTORY"
        description1 = "The first usage, imports the SDI library to the " + \
                       "given directory."
        description2 = "The second usage, generates the C++ file from the " + \
                       "SDI files to the given directory."
        argumentsText = "The mandatory arguments for long options are also " + \
                        "mandatory for short options."
    
        cprint(usageText + usageExample1)
        cprint(orText + usageExample2)
        print(description1)
        print(description2)
        print("")
        print(argumentsText)
        print(2 * space + 
              "-h, --help" + 
              18 * space + 
              "shows the synopsis.")
        print(2 * space + 
              "-f, --force" + 
              17 * space + 
              "forces any action by the tool.")
        print(2 * space + 
              "-i, --import-sdi-lib" + 
              8 * space + 
              "imports the SDI library.")
        print(2 * space + 
              "-g, --generate" + 
              14 * space + 
              "generates the C++ file from SDI files.")

        exit(2)


    ############################################################################
    # Check
    ############################################################################
    @staticmethod
    def Check(inputArguments):
        oResult = SdiAppAction.E_APP_ACTION_NONE
        isForced = False
        appError = sys.argv[0] + ": "
        notExistError = ": No such file or directory."
        notSdiFile = ": It is not a SDI file."
        notOptionError = "unhandled option"

        try:
            optionsList, argumentsList = getopt.getopt(sys.argv[1:], 
                                                       "hfig", 
                                                       ["help",
                                                        "force",
                                                        "import-sdi-lib",
                                                        "generate"])
        except getopt.GetoptError as errorMsg:
            cprint(errorMsg, "red")
            SdiArgumentsChecker.PrintSynopsis()
    
        for option in(optionsList):
            if(option[0] in("-h", "--help")):
                SdiArgumentsChecker.PrintSynopsis()
            elif(option[0] in("-f", "--force")):
                isForced = True
            elif(option[0] in("-i", "--import-sdi-lib")):

                if(1 == len(argumentsList)):

                    if(True == os.path.isdir(argumentsList[0])):

                        if(False == isForced):
                            oResult = SdiAppAction.E_APP_ACTION_IMPORT_SDI_LIB
                        else:
                            oResult = SdiAppAction.E_APP_ACTION_IMPORT_SDI_LIB_FORCE

                    else:
                        SdiArgumentsChecker.__PrintError(appError + 
                                                         argumentsList[0] + 
                                                         notExistError)

                else:
                    SdiArgumentsChecker.PrintSynopsis()
                    

            elif(option[0] in("-g", "--generate")):
                if(2 == len(argumentsList)):

                    if(True == os.path.isfile(argumentsList[0]) and 
                       True == os.path.isdir(argumentsList[1])):

                        file = os.path.splitext(argumentsList[0])

                        if(".sdi" == file[1]):
                            
                            inputArguments["sdiFileName"] = argumentsList[0]
                            inputArguments["outputDirectory"] = argumentsList[1]

                            if(False == isForced):
                                oResult = SdiAppAction.E_APP_ACTION_GENERATE
                            else:
                                oResult = SdiAppAction.E_APP_ACTION_GENERATE_FORCE

                        else:
                            SdiArgumentsChecker.__PrintError(appError + 
                                                             argumentsList[0] + 
                                                             notSdiFile)

                    elif(True == os.path.isdir(argumentsList[1])):
                        SdiArgumentsChecker.__PrintError(appError + 
                                                         argumentsList[0] + 
                                                         notExistError)

                    else:
                        SdiArgumentsChecker.__PrintError(appError + 
                                                         argumentsList[1] + 
                                                         notExistError)

                else:
                    SdiArgumentsChecker.PrintSynopsis()

            else:
                cprint(notOptionError, "red")
    
        return oResult