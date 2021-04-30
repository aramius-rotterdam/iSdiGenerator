/*
 * SdiNumberGuard.hpp
 *
 * Copyright (c) 2021 ArAmIuS de Rotterdam <bchowa@gmail.com>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 *
 *
 */

#ifndef SDINUMBERGUARD_HPP_
#define SDINUMBERGUARD_HPP_

/**
 * @class      SdiNumberGuard
 * @brief      This template is used as a guard for SdiInteger and SdiFloat.
 * @author     ArAmIuS de Rotterdam
 * @version    0.1
 * @date       2021-04-25
 */
template<bool condition>
class SdiNumberGuard;

template<>
class SdiNumberGuard<true>
{

};

#endif // SDINUMBERGUARD_HPP_