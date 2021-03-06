################################################################################
# SditBuilderBase.py
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
import os
import pwd
from datetime import datetime
from xdg.BaseDirectory import xdg_data_dirs

################################################################################
# Class SdiBuilderBase
################################################################################
class SdiBuilderBase:
    ############################################################################
    # __init__
    ############################################################################
    def __init__(self, regexConstants):
        self.regexConstants = regexConstants
        self.template = ""
        self.placeHoldersMap = {}
        self.templatesPath = xdg_data_dirs[2] + "isdigenerator/templates/"

    ############################################################################
    # __buildMethods
    ############################################################################  
    def __buildMethods(self, indented, propertyName, propertyType):
        placeHoldersMap = {}
        propertyNameRegex = re.compile(self.regexConstants.CSyntaxPropertyName)

        with open(self.templatesPath + "methods_hpp.py_template", "r") as(
                                                                  templateFile):
            template = templateFile.read()

        if(0 < len(template) and 
           None != propertyNameRegex.match(propertyName)):

            methodName = propertyNameRegex.sub("\\g<Property>", propertyName)
            placeHoldersMap["Indented"] = indented
            placeHoldersMap["MethodName"] = methodName.capitalize()
            placeHoldersMap["Author"] = self.placeHoldersMap["Author"]
            placeHoldersMap["GenerationDate"] = self.placeHoldersMap["GenerationDate"]
            placeHoldersMap["PropertyName"] = propertyName
            placeHoldersMap["PropertyType"] = propertyType
            oResult = template.format(**placeHoldersMap)

        return oResult

    ############################################################################
    # __buildAttribute
    ############################################################################  
    def __buildAttribute(self, indented, propertyName, propertyType):
        placeHoldersMap = {}
        
        with open(self.templatesPath + "attribute_hpp.py_template", "r") as(templateFile):
            template = templateFile.read()

        if(0 < len(template)):
            placeHoldersMap["Indented"] = indented
            placeHoldersMap["PropertyName"] = propertyName
            placeHoldersMap["PropertyType"] = propertyType
            oResult = template.format(**placeHoldersMap)

        return oResult

    ############################################################################
    # __isBasicDataType
    ############################################################################
    def __isBasicDataType(self, typeDefinition, originalTypesMap):
        oResult = False
        includedSdiTypeRegex = re.compile(self.regexConstants.CIncludedSdiType)
        syntaxBasicTypesRegex = re.compile(
                                          self.regexConstants.CSyntaxBasicTypes)

        while(typeDefinition in(originalTypesMap)):
            typeDefinition = originalTypesMap[typeDefinition]

        if(None != syntaxBasicTypesRegex.match(typeDefinition)):
            oResult = True
        else:
            includedSdiTypeMatch = includedSdiTypeRegex.match(typeDefinition)
            
            if(None != includedSdiTypeMatch):
                if(None != syntaxBasicTypesRegex.match(
                                                includedSdiTypeMatch.group(2))):
                    oResult = True

        
        return oResult

    ############################################################################
    # buildProperties
    ############################################################################
    def buildProperties(self, itemType, propertiesMap):
        self.placeHoldersMap[itemType + "Methods"] = ""
        self.placeHoldersMap[itemType + "Attributes"] = ""
        propertiesCounter = 0
        indented = ""

        if(self.regexConstants.CItemStruct == itemType):
            indented = (4 * self.regexConstants.CSpace)
        
        for propertyName in(propertiesMap):

            if(0 < propertiesCounter):
                self.placeHoldersMap[itemType + "Methods"] += (2 * self.regexConstants.CCarriageReturn)
                self.placeHoldersMap[itemType + "Attributes"] += (2 * self.regexConstants.CCarriageReturn)
            else:
                self.placeHoldersMap[itemType + "Methods"] = ""
                self.placeHoldersMap[itemType + "Attributes"] = ""

            self.placeHoldersMap[itemType + "Methods"] += self.__buildMethods(
                                                    indented,
                                                    propertyName,
                                                    propertiesMap[propertyName])
            self.placeHoldersMap[itemType + "Attributes"] += self.__buildAttribute(
                                                    indented,
                                                    propertyName,
                                                    propertiesMap[propertyName])
            propertiesCounter += 1

    ############################################################################
    # buildMembersRegistration
    ############################################################################
    def buildMembersRegistration(self,
                                 itemName,
                                 originalTypesMap,
                                 propertiesMap):
        oResult = ""
        placeHoldersMap = {}
        syntaxVectorRegex = re.compile(self.regexConstants.CSyntaxVector)
        syntaxPropertyNameRegex = re.compile(
                                        self.regexConstants.CSyntaxPropertyName)
        propertiesCounter = 0
        
        with open(self.templatesPath + "methods_registration_cpp.py_template", "r") as(templateFile):
            template = templateFile.read()

        if(0 < len(template)):

            for propertyName in(propertiesMap):

                if(0 < propertiesCounter):
                    oResult += (2 * self.regexConstants.CCarriageReturn)

                memberType = self.regexConstants.CMemberTypeSimple
                memberDataType = self.regexConstants.CMemberDataTypeBasic
                finalPropertyType = propertiesMap[propertyName]
                while(finalPropertyType in(originalTypesMap)):
                    finalPropertyType = originalTypesMap[finalPropertyType]

                syntaxVectorMatch = syntaxVectorRegex.match(finalPropertyType)
                if(None != syntaxVectorMatch):

                    memberType = self.regexConstants.CMemberTypeVector
                    isBasicType = self.__isBasicDataType(
                                                     syntaxVectorMatch.group(1),
                                                     originalTypesMap)
                else:
                    isBasicType = self.__isBasicDataType(finalPropertyType,
                                                         originalTypesMap)
                                                    
                if(False == isBasicType):
                    memberDataType = self.regexConstants.CMemberDataTypeStruct

                memberName = syntaxPropertyNameRegex.sub("\\g<Property>", 
                                                         propertyName)
                placeHoldersMap["MemberName_Capatalize"] = memberName.capitalize()
                placeHoldersMap["MemberName"] = memberName
                placeHoldersMap["DataType"] = propertiesMap[propertyName]
                placeHoldersMap["MembeType"] = memberType
                placeHoldersMap["MemberDataType"] = memberDataType
                placeHoldersMap["ItemName"] = itemName
                oResult += template.format(**placeHoldersMap)

                propertiesCounter += 1

        return oResult

    ############################################################################
    # readTemplate
    ############################################################################
    def readTemplate(self, filePath):
        oResult = False

        with open(filePath, "r") as(templateFile):
            self.template = templateFile.read()

        if(0 < len(self.template)):
            oResult = True

        return oResult

    ############################################################################
    # build
    ############################################################################
    def buildCommon(self):
        passwd = pwd.getpwuid(os.getuid())

        if("" != passwd[4]):
            self.placeHoldersMap["Author"] = passwd[4]
        else:
            self.placeHoldersMap["Author"] = passwd[0]

        self.placeHoldersMap["GenerationDate"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.placeHoldersMap["Brief"] = "Generated class"