################################################################################
# SdiRegexConstants.py
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
# Class SdiRegexConstants
################################################################################
class SdiRegexConstants:
    ############################################################################
    # __init__
    ############################################################################
    def __init__(self):
        self.CInlineComment = "(//(.*))|(/(\\*+)(.*)(\\*+)/)"
        self.COpeningMultiComment = "(/\\*)(.*)"
        self.CClosingMultiComment = "(.*)(\\*/)"
        self.CDirectiveBeginning = "#([A-Za-z]+)(.*)"
        self.CDirectiveInclude = "#include"
        self.CCompleteInclude = "#include(([ \\t]+)<(.+)>)"
        self.CFileInclude = "([A-Za-z0-9]+)\\.sdi"
        self.CDirectivePragma = "#pragma"
        self.CCompletePragmaRange = "#pragma(([ \\t]+)([A-Za-z0-9]+)([ \\t]+)((\\[)([ \\t]*)([0-9]+)([ \\t]*)(\\-)([ \\t]*)([0-9]+)([ \\t]*)(\\])))"
        self.CCompletePragmaDefault = "#pragma(([ \\t]+)([A-Za-z0-9]+)([ \\t]+)((\\[)(default\\:)([ \\t]*)([0-9]+)(\\])))"
        self.CSyntaxInterface = "interface([ \\t]+)([A-Za-z0-9]+)([ \\t]*)([\\{]*)"
        self.COpeningBracket = "{"
        self.CClosingBracket = "}"
        self.CSemiColon = ";"
        self.CSpace = " "
        self.CCarriageReturn = "\n"
        self.CTypedefBeginning = "typedef(.*)"
        self.CSyntaxTypedef = "typedef((([ \\t]+)([:<>A-Za-z0-9]+))+)(([ \\t]+)([A-Za-z0-9]+))(([ \\t]*);)"
        self.CSyntaxBasicTypesMap = {
            "UChar": "(unsigned([ \\t]+)char)",
            "Char": "(char)",
            "SChar": "(signed([ \\t]+)char)",
            "UShort": "(unsigned([ \\t]+)short)",
            "UShortInt": "(unsigned([ \\t]+)short([ \\t]+)int)",
            "Short": "(short)",
            "ShortInt": "(short([ \\t]+)int)",
            "SShort": "(signed([ \\t]+)short)",
            "SShortInt": "(signed([ \\t]+)short([ \\t]+)int)",
            "UInt": "(unsigned([ \\t]+)int)",
            "Int": "(int)",
            "SInt": "(signed([ \\t]+)int)",
            "ULong": "(unsigned([ \\t]+)long)",
            "ULongInt": "(unsigned([ \\t]+)long([ \\t]+)int)",
            "Long": "(long)",
            "LongInt": "(long([ \\t]+)int)",
            "SLong": "(signed([ \\t]+)long)",
            "SLongInt": "(signed([ \\t]+)long([ \\t]+)int)",
            "ULLong": "(unsigned([ \\t]+)long([ \\t]+)long)",
            "ULLongInt": "(unsigned([ \\t]+)long([ \\t]+)long([ \\t]+)int)",
            "LLong": "(long([ \\t]+)long)",
            "LLongInt": "(long([ \\t]+)long([ \\t]+)int)",
            "SLLong": "(signed([ \\t]+)long([ \\t]+)long)",
            "SLLongInt": "(signed([ \\t]+)long([ \\t]+)long([ \\t]+)int)",
            "Float": "(float)",
            "Double": "(double)",
            "LDouble": "(long([ \\t]+)double)",
            "Size": "(__SIZE_TYPE__)",
            "StdString": "(std::string)"
        }
        self.CSyntaxVector = "std::vector<(.+)>"

        self.CSyntaxBasicTypes = "^("
        typeCounter = 0
        syntaxBasicTypes = "("
        for key in self.CSyntaxBasicTypesMap:
            if(0 < typeCounter):
                syntaxBasicTypes += "|"
            syntaxBasicTypes += self.CSyntaxBasicTypesMap[key]
            typeCounter += 1
        syntaxBasicTypes += ")"
        self.CSyntaxBasicTypes += syntaxBasicTypes
        self.CSyntaxBasicTypes += ")$"

        sdiRange = "(([0-9]+)|"
        sdiRange += "(std\\:\\:numeric\\_limits\\<"
        sdiRange += syntaxBasicTypes 
        sdiRange += "\\>\\:\\:min\\(\\))|"
        sdiRange += "(std\\:\\:numeric\\_limits\\<" 
        sdiRange += syntaxBasicTypes
        sdiRange += "\\>\\:\\:max\\(\\)))"
        self.CSdiNumber = "(?P<SdiNumber>SdiNumber\\<"
        self.CSdiNumber += syntaxBasicTypes + "\\, )"
        self.CSdiNumber += "(?P<MinNumber>" + sdiRange + "\\, )"
        self.CSdiNumber += "(?P<MaxNumber>" + sdiRange + "\\, )"
        self.CSdiNumber += "(?P<DefaultNumber>([0-9]+)\\>)"
        

    