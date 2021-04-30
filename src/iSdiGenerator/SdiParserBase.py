################################################################################
# SdiParserBase.py
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
from SdiRegexConstants import SdiRegexConstants
from SdiErrorsCollector import Errno

################################################################################
# Class SdiParserBase
################################################################################
class SdiParserBase:
    ############################################################################
    # __init__
    ############################################################################
    def __init__(self):
        self.regexConstants = SdiRegexConstants()

    ############################################################################
    # parseComments
    ############################################################################
    def parseComments(self, line, regexMap, syntaxIndicatorsMap):
        if(None != regexMap["inlineComment"].match(line)):
            syntaxIndicatorsMap["isComment"] = True
        elif(None != regexMap["openingMultiComment"].match(line)):
            syntaxIndicatorsMap["hasOpenedMultiComment"] = True
        elif(True == syntaxIndicatorsMap["hasOpenedMultiComment"] and 
             None != regexMap["closingMultiComment"].match(line)):
            syntaxIndicatorsMap["hasOpenedMultiComment"] = False
            syntaxIndicatorsMap["isComment"] = True

    ############################################################################
    # parseSyntaxItem
    ############################################################################
    def parseSyntaxItem(self, 
                        itemType, 
                        line, 
                        regexMap, 
                        syntaxIndicatorsMap):
        itemMatch = regexMap["syntax" + itemType].match(line)
        itemName = None

        if(None != itemMatch):
            itemName = itemMatch.group(2)
            syntaxIndicatorsMap["is" + itemType] = True
            syntaxIndicatorsMap["is" + itemType + "Found"] = True

            if(self.regexConstants.COpeningBracket == line[len(line) - 1]):
                syntaxIndicatorsMap["hasOpened" + itemType + "Bracket"] = True

        return itemName

    ############################################################################
    # parseSyntaxBlockBeginning
    ############################################################################
    def parseSyntaxBlockOpening(self,
                                blockType,
                                line,
                                syntaxIndicatorsMap):
        oResult = Errno.E_ERRNO_NONE

        if(self.regexConstants.COpeningBracket == line and
             True == syntaxIndicatorsMap["hasOpened"+ blockType + "Bracket"]):
             oResult = Errno.E_ERRNO_OPENNING_BRACKET_NOT_EXPECTED
        
        elif(self.regexConstants.COpeningBracket == line):
            syntaxIndicatorsMap["isOpeneningBracket"] = True
            syntaxIndicatorsMap["hasOpened" + blockType + "Bracket"] = True

        return oResult