//
// Created by Saurabh Tavildar on 5/17/16.
//

#include "PolarCode.h"
#include <iostream>
#include <cmath>       /* log */
#include <sstream>      // std::stringstream
#include <fstream>
#include <iomanip>      // std::setprecision
#include <random>
#include <algorithm>
#include <chrono>



void PolarCode::initialize_frozen_bits() {
    std::vector<double> channel_vec(_block_length);

    for (uint16_t i = 0; i < _block_length; ++i) {
        channel_vec.at(i) = _design_epsilon;
    }
    //CONSTRUCTION _design_epsilon=z
    for (uint8_t iteration = 0; iteration < _n; ++iteration) {
        uint16_t  increment = 1 << iteration;
        for (uint16_t j = 0; j < increment; j +=  1) {
            for (uint16_t i = 0; i < _block_length; i += 2 * increment) {
                double c1 = channel_vec.at(i + j);
                double c2 = channel_vec.at(i + j + increment);
                channel_vec.at(i + j) = c1 + c2 - c1*c2;
                channel_vec.at(i + j + increment) = c1*c2;
            }
        }
    }

    _channel_order_descending.resize(_block_length);
    std::size_t n_t(0);
    std::generate(std::begin(_channel_order_descending), std::end(_channel_order_descending), [&]{ return n_t++; });
    std::sort(  std::begin(_channel_order_descending),
                std::end(_channel_order_descending),
                [&](int i1, int i2) { return channel_vec[_bit_rev_order.at(i1)] < channel_vec[_bit_rev_order.at(i2)]; } );

    uint16_t  effective_info_length = _info_length + _crc_size;
    //frozen bits locations?
    
    for (uint16_t i = 0; i < effective_info_length; ++i) {
        _frozen_bits.at(_channel_order_descending.at(i)) = 0;
    }
    for (uint16_t i = effective_info_length; i < _block_length; ++i) {
        _frozen_bits.at(_channel_order_descending.at((i))) = 1;
    }
    
    _crc_matrix.resize(_crc_size);
    for (uint8_t bit = 0; bit < _crc_size; ++bit) {
        _crc_matrix.at(bit).resize(_info_length);
        for (uint16_t info_bit = 0; info_bit < _info_length; ++info_bit )
            _crc_matrix.at(bit).at(info_bit) = (uint8_t) (rand() % 2);
    }

}

std::vector<uint8_t> PolarCode::encode(std::vector<uint8_t> info_bits) {

    std::vector<uint8_t> info_bits_padded(_block_length, 0);
    std::vector<uint8_t> coded_bits(_block_length);

    for (uint16_t i = 0; i < _info_length; ++i) {
        info_bits_padded.at(_channel_order_descending.at(i)) = info_bits.at(i);
    }
    for (uint16_t i = _info_length+_crc_size; i < _block_length; ++i) {
        info_bits_padded.at(_channel_order_descending.at(i)) = _frozen_bits_values.at(i);
    }
    //std::cout << "info_padded\n";
    for (uint16_t i = 0; i < _block_length; ++i) {
		_info_bits_padded.at(i)=info_bits_padded.at(i);
      //  std::cout<< +(_info_bits_padded.at(i));
    }
    //std::cout <<"\n";
    // adding CRC
    for (uint16_t i = _info_length; i < _info_length + _crc_size; ++i) {
        uint8_t  crc_bit = 0;
        for (uint16_t j = 0; j < _info_length; ++j) {
            crc_bit = (uint8_t) ((crc_bit + _crc_matrix.at(i - _info_length).at(j) * info_bits.at(j)) % 2);
        }
        info_bits_padded.at(_channel_order_descending.at(i)) = crc_bit;
        //modification for CB
        info_bits_padded.at(_channel_order_descending.at(i)) = info_bits.at(i-_info_length);
    }

    for (uint8_t iteration = 0; iteration < _n; ++iteration) {
        uint16_t  increment = (uint16_t) (1 << iteration);
        for (uint16_t j = 0; j < increment; j +=  1) {
            for (uint16_t i = 0; i < _block_length; i += 2 * increment) {
                info_bits_padded.at(i + j) = (uint8_t)((info_bits_padded.at(i + j) + info_bits_padded.at(i + j + increment)) % 2);
            }
        }
    }


    for (uint16_t i = 0; i < _block_length; ++i) {
        coded_bits.at(i) = info_bits_padded.at(_bit_rev_order.at(i));
    }

    return coded_bits;

}
std::vector<uint8_t> PolarCode::reverse_arikan(std::vector<uint8_t> info_bits_padded) {

    //std::vector<uint8_t> rev_info_bits_padded(_block_length, 0);
    std::vector<uint8_t> rev_coded_bits(_block_length);
    std::vector<uint8_t> rev_info_bits_des_order(_block_length);
    

    for (uint8_t iteration = 0; iteration < _n; ++iteration) {
        uint16_t  increment = (uint16_t) (1 << iteration);
        for (uint16_t j = 0; j < increment; j +=  1) {
            for (uint16_t i = 0; i < _block_length; i += 2 * increment) {
                info_bits_padded.at(i + j) = (uint8_t)((info_bits_padded.at(i + j) + info_bits_padded.at(i + j + increment)) % 2);
            }
        }
    }

    for (uint16_t i = 0; i < _block_length; ++i) {
        rev_coded_bits.at(i) = info_bits_padded.at(_bit_rev_order.at(i));
    }
    for (uint16_t i = 0; i < _block_length; ++i) {
        rev_info_bits_des_order.at(i) = rev_coded_bits.at(_channel_order_descending.at(i));
    }

    return rev_info_bits_des_order;
}

