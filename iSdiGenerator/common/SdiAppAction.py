################################################################################
# SdiAppAction.py
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
from enum import Enum

################################################################################
# Class SdiAppAction
################################################################################
class SdiAppAction(Enum):
    E_APP_ACTION_NONE = 0
    E_APP_ACTION_GENERATE = 1
    E_APP_ACTION_GENERATE_FORCE = 2
    E_APP_ACTION_IMPORT_SDI_LIB = 3
    E_APP_ACTION_IMPORT_SDI_LIB_FORCE = 4