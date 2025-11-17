#include "QueueingSystem.hpp"
#include <iostream>
#include <fstream>
#include<iomanip>

QueueingSystem::QueueingSystem(SystemParams params) :
  poisson_generator(params.lambda),
  uniform_generator(params.a, params.b),
  sources(params.sources_nmb, RequestSource(&poisson_generator)),
  handlers(params.handlers_nmb, Handler(&uniform_generator)),
  buffer(params.buffer_sz),
  modeling_end_time(params.modelligng_time)
{
  for (size_t i = 0; i < params.sources_nmb; ++i)
  {
    sources[i].setName(i);
  }
  for (size_t i = 0; i < params.handlers_nmb; ++i)
  {
    handlers[i].setNmb(i);
  }
}

void QueueingSystem::autoModeling()
{
  std::cout << "Auto modeling start.\n";
  double current_time = 0.;
  for (size_t i = 0; i < sources.size(); ++i)
  {
    Event new_event;
    new_event.type = Event_t::new_request;
    new_event.request = sources[i](current_time);
    new_event.event_time = new_event.request->creation_time;
    calendar.push(new_event);
  }

  while (!calendar.empty())
  {
    nextEvent();
  }

  //print_stats(std::cout);

}

void QueueingSystem::stepByStepModeling()
{
  std::cout << "Step by step modeling start.\n";
  double current_time = 0.;
  for (size_t i = 0; i < sources.size(); ++i)
  {
    Event new_event;
    new_event.type = Event_t::new_request;
    new_event.request = sources[i](current_time);
    new_event.event_time = new_event.request->creation_time;
    calendar.push(new_event);
  }

  while (!calendar.empty())
  {
    char c;
    print_state();
    nextEvent();
    std::cin >> c;
    if (c == 'x')
      return;
  }
}

void QueueingSystem::print_state()
{
  std::cout << "Event type: " << (calendar.top().type == Event_t::new_request ? "new request" : "freeing handler") << "\n";
  std::cout << "Current time: " << calendar.top().event_time << "\n";
  std::cout << "Buffer state:\n";
  const std::vector<Request*> buffer_data = buffer.getData();

  for (size_t i = 0; i < buffer_data.size(); ++i)
  {
    std::cout << i << ": ";
    if (buffer_data[i])
      std::cout << "Request " << buffer_data[i]->request_number << " from source" << buffer_data[i]->source->getSourceNmb()
                << "  " << buffer_data[i]->creation_time << "\n";
    else
      std::cout << " -\n";
  }
  std::cout << "Request Sources state:\n";
  for (size_t i = 0; i < sources.size(); ++i)
  {
    std::cout << i << ": ";
    std::cout << sources[i].getNext()->creation_time << "\n";
  }
  std::cout << "Processing Units state:\n";
  for (size_t i = 0; i < handlers.size(); ++i)
  {
    std::cout << i << ": ";
    if (handlers[i].isFree())
      std::cout << " -\n";
    else
      std::cout << handlers[i].getRequestInfo()->end_time << "\n";
  }

  std::cout << "\n\n" << std::endl;
}