std::vector<uint8_t> PolarCode::arikan(std::vector<uint8_t> info_bits) {

    std::vector<uint8_t> info_bits_padded(_block_length, 0);
    std::vector<uint8_t> coded_bits(_block_length);

    for (uint16_t i = 0; i < _info_length; ++i) {
        info_bits_padded.at(_channel_order_descending.at(i)) = info_bits.at(i);
    }
    for (uint16_t i = _info_length+_crc_size; i < _block_length; ++i) {
        info_bits_padded.at(_channel_order_descending.at(i)) = info_bits.at(i);
    }

    for (uint8_t iteration = 0; iteration < _n; ++iteration) {
        uint16_t  increment = (uint16_t) (1 << iteration);
        for (uint16_t j = 0; j < increment; j +=  1) {
            for (uint16_t i = 0; i < _block_length; i += 2 * increment) {
                info_bits_padded.at(i + j) = (uint8_t)((info_bits_padded.at(i + j) + info_bits_padded.at(i + j + increment)) % 2);
            }
        }
    }


    for (uint16_t i = 0; i < _block_length; ++i) {
        coded_bits.at(i) = info_bits_padded.at(_bit_rev_order.at(i));
    }

    return coded_bits;

}

bool PolarCode::crc_check(uint8_t * info_bit_padded) {
    bool crc_pass = true;
    for (uint16_t i = _info_length; i < _info_length + _crc_size; ++i) {
        uint8_t  crc_bit = 0;
        for (uint16_t j = 0; j < _info_length; ++j) {
            crc_bit = (uint8_t) ((crc_bit + _crc_matrix.at(i - _info_length).at(j) * info_bit_padded[_channel_order_descending.at(j)]) % 2);
        }
        //modification for CB
        crc_bit= info_bit_padded[_channel_order_descending.at(i-_info_length)];
        if (crc_bit != info_bit_padded[_channel_order_descending.at(i)]) {
            crc_pass = false;
            break;
        }
    }

    return crc_pass;
}

std::vector<uint8_t> PolarCode::decode_scl_p1(std::vector<double> p1, std::vector<double> p0, uint16_t list_size) {

    _list_size = list_size;
    _llr_based_computation = false;

    initializeDataStructures();

    uint16_t  l = assignInitialPath();

    double * p_0 = getArrayPointer_P(0, l);

    for (uint16_t beta = 0; beta < _block_length; ++beta ) {
        p_0[2*beta] = (double) p0.at(beta);
        p_0[2*beta + 1] = (double) p1.at(beta);
    }

    return decode_scl();

}

std::vector<uint8_t> PolarCode::decode_scl_llr(std::vector<double> llr, uint16_t list_size) {

    _list_size = list_size;

    _llr_based_computation = true;

    initializeDataStructures();

    uint16_t  l = assignInitialPath();

    double * llr_0 = getArrayPointer_LLR(0, l);

    for (uint16_t beta = 0; beta < _block_length; ++beta ) {
        llr_0[beta] = llr.at(beta);
    }

    return decode_scl();

}

std::vector<uint8_t> PolarCode::decode_scl() {

    for (uint16_t phi = 0; phi < _block_length; ++phi ){

        if (_llr_based_computation )
            recursivelyCalcLLR(_n, phi);
        else
            recursivelyCalcP(_n, phi);


        if (_frozen_bits.at(phi) == 1)
			{
				/*std::cout << phi;
				std::cout<< ":";
				std::cout<< +(_frozen_bits_values.at(phi));
				std::cout<<",";*/
                continuePaths_FrozenBit(phi);
		}
        else
            continuePaths_UnfrozenBit(phi);

        if ((phi%2) == 1)
            recursivelyUpdateC(_n, phi);

    }
    uint16_t l = findMostProbablePath((bool) _crc_size);
    //std::cout << l;
    uint8_t * c_0 = _arrayPointer_Info.at(l);
    std::vector<uint8_t> deocded_info_bits(_info_length);
    std::vector<uint8_t> deocded_block(_block_length);
    for (uint16_t beta = 0; beta < _info_length; ++beta )
        deocded_info_bits.at(beta) = c_0[_channel_order_descending.at(beta)];
    
    //std::cout << "decoded:\n";
    for (uint16_t beta = 0; beta < _block_length; ++beta )
        {
		deocded_block.at(beta) = c_0[_channel_order_descending.at(beta)];        
        //std::cout << +(deocded_block.at(beta));
        }
	

    for (uint16_t s = 0; s < _list_size; ++s) {
        delete[] _arrayPointer_Info.at(s);
        for (uint16_t lambda = 0; lambda < _n + 1; ++lambda) {

            if (_llr_based_computation )
                delete[] _arrayPointer_LLR.at(lambda).at(s);
            else
                delete[] _arrayPointer_P.at(lambda).at(s);
            delete[] _arrayPointer_C.at(lambda).at(s);
        }
    }

    return deocded_info_bits;

}
//------------file
std::vector<uint8_t> PolarCode::decode_scl_llr_file(std::vector<double> llr, uint16_t list_size) {

    _list_size = list_size;

    _llr_based_computation = true;

    initializeDataStructures();

    uint16_t  l = assignInitialPath();

    double * llr_0 = getArrayPointer_LLR(0, l);

    for (uint16_t beta = 0; beta < _block_length; ++beta ) {
        llr_0[beta] = llr.at(beta);
    }

    return decode_scl_file();

}

