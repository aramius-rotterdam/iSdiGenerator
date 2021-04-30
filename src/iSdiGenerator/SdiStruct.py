################################################################################
# SdiStruct.py
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
# Class SdiStruct
################################################################################
class SdiStruct:
    ############################################################################
    # __init__
    ############################################################################
    def __init__(self, name):
        self.__name = name
        self.__propertiesMap = {}

    ############################################################################
    # isPropertyExist
    ############################################################################
    def isPropertyExist(self, propertyName):
        return propertyName in(self.__propertiesMap)

    ############################################################################
    # addProperty
    ############################################################################
    def addProperty(self, propertyName, propertyType):
        self.__propertiesMap[propertyName] = propertyType

    ############################################################################
    # getName
    ############################################################################
    def getName(self):
        return self.__name

    ############################################################################
    # getPropertiesMap
    ############################################################################
    def getPropertiesMap(self):
        return self.__propertiesMap