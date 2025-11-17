#ifndef BASICSTRUCTURES_HPP
#define BASICSTRUCTURES_HPP

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

  bool operator>(const Event& other) const { return event_time > other.event_time; }
};

#endif
