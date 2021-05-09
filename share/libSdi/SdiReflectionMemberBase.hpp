/*
 * SdiReflectionMemberBase.hpp
 *
 * Copyright (c) 2021 ArAmIuS de Rotterdam
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

#ifndef SDIREFLECTIONMEMBERBASE_HPP_
#define SDIREFLECTIONMEMBERBASE_HPP_

#include <memory>

/**
 * @class      SdiReflectionMemberBase
 * @brief      This base class is used to provide polymorphism to the reflection
 *             of a member.
 * @author     ArAmIuS de Rotterdam
 * @version    0.1
 * @date       2021-05-03
 */
class SdiReflectionMemberBase
{
public:
    /**
     * Self.
     */
    typedef SdiReflectionMemberBase Self;

    /**
     * SharedPtr.
     */
    typedef std::shared_ptr<Self> SharedPtr;

    /**
     * WeakPtr.
     */
    typedef std::weak_ptr<Self> WeakPtr;

   /**
     * Enumeration to define the members' type.
     * <ul>
     *  <li>
     *      E_MEMBER_TYPE_SIMPLE: For members which contains data as simple
     *      form.
     *  </li>
     *  <li>
     *      E_MEMBER_TYPE_VECTOR: For members which contains data distributed 
     *      in a vector.
     *  </li>
     * </ul>
     */
    enum MemberType
    {
        E_MEMBER_TYPE_SIMPLE,
        E_MEMBER_TYPE_VECTOR
    };

    /**
     * Enumeration to define the data type.
     * <ul>
     *  <li>E_DATA_TYPE_BASIC: Type basic.</li>
     *  <li>E_DATA_TYPE_STRUCT: Type struct.</li>
     * </ul>
     */
    enum DataType
    {
        E_DATA_TYPE_BASIC,
        E_DATA_TYPE_STRUCT
    };

    /**
     * Default constructor.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-03
     */
    SdiReflectionMemberBase(void)
    {

    }

    /**
     * Default destroyer.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-03
     */
    virtual ~SdiReflectionMemberBase(void)
    {

    }

private:
    /** 
     * Private copy constructor to disallow copying.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-03
     * @param      iOtherInstance the other instance to copy from.
     */
    SdiReflectionMemberBase(const SdiReflectionMemberBase &iOtherInstance);

   /**
    * Private assignment operator to disallow copying.
    * @author     ArAmIuS de Rotterdam
    * @version    0.1
    * @date       2021-05-03
    * @param      iOtherInstance the other instance to copy from.
    */
    SdiReflectionMemberBase &operator=(
                                 const SdiReflectionMemberBase &iOtherInstance);
};

#endif // SDIREFLECTIONMEMBERBASE_HPP_