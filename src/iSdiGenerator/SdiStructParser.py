################################################################################
# SdiStructParser.py
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
from SdiParserBase import SdiParserBase
from SdiStruct import SdiStruct
from SdiStructBuilder import SdiStructBuilder
from SdiErrorsCollector import Errno

################################################################################
# Class SdiStructParser
################################################################################
class SdiStructParser(SdiParserBase):
    ############################################################################
    # __init__
    ############################################################################
    def __init__(self, interfaceBuilder):
        SdiParserBase.__init__(self)
        self.__structBuilder = SdiStructBuilder(self.regexConstants)
        self.__interfaceBuilder = interfaceBuilder

    ############################################################################
    # __parseSyntaxStruct
    ############################################################################
    def __parseSyntaxStruct(self, line, regexMap, syntaxIndicatorsMap):
        oResult = Errno.E_ERRNO_NONE
        structName = None

        structName = self.parseSyntaxItem(self.regexConstants.CItemStruct, 
                                          line, 
                                          regexMap, 
                                          syntaxIndicatorsMap)

        if(None != structName):
            struct = SdiStruct(structName)

            if(None == self.__structBuilder.getStruct(structName)):
                self.__structBuilder.addStruct(struct)
                self.__interfaceBuilder.addTypeDefinition(structName)
            else:
                oResult = Errno.E_ERRNO_STRUCT_DUPLICATED

        return oResult, structName

    ############################################################################
    # __parseStructBlock
    ############################################################################
    def __parseStructBlock(self, 
                           line, 
                           regexMap, 
                           syntaxIndicatorsMap, 
                           structName):
        oResult = Errno.E_ERRNO_NONE
        syntaxPropertyMatch = regexMap["syntaxProperty"].match(line)
        
        if((self.regexConstants.CClosingBracket +
            self.regexConstants.CSemiColon != line) and
            True == syntaxIndicatorsMap["hasOpenedStructBracket"] and
            None != syntaxPropertyMatch):

            propertyName = syntaxPropertyMatch.group(69)
            propertyType = syntaxPropertyMatch.group(1)
            syntaxBasicTypesMatch = regexMap["syntaxBasicTypes"].match(
                                                                   propertyType)
            syntaxVectorMatch = regexMap["syntaxVector"].match(propertyType)

            if(None != structName):
                struct = self.__structBuilder.getStruct(structName)

                if(None != struct):
                    if(None != regexMap["syntaxPropertyName"].match(
                                                                 propertyName)):

                        if(False == struct.isPropertyExist(propertyName)):

                            if(None != syntaxBasicTypesMatch):
                        
                                struct.addProperty(propertyName, 
                                                   propertyType)
                                syntaxIndicatorsMap["isProperty"] = True

                            elif(None != syntaxVectorMatch):
                            
                                syntaxBasicTypesMatch = regexMap["syntaxBasicTypes"].match(
                                             syntaxVectorMatch.group(1).strip())
                    
                                if(None != syntaxBasicTypesMatch or
                                   True == self.__interfaceBuilder.isTypeDefinitionExist(
                                                   syntaxVectorMatch.group(1))):
                            
                                    struct.addProperty(propertyName, 
                                                       propertyType)
                                    syntaxIndicatorsMap["isProperty"] = True

                                else:
                                    oResult = Errno.E_ERRNO_DATA_TYPE_NOT_EXIST

                            elif(True == self.__interfaceBuilder.isTypeDefinitionExist(
                                                        propertyType.strip())):

                                struct.addProperty(propertyName, 
                                                   propertyType)
                                syntaxIndicatorsMap["isProperty"] = True
                            else:
                                oResult = Errno.E_ERRNO_DATA_TYPE_NOT_EXIST
                        else:
                            oResult = Errno.E_ERRNO_STRUCT_PROPERTY_DUPLICATED
                    else:
                        oResult = Errno.E_ERRNO_STRUCT_PROPERTY_NAME_MALFORMED
                    

        elif(self.regexConstants.CClosingBracket +
             self.regexConstants.CSemiColon == line):
            syntaxIndicatorsMap["hasOpenedStructBracket"] = False

        return oResult

    ############################################################################
    # __isUnknownSyntax
    ############################################################################
    def __isUnknownSyntax(self, line, syntaxIndicatorsMap, errno):
        oResult = False

        if((self.regexConstants.CClosingBracket +
            self.regexConstants.CSemiColon != line) and
            "" != line and
            False == syntaxIndicatorsMap["isStruct"] and
            False == syntaxIndicatorsMap["isProperty"] and
            False == syntaxIndicatorsMap["isOpeneningBracket"] and
            Errno.E_ERRNO_NONE == errno):

            oResult = True

        return oResult

    ############################################################################
    # checkSyntax
    ############################################################################
    def checkSyntax(self, fileLines, lineOffset):
        oResult = Errno.E_ERRNO_NONE
        structName = None
        regexMap = {
            "inlineComment": re.compile(self.regexConstants.CInlineComment),
            "openingMultiComment": re.compile(
                                      self.regexConstants.COpeningMultiComment),
            "closingMultiComment": re.compile(
                                      self.regexConstants.CClosingMultiComment),
            "syntaxStruct": re.compile(self.regexConstants.CSyntaxStruct),
            "syntaxProperty": re.compile(self.regexConstants.CSyntaxProperty),
            "syntaxPropertyName": re.compile(
                                       self.regexConstants.CSyntaxPropertyName),
            "syntaxBasicTypes": re.compile(
                                         self.regexConstants.CSyntaxBasicTypes),
            "syntaxVector": re.compile(self.regexConstants.CSyntaxVector)                                         
        }
        syntaxIndicatorsMap = {
            "isComment": False,
            "hasOpenedMultiComment": False,
            "isStruct": False,
            "isStructFound": False,
            "isProperty": False,
            "isOpeneningBracket": False,
            "hasOpenedStructBracket": False,
        }

        for lineNumber in(range(lineOffset, len(fileLines))):
            syntaxIndicatorsMap["isComment"] = False
            syntaxIndicatorsMap["isStruct"] = False
            syntaxIndicatorsMap["isProperty"] = False
            syntaxIndicatorsMap["isOpeneningBracket"] = False
            line = fileLines[lineNumber].strip()

            # Parses comments
            self.parseComments(line,  regexMap, syntaxIndicatorsMap)

            # Checks the line is not a commentary, and there is not 
            # an opened multi commentary. In this case, parses syntax struct.
            if(False == syntaxIndicatorsMap["isComment"] and 
               False == syntaxIndicatorsMap["hasOpenedMultiComment"]):

                if(False == syntaxIndicatorsMap["isStructFound"]):
                    oResult, structName = self.__parseSyntaxStruct(
                                                            line, 
                                                            regexMap, 
                                                            syntaxIndicatorsMap)

                # Checks the struct was found. In this case, parses the block
                # beginning.
                if(True == syntaxIndicatorsMap["isStructFound"] and 
                   Errno.E_ERRNO_NONE == oResult):
                
                    oResult = self.parseSyntaxBlockOpening(
                                                self.regexConstants.CItemStruct,
                                                line,
                                                syntaxIndicatorsMap)

                # Checks the line is not struct syntax and that this 
                # syntax was found before. Also checks the line is not a 
                # openning bracket and that was found before.
                # In this case, parses the struct block.
                if(False == syntaxIndicatorsMap["isStruct"] and
                   True == syntaxIndicatorsMap["isStructFound"] and
                   False == syntaxIndicatorsMap["isOpeneningBracket"] and
                   True == syntaxIndicatorsMap["hasOpenedStructBracket"] and
                   Errno.E_ERRNO_NONE == oResult):

                    oResult = self.__parseStructBlock(line,
                                                      regexMap,
                                                      syntaxIndicatorsMap,
                                                      structName)

                    if(False == syntaxIndicatorsMap["hasOpenedStructBracket"]):
                        break

                # Checks is unknown syntax.
                if(True == self.__isUnknownSyntax(line, 
                                                  syntaxIndicatorsMap,
                                                  oResult)):
                    oResult = Errno.E_ERRNO_UNKNOWN_SYNTAX

            if(Errno.E_ERRNO_NONE != oResult):
                break

        # Checks whether the closing struct block exists.
        if(True == syntaxIndicatorsMap["hasOpenedStructBracket"] and
           Errno.E_ERRNO_NONE == oResult):
            oResult = Errno.E_ERRNO_CLOSING_BRACKET_EXPECTED

        return oResult, lineNumber

    ############################################################################
    # isStructExist
    ############################################################################
    def isStructExist(self, structName):
        return self.__structBuilder.isStructExist(structName)

    ############################################################################
    # addTypedef
    ############################################################################
    def addTypedef(self, typeDefinition, typedefSyntax):
        self.__structBuilder.addTypedef(typeDefinition, typedefSyntax)

    ############################################################################
    # build
    ############################################################################
    def build(self):
        self.__structBuilder.build()
        return self.__structBuilder.getBuiltStructs()