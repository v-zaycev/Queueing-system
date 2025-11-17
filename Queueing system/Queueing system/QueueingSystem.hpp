#ifndef QUEUEINGSYSTEM_HPP
#define QUEUEINGSYSTEM_HPP
#include <queue>
#include "Generators.hpp"
#include "BasicStructures.hpp"
#include "Buffer.hpp"
#include "Handler.hpp"
#include "RequestSource.hpp"


enum struct SystemParamsSetters
{
  sources_nmb = 1,
  handlers_nmb = 2,
  buffer_sz = 3
};

struct SystemParams
{
  size_t sources_nmb;
  double lambda;
  size_t handlers_nmb;
  double a;
  double b;
  size_t buffer_sz;
  double modelligng_time;

  void set_param(SystemParamsSetters setter, size_t param)
  {
    switch (setter)
    {
    case SystemParamsSetters::sources_nmb:
      sources_nmb = param;
      break;
    case SystemParamsSetters::handlers_nmb:
      handlers_nmb = param;
      break;
    case SystemParamsSetters::buffer_sz:
      buffer_sz = param;
      break;

    }
  }
};

class QueueingSystem
{
public:
  QueueingSystem(SystemParams params);
  ~QueueingSystem()
  {
    for (auto i : finished_requests)
      delete i;
  }
  void autoModeling();
  void stepByStepModeling();
  void print_state();
  void print_stats(std::ostream& out);
  std::ofstream& print_stats_json(std::ofstream& out);
private:
  PoissonGenerator poisson_generator;
  UniformGenerator uniform_generator;
  Buffer buffer;
  std::vector<RequestSource> sources;
  std::vector<Handler> handlers;
  std::priority_queue<Event, std::vector<Event>, std::greater<Event>> calendar;
  std::vector<Request*> finished_requests;
  double modeling_end_time;

  bool nextEvent();
  void printRequest(const Request* request);
};


#endif

