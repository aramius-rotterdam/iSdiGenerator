/*
 * SdiReflectionBase.hpp
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

#ifndef SDIREFLECTIONBASE_HPP_
#define SDIREFLECTIONBASE_HPP_

#include <SdiReflectionMember.hpp>
#include <map>
#include <string>
#include <iostream>
#include <exception>
#include <cxxabi.h>

/**
 * @class      SdiReflectionBase
 * @brief      This base class is used to apply the reflection technique to the 
 *             classes which inherit from it.
 * @author     ArAmIuS de Rotterdam
 * @version    0.1
 * @date       2021-05-03
 * @tparam     ClassT the class type.
 */
template<class ClassT>
class SdiReflectionBase
{
public:
    /**
     * MemberName.
     */
    typedef std::string MemberName;

    /**
     * Gets the class provided member by a given name.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-03
     * @exception  std::exception
     * @tparam     DataT the data type.
     * @param      iMemberName the member's name.
     * @return     The class provided member.
     */
    template<typename DataT>
    const typename SdiReflectionMember<ClassT, DataT>::SharedPtr getMember(
                                            const MemberName &iMemberName) const
    {
        typedef SdiReflectionMember<ClassT, DataT> ReflectionMember;
        const std::string CMemberTypeError(
                                     "The member '%s' is not defined as '%s'.");
        const std::string CMemberExistError("The member '%s' doesn't exist.");
        typename ReflectionMember::SharedPtr opResult;
        int status;
        ReflectionMembersMap::const_iterator findIt = 
                                                 m_membersMap.find(iMemberName);
        std::string tParameterName = typeid(DataT).name();
        char *pDemangledTParameterName = abi::__cxa_demangle(
                                                         tParameterName.c_str(), 
                                                         NULL, 
                                                         NULL, 
                                                         &status);
        if(0 == status)
        {
            tParameterName = pDemangledTParameterName;
            std::free(pDemangledTParameterName);
        }

        if(m_membersMap.end() != findIt)
        {
            opResult = std::dynamic_pointer_cast<ReflectionMember>(
                                                                findIt->second);

            if(nullptr == opResult)
            {
                throwException(CMemberTypeError, iMemberName, tParameterName);
            }
        }
        else
        {
            throwException(CMemberTypeError, iMemberName);
        }

        return(opResult);
    }

protected:
    /**
     * Default constructor.
     * Constructor to init the reflection of owner class.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-03
     * @param      iOwner the reference to the owner class instance.
     */
    SdiReflectionBase(ClassT &iOwner)
     : m_owner(std::reference_wrapper(iOwner)),
       m_membersMap()
    {

    }

    /** 
     * Copy constructor.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-06
     * @param      iOtherInstance the other instance to copy from.
     */
    SdiReflectionBase(const SdiReflectionBase &iOtherInstance)
     : m_owner(iOtherInstance.m_owner),
       m_membersMap(iOtherInstance.m_membersMap)
    {

    }

    /**
     * Assignment operator.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-06
     * @param      iOtherInstance the other instance to copy from.
     */
    SdiReflectionBase &operator=(const SdiReflectionBase &iOtherInstance)
    {
        m_owner = iOtherInstance.m_owner;
        m_membersMap = iOtherInstance.m_membersMap;

        return(*this);
    }

    /**
     * Default destroyer.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-03
     */
    virtual ~SdiReflectionBase(void)
    {

    }

    /**
     * Registers the class provided methods, and indicates whether it 
     * was done propertly.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-03
     * @tparam     DataT the data type.
     * @param      iMemberName the member's name.
     * @param      iMemberType the member's type.
     * @param      iDataType the data type.
     * @param      iGetterFunctor the getter functor.
     * @param      iSetterFunctor the setter functor.
     * @return     Indicates whether the registration was done properly.
     */
    template<typename DataT>
    const bool registerMethods(
              const MemberName                                  &iMemberName, 
              const SdiReflectionMemberBase::MemberType         &iMemberType,
              const SdiReflectionMemberBase::DataType           &iDataType,
              const typename SdiReflectionMember<
                                          ClassT, 
                                          DataT>::GetterFunctor &iGetterFunctor,
              const typename SdiReflectionMember<
                                          ClassT, 
                                          DataT>::SetterFunctor &iSetterFunctor)
    {
        bool oResult = false;
        ReflectionMembersMap::const_iterator findIt = 
                                                 m_membersMap.find(iMemberName);
        typename SdiReflectionMember<ClassT, 
                                     DataT>::SharedPtr pReflectionMember;

        if(m_membersMap.end() == findIt)
        {
            pReflectionMember =
                        std::make_shared<
                                   SdiReflectionMember<ClassT, 
                                                       DataT> >(m_owner, 
                                                                iMemberType,
                                                                iDataType,
                                                                iGetterFunctor, 
                                                                iSetterFunctor);

            m_membersMap.insert(std::make_pair(iMemberName, 
                                               pReflectionMember));

            oResult = true;
        }

        return(oResult);
    }

private:
    /**
     * ReflectionMembersMap.
     */
    typedef std::map<MemberName, 
                     SdiReflectionMemberBase::SharedPtr> ReflectionMembersMap;

    /**
     * Virtual method to be implemented by the owner class. In this point 
     * the class has to register every its members.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-03
     */
    virtual void registerMembers(void) = 0;

    /**
     * Throws an exception.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-05-06
     * @exception  std::exception
     * @param      iMessageError the format of message error.
     * @param      iMemberName the member name.
     * @param      iTParameterName the template parameter name.
     */
    void throwException(
                       const std::string &iMessageErrorFromat, 
                       const std::string &iMemberName, 
                       const std::string &iTParameterName = std::string()) const
    {
        const __SIZE_TYPE__ CErrorMsgSize = 150;
        char errorMsg[CErrorMsgSize];

        sprintf(errorMsg,
                iMessageErrorFromat.c_str(),
                iMemberName.c_str(),
                iTParameterName.c_str());

        throw std::runtime_error(errorMsg);
    }

    /**
     * Reference to the owner class instance.
     */
    ClassT &m_owner;

    /**
     * Map of the class provided members.
     */
    ReflectionMembersMap m_membersMap;
};

#endif // SDIREFLECTIONBASE_HPP_