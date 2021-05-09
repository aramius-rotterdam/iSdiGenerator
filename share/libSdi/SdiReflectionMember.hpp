/*
 * SdiReflectionMember.hpp
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

#ifndef SDIREFLECTIONMEMBER_HPP_
#define SDIREFLECTIONMEMBER_HPP_

#include <SdiReflectionMemberBase.hpp>

/**
 * @class      SdiReflectionMember
 * @brief      This class is used to provide a point of access to reflection
 *             of a member.
 * @author     ArAmIuS de Rotterdam
 * @version    0.1
 * @date       2021-05-03
 * @tparam     ClassT the class type.
 * @tparam     DataT the data type.
 */
template<class ClassT, typename DataT>
class SdiReflectionMember : public SdiReflectionMemberBase
{
public:
    /**
     * Self.
     */
    typedef SdiReflectionMember<ClassT, DataT> Self;
    
    /**
     * SharedPtr.
     */
    typedef std::shared_ptr<Self> SharedPtr;
    
    /**
     * WeakPtr.
     */
    typedef std::weak_ptr<Self> WeakPtr; 

    /** 
     * GetterFunctor. A reference to the client provided getter.
     */
    typedef const DataT& (ClassT:: *GetterFunctor)(void) const;

    /** 
     * SetterFunctor. A reference to the client provided setter.
     */
    typedef void (ClassT:: *SetterFunctor)(const DataT &iValue);

    /**
     * Default constructor.
     * Constructor to init the reflection of owner class provided methods.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-03
     * @param      iOwner the reference to the owner class instance.
     * @param      iMemberType the member's type.
     * @param      iDataType the data type.
     * @param      ipGetterFunctor the getter functor.
     * @param      ipSetterFunctor the setter functor.
     */
    SdiReflectionMember(ClassT              &iOwner,
                        const MemberType    &iMemberType,
                        const DataType      &iDataType,
                        const GetterFunctor  ipGetterFunctor,
                        const SetterFunctor  ipSetterFunctor)
     : m_owner(iOwner),
       m_memberType(iMemberType),
       m_dataType(iDataType),
       m_pGetterFunctor(ipGetterFunctor),
       m_pSetterFunctor(ipSetterFunctor)
    {

    }

    /** 
     * Copy constructor.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-06
     * @param      iOtherInstance the other instance to copy from.
     */
    SdiReflectionMember(const SdiReflectionMember &iOtherInstance)
     : m_owner(iOtherInstance.m_owner),
       m_memberType(iOtherInstance.m_memberType),
       m_dataType(iOtherInstance.m_dataType),
       m_pGetterFunctor(iOtherInstance.m_pGetterFunctor),
       m_pSetterFunctor(iOtherInstance.m_pSetterFunctor)
    {

    }

    /**
     * Assignment operator.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-06
     * @param      iOtherInstance the other instance to copy from.
     */
    SdiReflectionMember &operator=(const SdiReflectionMember &iOtherInstance)
    {
        m_owner = iOtherInstance.m_owner;
        m_memberType = iOtherInstance.m_memberType;
        m_dataType = iOtherInstance.m_dataType;
        m_pGetterFunctor = iOtherInstance.m_pGetterFunctor;
        m_pSetterFunctor = iOtherInstance.m_pSetterFunctor;
    }

    /**
     * Default destroyer.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-03
     */
    virtual ~SdiReflectionMember(void)
    {

    }

    /**
     * Gets the member's type.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-06
     * @return     The member's type.
     */
    const MemberType &getMemberType(void) const
    {
        return(m_memberType);
    }

    /**
     * Gets the data type.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-06
     * @return     The data type.
     */
    const DataType &getDataType(void) const
    {
        return(m_dataType);
    }

    /**
     * Invokes the getter method returning the value of the related attribute.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-03
     * @return     The value of the related attribute.
     */
    const DataT &invokeGetter(void) const
    {
        return((m_owner.*m_pGetterFunctor)());
    }

    /**
     * Invokes the setter method setting the value to the related attribute.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-03
     * @param      iValue the value to set into the related attribute.
     */
    void invokeSetter(const DataT &iValue)
    {
        (m_owner.*m_pSetterFunctor)(iValue);
    }

private:
    /**
     * Reference to the owner class instance.
     */
    ClassT &m_owner;

    /**
     * Member's type.
     */
    MemberType m_memberType;

    /**
     * Data type.
     */
    DataType m_dataType;

    /**
     * Getter functor.
     */
    GetterFunctor m_pGetterFunctor;
    
    /**
     * Setter functor.
     */
    SetterFunctor m_pSetterFunctor;
};

#endif // SDIREFLECTIONMEMBER_HPP_