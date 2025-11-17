#include "RequestSource.hpp"

RequestSource::RequestSource(PoissonGenerator* generator) :
  generator_(generator),
  counter_(0),
  source_nmb_(-1),
  next(nullptr)
{
}
void RequestSource::setName(size_t source_nmb)
{
  source_nmb_ = source_nmb;
}
const Request* RequestSource::getNext() const
{
  return next;
}
Request* RequestSource::operator()(double current_time)
{
  next = new Request();
  next->source = this;
  next->request_number = counter_++;
  next->creation_time = current_time + (*generator_)();
  next->start_time = -1.;
  next->end_time = -1.;
  next->handler = nullptr;
  next->status = Status_t::created;

  return next;
}
