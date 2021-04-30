################################################################################
# SdiStructBuilder.py
# 
# Copyright (c) 2021 ArAmIuS de Rotterdam <bchowa@gmail.com>
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
from SdiStruct import SdiStruct

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
        self.__builtStructs = ""

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
    # addTypedef
    ############################################################################
    def addTypedef(self, structName, typedefSyntax):
        if(not structName in(self.__typedefsSyntaxMap)):
            self.__typedefsSyntaxMap[structName] = []

        self.__typedefsSyntaxMap[structName].append(typedefSyntax)

    ############################################################################
    # build
    ############################################################################
    def build(self):
        if(True == self.readTemplate(
                               "../../share/templates/struct_hpp.py_template")):

            self.buildCommon()

            for structName in(self.__structsMap):
                self.placeHoldersMap["StructName"] = self.__structsMap[structName].getName()
                self.buildProperties(self.regexConstants.CItemStruct,
                                     self.__structsMap[structName].getPropertiesMap())
                self.__buildTypes(structName)
                self.__builtStructs += self.template.format(
                                                         **self.placeHoldersMap)

    ############################################################################
    # getBuiltStructs
    ############################################################################
    def getBuiltStructs(self):
        return self.__builtStructs