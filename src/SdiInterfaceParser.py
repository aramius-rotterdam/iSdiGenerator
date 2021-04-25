################################################################################
# SdiInterfaceParser.py
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
import re
from SdiInterfaceBuilder import SdiInterfaceBuilder
from SdiRegexConstants import SdiRegexConstants
from SdiErrorsCollector import Errno

################################################################################
# Class SdiInterfaceParser
################################################################################
class SdiInterfaceParser:
    ############################################################################
    # __init__
    ############################################################################
    def __init__(self, sdiFileName):
        self.__sdiFileName = sdiFileName
        self.__interfaceBuilder = SdiInterfaceBuilder()
        self.__regexConstants = SdiRegexConstants()

    ############################################################################
    # __parseComments
    ############################################################################
    def __parseComments(self, line, regexMap, syntaxIndicatorsMap):
        if(None != regexMap["inlineComment"].match(line)):
            syntaxIndicatorsMap["isComment"] = True
        elif(None != regexMap["openingMultiComment"].match(line)):
            syntaxIndicatorsMap["hasOpenedMultiComment"] = True
        elif(True == syntaxIndicatorsMap["hasOpenedMultiComment"] and 
             None != regexMap["closingMultiComment"].match(line)):
            syntaxIndicatorsMap["hasOpenedMultiComment"] = False
            syntaxIndicatorsMap["isComment"] = True

    ############################################################################
    # __parseIncludes
    ############################################################################
    def __parseIncludes(self, line, regexMap, syntaxIndicatorsMap):
        oResult = Errno.E_ERRNO_NONE
        
        if(None != regexMap["directiveBeginning"].match(line) and
           None == regexMap["directivePragma"].match(line)):
            if(None != regexMap["directiveInclude"].match(line)):
                completeIncludeMatch = regexMap["completeInclude"].match(line)
                if(None != completeIncludeMatch):
                    fileIncludeMatch = regexMap["fileInclude"].match(
                                                  completeIncludeMatch.group(3))

                    if(None != fileIncludeMatch):
                        self.__interfaceBuilder.addInclude(
                                                      fileIncludeMatch.group(1), 
                                                      line)
                        syntaxIndicatorsMap["isInclude"] = True

                        if(True == syntaxIndicatorsMap["isInterfaceFound"]):
                            oResult = Errno.E_ERRNO_INCLUDE_NOT_EXPECTED
                    else:
                        oResult = Errno.E_ERRNO_SDI_FILE_EXPECTED
                else:
                    oResult = Errno.E_ERRNO_INCLUDE_MALFORMED
            else:
                oResult = Errno.E_ERRNO_DIRECTIVE_NOT_EXIST

        return oResult

    ############################################################################
    # __parseSyntaxInterface
    ############################################################################
    def __parseSyntaxInterface(self, line, regexMap, syntaxIndicatorsMap):
        oResult = Errno.E_ERRNO_NONE
        interfaceMatch = regexMap["syntaxInterface"].match(line)

        if(None != interfaceMatch):
            self.__interfaceBuilder.addInterfaceName(interfaceMatch.group(2))
            syntaxIndicatorsMap["isInterface"] = True
            syntaxIndicatorsMap["isInterfaceFound"] = True
            if(self.__regexConstants.COpeningBracket == line[len(line) - 1]):
                syntaxIndicatorsMap["hasOpenedInterfaceBracket"] = True
        elif(self.__regexConstants.COpeningBracket == line and 
             True == syntaxIndicatorsMap["hasOpenedInterfaceBracket"]):
            oResult = Errno.E_ERRNO_OPENNING_BRACKET_NOT_EXPECTED
        elif(self.__regexConstants.COpeningBracket == line):
            syntaxIndicatorsMap["hasOpenedInterfaceBracket"] = True
            syntaxIndicatorsMap["isOpeneningBracket"] = True

        return oResult

    ############################################################################
    # __parseSyntaxTypedef
    ############################################################################
    def __parseSyntaxTypedef(self, line, regexMap, syntaxIndicatorsMap):
        oResult = Errno.E_ERRNO_NONE
        syntaxTypedefMatch = regexMap["syntaxTypedef"].match(line)
        typedefSyntax = ""

        if(None != regexMap["typedefBeginning"].match(line)):
            if(None != syntaxTypedefMatch):
                syntaxBasicTypesMatch = regexMap["syntaxBasicTypes"].match(
                                            syntaxTypedefMatch.group(1).strip())
                syntaxVectorMatch = regexMap["syntaxVector"].match(
                                            syntaxTypedefMatch.group(1).strip())
                typeDefinition = syntaxTypedefMatch.group(7)
                typedefSyntax = re.sub(" +", self.__regexConstants.CSpace, line)
                typedefSyntax = re.sub(self.__regexConstants.CSemiColon, 
                                       "", 
                                       typedefSyntax)
                typedefSyntax = typedefSyntax.strip()
                typedefSyntax += self.__regexConstants.CSemiColon
                typedefSyntax += self.__regexConstants.CCarriageReturn
                typedefSyntax = (4 * self.__regexConstants.CSpace) + typedefSyntax
            
                if(None != syntaxBasicTypesMatch):
                    if(False == self.__interfaceBuilder.isTypedefExist(
                                                               typeDefinition)):
                        self.__interfaceBuilder.addTypedef(typeDefinition, 
                                                           typedefSyntax)
                        self.__interfaceBuilder.addOriginalType(typeDefinition,
                                                                syntaxBasicTypesMatch.group(1))
                        syntaxIndicatorsMap["isTypedef"] = True
                    else:
                        oResult = Errno.E_ERRNO_TYPEDEF_DUPLICATE
                elif(None != syntaxVectorMatch):
                    syntaxBasicTypesMatch = regexMap["syntaxBasicTypes"].match(
                                                     syntaxVectorMatch.group(1))
                    if(None != syntaxBasicTypesMatch or
                       True == self.__interfaceBuilder.isTypedefExist(
                                                   syntaxVectorMatch.group(1))):
                        if(False == self.__interfaceBuilder.isTypedefExist(
                                                               typeDefinition)):
                            self.__interfaceBuilder.addTypedef(typeDefinition, 
                                                               typedefSyntax)
                            syntaxIndicatorsMap["isTypedef"] = True
                        else:
                            oResult = Errno.E_ERRNO_TYPEDEF_DUPLICATE
                    else:
                        oResult = Errno.E_ERRNO_DATA_TYPE_NOT_EXIST
                else:
                    oResult = Errno.E_ERRNO_DATA_TYPE_NOT_EXIST
            else:
                oResult = Errno.E_ERRNO_TYPEDEF_MALFORMED

        return oResult

    ############################################################################
    # __parsePragma
    ############################################################################
    def __parsePragma(self, line, regexMap, syntaxIndicatorsMap):
        oResult = Errno.E_ERRNO_NONE

        if(None != regexMap["directiveBeginning"].match(line)):
            if(None != regexMap["directivePragma"].match(line)):
                completePragmaRangeMatch = regexMap["completePragmaRange"].match(line)
                completePragmaDefaultMatch = regexMap["completePragmaDefault"].match(line)
                if(None != completePragmaRangeMatch):
                    if(True == self.__interfaceBuilder.isTypedefExist(
                                            completePragmaRangeMatch.group(3))):
                        self.__interfaceBuilder.addSdiNumberByRange(
                                             completePragmaRangeMatch.group(3),
                                             completePragmaRangeMatch.group(8),
                                             completePragmaRangeMatch.group(12))
                        syntaxIndicatorsMap["isPragma"] = True
                    else:
                        oResult = Errno.E_ERRNO_TYPEDEF_NOT_EXIST

                if(None != completePragmaDefaultMatch):
                    if(True == self.__interfaceBuilder.isTypedefExist(
                                          completePragmaDefaultMatch.group(3))):
                        self.__interfaceBuilder.addSdiNumberByDefaultNumber(
                                            completePragmaDefaultMatch.group(3),
                                            completePragmaDefaultMatch.group(9))
                        syntaxIndicatorsMap["isPragma"] = True
                    else:
                        oResult = Errno.E_ERRNO_TYPEDEF_NOT_EXIST

        return oResult

    ############################################################################
    # __parseInterfaceBlock
    ############################################################################
    def __parseInterfaceBlock(self, line, regexMap, syntaxIndicatorsMap):
        oResult = Errno.E_ERRNO_NONE

        if(False == syntaxIndicatorsMap["isOpeneningBracket"] and
           (self.__regexConstants.CClosingBracket +
            self.__regexConstants.CSemiColon != line) and
            True == syntaxIndicatorsMap["hasOpenedInterfaceBracket"]):
            oResult = self.__parseSyntaxTypedef(line, 
                                                regexMap,
                                                syntaxIndicatorsMap)

            if(False == syntaxIndicatorsMap["isTypedef"]):
                oResult = self.__parsePragma(line,
                                             regexMap,
                                             syntaxIndicatorsMap)
        elif(self.__regexConstants.CClosingBracket +
             self.__regexConstants.CSemiColon == line):
            syntaxIndicatorsMap["hasOpenedInterfaceBracket"] = False

        return oResult

    ############################################################################
    # __isUnknownSyntax
    ############################################################################
    def __isUnknownSyntax(self, line, syntaxIndicatorsMap, errno):
        oResult = False

        if((self.__regexConstants.CClosingBracket +
            self.__regexConstants.CSemiColon != line) and
            "" != line and
            False == syntaxIndicatorsMap["isInterface"] and
            False == syntaxIndicatorsMap["isOpeneningBracket"] and
            False == syntaxIndicatorsMap["isTypedef"] and
            False == syntaxIndicatorsMap["isPragma"] and
            Errno.E_ERRNO_NONE == errno):
            oResult = True

        return oResult

    ############################################################################
    # checkSyntax
    ############################################################################
    def checkSyntax(self, errorsCollector):
        oResult = True
        regexMap = {
            "inlineComment": re.compile(self.__regexConstants.CInlineComment),
            "openingMultiComment": re.compile(
                                    self.__regexConstants.COpeningMultiComment),
            "closingMultiComment": re.compile(
                                    self.__regexConstants.CClosingMultiComment),
            "directiveBeginning": re.compile(
                                     self.__regexConstants.CDirectiveBeginning),
            "directiveInclude": re.compile(
                                       self.__regexConstants.CDirectiveInclude),
            "completeInclude": re.compile(
                                        self.__regexConstants.CCompleteInclude),
            "fileInclude": re.compile(self.__regexConstants.CFileInclude),
            "directivePragma": re.compile(
                                        self.__regexConstants.CDirectivePragma),
            "completePragmaRange": re.compile(
                                    self.__regexConstants.CCompletePragmaRange),
            "completePragmaDefault": re.compile(
                                  self.__regexConstants.CCompletePragmaDefault),
            "syntaxInterface": re.compile(
                                        self.__regexConstants.CSyntaxInterface),
            "typedefBeginning": re.compile(
                                       self.__regexConstants.CTypedefBeginning),
            "syntaxTypedef": re.compile(self.__regexConstants.CSyntaxTypedef),
            "syntaxBasicTypes": re.compile(
                                       self.__regexConstants.CSyntaxBasicTypes),
            "syntaxVector": re.compile(self.__regexConstants.CSyntaxVector)
        }
        syntaxIndicatorsMap = {
            "isComment": False,
            "hasOpenedMultiComment": False,
            "isInclude": False,
            "isPragma": False,
            "isInterface": False,
            "isInterfaceFound": False,
            "isOpeneningBracket": False,
            "hasOpenedInterfaceBracket": False,
            "isTypedef": False
        }
        interfaceFile = open(self.__sdiFileName, "r")
        fileLines = interfaceFile.readlines()
        lineCounter = 0

        for line in(fileLines):
            syntaxIndicatorsMap["isComment"] = False
            syntaxIndicatorsMap["isInclude"] = False
            syntaxIndicatorsMap["isPragma"] = False
            syntaxIndicatorsMap["isInterface"] = False
            syntaxIndicatorsMap["isOpeneningBracket"] = False
            syntaxIndicatorsMap["isTypedef"] = False
            line = line.strip()
            lineCounter += 1
            errno = Errno.E_ERRNO_NONE

            # Parses comments
            self.__parseComments(line, regexMap, syntaxIndicatorsMap)

            # Parses includes
            if(False == syntaxIndicatorsMap["isComment"] and 
               False == syntaxIndicatorsMap["hasOpenedMultiComment"]):
                errno = self.__parseIncludes(line, 
                                             regexMap, 
                                             syntaxIndicatorsMap)
                # Parses interface syntax
                if(False == syntaxIndicatorsMap["isInclude"] and
                   Errno.E_ERRNO_NONE == errno):
                    errno = self.__parseSyntaxInterface(line, 
                                                        regexMap, 
                                                        syntaxIndicatorsMap)

                    # Parses interface block
                    if(False == syntaxIndicatorsMap["isInterface"] and
                       Errno.E_ERRNO_NONE == errno):
                        errno = self.__parseInterfaceBlock(line, 
                                                           regexMap, 
                                                           syntaxIndicatorsMap)

                    # Check is unknown syntax.
                    if(True == self.__isUnknownSyntax(line, 
                                                      syntaxIndicatorsMap,
                                                      errno)):
                       errno = Errno.E_ERRNO_UNKNOWN_SYNTAX
                    
            
            # Adds an error.
            if(Errno.E_ERRNO_NONE != errno):
                errorsCollector.addError(self.__sdiFileName, errno, lineCounter)
                oResult = False

        # Checks whether the closing interface block exists.
        if(True == syntaxIndicatorsMap["hasOpenedInterfaceBracket"]):
            errorsCollector.addError(self.__sdiFileName, 
                                     Errno.E_ERRNO_CLOSING_BRACKET_EXPECTED, 
                                     lineCounter)
            oResult = False

        return oResult

    ############################################################################
    # build
    ############################################################################
    def build(self):
        self.__interfaceBuilder.build()