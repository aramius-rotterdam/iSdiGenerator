################################################################################
# SdiInterfaceBuilder.py
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
import re
from SdiBuilderBase import SdiBuilderBase

################################################################################
# Class SdiInterfaceBuilder
################################################################################
class SdiInterfaceBuilder(SdiBuilderBase):
    ############################################################################
    # __init__
    ############################################################################
    def __init__(self, regexConstants):
        SdiBuilderBase.__init__(self, regexConstants)
        self.__includesMap = {}
        self.__interfaceName = ""
        self.__typesDefinitionList = []
        self.__typedefsSyntaxMap = {}
        self.__originalTypesMap = {}
        self.__specialTypesMap = {}
        self.__propertiesMap = {}

    ############################################################################
    # __buildIncludes
    ############################################################################
    def __buildIncludes(self):
        self.placeHoldersMap["IncludedInterfaces"] = ""
        includesCounter = 0

        for includedInterface in(self.__includesMap):

            if(0 < includesCounter):
                include = self.regexConstants.CCarriageReturn
            else:
                include = ""

            include += self.__includesMap[includedInterface].replace(
                                          self.regexConstants.CExtensionSdi,
                                          self.regexConstants.CExtensionHpp)

            self.placeHoldersMap["IncludedInterfaces"] += include
            includesCounter += 1

    ############################################################################
    # __buildTypes
    ############################################################################
    def __buildTypes(self):
        self.placeHoldersMap["InterfaceTypes"] = ""
        typedefsCounter = 0

        for typeDefinition in(self.__typedefsSyntaxMap):
            
            if(0 < typedefsCounter):
                typedef = self.regexConstants.CCarriageReturn
            else:
                typedef = ""
            
            typedef += (4 * self.regexConstants.CSpace)
            typedef += self.__typedefsSyntaxMap[typeDefinition]
            
            if(typeDefinition in(self.__specialTypesMap)):

                if(typeDefinition in(self.__originalTypesMap)):

                    typedef = typedef.replace(
                                        self.__originalTypesMap[typeDefinition],
                                        self.__specialTypesMap[typeDefinition])

            self.placeHoldersMap["InterfaceTypes"] += typedef
            typedefsCounter += 1

    ############################################################################
    # __writeFile
    ############################################################################
    def __writeFile(self, filePath, fileContent):
        with open(filePath, "w") as(file):
            file.write(fileContent)

    ############################################################################
    # __generateHpp
    ############################################################################
    def __buildHpp(self, builtStructs, fileName, outputDirectory):

        filePath = outputDirectory + self.regexConstants.CSlash 
        filePath += fileName.replace(self.regexConstants.CExtensionSdi, 
                                     self.regexConstants.CExtensionHpp)

        # TODO path is temporary
        if(True == self.readTemplate(
                            "../../share/templates/interface_hpp.py_template")):

            self.buildCommon()
            self.placeHoldersMap["InterfaceName"] = self.__interfaceName
            self.placeHoldersMap["InterfaceName_UpperCase"] = self.__interfaceName.upper()
            self.placeHoldersMap["InhiretedInterface"] = ""
            self.__buildIncludes()
            self.placeHoldersMap["InterfaceStructs"] = builtStructs
            self.__buildTypes()
            self.placeHoldersMap["InterfaceMethods"] = ""
            self.placeHoldersMap["InterfaceAttributes"] = ""
            self.buildProperties(self.regexConstants.CItemInterface,
                                 self.__propertiesMap)

            self.__writeFile(filePath, 
                             self.template.format(**self.placeHoldersMap))

    ############################################################################
    # isIncludeExist
    ############################################################################
    def isIncludeExist(self, includedInterface):
        return includedInterface in(self.__includesMap)

    ############################################################################
    # addInclude
    ############################################################################
    def addInclude(self, includedInterface, include):
        self.__includesMap[includedInterface] = include

    ############################################################################
    # getIncludesMap
    ############################################################################
    def getIncludesMap(self):
        return self.__includesMap

    ############################################################################
    # addInterfaceName
    ############################################################################
    def addInterfaceName(self, interfaceName):
        self.__interfaceName = interfaceName

    ############################################################################
    # getInterfaceName
    ############################################################################
    def getInterfaceName(self):
        return self.__interfaceName

    ############################################################################
    # isTypeDefinitionExist
    ############################################################################
    def isTypeDefinitionExist(self, typeDefinition):
        return typeDefinition in(self.__typesDefinitionList)

    ############################################################################
    # addTypeDefinition
    ############################################################################
    def addTypeDefinition(self, typeDefinition):
        self.__typesDefinitionList.append(typeDefinition)

    ############################################################################
    # getTypesDefinitionList
    ############################################################################
    def getTypesDefinitionList(self):
        return self.__typesDefinitionList

    ############################################################################
    # isTypedefSyntaxExist
    ############################################################################
    def isTypedefSyntaxExist(self, typeDefinition):
        return typeDefinition in(self.__typedefsSyntaxMap)

    ############################################################################
    # addTypedef
    ############################################################################
    def addTypedef(self, typeDefinition, typedefSyntax):
        self.__typedefsSyntaxMap[typeDefinition] = typedefSyntax

    ############################################################################
    # isOriginalTypeExist
    ############################################################################
    def isOriginalTypeExist(self, typeDefinition):
        return typeDefinition in(self.__originalTypesMap)

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

                sdiNumberRegex = re.compile(self.regexConstants.CSdiNumber)
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

                sdiNumberRegex = re.compile(self.regexConstants.CSdiNumber)
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
    # isPropertyExist
    ############################################################################
    def isPropertyExist(self, propertyName):
        return propertyName in(self.__propertiesMap)

    ############################################################################
    # addProperty
    ############################################################################
    def addProperty(self, propertyName, propertyType):
        self.__propertiesMap[propertyName] = propertyType

    ############################################################################
    # build
    ############################################################################
    def build(self, builtStructs, fileName, outputDirectory):
        self.__buildHpp(builtStructs, fileName, outputDirectory)
        