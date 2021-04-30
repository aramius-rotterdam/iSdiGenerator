################################################################################
# SdiRegexConstants.py
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
        self.CCompletePragmaRange = "#pragma(([ \\t]+)([\\_A-Za-z0-9]+)([ \\t]+)"
        self.CCompletePragmaRange += "((\\[)([ \\t]*)([0-9]+)([ \\t]*)(\\-)([ \\t]*)"
        self.CCompletePragmaRange += "([0-9]+)([ \\t]*)(\\])))"
        self.CCompletePragmaDefault = "#pragma(([ \\t]+)([\\_A-Za-z0-9]+)([ \\t]+)"
        self.CCompletePragmaDefault += "((\\[)(default\\:)([ \\t]*)([0-9]+)(\\])))"
        self.CSyntaxInterface = "interface([ \\t]+)([\\_A-Za-z0-9]+)([ \\t]*)([\\{]*)$"
        self.CSyntaxStruct = "struct([ \\t]+)([\\_A-Za-z0-9]+)([ \\t]*)([\\{]*)$"
        self.CTypedefBeginning = "typedef(.*)"
        self.CSyntaxTypedef = "typedef((([ \\t]+)([\\:\\<\\>\\_A-Za-z0-9]+))+)"
        self.CSyntaxTypedef += "(([ \\t]+)([\\_A-Za-z0-9]+))(([ \\t]*)(\\;))"
        
        syntaxBasicNumericTypesMap = {
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
        typeCounter = 0
        syntaxBasicNumericTypes = "("
        for key in syntaxBasicNumericTypesMap:
            if(0 < typeCounter):
                syntaxBasicNumericTypes += "|"
            syntaxBasicNumericTypes += syntaxBasicNumericTypesMap[key]
            typeCounter += 1
        syntaxBasicNumericTypes += ")"
        self.CSyntaxBasicTypes = "^("
        self.CSyntaxBasicTypes += "((bool)|" + syntaxBasicNumericTypes + ")"
        self.CSyntaxBasicTypes += ")$"
        self.CSyntaxVector = "std::vector<(.+)>"

        sdiNumberRange = "(([0-9]+)|"
        sdiNumberRange += "(std\\:\\:numeric\\_limits\\<"
        sdiNumberRange += syntaxBasicNumericTypes 
        sdiNumberRange += "\\>\\:\\:min\\(\\))|"
        sdiNumberRange += "(std\\:\\:numeric\\_limits\\<" 
        sdiNumberRange += syntaxBasicNumericTypes
        sdiNumberRange += "\\>\\:\\:max\\(\\)))"
        self.CSdiNumber = "(?P<SdiNumber>SdiNumber\\<"
        self.CSdiNumber += syntaxBasicNumericTypes + "\\, )"
        self.CSdiNumber += "(?P<MinNumber>" + sdiNumberRange + "\\, )"
        self.CSdiNumber += "(?P<MaxNumber>" + sdiNumberRange + "\\, )"
        self.CSdiNumber += "(?P<DefaultNumber>([0-9]+)\\>)"
        self.CSyntaxProperty = "((bool)|" + syntaxBasicNumericTypes + "|(" + self.CSyntaxVector + ")|([\\_A-Za-z0-9]+))"
        self.CSyntaxProperty += "([ \t]+)([\\_A-Za-z0-9]+)([ \t]*)(\\;)$"
        self.CSyntaxPropertyName = "((?P<Prefix>m\\_)(?P<Property>[A-Za-z0-9]+))"
        self.CSyntaxInterfaceProperties = "properties([ \\t]*)([\\{]*)$"

        self.COpeningBracket = "{"
        self.CClosingBracket = "}"
        self.CSemiColon = ";"
        self.CSpace = " "
        self.CSlash = "/"
        self.CCarriageReturn = "\n"
        self.CItemInterface = "Interface"
        self.CItemStruct = "Struct"
        self.CItemInterfaceProperties="InterfaceProperties"
        self.CExtensionSdi = ".sdi"
        self.CExtensionHpp = ".hpp"
        self.CExtensionCpp = ".cpp"
        

    