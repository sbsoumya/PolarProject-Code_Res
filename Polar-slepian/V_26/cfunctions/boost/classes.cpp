#include <boost/python.hpp>
#include <boost/python/list.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/python/stl_iterator.hpp>
#include <boost/python/extract.hpp>
#include <string>
#include <sstream>
#include <vector>
#include <iostream>
#include <memory>


struct World
{
	std::vector<uint8_t> py_list_to_std_vector( const boost::python::object& iterable )
	{
		return std::vector<uint8_t>( boost::python::stl_input_iterator<uint8_t>( iterable ),
                             boost::python::stl_input_iterator<uint8_t>( ) );
	}
	
	boost::python::list std_vector_to_py_list(std::vector<uint8_t> vector) {
	std::vector<uint8_t>::iterator iter;
	typename boost::python::list list;
	for (iter = vector.begin(); iter != vector.end(); ++iter) {
			list.append(*iter);
		}
    return list;
	}
	
    void set(std::string msg) { mMsg = msg; }
    void many(boost::python::list msgs) {
        long l = len(msgs);
        std::stringstream ss;
        for (long i = 0; i<l; ++i) {
            if (i>0) ss << ", ";
            std::string s = boost::python::extract<std::string>(msgs[i]);
            ss << s;
        }
        mMsg = ss.str();
    }
    std::string greet() { return mMsg; }
    std::string mMsg;
    std::vector<uint8_t> vMsg;
    
    void setvector(boost::python::list binarystring)  
    {
		vMsg=py_list_to_std_vector(binarystring);
	    for (std::vector<uint8_t>::const_iterator i = vMsg.begin(); i != vMsg.end(); ++i)
		std::cout << +(*i) << ' ';
		}
	boost::python::list getvector() { return std_vector_to_py_list(vMsg); }	
};

using namespace boost::python;

BOOST_PYTHON_MODULE(classes)
{
    class_<World>("World")
        .def("greet", &World::greet)
        .def("set", &World::set)
        .def("many", &World::many)
        .def("setvector",&World::setvector)
        .def("getvector",&World::getvector)
    ;
};

