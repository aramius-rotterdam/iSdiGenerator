/*
 * SdiNumber.hpp
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

#ifndef SDINUMBER_HPP_
#define SDINUMBER_HPP_

#include <SdiNumberGuard.hpp>

template<typename NumberT, 
         NumberT  minNumberV, 
         NumberT  maxNumberV, 
         NumberT  defaultNumberV>
class SdiNumber
{
public:
    /** 
    * The wrapped type for NumberT to be used into the template.
    */
    typedef NumberT InternalType;

    /** 
    * Default constructor. 
    * It ensures that m_value has the default number. It also checks at compile 
    * time that the size of SdiNumber is the same as the number type wrapped.
    * @author     ArAmIuS de Rotterdam
    * @version    0.1
    * @date       2021-04-25
    */
    SdiNumber(void)
    : m_value(checkRange(static_cast<NumberT>(defaultNumberV)))
    {
        // Size Mismatch Guard.
        //
        SdiNumberGuard<sizeof(m_value) == sizeof(*this)>();
    }

    /** 
    * Copy constructor. 
    * @author     ArAmIuS de Rotterdam
    * @version    0.1
    * @date       2021-04-25
    * @param      iOtherInstance the other instance.
    */
    SdiNumber(const SdiNumber &iOtherInstance)
    : m_value(checkRange(iOtherInstance.m_value))
    {

    }

    /** 
    * This constructor creates a SdiNumber from an NumberT value.
    * It must be called explicitly.
    * @author     ArAmIuS de Rotterdam
    * @version    0.1
    * @date       2021-04-25
    * @param      NumberT the value.
    */
    explicit SdiNumber(const NumberT &iValue)
     : m_value(checkRange(iValue))
    {
        // Size Mismatch Guard.
        //
        SdiNumberGuard<sizeof(m_value) == sizeof(*this)>();
    }

    /** 
    * This constructor creates a SdiNumber from a 'different' SdiNumber,
    * casting the internal value to the internal type.
    * It must be called explicitly.
    * @author     ArAmIuS de Rotterdam
    * @version    0.1
    * @date       2021-04-25
    * @param      NumberT the value.
    */
    template<typename NumberT2, 
             NumberT2 minNumberV2, 
             NumberT2 maxNumberV2, 
             NumberT2 defaultNumberV2>
    explicit SdiNumber(const SdiNumber<NumberT2, 
                                       minNumberV2, 
                                       maxNumberV2, 
                                       defaultNumberV2> &iSdiNumber)
     : m_value(checkRange(static_cast<NumberT>(iSdiNumber.getValue())))
    {
        // Size Mismatch Guard.
        //
        SdiNumberGuard<sizeof(m_value) == sizeof(*this)>();
    }

    /**
     * Returns the internal number.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-04-25
     * @return     The internal number m_value.
     */
    const NumberT &getValue(void) const
    {
        return(this->m_value);
    }

    /**
     * Modifies the internal number m_value.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-04-25
     * @param      iValue the value.
     */
    void setValue(const NumberT &iValue)
    {
        this->m_value = checkRange(iValue);
    }

    /**
     * Copy by operator.
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-04-25
     * @param      iOtherInstance the other instance.
     * @return     The updated instance.
     */
    const SdiNumber &operator=(const SdiNumber &iOtherInstance)
    {
        if(&iOtherInstance != this)
        {
            this->m_value = checkRange(iOtherInstance.m_value)
        }

        return(this->m_value)
    }

    /**
     * This friend function allows the use of SdiNumber in ostreams. It is a
     * friend function but it is declared and defined inside the template
     * (it is legal and probably clearer and better that define it in an
     * independent .cpp file).
     * @author     ArAmIuS de Rotterdam
     * @version    0.1
     * @date       2021-04-25
     * @param      oStream the output stream
     * @param      iSdiNumber the SdiNumber
     * @return     The output stream
     */
    friend std::ostream &operator<<(std::ostream     &oStream, 
                                    const SdiNumber  &iSdiNumber)
    {
        return(oStream << iSdiNumber.m_value);
    }

private:
    /** 
    * Checks whether the value is less than defined min number.
    * @author     ArAmIuS de Rotterdam
    * @version    0.1
    * @date       2021-04-25
    * @param      iValue the value.
    * @param      iMinNumber the defined min number.
    */
    inline bool lessCheck(const NumberT &iValue, const NumberT &iMinNumber)
    {
        return(static_cast<long long>(iValue) < iMinNumber);
    }

    /** 
    * Checks whether the value is greater than defined max number.
    * @author     ArAmIuS de Rotterdam
    * @version    0.1
    * @date       2021-04-25
    * @param      iValue the value.
    * @param      iMaxNumber the defined max number.
    */
    inline bool greaterCheck(const NumberT &iValue, const NumberT &iMaxNumber)
    {
        return(static_cast<long long>(iValue) > iMaxNumber);
    }

    /** 
    * Checks value range.
    * @author     ArAmIuS de Rotterdam
    * @version    0.1
    * @date       2021-04-25
    * @param      iValue the value.
    */
    inline NumberT checkRange(const NumberT &iValue)
    {
        if(lessCheck(iValue, minNumberV) || greaterCheck(iValue, maxNumberV))
        {
            std::stringstream numberRangeError;

            numberRangeError << "Value: " 
                              << iValue
                              << " outside limits ["
                              << minNumberV
                              << ","
                              << maxNumberV
                              << "]"

            throw std::exception(numberRangeError.str().c_str());
        }
    }

    /**
     * Internal number.
     */
    NumberT m_value;
};

#endif // SDIINTEGER_HPP_