void QueueingSystem::print_stats(std::ostream& out)
{
  std::vector<size_t>requests_count(sources.size(), 0);
  std::vector<size_t>rejects_count(sources.size(), 0);
  std::vector<double>total_time(sources.size(), 0);
  std::vector<double>processing_time(sources.size(), 0);

  for (size_t i = 0; i < finished_requests.size(); ++i)
  {
    ++requests_count[finished_requests[i]->source->getSourceNmb()];
    if (finished_requests[i]->status == Status_t::rejected)
    {
      ++rejects_count[finished_requests[i]->source->getSourceNmb()];
      continue;
    }
    total_time[finished_requests[i]->source->getSourceNmb()] += finished_requests[i]->end_time - finished_requests[i]->creation_time;
    processing_time[finished_requests[i]->source->getSourceNmb()] += finished_requests[i]->end_time - finished_requests[i]->start_time;
  }

  std::vector<double>processing_time_d(sources.size(), 0);
  std::vector<double>buffer_time_d(sources.size(), 0);

  for (const Request* req : finished_requests)
  {
    size_t j = req->source->getSourceNmb();
    if (req->status != Status_t::completed)
    {
      continue;
    }
    double mean_proc = processing_time[j] / (requests_count[j] - rejects_count[j]);
    double cur_proc = req->end_time - req->start_time;
    processing_time_d[j] += std::pow(cur_proc - mean_proc, 2);

    double mean_buff = (total_time[j] - processing_time[j]) / (requests_count[j] - rejects_count[j]);
    double cur_buff = req->start_time - req->creation_time;
    buffer_time_d[j] += std::pow(cur_buff - mean_buff, 2);
  }

  for (size_t i = 0; i < sources.size(); ++i)
  {
    out << "Source: " << i << "\n";
    out << "Total requests: " << requests_count[i] << "\n";
    out << "Probability of refusal: " << ((double)rejects_count[i]) / requests_count[i] << "\n";
    out << "Mean time in system: " << total_time[i] / (requests_count[i] - rejects_count[i]) << "\n";
    out << "Mean time in buffer: " << (total_time[i] - processing_time[i]) / (requests_count[i] - rejects_count[i]) << "\n";
    out << "Mean time of processing: " << processing_time[i] / (requests_count[i] - rejects_count[i]) << "\n";
    out << "Disp of time in buffer: " << buffer_time_d[i] / requests_count[i] << "\n";
    out << "Disp of processing time: " << processing_time_d[i] / (requests_count[i] - rejects_count[i]) << "\n";
    out << "\n";
  }

  //кол-во заявок от каждого источника
  //вероятсность отказа для каждого источника
  //среднее время прибывания заявки в системе
  //дисперсии времён в буфере и в приборе
  //коэффициенты использования приборов

  std::vector<double>start_time(handlers.size(), -1);
  std::vector<double>end_time(handlers.size());
  std::vector<double>total_time1(handlers.size());

  for (const Request* req : finished_requests)
  {
    if (req->status != Status_t::completed)
    {
      continue;
    }
    size_t i = req->handler->getHandlerNmb();
    if (start_time[i] == -1)
    {
      start_time[i] = req->start_time;
    }
    end_time[i] = req->end_time;
    total_time1[i] += req->end_time - req->start_time;
  }

  for (size_t i = 0; i < handlers.size(); ++i)
  {
    out << "Handler: " << i << "\n";
    out << "Utilization rate: " << total_time1[i] / (end_time[i] - start_time[i]) << "\n";
    out << "\n";
  }

}

