#ifndef BUFFER_HPP
#define BUFFER_HPP
#include "BasicStructures.hpp"
#include <vector>

class Buffer
{
public:
  Buffer(size_t buff_capacity);
  ~Buffer();

  Request* extract();
  Request* insert(Request* request);
  const std::vector<Request*>& getData() { return buffer_data; }
  size_t size() const noexcept { return buffer_data.size(); };
private:
  std::vector<Request*> buffer_data;
  size_t size_;
};

#endif
