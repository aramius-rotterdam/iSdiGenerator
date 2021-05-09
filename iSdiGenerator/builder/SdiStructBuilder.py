################################################################################
# SdiStructBuilder.py
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
from iSdiGenerator.common.SdiStruct import SdiStruct
from iSdiGenerator.builder.SdiBuilderBase import SdiBuilderBase

################################################################################
# Class SdiStructBuilder
################################################################################
class SdiStructBuilder(SdiBuilderBase):
    ############################################################################
    # __init__
    ############################################################################
    def __init__(self, regexConstants):
        SdiBuilderBase.__init__(self, regexConstants)
        self.__structsMap = {}
        self.__typedefsSyntaxMap = {}
        self.__builtStructsHpp = ""
        self.__builtStructsCpp = ""

    ############################################################################
    # __buildTypes
    ############################################################################
    def __buildTypes(self, structName):
        self.placeHoldersMap["InterfaceTypes"] = ""
        typedefsCounter = 0

        if(structName in(self.__typedefsSyntaxMap)):
            for typedefSyntax in(self.__typedefsSyntaxMap[structName]):
            
                if(0 < typedefsCounter):
                    typedef = self.regexConstants.CCarriageReturn
                else:
                    typedef = ""
            
                typedef += (4 * self.regexConstants.CSpace)
                typedef += typedefSyntax

                self.placeHoldersMap["InterfaceTypes"] += typedef
                typedefsCounter += 1

    ############################################################################
    # isStructExist
    ############################################################################
    def isStructExist(self, structName):
        return structName in(self.__structsMap)

    ############################################################################
    # addStruct
    ############################################################################
    def addStruct(self, struct):
        self.__structsMap[struct.getName()] = struct

    ############################################################################
    # getStruct
    ############################################################################
    def getStruct(self, structName):
        oResult = None

        if(structName in(self.__structsMap)):
            oResult = self.__structsMap[structName]

        return oResult

    ############################################################################
    # addTypedefSyntax
    ############################################################################
    def addTypedefSyntax(self, structName, typedefSyntax):
        if(not structName in(self.__typedefsSyntaxMap)):
            self.__typedefsSyntaxMap[structName] = []

        self.__typedefsSyntaxMap[structName].append(typedefSyntax)

    ############################################################################
    # __buildHpp
    ############################################################################
    def __buildHpp(self):

        if(True == self.readTemplate(
                                self.templatesPath + "struct_hpp.py_template")):

            self.buildCommon()

            for structName in(self.__structsMap):
                self.placeHoldersMap["StructName"] = self.__structsMap[structName].getName()
                self.buildProperties(self.regexConstants.CItemStruct,
                                     self.__structsMap[structName].getPropertiesMap())
                self.__buildTypes(structName)
                self.__builtStructsHpp += self.template.format(
                                                         **self.placeHoldersMap)

    ############################################################################
    # __buildCpp
    ############################################################################
    def __buildCpp(self, interfaceName, originalTypesMap):
        propertiesCounter = 0

        if(True == self.readTemplate(
                self.templatesPath + "struct_cpp.py_template")):

            for structName in(self.__structsMap):
                
                if(0 < propertiesCounter):
                    self.__builtStructsCpp += (2 * self.regexConstants.CCarriageReturn)

                propertiesMap = self.__structsMap[structName].getPropertiesMap()

                self.placeHoldersMap["InterfaceName"] = interfaceName
                self.placeHoldersMap["StructName"] = structName
                methodsRegistration = self.buildMembersRegistration(structName,
                                              originalTypesMap,
                                              propertiesMap)
                self.placeHoldersMap["MethodsRegistration"] = methodsRegistration                                     
                self.__builtStructsCpp += self.template.format(
                                                         **self.placeHoldersMap)

                propertiesCounter += 1

    ############################################################################
    # build
    ############################################################################
    def build(self, interfaceName, originalTypesMap):
        self.__buildHpp()
        self.__buildCpp(interfaceName, originalTypesMap)

    ############################################################################
    # getBuiltStructsHpp
    ############################################################################
    def getBuiltStructsHpp(self):
        return self.__builtStructsHpp

    ############################################################################
    # getBuiltStructsCpp
    ############################################################################
    def getBuiltStructsCpp(self):
        return self.__builtStructsCpp