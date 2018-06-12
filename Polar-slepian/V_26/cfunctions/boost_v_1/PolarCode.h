//
// Created by Saurabh Tavildar on 5/17/16.
//

#ifndef POLARC_POLARCODE_H
#define POLARC_POLARCODE_H


#include <cstdint>
#include <vector>
#include <math.h>
#include <stack>          // std::stack

#include <boost/python.hpp>
#include <boost/python/list.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/python/stl_iterator.hpp>
#include <boost/python/extract.hpp>

class PolarCode {


public:

    PolarCode(uint8_t num_layers, uint16_t info_length, double epsilon, uint16_t crc_size) :
            _n(num_layers), _info_length(info_length), _design_epsilon(epsilon),
            _crc_size(crc_size), _llr_based_computation(true)
    {
        _block_length = (uint16_t) (1 << _n);
        _frozen_bits.resize(_block_length);
        _info_bits_padded.resize(_block_length);
        _frozen_bits_values.resize(_block_length);
        _bit_rev_order.resize(_block_length);
        create_bit_rev_order();
        initialize_frozen_bits();
    }

    std::vector<uint8_t> encode(std::vector<uint8_t> info_bits);
    std::vector<uint8_t> reverse_arikan(std::vector<uint8_t> info_bits_padded);
     std::vector<uint8_t> arikan(std::vector<uint8_t> info_bits_padded);
    std::vector<uint8_t> decode_scl_p1(std::vector<double> p1, std::vector<double> p0, uint16_t list_size);
    std::vector<uint8_t> decode_scl_llr(std::vector<double> llr, uint16_t list_size);
    std::vector<uint8_t> decode_scl_llr_file(std::vector<double> llr, uint16_t list_size);

    std::vector<std::vector<double>> get_bler_quick(std::vector<double> ebno_vec, std::vector<uint8_t> list_size);
 
    std::vector<uint8_t> py_list_to_std_vector( const boost::python::object& iterable );
    boost::python::list std_vector_to_py_list(std::vector<uint8_t> vector);
    
    std::vector<uint16_t> py_list_to_std_vector16( const boost::python::object& iterable );
    boost::python::list std_vector_to_py_list16(std::vector<uint16_t> vector);
    
    std::vector<double> py_list_to_std_vector_dbl( const boost::python::object& iterable );
    boost::python::list std_vector_to_py_list_dbl(std::vector<double> vector)   ; 
    
    void setvector(boost::python::list binarystring);
    boost::python::list getvector();
    
    void setfrozen_bits(boost::python::list binarystring) ;
    boost::python::list getfrozen_bits();
    void setchannel_order_descending(boost::python::list pylist);
    boost::python::list getchannel_order_descending();
    
    void setfrozen_bits_indic(boost::python::list binarystring) ;
    boost::python::list getfrozen_bits_indic();
   
    
    
    boost::python::list encode_wrapper(boost::python::list info_bits);
    boost::python::list decode_wrapper(boost::python::list llr, uint8_t list_size);
    boost::python::list decode_wrapper_f(boost::python::list llr, uint8_t list_size);
    boost::python::list reverse_arikan_wrapper(boost::python::list info_bits);
    boost::python::list arikan_wrapper(boost::python::list info_bits);
      
    uint8_t _n;
    uint16_t _info_length;
    uint16_t _block_length;
    uint16_t _crc_size;

    double _design_epsilon;
 


private:

	std::vector<uint8_t> vMsg;// is a dummy

	std::vector<uint8_t> _frozen_bits;
	std::vector<uint8_t> _frozen_bits_values;
	std::vector<uint8_t> _info_bits_padded;
    std::vector<uint16_t> _channel_order_descending;
    std::vector<std::vector<uint8_t>> _crc_matrix;
    std::vector<uint16_t> _bit_rev_order;
   
    
    void initialize_frozen_bits();
    void create_bit_rev_order();

    std::vector<uint8_t> decode_scl();
    std::vector<uint8_t> decode_scl_file();
    bool _llr_based_computation;

    std::vector<std::vector<double *>> _arrayPointer_LLR;
    std::vector<double> _pathMetric_LLR;

    uint16_t _list_size;

    std::stack<uint16_t> _inactivePathIndices;
    std::vector<uint16_t > _activePath;
    std::vector<std::vector<double *>> _arrayPointer_P;
    std::vector<std::vector<uint8_t *>> _arrayPointer_C;
    std::vector<uint8_t *> _arrayPointer_Info;
    std::vector<std::vector<uint16_t>> _pathIndexToArrayIndex;
    std::vector<std::stack<uint16_t>> _inactiveArrayIndices;
    std::vector<std::vector<uint16_t>> _arrayReferenceCount;

    void initializeDataStructures();
    uint16_t assignInitialPath();
    uint16_t clonePath(uint16_t);
    void killPath(uint16_t l);

    double * getArrayPointer_P(uint16_t lambda, uint16_t  l);
    double * getArrayPointer_LLR(uint16_t lambda, uint16_t  l);
    uint8_t * getArrayPointer_C(uint16_t lambda, uint16_t  l);

    void recursivelyCalcP(uint16_t lambda, uint16_t phi);
    void recursivelyCalcLLR(uint16_t lambda, uint16_t phi);
    void recursivelyUpdateC(uint16_t lambda, uint16_t phi);

    void continuePaths_FrozenBit(uint16_t phi);
    void continuePaths_UnfrozenBit(uint16_t phi);

    uint16_t findMostProbablePath(bool check_crc);

    bool crc_check(uint8_t * info_bits_padded);

};
using namespace boost::python;

BOOST_PYTHON_MODULE(PolarCode)
{
    class_<PolarCode>("PolarCode", init<uint8_t,uint16_t,double,uint16_t>())
        .def_readwrite("n", & PolarCode::_n)
        .def_readwrite("info_length", & PolarCode::_info_length)
        .def_readwrite("design_p", & PolarCode::_design_epsilon)
        .def_readwrite("crc_size", & PolarCode::_crc_size)
        
   
        .def("encode", &PolarCode::encode_wrapper)
        .def("arikan", &PolarCode::arikan_wrapper)
        .def("rev_arikan", &PolarCode::reverse_arikan_wrapper)
        //.def("decode_scl_p1",&PolarCode::decode_scl_p1)
        .def("decode_scl",&PolarCode::decode_wrapper)
        .def("decode_scl_file",&PolarCode::decode_wrapper_f)
        //.def("get_bler_quick",&PolarCode::get_bler_quick)
        
        
        .def("setvector",&PolarCode::setvector)
        .def("getvector",&PolarCode::getvector)    
        
        .def("py_list_to_std_vector",&PolarCode::py_list_to_std_vector)
        .def("std_vector_to_py_list",&PolarCode::std_vector_to_py_list)
        
        .add_property("frozen_bits", &PolarCode::getfrozen_bits, &PolarCode:: setfrozen_bits)
        .add_property("frozen_bits_indic", &PolarCode::getfrozen_bits_indic, &PolarCode:: setfrozen_bits_indic)
        .add_property("channel_ordering", &PolarCode:: getchannel_order_descending, &PolarCode::  setchannel_order_descending)
      //  .add_property("crc_matrix", &PolarCode::getcrc_matrix, &PolarCode:: _setcrc_matrix)
      // .add_property("bit_rev_order", &PolarCode::getbit_rev_order, &PolarCode:: setbit_rev_order)
        .add_property("vMsg", &PolarCode::getvector, &PolarCode::setvector)
    ;

 
}



#endif //POLARC_POLARCODE_H