std::vector<uint8_t> PolarCode::decode_scl_file() {

    for (uint16_t phi = 0; phi < _block_length; ++phi ){

        if (_llr_based_computation )
            recursivelyCalcLLR(_n, phi);
        else
            recursivelyCalcP(_n, phi);


        if (_frozen_bits.at(phi) == 1)
			{
				/*std::cout << phi;
				std::cout<< ":";
				std::cout<< +(_frozen_bits_values.at(phi));
				std::cout<<",";*/
                continuePaths_FrozenBit(phi);
		}
        else
            continuePaths_UnfrozenBit(phi);

        if ((phi%2) == 1)
            recursivelyUpdateC(_n, phi);

    }
    uint16_t l = findMostProbablePath((bool) _crc_size);
    //std::cout << l;
    uint8_t * c_0 = _arrayPointer_Info.at(l);
    std::vector<uint8_t> deocded_info_bits(_info_length);
    std::vector<uint8_t> deocded_block(_block_length);
    for (uint16_t beta = 0; beta < _info_length; ++beta )
        deocded_info_bits.at(beta) = c_0[_channel_order_descending.at(beta)];
    
    std::cout << "decoded:\n";
    for (uint16_t beta = 0; beta < _block_length; ++beta )
        {
		deocded_block.at(beta) = c_0[_channel_order_descending.at(beta)];        
        std::cout << +(deocded_block.at(beta));
        }
	

    for (uint16_t s = 0; s < _list_size; ++s) {
        delete[] _arrayPointer_Info.at(s);
        for (uint16_t lambda = 0; lambda < _n + 1; ++lambda) {

            if (_llr_based_computation )
                delete[] _arrayPointer_LLR.at(lambda).at(s);
            else
                delete[] _arrayPointer_P.at(lambda).at(s);
            delete[] _arrayPointer_C.at(lambda).at(s);
        }
    }

    return deocded_block;

}
//---file end
void PolarCode::initializeDataStructures() {

    while (_inactivePathIndices.size()) {
        _inactivePathIndices.pop();
    };
    _activePath.resize(_list_size);

    if (_llr_based_computation) {
        _pathMetric_LLR.resize(_list_size);
        _arrayPointer_LLR.resize(_n + 1);
        for (int i = 0; i < _n + 1; ++i)
            _arrayPointer_LLR.at(i).resize(_list_size);
    }
    else {
        _arrayPointer_P.resize(_n + 1);
        for (int i = 0; i < _n + 1; ++i)
            _arrayPointer_P.at(i).resize(_list_size);
    }

    _arrayPointer_C.resize(_n + 1);
    for (int i = 0; i < _n + 1; ++i)
        _arrayPointer_C.at(i).resize(_list_size);

    _arrayPointer_Info.resize(_list_size);

    _pathIndexToArrayIndex.resize(_n + 1);
    for (int i = 0; i < _n + 1; ++i)
        _pathIndexToArrayIndex.at(i).resize(_list_size);

    _inactiveArrayIndices.resize(_n + 1);
    for (int i = 0; i < _n + 1; ++i) {
        while (_inactiveArrayIndices.at(i).size()) {
            _inactiveArrayIndices.at(i).pop();
        };
    }

    _arrayReferenceCount.resize(_n + 1);
    for (int i = 0; i < _n + 1; ++i)
        _arrayReferenceCount.at(i).resize(_list_size);

    for (uint16_t s = 0; s < _list_size; ++s) {
        _arrayPointer_Info.at(s) = new uint8_t[_block_length]();
        for (uint16_t lambda = 0; lambda < _n + 1; ++lambda) {
            if (_llr_based_computation) {
                _arrayPointer_LLR.at(lambda).at(s) = new double[(1 << (_n - lambda))]();
            }
            else {
                _arrayPointer_P.at(lambda).at(s) = new double[2 * (1 << (_n - lambda))]();
            }
            _arrayPointer_C.at(lambda).at(s) = new uint8_t[2 * (1 << (_n - lambda))]();
            _arrayReferenceCount.at(lambda).at(s) = 0;
            _inactiveArrayIndices.at(lambda).push(s);
        }
    }

    for (uint16_t l = 0; l < _list_size; ++l) {
        _activePath.at(l) = 0;
        _inactivePathIndices.push(l);
        if (_llr_based_computation) {
            _pathMetric_LLR.at(l) = 0;
        }
    }
}

uint16_t PolarCode::assignInitialPath() {

    uint16_t  l = _inactivePathIndices.top();
    _inactivePathIndices.pop();
    _activePath.at(l) = 1;
    // Associate arrays with path index
    for (uint16_t lambda = 0; lambda < _n + 1; ++lambda) {
        uint16_t  s = _inactiveArrayIndices.at(lambda).top();
        _inactiveArrayIndices.at(lambda).pop();
        _pathIndexToArrayIndex.at(lambda).at(l) = s;
        _arrayReferenceCount.at(lambda).at(s) = 1;
    }
    return l;
}

uint16_t PolarCode::clonePath(uint16_t l) {
    uint16_t l_p = _inactivePathIndices.top();
    _inactivePathIndices.pop();
    _activePath.at(l_p) = 1;

    if (_llr_based_computation)
        _pathMetric_LLR.at(l_p) = _pathMetric_LLR.at(l);

    for (uint16_t lambda = 0; lambda < _n + 1; ++lambda ) {
        uint16_t s = _pathIndexToArrayIndex.at(lambda).at(l);
        _pathIndexToArrayIndex.at(lambda).at(l_p) = s;
        _arrayReferenceCount.at(lambda).at(s)++;
    }
    return l_p;
}

