################################################################################
# SdiInterfacePropertiesParser.py
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
from iSdiGenerator.common.SdiErrorsCollector import SdiErrno
from iSdiGenerator.parser.SdiParserBase import SdiParserBase

################################################################################
# Class SdiInterfacePropertiesParser
################################################################################
class SdiInterfacePropertiesParser(SdiParserBase):
    ############################################################################
    # __init__
    ############################################################################
    def __init__(self, interfaceBuilder):
        SdiParserBase.__init__(self)
        self.__interfaceBuilder = interfaceBuilder

    ############################################################################
    # __parseSyntaxInterfaceProperties
    ############################################################################
    def __parseSyntaxInterfaceProperties(self, 
                                         line, 
                                         regexMap, 
                                         syntaxIndicatorsMap):
        dummyItem = None

        if(False == syntaxIndicatorsMap["isInterfacePropertiesFound"]):
            dummyItem = self.parseSyntaxItem(
                                   self.regexConstants.CItemInterfaceProperties, 
                                   line, 
                                   regexMap, 
                                   syntaxIndicatorsMap)

    ############################################################################
    # __isUnknownSyntax
    ############################################################################
    def __isUnknownSyntax(self, line, syntaxIndicatorsMap, errno):
        oResult = False

        if((self.regexConstants.CClosingBracket +
            self.regexConstants.CSemiColon != line) and
           "" != line and
           False == syntaxIndicatorsMap["isInterfaceProperties"] and
           False == syntaxIndicatorsMap["isProperty"] and
           False == syntaxIndicatorsMap["isOpeneningBracket"] and
            SdiErrno.E_ERRNO_NONE == errno):

            oResult = True

        return oResult

    ############################################################################
    # __parseInterfacePropertiesBlock
    ############################################################################
    def __parseInterfacePropertiesBlock(self, 
                                        line, 
                                        regexMap, 
                                        syntaxIndicatorsMap):
        oResult = SdiErrno.E_ERRNO_NONE
        syntaxPropertyMatch = regexMap["syntaxProperty"].match(line)

        if((self.regexConstants.CClosingBracket +
            self.regexConstants.CSemiColon != line) and
           True == syntaxIndicatorsMap["hasOpenedInterfacePropertiesBracket"] and
           None != syntaxPropertyMatch):

            propertyName = syntaxPropertyMatch.group(70)
            propertyType = syntaxPropertyMatch.group(1)
            syntaxBasicTypesMatch = regexMap["syntaxBasicTypes"].match(
                                                                   propertyType)
            syntaxVectorMatch = regexMap["syntaxVector"].match(propertyType)

            if(None != regexMap["syntaxPropertyName"].match(propertyName)):

                if(False == self.__interfaceBuilder.isPropertyExist(
                                                                 propertyName)):

                    if(None != syntaxBasicTypesMatch):
            
                        self.__interfaceBuilder.addProperty(propertyName, 
                                                            propertyType)
                        syntaxIndicatorsMap["isProperty"] = True

                    elif(None != syntaxVectorMatch):
                
                        syntaxBasicTypesMatch = regexMap["syntaxBasicTypes"].match(
                                             syntaxVectorMatch.group(1).strip())
        
                        if(None != syntaxBasicTypesMatch or
                           True == self.__interfaceBuilder.isTypeDefinitionExist(
                                                   syntaxVectorMatch.group(1))):
                
                            self.__interfaceBuilder.addProperty(propertyName, 
                                                                propertyType)
                            syntaxIndicatorsMap["isProperty"] = True

                        else:
                            oResult = SdiErrno.E_ERRNO_DATA_TYPE_NOT_EXIST

                    elif(True == self.__interfaceBuilder.isTypeDefinitionExist(
                                                         propertyType.strip())):

                        self.__interfaceBuilder.addProperty(propertyName, 
                                                            propertyType)
                        syntaxIndicatorsMap["isProperty"] = True
                    else:
                        oResult = SdiErrno.E_ERRNO_DATA_TYPE_NOT_EXIST
                else:
                    oResult = SdiErrno.E_ERRNO_INTERFACE_PROPERTY_DUPLICATED
            else:
                oResult = SdiErrno.E_ERRNO_INTERFACE_PROPERTY_NAME_MALFORMED
        
        elif(self.regexConstants.CClosingBracket +
             self.regexConstants.CSemiColon == line):
            syntaxIndicatorsMap["hasOpenedInterfacePropertiesBracket"] = False

        return oResult

    ############################################################################
    # checkSyntax
    ############################################################################
    def checkSyntax(self, fileLines, lineOffset):
        oResult = SdiErrno.E_ERRNO_NONE
        regexMap = {
            "inlineComment": re.compile(self.regexConstants.CInlineComment),
            "openingMultiComment": re.compile(
                                      self.regexConstants.COpeningMultiComment),
            "closingMultiComment": re.compile(
                                      self.regexConstants.CClosingMultiComment),
            "syntaxInterfaceProperties": re.compile(
                                self.regexConstants.CSyntaxInterfaceProperties),
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
            "isInterfaceProperties": False,
            "isInterfacePropertiesFound": False,
            "isProperty": False,
            "isOpeneningBracket": False,
            "hasOpenedInterfacePropertiesBracket": False,
        }
        
        for lineNumber in(range(lineOffset, len(fileLines))):
            syntaxIndicatorsMap["isComment"] = False
            syntaxIndicatorsMap["isInterfaceProperties"] = False
            syntaxIndicatorsMap["isProperty"] = False
            syntaxIndicatorsMap["isOpeneningBracket"] = False
            line = fileLines[lineNumber].strip()

            # Parses comments
            self.parseComments(line, regexMap, syntaxIndicatorsMap)

            # Checks the line is not a commentary, and there is not 
            # an opened multi commentary. In this case, parses syntax struct.
            if(False == syntaxIndicatorsMap["isComment"] and 
               False == syntaxIndicatorsMap["hasOpenedMultiComment"]):
                
                if(False == syntaxIndicatorsMap["isInterfacePropertiesFound"]):
                    self.__parseSyntaxInterfaceProperties(line,
                                                          regexMap,
                                                          syntaxIndicatorsMap)

                # Checks the interface properties was found. In this case, 
                # parses the block beginning.
                if(True == syntaxIndicatorsMap["isInterfacePropertiesFound"] and 
                   SdiErrno.E_ERRNO_NONE == oResult):
                
                    oResult = self.parseSyntaxBlockOpening(
                                   self.regexConstants.CItemInterfaceProperties,
                                   line,
                                   syntaxIndicatorsMap)

                # Checks the line is not interface properties syntax and 
                # that this syntax was found before. Also checks the line 
                # is not a openning bracket and that was found before.
                # In this case, parses the struct block.
                if(False == syntaxIndicatorsMap["isInterfaceProperties"] and
                   True == syntaxIndicatorsMap["isInterfacePropertiesFound"] and
                   False == syntaxIndicatorsMap["isOpeneningBracket"] and
                   True == syntaxIndicatorsMap["hasOpenedInterfacePropertiesBracket"] and
                   SdiErrno.E_ERRNO_NONE == oResult):

                    oResult = self.__parseInterfacePropertiesBlock(
                                                            line,
                                                            regexMap,
                                                            syntaxIndicatorsMap)

                    if(False == syntaxIndicatorsMap["hasOpenedInterfacePropertiesBracket"]):
                        break

                # Checks is unknown syntax.
                if(True == self.__isUnknownSyntax(line, 
                                                  syntaxIndicatorsMap,
                                                  oResult)):
                    oResult = SdiErrno.E_ERRNO_UNKNOWN_SYNTAX
            
            if(SdiErrno.E_ERRNO_NONE != oResult):
                break

        # Checks whether the closing interface properties block exists.
        if(True == syntaxIndicatorsMap["hasOpenedInterfacePropertiesBracket"] and
           SdiErrno.E_ERRNO_NONE == oResult):
            oResult = SdiErrno.E_ERRNO_CLOSING_BRACKET_EXPECTED

        return oResult, lineNumber