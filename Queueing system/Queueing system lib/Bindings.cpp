#define PYBIND11_EXPORT __declspec(dllexport)
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../Queueing system/QueueingSystem.hpp"

namespace py = pybind11;

PYBIND11_MODULE(queueing_system, m) {


    m.doc() = "Queueing system module";

    py::enum_<Status_t>(m, "Status_t")
        .value("created", Status_t::created)
        .value("rejected", Status_t::rejected)
        .value("completed", Status_t::completed);

    py::enum_<Event_t>(m, "Event_t")
        .value("new_request", Event_t::new_request)
        .value("freeing_handler", Event_t::freeing_handler);

    py::class_<Request>(m, "Request")
        .def(py::init<>())
        .def_readwrite("creation_time", &Request::creation_time)
        .def_readwrite("start_time", &Request::start_time)
        .def_readwrite("end_time", &Request::end_time)
        .def_readwrite("source", &Request::source)
        .def_readwrite("request_number", &Request::request_number)
        .def_readwrite("handler", &Request::handler)
        .def_readwrite("status", &Request::status);

    py::class_<Event>(m, "Event")
        .def(py::init<>())
        .def_readwrite("event_time", &Event::event_time)
        .def_readwrite("request", &Event::request)
        .def_readwrite("type", &Event::type)
        .def("__gt__", &Event::operator>);

    py::class_<PoissonGenerator>(m, "PoissonGenerator")
        .def(py::init<double>(), py::arg("lambda"))
        .def("__call__", &PoissonGenerator::operator());

    py::class_<UniformGenerator>(m, "UniformGenerator")
        .def(py::init<double, double>(), py::arg("a"), py::arg("b"))
        .def("__call__", &UniformGenerator::operator());

    py::class_<Handler>(m, "Handler")
        .def(py::init<UniformGenerator*>(), py::arg("generator"))
        .def("setNmb", &Handler::setNmb, py::arg("handler_nmb"))
        .def("setRequest", &Handler::setRequest, py::arg("request"), py::arg("current_time"))
        .def("getHandlerNmb", &Handler::getHandlerNmb)
        .def("getRequestInfo", &Handler::getRequestInfo)
        .def("finishRequest", &Handler::finishRequest)
        .def("isFree", &Handler::isFree);

    py::class_<RequestSource>(m, "RequestSource")
        .def(py::init<PoissonGenerator*>(), py::arg("generator"))
        .def("setName", &RequestSource::setName, py::arg("source_nmb"))
        .def("getNext", &RequestSource::getNext)
        .def("getSourceNmb", &RequestSource::getSourceNmb)
        .def("__call__", &RequestSource::operator());

    py::class_<Buffer>(m, "Buffer")
        .def(py::init<size_t>(), py::arg("buff_capacity"))
        .def("insert", &Buffer::insert, py::arg("request"))
        .def("extract", &Buffer::extract)
        .def("size", &Buffer::size)
        .def("getData", &Buffer::getData);


    py::enum_<SystemParamsSetters>(m, "SystemParamsSetters")
        .value("sources_nmb", SystemParamsSetters::sources_nmb)
        .value("handlers_nmb", SystemParamsSetters::handlers_nmb)
        .value("buffer_sz", SystemParamsSetters::buffer_sz);


    py::class_<SystemParams>(m, "SystemParams")
        .def(py::init<>())
        .def_readwrite("a", &SystemParams::a)
        .def_readwrite("b", &SystemParams::b)
        .def_readwrite("buffer_sz", &SystemParams::buffer_sz)
        .def_readwrite("handlers_nmb", &SystemParams::handlers_nmb)
        .def_readwrite("lambda_", &SystemParams::lambda)
        .def_readwrite("modelligng_time", &SystemParams::modelligng_time)
        .def_readwrite("sources_nmb", &SystemParams::sources_nmb)
        .def("set_param", &SystemParams::set_param);

    py::class_<SourceStats>(m, "SourceStats")
        .def(py::init<>())
        .def_readwrite("dispersion_processing_time", &SourceStats::dispersion_processing_time)
        .def_readwrite("dispersion_time_in_buffer", &SourceStats::dispersion_time_in_buffer)
        .def_readwrite("mean_time_in_buffer", &SourceStats::mean_time_in_buffer)
        .def_readwrite("mean_time_in_system", &SourceStats::mean_time_in_system)
        .def_readwrite("mean_time_of_processing", &SourceStats::mean_time_of_processing)
        .def_readwrite("probability_of_refusal", &SourceStats::probability_of_refusal)
        .def_readwrite("total_requests", &SourceStats::total_requests);

    py::class_<SystemState>(m, "SystemState")
        .def(py::init<>())
        .def_readwrite("event", &SystemState::event)
        .def_readwrite("current_time", &SystemState::current_time)
        .def_readwrite("buffer", &SystemState::buffer)
        .def_readwrite("sources", &SystemState::sources)
        .def_readwrite("handlers", &SystemState::handlers);


    py::class_<SystemResult>(m, "SystemResult")
        .def(py::init<>())
        .def_readwrite("sources", &SystemResult::sources)
        .def_readwrite("handlers", &SystemResult::handlers)
        .def_readwrite("buffer_size", &SystemResult::buffer_size);

    py::class_<QueueingSystem>(m, "QueueingSystem")
        .def(py::init<SystemParams>())
        .def("init", &QueueingSystem::init)
        .def("nextEvent", &QueueingSystem::nextEvent)
        .def("autoModeling", &QueueingSystem::autoModeling)
        .def("getState", &QueueingSystem::getState)
        .def("getResult", &QueueingSystem::getResult);
}