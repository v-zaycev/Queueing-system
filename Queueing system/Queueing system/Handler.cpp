#include "Handler.hpp"

Handler::Handler(UniformGenerator* generator) :
  generator_(generator),
  current_(nullptr),
  handler_nmb_(-1)
{
}
void Handler::setNmb(size_t handler_nmb)
{
  handler_nmb_ = handler_nmb;
}
Event Handler::setRequest(Request* request, double current_time)
{
  current_ = request;
  request->handler = this;
  request->start_time = current_time;
  request->end_time = current_time + (*generator_)();
  Event event;
  event.type = Event_t::freeing_handler;
  event.request = request;
  event.event_time = request->end_time;

  return event;
}
Request* Handler::finishRequest()
{
  current_->status = Status_t::completed;
  Request* return_value = current_;
  current_ = nullptr;
  return return_value;
}
bool Handler::isFree()
{
  return current_ == nullptr;
}
