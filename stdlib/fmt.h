#pragma once
#include <iostream>
#include <sstream>
#include <vector>

#include "_string.h"

namespace fmt {
// export fmt::write
template <typename T> void write(T t) { std::cout << t; }
template <typename T> void write(std::vector<T> t) {
  std::cout << "[" << string::join(t, " ") << "]";
}

// export fmt::print
template <typename T> void print(T t) {
  fmt::write(t);
  std::cout << std::endl;
}

// export fmt::to_string
template <typename T> std::string to_string(T t) {
  std::stringstream s;
  s << t;
  return s.str();
}
}; // namespace fmt