void PolarCode::killPath(uint16_t l) {
    _activePath.at(l) = 0;
    _inactivePathIndices.push(l);
    if (_llr_based_computation )
        _pathMetric_LLR.at(l) = 0;

    for (uint16_t lambda = 0; lambda < _n + 1; ++lambda ) {
        uint16_t s = _pathIndexToArrayIndex.at(lambda).at(l);
        _arrayReferenceCount.at(lambda).at(s)--;
        if (_arrayReferenceCount.at(lambda).at(s) == 0 ) {
            _inactiveArrayIndices.at(lambda).push(s);
        }
    }
}

double * PolarCode::getArrayPointer_P(uint16_t lambda, uint16_t  l) {
    uint16_t  s = _pathIndexToArrayIndex.at(lambda).at(l);
    uint16_t s_p;
    if (_arrayReferenceCount.at(lambda).at(s) == 1) {
        s_p = s;
    }
    else {
        s_p = _inactiveArrayIndices.at(lambda).top();
        _inactiveArrayIndices.at(lambda).pop();

        //copy
        std::copy(_arrayPointer_P.at(lambda).at(s), _arrayPointer_P.at(lambda).at(s) +  (1 << (_n - lambda + 1)),  _arrayPointer_P.at(lambda).at(s_p));
        std::copy(_arrayPointer_C.at(lambda).at(s), _arrayPointer_C.at(lambda).at(s) +  (1 << (_n - lambda + 1)),  _arrayPointer_C.at(lambda).at(s_p));

        _arrayReferenceCount.at(lambda).at(s)--;
        _arrayReferenceCount.at(lambda).at(s_p) = 1;
        _pathIndexToArrayIndex.at(lambda).at(l) = s_p;
    }
    return _arrayPointer_P.at(lambda).at(s_p);
}

double * PolarCode::getArrayPointer_LLR(uint16_t lambda, uint16_t  l) {
    uint16_t  s = _pathIndexToArrayIndex.at(lambda).at(l);
    uint16_t s_p;
    if (_arrayReferenceCount.at(lambda).at(s) == 1) {
        s_p = s;
    }
    else {
        s_p = _inactiveArrayIndices.at(lambda).top();
        _inactiveArrayIndices.at(lambda).pop();

        //copy
        std::copy(_arrayPointer_C.at(lambda).at(s), _arrayPointer_C.at(lambda).at(s) +  (1 << (_n - lambda + 1)),  _arrayPointer_C.at(lambda).at(s_p));
        std::copy(_arrayPointer_LLR.at(lambda).at(s), _arrayPointer_LLR.at(lambda).at(s) +  (1 << (_n - lambda)),  _arrayPointer_LLR.at(lambda).at(s_p));

        _arrayReferenceCount.at(lambda).at(s)--;
        _arrayReferenceCount.at(lambda).at(s_p) = 1;
        _pathIndexToArrayIndex.at(lambda).at(l) = s_p;
    }
    return _arrayPointer_LLR.at(lambda).at(s_p);
}


uint8_t * PolarCode::getArrayPointer_C(uint16_t lambda, uint16_t  l) {
    uint16_t  s = _pathIndexToArrayIndex.at(lambda).at(l);
    uint16_t s_p;
    if (_arrayReferenceCount.at(lambda).at(s) == 1) {
        s_p = s;
    }
    else {

        s_p = _inactiveArrayIndices.at(lambda).top();
        _inactiveArrayIndices.at(lambda).pop();

        //copy
        if (_llr_based_computation )
            std::copy(_arrayPointer_LLR.at(lambda).at(s), _arrayPointer_LLR.at(lambda).at(s) +  (1 << (_n - lambda)),  _arrayPointer_LLR.at(lambda).at(s_p));
        else
            std::copy(_arrayPointer_P.at(lambda).at(s), _arrayPointer_P.at(lambda).at(s) +  (1 << (_n - lambda + 1)),  _arrayPointer_P.at(lambda).at(s_p));

        std::copy(_arrayPointer_C.at(lambda).at(s), _arrayPointer_C.at(lambda).at(s) +  (1 << (_n - lambda + 1)),  _arrayPointer_C.at(lambda).at(s_p));

        _arrayReferenceCount.at(lambda).at(s)--;
        _arrayReferenceCount.at(lambda).at(s_p) = 1;
        _pathIndexToArrayIndex.at(lambda).at(l) = s_p;

    }
    return _arrayPointer_C.at(lambda).at(s_p);
}

void PolarCode::recursivelyCalcP(uint16_t lambda, uint16_t phi) {
    if ( lambda == 0 )
        return;
    uint16_t psi = phi >> 1;
    if ( (phi % 2) == 0)
        recursivelyCalcP(lambda -1, psi);

    double sigma = 0.0f;
    for (uint16_t l = 0; l < _list_size; ++l) {
        if (_activePath.at(l) == 0)
            continue;
        double * p_lambda = getArrayPointer_P(lambda, l);
        double * p_lambda_1 = getArrayPointer_P(lambda - 1, l);

        uint8_t * c_lambda = getArrayPointer_C(lambda, l);
        for (uint16_t beta = 0; beta < (1 << (_n - lambda)); ++beta) {
            if ( (phi %2) == 0 ){
                p_lambda[2 * beta] = 0.5f * ( p_lambda_1[2*(2*beta)]*p_lambda_1[2*(2*beta+1)]
                                              + p_lambda_1[2*(2*beta) + 1]*p_lambda_1[2*(2*beta+1) + 1]);
                p_lambda[2 * beta + 1] = 0.5f * ( p_lambda_1[2*(2*beta) +1]*p_lambda_1[2*(2*beta+1)]
                                                  + p_lambda_1[2*(2*beta)]*p_lambda_1[2*(2*beta+1) + 1]);
            }
            else {
                uint8_t  u_p = c_lambda[2*beta];
                p_lambda[2 * beta] = 0.5f * p_lambda_1[2*(2*beta) + (u_p % 2)] *   p_lambda_1[2*(2*beta + 1)];
                p_lambda[2 * beta + 1] = 0.5f * p_lambda_1[2*(2*beta) + ((u_p+1) % 2)] *   p_lambda_1[2*(2*beta + 1) + 1];
            }
            sigma = std::max(sigma,  p_lambda[2 * beta]);
            sigma = std::max(sigma,  p_lambda[2 * beta + 1]);


        }
    }

    for (uint16_t l = 0; l < _list_size; ++l) {
        if (sigma == 0) // Typically happens because of undeflow
            break;
        if (_activePath.at(l) == 0)
            continue;
        double *p_lambda = getArrayPointer_P(lambda, l);
        for (uint16_t beta = 0; beta < (1 << (_n - lambda)); ++beta) {
            p_lambda[2 * beta] = p_lambda[2 * beta] / sigma;
            p_lambda[2 * beta + 1] = p_lambda[2 * beta + 1] / sigma;
        }
    }
}

