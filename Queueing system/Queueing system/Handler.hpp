#ifndef HANDLER_HPP
#define HANDLER_HPP
#include "BasicStructures.hpp"
#include "Generators.hpp"

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
#endif
