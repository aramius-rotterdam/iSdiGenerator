################################################################################
# SdiInterfaceParser.py
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
import os.path
from iSdiGenerator.common.SdiErrorsCollector import SdiErrno
from iSdiGenerator.parser.SdiParserBase import SdiParserBase
from iSdiGenerator.parser.SdiStructParser import SdiStructParser
from iSdiGenerator.parser.SdiInterfacePropertiesParser import SdiInterfacePropertiesParser
from iSdiGenerator.builder.SdiInterfaceBuilder import SdiInterfaceBuilder

################################################################################
# Class SdiInterfaceParser
################################################################################
class SdiInterfaceParser(SdiParserBase):
    ############################################################################
    # __init__
    ############################################################################
    def __init__(self, sdiFileName):
        SdiParserBase.__init__(self)
        
        sdiFileTuple = sdiFileName.rsplit(self.regexConstants.CSlash, 1)
        if(2 == len(sdiFileTuple)):
            self.__sdiFilePath = sdiFileTuple[0]
            self.__sdiFileName = sdiFileTuple[1]    
        else:
            self.__sdiFilePath = self.regexConstants.CDot
            self.__sdiFileName = sdiFileTuple[0]

        self.__interfaceBuilder = SdiInterfaceBuilder(self.regexConstants)
        self.__structParser = SdiStructParser(self.__interfaceBuilder)
        self.__propertiesParser= SdiInterfacePropertiesParser(
                                                        self.__interfaceBuilder)

    ############################################################################
    # __parseIncludes
    ############################################################################
    def __parseIncludes(self, line, regexMap, syntaxIndicatorsMap):
        oResult = SdiErrno.E_ERRNO_NONE

        if(None != regexMap["directiveBeginning"].match(line) and
           None == regexMap["directivePragma"].match(line)):

            if(None != regexMap["directiveInclude"].match(line)):

                completeIncludeMatch = regexMap["completeInclude"].match(line)
                
                if(None != completeIncludeMatch):

                    fileIncludeMatch = regexMap["fileInclude"].match(
                                                  completeIncludeMatch.group(3))

                    if(None != fileIncludeMatch):

                        if(False == self.__interfaceBuilder.isIncludeExist(
                                                    fileIncludeMatch.group(1))):
                            completeFile = fileIncludeMatch.group(1)
                            completeFile += self.regexConstants.CExtensionSdi
                            if(completeFile != self.__sdiFileName):
                                self.__interfaceBuilder.addInclude(
                                                      fileIncludeMatch.group(1), 
                                                      line)
                                syntaxIndicatorsMap["isInclude"] = True
                            else:
                                oResult = SdiErrno.E_ERRNO_INCLUDE_RECURSION
                        else:
                            oResult = SdiErrno.E_ERRNO_INCLUDE_DUPLICATED

                        if(True == syntaxIndicatorsMap["isInterfaceFound"]):
                            oResult = SdiErrno.E_ERRNO_INCLUDE_NOT_EXPECTED

                    else:
                        oResult = SdiErrno.E_ERRNO_SDI_FILE_EXPECTED

                else:
                    oResult = SdiErrno.E_ERRNO_INCLUDE_MALFORMED

            else:
                oResult = SdiErrno.E_ERRNO_DIRECTIVE_NOT_EXIST

        elif(False == syntaxIndicatorsMap["isInterfaceFound"] and
             None != regexMap["directivePragma"].match(line)):

            oResult = SdiErrno.E_ERRNO_PRAGMA_NOT_EXPECTED

        return oResult

    ############################################################################
    # __parseSyntaxInterface
    ############################################################################
    def __parseSyntaxInterface(self, line, regexMap, syntaxIndicatorsMap):
        interfaceName = None

        interfaceName = self.parseSyntaxItem(self.regexConstants.CItemInterface, 
                                             line, 
                                             regexMap, 
                                             syntaxIndicatorsMap)

        if(None != interfaceName):
            self.__interfaceBuilder.addInterfaceName(interfaceName)

    ############################################################################
    # __getFinalTypeDefinition
    ############################################################################
    def __getFinalTypeDefinition(self, typeDefinition, interfaceName):
        oResult = ""
        includedSdiTypeRegex = re.compile(self.regexConstants.CIncludedSdiType)

        if(None != includedSdiTypeRegex.match(typeDefinition)):
            oResult = typeDefinition
        else:
            oResult = interfaceName
            oResult += self.regexConstants.CColon
            oResult += self.regexConstants.CColon
            oResult += typeDefinition

        return oResult

    ############################################################################
    # __getFinalOriginalType
    ############################################################################
    def __getFinalOriginalType(self, originalType, interfaceName):
        oResult = ""
        includedSdiTypeRegex = re.compile(self.regexConstants.CIncludedSdiType)

        if(None != includedSdiTypeRegex.match(originalType)):
            oResult = originalType
        else:
            oResult = interfaceName
            oResult += self.regexConstants.CColon
            oResult += self.regexConstants.CColon
            oResult += originalType

        return oResult

    ############################################################################
    # __parseIncludedSDIFiles
    ############################################################################
    def __parseIncludedSDIFiles(self, syntaxIndicatorsMap, errorsCollector):
        oResult = SdiErrno.E_ERRNO_NONE
        includedInterfacesList = []

        includesMap = self.__interfaceBuilder.getIncludesMap()
        syntaxIndicatorsMap["isIncludedInterfacesLoaded"] = True

        for includedInterface in(includesMap):
            sdiFileName = includedInterface 
            sdiFileName += self.regexConstants.CExtensionSdi
            interfaceParser = SdiInterfaceParser(self.__sdiFilePath + 
                                                 self.regexConstants.CSlash +
                                                 sdiFileName)

            if(True == interfaceParser.checkSyntax(errorsCollector)):
                interfaceName = interfaceParser.getInterfaceName()
                
                if(not interfaceName in(includedInterfacesList)):
                    includedInterfacesList.append(interfaceName)

                    for typeDefinition in(interfaceParser.getTypesDefinitionList()):

                        finalTypeDefinition = self.__getFinalTypeDefinition(
                                             typeDefinition, 
                                             interfaceParser.getInterfaceName())

                        self.__interfaceBuilder.addTypeDefinition(
                                                            finalTypeDefinition)

                    originalTypesMap = interfaceParser.getOriginalTypesMap()
                    for typeDefinition in(originalTypesMap):

                        finalTypeDefinition = self.__getFinalTypeDefinition(
                                             typeDefinition, 
                                             interfaceParser.getInterfaceName())

                        finalOriginalType = self.__getFinalOriginalType(
                                              originalTypesMap[typeDefinition], 
                                              interfaceName)

                        self.__interfaceBuilder.addOriginalType(
                                                            finalTypeDefinition,
                                                            finalOriginalType)

                else:
                    oResult = SdiErrno.E_ERRNO_SDI_FILE_INTERFACE_DUPLICATED

            else:
                oResult = SdiErrno.E_ERRNO_SDI_FILE_INCLUDED_MALFORMED

        return oResult

    ############################################################################
    # __parseSyntaxTypedef
    ############################################################################
    def __parseSyntaxTypedef(self, line, regexMap, syntaxIndicatorsMap):
        oResult = SdiErrno.E_ERRNO_NONE
        syntaxTypedefMatch = regexMap["syntaxTypedef"].match(line)
        typedefSyntax = ""

        if(None != regexMap["typedefBeginning"].match(line)):
            
            if(None != syntaxTypedefMatch):

                syntaxBasicTypesMatch = regexMap["syntaxBasicTypes"].match(
                                            syntaxTypedefMatch.group(1).strip())
                syntaxVectorMatch = regexMap["syntaxVector"].match(
                                            syntaxTypedefMatch.group(1).strip())
                typeDefinition = syntaxTypedefMatch.group(7)
                typedefSyntax = re.sub(" +", self.regexConstants.CSpace, line)
                typedefSyntax = re.sub(self.regexConstants.CSemiColon, 
                                       "", 
                                       typedefSyntax)
                typedefSyntax = typedefSyntax.strip()
                typedefSyntax += self.regexConstants.CSemiColon
                
                if(False == self.__interfaceBuilder.isTypeDefinitionExist(
                                                               typeDefinition)):

                    if(None != syntaxBasicTypesMatch):
                    
                        self.__interfaceBuilder.addTypeDefinition(
                                                                 typeDefinition)
                        self.__interfaceBuilder.addTypedefSyntax(typeDefinition, 
                                                                 typedefSyntax)
                        self.__interfaceBuilder.addOriginalType(
                                                 typeDefinition,
                                                 syntaxBasicTypesMatch.group(1))
                        syntaxIndicatorsMap["isTypedef"] = True

                    elif(None != syntaxVectorMatch):

                        syntaxBasicTypesMatch = regexMap["syntaxBasicTypes"].match(
                                             syntaxVectorMatch.group(1).strip())
                        
                        if(None != syntaxBasicTypesMatch or
                           True == self.__interfaceBuilder.isTypeDefinitionExist(
                                                   syntaxVectorMatch.group(1))):

                            self.__interfaceBuilder.addTypeDefinition(
                                                                 typeDefinition)

                            if(None == syntaxBasicTypesMatch and 
                               True == self.__structParser.isStructExist(
                                                   syntaxVectorMatch.group(1))):

                                self.__structParser.addTypedefSyntax(
                                                     syntaxVectorMatch.group(1),
                                                     typedefSyntax)
                                self.__interfaceBuilder.addOriginalType(
                                                     typeDefinition,
                                                     syntaxVectorMatch.group(1))
                            else:

                                self.__interfaceBuilder.addTypedefSyntax(
                                                                 typeDefinition, 
                                                                 typedefSyntax)
                                self.__interfaceBuilder.addOriginalType(
                                                     typeDefinition,
                                                     syntaxVectorMatch.group(0))
                                                               
                            syntaxIndicatorsMap["isTypedef"] = True

                        else:
                            oResult = SdiErrno.E_ERRNO_DATA_TYPE_NOT_EXIST

                    elif(True == self.__interfaceBuilder.isTypeDefinitionExist(
                                          syntaxTypedefMatch.group(1).strip())):

                        self.__interfaceBuilder.addTypeDefinition(
                                                                 typeDefinition)

                        dataType = syntaxTypedefMatch.group(1).strip()
                        if(True == self.__structParser.isStructExist(dataType)):

                            self.__structParser.addTypedefSyntax(dataType,
                                                                 typedefSyntax)
                            self.__interfaceBuilder.addOriginalType(
                                                                 typeDefinition,
                                                                 dataType)
                            
                        else:

                            self.__interfaceBuilder.addTypedefSyntax(
                                                                 typeDefinition, 
                                                                 typedefSyntax)
                            self.__interfaceBuilder.addOriginalType(
                                                                 typeDefinition,
                                                                 dataType)  

                        syntaxIndicatorsMap["isTypedef"] = True

                    else:
                        oResult = SdiErrno.E_ERRNO_DATA_TYPE_NOT_EXIST

                else:
                    oResult = SdiErrno.E_ERRNO_TYPEDEF_DUPLICATED

            else:
                oResult = SdiErrno.E_ERRNO_TYPEDEF_MALFORMED

        return oResult

    ############################################################################
    # __parsePragma
    ############################################################################
    def __parsePragma(self, line, regexMap, syntaxIndicatorsMap):
        oResult = SdiErrno.E_ERRNO_NONE

        if(None != regexMap["directiveBeginning"].match(line)):
            
            if(None != regexMap["directivePragma"].match(line)):
                completePragmaRangeMatch = regexMap["completePragmaRange"].match(line)
                completePragmaDefaultMatch = regexMap["completePragmaDefault"].match(line)
                
                if(None != completePragmaRangeMatch or 
                   None != completePragmaDefaultMatch):
                    
                    if(None != completePragmaRangeMatch):
                        
                        if(True == self.__interfaceBuilder.isTypedefSyntaxExist(
                                            completePragmaRangeMatch.group(3))):
                            
                            if(True == self.__interfaceBuilder.isOriginalTypeExist(
                                            completePragmaRangeMatch.group(3))):

                                self.__interfaceBuilder.addSdiNumberByRange(
                                             completePragmaRangeMatch.group(3),
                                             completePragmaRangeMatch.group(8),
                                             completePragmaRangeMatch.group(12))
                                syntaxIndicatorsMap["isPragma"] = True

                            else:
                                oResult = SdiErrno.E_ERRNO_PRAGMA_NOT_VALID

                        else:
                            oResult = SdiErrno.E_ERRNO_TYPEDEF_NOT_EXIST
                            
                    if(None != completePragmaDefaultMatch):
                        
                        if(True == self.__interfaceBuilder.isTypedefSyntaxExist(
                                          completePragmaDefaultMatch.group(3))):
                            
                            if(True == self.__interfaceBuilder.isOriginalTypeExist(
                                          completePragmaDefaultMatch.group(3))):

                                self.__interfaceBuilder.addSdiNumberByDefaultNumber(
                                            completePragmaDefaultMatch.group(3),
                                            completePragmaDefaultMatch.group(9))
                                syntaxIndicatorsMap["isPragma"] = True

                            else:
                                oResult = SdiErrno.E_ERRNO_PRAGMA_NOT_VALID

                        else:
                            oResult = SdiErrno.E_ERRNO_TYPEDEF_NOT_EXIST

                else:
                    oResult = SdiErrno.E_ERRNO_PRAGMA_MALFORMED

        return oResult

    ############################################################################
    # __parseInterfaceBlock
    ############################################################################
    def __parseInterfaceBlock(self, line, regexMap, syntaxIndicatorsMap):
        oResult = SdiErrno.E_ERRNO_NONE

        if((self.regexConstants.CClosingBracket +
            self.regexConstants.CSemiColon != line) and
           True == syntaxIndicatorsMap["hasOpenedInterfaceBracket"]):

            oResult = self.__parseSyntaxTypedef(line, 
                                                regexMap,
                                                syntaxIndicatorsMap)

            if(False == syntaxIndicatorsMap["isTypedef"] and
               SdiErrno.E_ERRNO_NONE == oResult):

                oResult = self.__parsePragma(line,
                                             regexMap,
                                             syntaxIndicatorsMap)

        return oResult

    ############################################################################
    # __isClosingBlock
    ############################################################################
    def __isClosingBlock(self, line, syntaxIndicatorsMap):
        oResult = False

        if(False == syntaxIndicatorsMap["isInterface"] and
           False == syntaxIndicatorsMap["isStruct"] and
           False == syntaxIndicatorsMap["isInterfaceProperties"] and
           True == syntaxIndicatorsMap["isInterfaceFound"] and
           True == syntaxIndicatorsMap["hasOpenedInterfaceBracket"] and
           (self.regexConstants.CClosingBracket +
            self.regexConstants.CSemiColon == line)):

            oResult = True

        return oResult

    ############################################################################
    # __isUnknownSyntax
    ############################################################################
    def __isUnknownSyntax(self, line, syntaxIndicatorsMap, errno):
        oResult = False

        if((self.regexConstants.CClosingBracket +
            self.regexConstants.CSemiColon != line) and
           "" != line and
           False == syntaxIndicatorsMap["isPragma"] and
           False == syntaxIndicatorsMap["isInterface"] and
           False == syntaxIndicatorsMap["isStruct"] and
           False == syntaxIndicatorsMap["isInterfaceProperties"] and
           False == syntaxIndicatorsMap["isOpeneningBracket"] and
           False == syntaxIndicatorsMap["isTypedef"] and
            SdiErrno.E_ERRNO_NONE == errno):

            oResult = True

        return oResult

    ############################################################################
    # checkSyntax
    ############################################################################
    def checkSyntax(self, errorsCollector):
        oResult = True
        regexMap = {
            "inlineComment": re.compile(self.regexConstants.CInlineComment),
            "openingMultiComment": re.compile(
                                    self.regexConstants.COpeningMultiComment),
            "closingMultiComment": re.compile(
                                    self.regexConstants.CClosingMultiComment),
            "directiveBeginning": re.compile(
                                     self.regexConstants.CDirectiveBeginning),
            "directiveInclude": re.compile(
                                       self.regexConstants.CDirectiveInclude),
            "completeInclude": re.compile(
                                        self.regexConstants.CCompleteInclude),
            "fileInclude": re.compile(self.regexConstants.CFileInclude),
            "directivePragma": re.compile(
                                        self.regexConstants.CDirectivePragma),
            "completePragmaRange": re.compile(
                                    self.regexConstants.CCompletePragmaRange),
            "completePragmaDefault": re.compile(
                                  self.regexConstants.CCompletePragmaDefault),
            "syntaxInterface": re.compile(
                                        self.regexConstants.CSyntaxInterface),
            "syntaxStruct": re.compile(self.regexConstants.CSyntaxStruct),
            "typedefBeginning": re.compile(
                                       self.regexConstants.CTypedefBeginning),
            "syntaxTypedef": re.compile(self.regexConstants.CSyntaxTypedef),
            "syntaxBasicTypes": re.compile(
                                       self.regexConstants.CSyntaxBasicTypes),
            "syntaxVector": re.compile(self.regexConstants.CSyntaxVector),
            "syntaxInterfaceProperties": re.compile(
                                 self.regexConstants.CSyntaxInterfaceProperties)
        }
        syntaxIndicatorsMap = {
            "isComment": False,
            "hasOpenedMultiComment": False,
            "isInclude": False,
            "isPragma": False,
            "isInterface": False,
            "isInterfaceFound": False,
            "isStruct": False,
            "isOpeneningBracket": False,
            "hasOpenedInterfaceBracket": False,
            "isTypedef": False,
            "isIncludedInterfacesLoaded": False,
            "isInterfaceProperties": False,
            "isInterfacePropertiesFound": False
        }
        sdiFileFullPath = self.__sdiFilePath
        sdiFileFullPath += self.regexConstants.CSlash
        sdiFileFullPath += self.__sdiFileName

        if(os.path.isfile(sdiFileFullPath)):
            interfaceFile = open(sdiFileFullPath, "r")
            fileLines = interfaceFile.readlines()
            lineNumber = 0

            while lineNumber < len(fileLines):
                syntaxIndicatorsMap["isComment"] = False
                syntaxIndicatorsMap["isInclude"] = False
                syntaxIndicatorsMap["isPragma"] = False
                syntaxIndicatorsMap["isInterface"] = False
                syntaxIndicatorsMap["isStruct"] = False
                syntaxIndicatorsMap["isInterfaceProperties"] = False
                syntaxIndicatorsMap["isOpeneningBracket"] = False
                syntaxIndicatorsMap["isTypedef"] = False
                line = fileLines[lineNumber].strip()
                errno = SdiErrno.E_ERRNO_NONE
                
                # Parses comments
                self.parseComments(line, regexMap, syntaxIndicatorsMap)

                # Checks the line is not a commentary, and there is not 
                # an opened multi commentary. In this case, parses includes.
                if(False == syntaxIndicatorsMap["isComment"] and 
                   False == syntaxIndicatorsMap["hasOpenedMultiComment"]):

                    errno = self.__parseIncludes(line, 
                                                 regexMap, 
                                                 syntaxIndicatorsMap)

                    # Checks the line is not an include, and there is not an 
                    # error. In this case, parses interface syntax.
                    if(False == syntaxIndicatorsMap["isInclude"] and
                       False == syntaxIndicatorsMap["isInterfaceFound"] and
                       SdiErrno.E_ERRNO_NONE == errno):

                        self.__parseSyntaxInterface(line, 
                                                    regexMap, 
                                                    syntaxIndicatorsMap)

                    # Checks the interface was found. In this case, parses 
                    # the block beginning.
                    if(True == syntaxIndicatorsMap["isInterfaceFound"] and 
                       SdiErrno.E_ERRNO_NONE == errno):
                        
                        errno = self.parseSyntaxBlockOpening(
                                             self.regexConstants.CItemInterface,
                                             line,
                                             syntaxIndicatorsMap)

                    # Checks the line is not interface syntax, and that this 
                    # syntax was found before. Also checks the line is not 
                    # a openning bracket and that was found before.
                    # In this case, parses the included SDI files and 
                    # the interface block.
                    if(False == syntaxIndicatorsMap["isInterface"] and
                       True == syntaxIndicatorsMap["isInterfaceFound"] and
                       False == syntaxIndicatorsMap["isOpeneningBracket"] and
                       True == syntaxIndicatorsMap["hasOpenedInterfaceBracket"] and
                       SdiErrno.E_ERRNO_NONE == errno):

                        # Checks whether the included interfaces have not
                        # loaded yet.
                        if(False == syntaxIndicatorsMap["isIncludedInterfacesLoaded"]):
                            errno = self.__parseIncludedSDIFiles(
                                                            syntaxIndicatorsMap,
                                                            errorsCollector)

                        # Checks whether there are not errors. In this case,
                        # parses the inteface block.
                        if(SdiErrno.E_ERRNO_NONE == errno):
                            errno = self.__parseInterfaceBlock(
                                                            line, 
                                                            regexMap, 
                                                            syntaxIndicatorsMap)

                            # Checks the line is a struct syntax, and
                            # there are not errors. In this case,
                            # parses whole struct.
                            if(None != regexMap["syntaxStruct"].match(line) and
                               SdiErrno.E_ERRNO_NONE == errno):

                                lineOffset = lineNumber
                                errno, lineNumber = self.__structParser.checkSyntax(
                                                                     fileLines,
                                                                     lineOffset)
                                syntaxIndicatorsMap["isStruct"] = True

                    # Checks the line is a properties syntax, and there are not
                    # errors. In this case, parses properties syntax.
                    #
                    if(None != regexMap["syntaxInterfaceProperties"].match(
                                                                       line) and
                       SdiErrno.E_ERRNO_NONE == errno):

                        if(False == syntaxIndicatorsMap["isInterfacePropertiesFound"]):
                            lineOffset = lineNumber
                            errno, lineNumber = self.__propertiesParser.checkSyntax(
                                                                     fileLines,
                                                                     lineOffset)

                            syntaxIndicatorsMap["isInterfaceProperties"] = True
                            syntaxIndicatorsMap["isInterfacePropertiesFound"] = True
                        else:
                            errno = SdiErrno.E_ERRNO_INTERFACE_PROPERTIES_SYNTAX_DUPLICATED

                        # Checks is unknown syntax.
                        if(True == self.__isUnknownSyntax(line, 
                                                          syntaxIndicatorsMap,
                                                          errno)):
                            errno = SdiErrno.E_ERRNO_UNKNOWN_SYNTAX

                    if(True == self.__isClosingBlock(line, 
                                                     syntaxIndicatorsMap)):
                        syntaxIndicatorsMap["hasOpenedInterfaceBracket"] = False
                        
                # Adds an error.
                if(SdiErrno.E_ERRNO_NONE != errno):
                    if(SdiErrno.E_ERRNO_SDI_FILE_INCLUDED_MALFORMED == errno or
                       SdiErrno.E_ERRNO_SDI_FILE_INTERFACE_DUPLICATED == errno):
                        errorsCollector.addError(self.__sdiFileName, 
                                                 errno, 
                                                 0)
                    else:
                        errorsCollector.addError(self.__sdiFileName, 
                                                 errno, 
                                                 lineNumber + 1)
                    oResult = False

                lineNumber += 1

            # Checks whether the closing interface block exists.
            if(True == syntaxIndicatorsMap["hasOpenedInterfaceBracket"]):
                errorsCollector.addError(self.__sdiFileName, 
                                         SdiErrno.E_ERRNO_CLOSING_BRACKET_EXPECTED, 
                                         lineNumber + 1)
                oResult = False
        else:
            errorsCollector.addError(self.__sdiFileName, 
                                     SdiErrno.E_ERRNO_SDI_FILE_NOT_EXIST, 
                                     0)
            
        return oResult

    ############################################################################
    # getInterfaceName
    ############################################################################
    def getInterfaceName(self):
        return self.__interfaceBuilder.getInterfaceName()

    ############################################################################
    # getTypesDefinitionList
    ############################################################################
    def getTypesDefinitionList(self):
        return self.__interfaceBuilder.getTypesDefinitionList()

    ############################################################################
    # getOriginalTypesMap
    ############################################################################
    def getOriginalTypesMap(self):
        return self.__interfaceBuilder.getOriginalTypesMap()

    ############################################################################
    # build
    ############################################################################
    def build(self, outputDirectory):
        builtStructHpp, builtStructCpp = self.__structParser.build(
                                  self.__interfaceBuilder.getInterfaceName(), 
                                  self.__interfaceBuilder.getOriginalTypesMap())

        self.__interfaceBuilder.build(builtStructHpp,
                                      builtStructCpp,
                                      self.__sdiFileName,
                                      outputDirectory)