void PolarCode::recursivelyCalcLLR(uint16_t lambda, uint16_t phi) {
    if ( lambda == 0 )
        return;
    uint16_t psi = phi >> 1;
    if ( (phi % 2) == 0)
        recursivelyCalcLLR(lambda -1, psi);

    for (uint16_t l = 0; l < _list_size; ++l) {
        if (_activePath.at(l) == 0)
            continue;
        double * llr_lambda = getArrayPointer_LLR(lambda, l);
        double * llr_lambda_1 = getArrayPointer_LLR(lambda - 1, l);

        uint8_t * c_lambda = getArrayPointer_C(lambda, l);
        for (uint16_t beta = 0; beta < (1 << (_n - lambda)); ++beta) {
            if ( (phi %2) == 0 ){
                if (40 > std::max(std::abs(llr_lambda_1[2 * beta]), std::abs(llr_lambda_1[2 * beta + 1]))){
                    llr_lambda[beta] = std::log ( (exp(llr_lambda_1[2 * beta] + llr_lambda_1[2 * beta + 1]) + 1) /
                                                  (exp(llr_lambda_1[2*beta]) + exp(llr_lambda_1[2*beta+1])));
                }
                else {
                    llr_lambda[beta] = (double)  ((llr_lambda_1[2 * beta] < 0) ? -1 : (llr_lambda_1[2 * beta] > 0)) *
                                       ((llr_lambda_1[2 * beta + 1] < 0) ? -1 : (llr_lambda_1[2 * beta + 1] > 0)) *
                                       std::min( std::abs(llr_lambda_1[2 * beta]), std::abs(llr_lambda_1[2 * beta + 1]));
                }
            }
            else {
                uint8_t  u_p = c_lambda[2*beta];
                llr_lambda[beta] = (1 - 2 * u_p) * llr_lambda_1[2*beta] + llr_lambda_1[2*beta + 1];
            }

        }
    }
}

void PolarCode::recursivelyUpdateC(uint16_t lambda, uint16_t phi) {

    uint16_t psi = phi >> 1;
    for (uint16_t l = 0; l < _list_size; ++l) {
        if (_activePath.at(l) == 0)
            continue;
        uint8_t *c_lambda = getArrayPointer_C(lambda, l);
        uint8_t *c_lambda_1 = getArrayPointer_C(lambda - 1, l);
        for (uint16_t beta = 0; beta < (1 << (_n - lambda)); ++beta) {
            c_lambda_1[2 * (2 * beta) + (psi % 2)] = (uint8_t) ((c_lambda[2 * beta] + c_lambda[2 * beta + 1]) % 2);
            c_lambda_1[2 * (2 * beta + 1) + (psi % 2)] = c_lambda[2 * beta + 1];
        }
    }
    if ( (psi % 2) == 1)
        recursivelyUpdateC((uint16_t) (lambda - 1), psi);

}

void PolarCode::continuePaths_FrozenBit(uint16_t phi) {
    for (uint16_t l = 0; l < _list_size; ++ l) {
        if (_activePath.at(l) == 0)
            continue;
        uint8_t  * c_m = getArrayPointer_C(_n, l);
        //c_m[(phi % 2)] = _frozen_bits_values.at(phi); // frozen value assumed to be zero !!
        c_m[(phi % 2)]=_info_bits_padded.at(phi);
       
		//std::cout << phi;
		//std::cout<< "\n";
		//std::cout << (phi%2);
		//std::cout<<"\n";
		//std::cout<<"value";
		//std::cout<<"\n";
		//std::cout << +(_frozen_bits_values.at(phi));
		//c_m[0] = _frozen_bits_values.at(0);
		
        if (_llr_based_computation) {
            double *llr_p = getArrayPointer_LLR(_n, l);
            _pathMetric_LLR.at(l) += log(1 + exp(-llr_p[0]));
        }
        //_arrayPointer_Info.at(l)[phi] =_frozen_bits_values.at(phi); //check here for frozen bits
        _arrayPointer_Info.at(l)[phi] =_info_bits_padded.at(phi); //check here for frozen bits
        }
}

