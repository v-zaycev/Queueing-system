#ifndef REQUESTSOURCE_HPP
#define REQUESTSOURCE_HPP
#include "BasicStructures.hpp"
#include "Generators.hpp"

class RequestSource
{
public:
  RequestSource(PoissonGenerator* generator);
  void setName(size_t source_nmb);
  const Request* getNext() const;
  size_t getSourceNmb() const { return source_nmb_; }
  Request* operator()(double current_time);
private:
  PoissonGenerator* generator_;
  Request* next;
  size_t counter_;
  size_t source_nmb_;
};

#endif // !REQUESTSOURCE_HPP

