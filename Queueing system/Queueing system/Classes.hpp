#ifndef CLASSES
#define CLASSES

#include<random>
#include<string>
#include<vector>
#include<cmath>
#include<queue>
#include<limits>

enum struct Status_t
{
  created = 0,
  rejected = -1,
  completed = 1
};

enum struct Event_t
{
  new_request = 1,
  freeing_handler = 2
};

struct RequestSource;
struct Handler;

struct Request
{
  double creation_time;
  double start_time;
  double end_time;
  RequestSource* source;
  unsigned int request_number;
  Handler* handler;
  Status_t status;
};

struct Event
{
  double event_time;
  Request* request;
  Event_t type;

  bool operator>(const Event& other) const {return event_time > other.event_time;}
};

class PoissonGenerator
{
public:
  PoissonGenerator(double lambda);
  double operator()();
private:
  double lambda_;
  std::mt19937 number_generator_;
  std::uniform_real_distribution<double> distr_;
};

class UniformGenerator
{
public:
  UniformGenerator(double a, double b);
  double operator()();
private:
  std::mt19937 number_generator_;
  std::uniform_real_distribution<double> distr_;
};

class Buffer
{
public:
  Buffer(size_t buff_capacity);
  ~Buffer();

  Request* extract();
  Request* insert(Request* request);
  const std::vector<Request*>& getData() { return buffer_data; }

private:
  std::vector<Request*> buffer_data;
  size_t size_;
};

class RequestSource
{
public:
  RequestSource(PoissonGenerator* generator);
  void setName(size_t source_nmb);
  const Request* getNext() const;
  size_t getSourceNmb() const {return source_nmb_;}
  Request* operator()(double current_time);
private:
  PoissonGenerator* generator_;
  Request* next;
  size_t counter_;
  size_t source_nmb_;
};

class Handler
{
public:
  Handler(UniformGenerator* generator);
  void setNmb(size_t handler_nmb);
  Event setRequest(Request* request, double current_time);
  size_t getHandlerNmb() const { return handler_nmb_; }
  const Request* getRequestInfo() const { return current_; }
  Request* finishRequest();
  bool isFree();
private:
  Request* current_;
  UniformGenerator* generator_;
  size_t handler_nmb_;
};

class QueueingSystem
{
public:
  QueueingSystem(size_t sources_nmb, double lambda, size_t handlers_nmb, double a, double b, size_t buffer_sz);
  void autoModeling();
  void stepByStepModeling();
  void print_state();
  void print_stats();
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