std::ofstream& QueueingSystem::print_stats_json(std::ofstream& out)
{
  std::vector<size_t>requests_count(sources.size(), 0);
  std::vector<size_t>rejects_count(sources.size(), 0);
  std::vector<double>total_time(sources.size(), 0);
  std::vector<double>processing_time(sources.size(), 0);

  for (size_t i = 0; i < finished_requests.size(); ++i)
  {
    ++requests_count[finished_requests[i]->source->getSourceNmb()];
    if (finished_requests[i]->status == Status_t::rejected)
    {
      ++rejects_count[finished_requests[i]->source->getSourceNmb()];
      continue;
    }
    total_time[finished_requests[i]->source->getSourceNmb()] += finished_requests[i]->end_time - finished_requests[i]->creation_time;
    processing_time[finished_requests[i]->source->getSourceNmb()] += finished_requests[i]->end_time - finished_requests[i]->start_time;
  }

  std::vector<double>processing_time_d(sources.size(), 0);
  std::vector<double>buffer_time_d(sources.size(), 0);

  for (const Request* req : finished_requests)
  {
    size_t j = req->source->getSourceNmb();
    if (req->status != Status_t::completed)
    {
      continue;
    }
    double mean_proc = processing_time[j] / (requests_count[j] - rejects_count[j]);
    double cur_proc = req->end_time - req->start_time;
    processing_time_d[j] += std::pow(cur_proc - mean_proc, 2);

    double mean_buff = (total_time[j] - processing_time[j]) / (requests_count[j] - rejects_count[j]);
    double cur_buff = req->start_time - req->creation_time;
    buffer_time_d[j] += std::pow(cur_buff - mean_buff, 2);
  }

  out << std::fixed << std::setprecision(6);
  out << "{\n";
  out << "  \"sources\": [\n";
  for (size_t i = 0; i < sources.size(); ++i)
  {
    out << "    {\n";
    out << "      \"id\": " << i << ",\n";
    out << "      \"total_requests\": " << requests_count[i] << ",\n";
    out << "      \"probability_of_refusal\": " << ((double)rejects_count[i]) / requests_count[i] << ",\n";
    out << "      \"mean_time_in_system\": " << total_time[i] / (requests_count[i] - rejects_count[i]) << ",\n";
    out << "      \"mean_time_in_buffer\": " << (total_time[i] - processing_time[i]) / (requests_count[i] - rejects_count[i]) << ",\n";
    out << "      \"mean_time_of_processing\": " << processing_time[i] / (requests_count[i] - rejects_count[i]) << ",\n";
    out << "      \"dispersion_time_in_buffer\": " << buffer_time_d[i] / requests_count[i] << ",\n";
    out << "      \"dispersion_processing_time\": " << processing_time_d[i] / (requests_count[i] - rejects_count[i]) << "\n";
    out << "    }";
    if (i != sources.size() - 1)
      out << ",";
    out << "\n";
  }
  out << "  ],\n";

  //кол-во заявок от каждого источника
  //вероятсность отказа для каждого источника
  //среднее время прибывания заявки в системе
  //дисперсии времён в буфере и в приборе
  //коэффициенты использования приборов

  std::vector<double>start_time(handlers.size(), -1);
  std::vector<double>end_time(handlers.size());
  std::vector<double>total_time1(handlers.size());

  for (const Request* req : finished_requests)
  {
    if (req->status != Status_t::completed)
    {
      continue;
    }
    size_t i = req->handler->getHandlerNmb();
    if (start_time[i] == -1)
    {
      start_time[i] = req->start_time;
    }
    end_time[i] = req->end_time;
    total_time1[i] += req->end_time - req->start_time;
  }

  out << "  \"handlers\": [\n";
  for (size_t i = 0; i < handlers.size(); ++i)
  {
    out << "    {\n";
    out << "      \"id\": " << i << ",\n";
    out << "      \"utilization_rate\": " << total_time1[i] / (end_time[i] - start_time[i]) << "\n";
    out << "    }";
    if (i != handlers.size() - 1)
      out << ",";
    out << "\n";
  }
  out << "  ],\n";
  out << "  \"buffer_size\" : " << buffer.size() << "\n";
  out << "}";
  return out;
}

bool QueueingSystem::nextEvent()
{
  if (calendar.empty())
    return false;

  double current_time = calendar.top().event_time;

  if (calendar.top().type == Event_t::new_request)
  {
    RequestSource* current_source = calendar.top().request->source;

    Handler* free_handler = nullptr;
    for (size_t i = 0; i < handlers.size(); ++i)
    {
      if (handlers[i].isFree())
      {
        free_handler = &(handlers[i]);
        break;
      }
    }
    if (free_handler)
    {
      Event new_event = free_handler->setRequest(calendar.top().request, current_time);
      calendar.pop();
      calendar.push(new_event);
    }
    else
    {
      Request* rejected = buffer.insert(calendar.top().request);
      if (rejected)
      {
        finished_requests.push_back(rejected);
      }
      calendar.pop();
    }

    Event new_event;
    new_event.type = Event_t::new_request;
    new_event.request = (*current_source)(current_time);
    new_event.event_time = new_event.request->creation_time;
    if (modeling_end_time > new_event.event_time)
      calendar.push(new_event);
  }
  else
  {
    double current_time = calendar.top().event_time;
    finished_requests.push_back(calendar.top().request->handler->finishRequest());
    calendar.pop();

    Request* new_request = buffer.extract();
    if (new_request)
    {
      for (size_t i = 0; i < handlers.size(); ++i)
      {
        if (handlers[i].isFree())
        {
          handlers[i].setRequest(new_request, current_time);
          Event new_event;
          new_event.type = Event_t::freeing_handler;
          new_event.request = new_request;
          new_event.event_time = new_request->end_time;
          calendar.push(new_event);
        }
      }
    }
  }
  return true;
}

void QueueingSystem::printRequest(const Request* request)
{
  std::cout << "Request " << request->request_number << " from " << request->source->getSourceNmb()
    << " " << (request->status == Status_t::completed ? "completed" : "rejected") << "\n";
}