void PolarCode::continuePaths_UnfrozenBit(uint16_t phi) {

    std::vector<double>  probForks((unsigned long) (2 * _list_size));
    std::vector<double> probabilities;
    std::vector<uint8_t>  contForks((unsigned long) (2 * _list_size));


    uint16_t  i = 0;
    for (unsigned l = 0; l < _list_size; ++l) {
        if (_activePath.at(l) == 0) {
            probForks.at(2 * l) = NAN;
            probForks.at(2 * l + 1) = NAN;
        }
        else {
            if (_llr_based_computation ) {
                double *llr_p = getArrayPointer_LLR(_n, l);
                probForks.at(2 * l) =  - (_pathMetric_LLR.at(l) + log(1 + exp(-llr_p[0])));
                probForks.at(2 * l + 1) = -  (_pathMetric_LLR.at(l) + log(1 + exp(llr_p[0])));
            }
            else {
                double *p_m = getArrayPointer_P(_n, l);
                probForks.at(2 * l) = p_m[0];
                probForks.at(2 * l + 1) = p_m[1];
            }

            probabilities.push_back(probForks.at(2 * l));
            probabilities.push_back(probForks.at(2 * l +1));

            i++;
        }
    }

    uint16_t  rho = _list_size;
    if ( (2*i) < _list_size)
        rho = (uint16_t) 2 * i;

    for (uint8_t l = 0; l < 2 * _list_size; ++l) {
        contForks.at(l) = 0;
    }
    std::sort(probabilities.begin(), probabilities.end(), std::greater<double>());

    double threshold = probabilities.at((unsigned long) (rho - 1));
    uint16_t num_paths_continued = 0;

    for (uint8_t l = 0; l < 2 * _list_size; ++l) {
        if (probForks.at(l) > threshold) {
            contForks.at(l) = 1;
            num_paths_continued++;
        }
        if (num_paths_continued == rho) {
            break;
        }
    }

    if  ( num_paths_continued < rho ) {
        for (uint8_t l = 0; l < 2 * _list_size; ++l) {
            if (probForks.at(l) == threshold) {
                contForks.at(l) = 1;
                num_paths_continued++;
            }
            if (num_paths_continued == rho) {
                break;
            }
        }
    }

    for (unsigned l = 0; l < _list_size; ++l) {
        if (_activePath.at(l) == 0)
            continue;
        if ( contForks.at(2 * l)== 0 && contForks.at(2 * l + 1) == 0 )
            killPath(l);
    }

    for (unsigned l = 0; l < _list_size; ++l) {
        if ( contForks.at(2 * l) == 0 && contForks.at(2 * l + 1) == 0 )
            continue;
        uint8_t * c_m = getArrayPointer_C(_n, l);

        if ( contForks.at(2 * l) == 1 && contForks.at(2 * l + 1) == 1 ) {

            c_m[(phi%2)] = 0;
            uint16_t l_p = clonePath(l);
            c_m = getArrayPointer_C(_n, l_p);
            c_m[(phi%2)] = 1;

            std::copy(_arrayPointer_Info.at(l), _arrayPointer_Info.at(l) +  phi,  _arrayPointer_Info.at(l_p));
            _arrayPointer_Info.at(l)[phi] = 0;
            _arrayPointer_Info.at(l_p)[phi] = 1;

            if (_llr_based_computation ) {
                double *llr_p = getArrayPointer_LLR(_n, l);
                _pathMetric_LLR.at(l) += log(1 + exp(-llr_p[0]));
                llr_p = getArrayPointer_LLR(_n, l_p);
                _pathMetric_LLR.at(l_p) += log(1 + exp(llr_p[0]));
            }

        }
        else {
            if ( contForks.at(2 * l) == 1) {
                c_m[(phi%2)] = 0;
                _arrayPointer_Info.at(l)[phi] = 0;

                if (_llr_based_computation ) {
                    double *llr_p = getArrayPointer_LLR(_n, l);
                    _pathMetric_LLR.at(l) += log(1 + exp(-llr_p[0]));
                }
            }
            else {
                c_m[(phi%2)] = 1;
                _arrayPointer_Info.at(l)[phi] = 1;
                if (_llr_based_computation ) {
                    double *llr_p = getArrayPointer_LLR(_n, l);
                    _pathMetric_LLR.at(l) += log(1 + exp(llr_p[0]));
                }
            }
        }
    }

}

uint16_t PolarCode::findMostProbablePath(bool check_crc) {

    uint16_t  l_p = 0;
    double p_p1 = 0;
    double p_llr = std::numeric_limits<double>::max();
    bool path_with_crc_pass = false;
    for (uint16_t l = 0; l < _list_size; ++l) {

        if (_activePath.at(l) == 0)
            continue;

        if ( (check_crc) && (! crc_check(_arrayPointer_Info.at(l))))
            continue;

        path_with_crc_pass = true;

        if (_llr_based_computation) {
            if (_pathMetric_LLR.at(l) < p_llr ) {
                p_llr = _pathMetric_LLR.at(l);
                l_p  = l;
            }
        }
        else {
            uint8_t * c_m = getArrayPointer_C(_n, l);
            double * p_m = getArrayPointer_P(_n, l);
            if ( p_p1 < p_m[c_m[1]]) {
                l_p = l;
                p_p1 = p_m[c_m[1]];
            }
        }
    }
    if ( path_with_crc_pass)
        return l_p;
    else
        return findMostProbablePath(false);
}


void PolarCode::create_bit_rev_order() {
    for (uint16_t i = 0; i < _block_length; ++i) {
        uint16_t to_be_reversed = i;
        _bit_rev_order.at(i) = (uint16_t) ((to_be_reversed & 1) << (_n - 1));
        for (uint8_t j = (uint8_t) (_n - 1); j; --j) {
            to_be_reversed >>= 1;
            _bit_rev_order.at(i) += (to_be_reversed & 1) << (j - 1);
        }
    }
}

