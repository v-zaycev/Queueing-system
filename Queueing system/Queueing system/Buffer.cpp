#include "Buffer.hpp"

Buffer::Buffer(size_t buff_capacity) :
  buffer_data(buff_capacity, nullptr),
  size_(0)
{
}
Buffer::~Buffer()
{
  for (size_t i = 0; i < buffer_data.size(); ++i)
  {
    delete buffer_data[i];
  }
}
Request* Buffer::extract()
{
  if (!size_)
  {
    return nullptr;
  }

  double newest_time = std::numeric_limits<double>::lowest();
  double newest_id = -1;
  Request* extracted = nullptr;

  for (size_t i = 0; i < buffer_data.size(); ++i)
  {
    if (buffer_data[i] && buffer_data[i]->creation_time > newest_time)
    {
      newest_time = buffer_data[i]->creation_time;
      newest_id = i;
    }
  }

  extracted = buffer_data[newest_id];
  buffer_data[newest_id] = nullptr;
  --size_;
  return extracted;
}
Request* Buffer::insert(Request* request)
{
  if (size_ == buffer_data.size())
  {
    double oldest_time = std::numeric_limits<double>::max();
    long long oldest_id = -1;
    Request* rejected = nullptr;
    for (size_t i = 0; i < buffer_data.size(); ++i)
    {
      if (buffer_data[i]->creation_time < oldest_time)
      {
        oldest_time = buffer_data[i]->creation_time;
        oldest_id = i;
      }
    }

    rejected = buffer_data[oldest_id];
    rejected->end_time = request->creation_time;
    rejected->status = Status_t::rejected;
    buffer_data[oldest_id] = request;

    return rejected;
  }

  for (size_t i = 0; i < buffer_data.size(); ++i)
  {
    if (buffer_data[i] == nullptr)
    {
      buffer_data[i] = request;
      break;
    }
  }
  ++size_;
  return nullptr;
}
