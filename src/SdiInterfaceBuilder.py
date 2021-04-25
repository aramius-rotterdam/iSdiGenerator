################################################################################
# SdiInterfaceBuilder.py
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
import getpass
import re
from datetime import datetime
from SdiRegexConstants import SdiRegexConstants

################################################################################
# Class SdiInterfaceBuilder
################################################################################
class SdiInterfaceBuilder:
    ############################################################################
    # __init__
    ############################################################################
    def __init__(self):
        self.__regexConstants = SdiRegexConstants()
        self.__interfaceTemplate = ""
        self.__includesMap = {}
        self.__interfaceName = ""
        self.__typedefsMap = {}
        self.__originalTypesMap = {}
        self.__specialTypesMap = {}
        self.__placeHoldersMap = {}

    ############################################################################
    # __readTemplate
    ############################################################################
    def __readTemplate(self, fileName):
        oResult = False

        with open(fileName, "r") as(templateFile):
            self.__interfaceTemplate = templateFile.read()

        if(0 < len(self.__interfaceTemplate)):
            oResult = True

        return oResult

    ############################################################################
    # __buildIncludes
    ############################################################################
    def __buildIncludes(self):
        self.__placeHoldersMap["IncludedInterfaces"] = ""
        for key in(self.__includesMap):
            self.__placeHoldersMap["IncludedInterfaces"] += self.__includesMap[key]

    ############################################################################
    # __buildTypes
    ############################################################################
    def __buildTypes(self):
        self.__placeHoldersMap["InterfaceTypes"] = ""
        for key in(self.__typedefsMap):
            typedef = self.__typedefsMap[key]
            if(key in(self.__specialTypesMap)):
                if(key in(self.__originalTypesMap)):
                    typedef = typedef.replace(self.__originalTypesMap[key],
                                              self.__specialTypesMap[key])
            self.__placeHoldersMap["InterfaceTypes"] += typedef

    ############################################################################
    # addInclude
    ############################################################################
    def addInclude(self, includedInterface, include):
        self.__includesMap[includedInterface] = include

    ############################################################################
    # addInterfaceName
    ############################################################################
    def addInterfaceName(self, interfaceName):
        self.__interfaceName = interfaceName

    ############################################################################
    # isTypedefExist
    ############################################################################
    def isTypedefExist(self, typeDefinition):
        return typeDefinition in self.__typedefsMap

    ############################################################################
    # addTypedef
    ############################################################################
    def addTypedef(self, typeDefinition, typedefSyntax):
        self.__typedefsMap[typeDefinition] = typedefSyntax

    ############################################################################
    # addOriginalType
    ############################################################################
    def addOriginalType(self, typeDefinition, originalType):
        self.__originalTypesMap[typeDefinition] = originalType

    ############################################################################
    # addSdiNumber
    ############################################################################    
    def addSdiNumberByRange(self, typeDefinition, minNumber, maxNumber):
        sdiNumber = ""

        if(typeDefinition in(self.__originalTypesMap)):
            if(typeDefinition in(self.__specialTypesMap)):
                sdiNumberRegex = re.compile(self.__regexConstants.CSdiNumber)
                sdiNumberMatch = sdiNumberRegex.match(
                                         self.__specialTypesMap[typeDefinition])

                if(None != sdiNumberMatch):
                    sdiNumber = sdiNumberRegex.sub(
                                         "\\g<SdiNumber>" + 
                                         minNumber + 
                                         ", " + 
                                         maxNumber +
                                         ", " +
                                         "\\g<DefaultNumber>",
                                         self.__specialTypesMap[typeDefinition])
            else:
                sdiNumber = "SdiNumber<"
                sdiNumber += self.__originalTypesMap[typeDefinition]
                sdiNumber += ", "
                sdiNumber += minNumber
                sdiNumber += ", "
                sdiNumber += maxNumber
                sdiNumber += ", "
                sdiNumber += minNumber
                sdiNumber += ">"
            
            self.__specialTypesMap[typeDefinition] = sdiNumber

    ############################################################################
    # addSdiNumber
    ############################################################################    
    def addSdiNumberByDefaultNumber(self, typeDefinition, defultNumber):
        sdiNumber = ""

        if(typeDefinition in(self.__originalTypesMap)):
            if(typeDefinition in(self.__specialTypesMap)):
                sdiNumberRegex = re.compile(self.__regexConstants.CSdiNumber)
                sdiNumberMatch = sdiNumberRegex.match(
                                         self.__specialTypesMap[typeDefinition])

                if(None != sdiNumberMatch):
                    sdiNumber = sdiNumberRegex.sub(
                                "\\g<SdiNumber>\\g<MinNumber>\\g<MaxNumber>" + 
                                defultNumber + ">",
                                self.__specialTypesMap[typeDefinition])
            else:
                sdiNumber = "SdiNumber<"
                sdiNumber += self.__originalTypesMap[typeDefinition]
                sdiNumber += ", "
                sdiNumber += "std::numeric_limits<"
                sdiNumber += self.__originalTypesMap[typeDefinition]
                sdiNumber += ">::min()"
                sdiNumber += ", "
                sdiNumber += "std::numeric_limits<"
                sdiNumber += self.__originalTypesMap[typeDefinition]
                sdiNumber += ">::max()"
                sdiNumber += ", "
                sdiNumber += defultNumber
                sdiNumber += ">"

            self.__specialTypesMap[typeDefinition] = sdiNumber

    ############################################################################
    # build
    ############################################################################
    def build(self):
        if(True == self.__readTemplate("../share/templates/interface.py_template")):
            self.__placeHoldersMap["InterfaceName"] = self.__interfaceName
            self.__placeHoldersMap["Author"] = getpass.getuser()
            self.__placeHoldersMap["GenerationDate"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.__placeHoldersMap["InterfaceName_UpperCase"] = self.__interfaceName.upper()
            self.__placeHoldersMap["InterfaceBrief"] = "Generated class"
            self.__placeHoldersMap["InhiretedInterface"] = ""
            self.__buildIncludes()
            self.__buildTypes()
            self.__placeHoldersMap["InterfaceMethods"] = ""
            self.__placeHoldersMap["InterfaceStructs"] = ""
            self.__placeHoldersMap["InterfaceAttributes"] = ""
            print(self.__interfaceTemplate.format(**self.__placeHoldersMap))