std::vector<std::vector<double>> PolarCode::get_bler_quick(std::vector<double> flipp_vec,
                                                           std::vector<uint8_t> list_size_vec) {

    int max_err = 1000;
    int max_runs = 500000;

    std::vector<std::vector<double>> bler;
    std::vector<std::vector<double>> num_err;
    std::vector<std::vector<double>> num_run;

    bler.resize(list_size_vec.size());
    num_err.resize((list_size_vec.size()));
    num_run.resize(list_size_vec.size());

    for (unsigned l = 0; l < list_size_vec.size(); ++l) {
        bler.at(l).resize(flipp_vec.size(), 0);
        num_err.at(l).resize(flipp_vec.size(), 0);
        num_run.at(l).resize(flipp_vec.size(), 0);
    }

    std::vector<uint8_t> coded_bits;
    //std::vector<double> bpsk(_block_length);
    std::vector<double> received_signal(_block_length, 0);
    std::vector<uint8_t> info_bits(_info_length, 0);

    //double N_0  = 1.0;
//    double sigma_sqrt_pi = std::sqrt(N_0 * 3.1415f);

    std::vector<uint8_t> noise(_block_length, 0);

    //std::normal_distribution<double> gauss_dist(0.0f, N_0);
    //std::default_random_engine generator;

//    std::vector<double> p0(_block_length), p1(_block_length);
    std::vector<double> llr(_block_length);

    std::chrono::high_resolution_clock::time_point t1 = std::chrono::high_resolution_clock::now();

    for (int run = 0; run < max_runs; ++run) {
        if ((run % (max_runs/100)) == 0) {
            std::chrono::high_resolution_clock::time_point t2 = std::chrono::high_resolution_clock::now();
            auto duration = std::chrono::duration_cast<std::chrono::microseconds>( t2 - t1 ).count();
            std::cout << "Running iteration " << run << "; time elapsed = " << duration/1000/1000 << " seconds"
                "; percent complete = " << (100 * run)/max_runs << "." << std::endl;
        }
        if ( (run % 100) == 0) {
            for(uint16_t i = 0; i < _info_length; ++ i ){
                info_bits.at(i) = (uint8_t) ( rand() % 2);
            }
        }
        //for(uint16_t i = 0; i < _block_length; ++ i ) {
          //noise.at(i) = (double) gauss_dist(generator);
                 
        //}

        coded_bits = encode(info_bits);

        //for(uint16_t i = 0; i < _block_length; ++ i ) {
          //  bpsk.at(i) = 2.0f * ((double) coded_bits.at(i)) - 1.0f;
        //}

        for (unsigned l_index = 0; l_index < list_size_vec.size(); ++l_index) {

            std::vector<bool> prev_decoded(0);
            prev_decoded.resize(flipp_vec.size(), false);

            for (unsigned i_flipp = 0; i_flipp < flipp_vec.size(); ++i_flipp) {

                if ( num_err.at(l_index).at(i_flipp) > max_err )
                    continue;

                num_run.at(l_index).at(i_flipp)++;

                bool run_sim = true;
                /*
                for(unsigned i_flipp2 = 0; i_flipp2 > i_ebno; ++i_ebno2) {
                    if (prev_decoded.at(i_ebno2)) {
                        //  This is a hack to speed up simulations -- it assumes that this run will be decoded
                        // correctly since it was decoded correctly for a lower EbNo
                        run_sim = false;
                    }
                }*/

                 if (!run_sim) {
                     continue;
                 }

                //double snr_sqrt_linear = std::pow(10.0f, ebno_vec.at(i_ebno)/20)
                //                         * std::sqrt( ((double) _info_length )/((double) (_block_length) )) ;
                for (uint16_t i = 0; i < _block_length; ++i) {
                    //received_signal.at(i) =  snr_sqrt_linear * bpsk.at(i) + std::sqrt(N_0 / 2) * noise.at(i);
                    received_signal.at(i) =  coded_bits.at(i)+(uint8_t) (rand()%100) < (flipp_vec.at(i_flipp)*100);
                    
                }
                for (uint16_t i = 0; i < _block_length; ++i) {
//                    p0.at(i) = exp(-(received_signal.at(i) + snr_sqrt_linear )*(received_signal.at(i) + snr_sqrt_linear )/N_0)/sigma_sqrt_pi;
//                    p1.at(i) = exp(-(received_signal.at(i) - snr_sqrt_linear )*(received_signal.at(i) - snr_sqrt_linear )/N_0)/sigma_sqrt_pi;
                      //llr.at(i) = - 4 * received_signal.at(i) * snr_sqrt_linear / N_0;
                      //Above indicates p0/p1
                      if (received_signal.at(i)==1)
                      {
						  llr.at(i)= log((flipp_vec.at(i_flipp))/(1-flipp_vec.at(i_flipp)))  ; // p1_0/ p1_1
					  }
					  else
					  {
						  llr.at(i)= log((1-flipp_vec.at(i_flipp))/flipp_vec.at(i_flipp));//p0_0/p1_1
					  }
                }

//                std::vector<uint8_t> decoded_info_bits = polar_code.decode_scl_p1(p1, p0, list_size);
                std::vector<uint8_t> decoded_info_bits = decode_scl_llr(llr, list_size_vec.at(l_index)); //llr and listsize

                bool err = false;
                for (uint16_t i = 0; i < _info_length; ++i) {
                    if (info_bits.at(i) != decoded_info_bits.at(i)) {
                        err = true;
                        break;
                    }
                }

                if (err)
                    num_err.at(l_index).at(i_flipp)++;
                else
                    prev_decoded.at(i_flipp) = true;

            } // EbNo Loop End

        } //List_size loop end

    } // run loop end

    for (unsigned l_index = 0; l_index < list_size_vec.size(); ++l_index) {
        for (unsigned i_flipp = 0; i_flipp < flipp_vec.size(); ++i_flipp) {
            bler.at(l_index).at(i_flipp) = num_err.at(l_index).at(i_flipp)/num_run.at(l_index).at(i_flipp);
        }
    }

    return bler;

}
//------------------------member wrappers

