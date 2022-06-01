#pragma once
#include <iostream>
#include <sstream>
#include <vector>

#include "_string.h"

namespace fmt {
// export fmt::to_string
template <typename T> std::string to_string(T t) {
  std::stringstream s;
  s << t;
  return s.str();
}
template <typename T> std::string to_string(std::vector<T> t) {
  std::vector<std::string> elems;
  for (auto elem : t)
    elems.push_back(fmt::to_string(elem));
  return "[" + string::join(elems, " ") + "]";
}

// export fmt::write
template <typename T> void write(T t) { std::cout << fmt::to_string(t); }

// export fmt::print
template <typename T> void print(T t) {
  fmt::write(t);
  fmt::write("\n");
}
}