//pylist to vector converters.
std::vector<uint8_t> PolarCode::py_list_to_std_vector( const boost::python::object& iterable )
{
	return std::vector<uint8_t>( boost::python::stl_input_iterator<uint8_t>( iterable ),
                            boost::python::stl_input_iterator<uint8_t>( ) );
}
	
boost::python::list PolarCode::std_vector_to_py_list(std::vector<uint8_t> vector) {
std::vector<uint8_t>::iterator iter;
typename boost::python::list list;
for (iter = vector.begin(); iter != vector.end(); ++iter) {
		list.append(*iter);
	}
   return list;
}
//----
std::vector<uint16_t> PolarCode::py_list_to_std_vector16( const boost::python::object& iterable )
{
	return std::vector<uint16_t>( boost::python::stl_input_iterator<uint16_t>( iterable ),
                            boost::python::stl_input_iterator<uint16_t>( ) );
}
	
boost::python::list PolarCode::std_vector_to_py_list16(std::vector<uint16_t> vector) {
std::vector<uint16_t>::iterator iter;
typename boost::python::list list;
for (iter = vector.begin(); iter != vector.end(); ++iter) {
		list.append(*iter);
	}
   return list;
}
//----
std::vector<double> PolarCode::py_list_to_std_vector_dbl( const boost::python::object& iterable )
{
	return std::vector<double>( boost::python::stl_input_iterator<double>( iterable ),
                            boost::python::stl_input_iterator<double>( ) );
}
	
boost::python::list PolarCode::std_vector_to_py_list_dbl(std::vector<double> vector) {
std::vector<double>::iterator iter;
typename boost::python::list list;
for (iter = vector.begin(); iter != vector.end(); ++iter) {
		list.append(*iter);
	}
   return list;
}

//----------------converters end
// dummy setvector
void PolarCode::setvector(boost::python::list binarystring)  
{
	vMsg=py_list_to_std_vector(binarystring);
    for (std::vector<uint8_t>::const_iterator i = vMsg.begin(); i != vMsg.end(); ++i)
	std::cout << +(*i) << ' ';
	}
boost::python::list PolarCode::getvector() { return std_vector_to_py_list(vMsg); }	

//other params
void PolarCode::setfrozen_bits(boost::python::list binarystring)  
{
	_frozen_bits_values=py_list_to_std_vector(binarystring);
	//for (uint16_t i = _info_length+_crc_size; i < _block_length; ++i) {
      //  _info_bits_padded.at(_channel_order_descending.at(i)) = _frozen_bits_values.at(i);
   // }
    //for (std::vector<uint8_t>::const_iterator i = _frozen_bits_values.begin(); i != _frozen_bits_values.end(); ++i)
	//std::cout << +(*i) << ' ';
	}
boost::python::list PolarCode::getfrozen_bits() { return std_vector_to_py_list(_frozen_bits_values); }

void PolarCode::setfrozen_bits_indic(boost::python::list binarystring)  
{
	_frozen_bits=py_list_to_std_vector(binarystring);
    //for (std::vector<uint8_t>::const_iterator i = _frozen_bits_values.begin(); i != _frozen_bits_values.end(); ++i)
	//std::cout << +(*i) << ' ';
	}
boost::python::list PolarCode::getfrozen_bits_indic() { return std_vector_to_py_list(_frozen_bits); }
	
void PolarCode::setchannel_order_descending(boost::python::list pylist)  
{
	_channel_order_descending=py_list_to_std_vector16(pylist);
    //for (std::vector<uint16_t>::const_iterator i = _channel_order_descending.begin(); i != _channel_order_descending.end(); ++i)
	//std::cout << +(*i) << ' ';
	}
boost::python::list PolarCode::getchannel_order_descending() { return std_vector_to_py_list16(_channel_order_descending); }	



/*---------------encdec wrappers*/
boost::python::list PolarCode::encode_wrapper(boost::python::list info_bits){ return std_vector_to_py_list(encode(py_list_to_std_vector(info_bits)));}

boost::python::list PolarCode::reverse_arikan_wrapper(boost::python::list info_bits){ return std_vector_to_py_list(reverse_arikan(py_list_to_std_vector(info_bits)));}

boost::python::list PolarCode::arikan_wrapper(boost::python::list info_bits){ return std_vector_to_py_list(arikan(py_list_to_std_vector(info_bits)));}

boost::python::list PolarCode::decode_wrapper(boost::python::list llr, uint8_t list_size)
{ return std_vector_to_py_list(decode_scl_llr(py_list_to_std_vector_dbl(llr),list_size));}

boost::python::list PolarCode::decode_wrapper_f(boost::python::list llr, uint8_t list_size)
{ return std_vector_to_py_list(decode_scl_llr_file(py_list_to_std_vector_dbl(llr),list_size));}
/*    
    
    
    
    std::vector<uint8_t> decode_scl_p1(std::vector<double> p1, std::vector<double> p0, uint16_t list_size);
    std::vector<uint8_t> decode_scl_llr(std::vector<double> llr, uint16_t list_size);

    std::vector<std::vector<double>> get_bler_quick(std::vector<double> ebno_vec, std::vector<uint8_t> list_size);
 
*/
