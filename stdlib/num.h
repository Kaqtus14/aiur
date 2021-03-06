#pragma once
#include <cmath>
#include <iostream>
#include <vector>

namespace num {
// export num::sqrt
float sqrt(float n) { return std::sqrt(n); }

// export num::from_string
float from_string(std::string s) { return std::stof(s); }

// export num::rand
float random() {
  srand(time(0));
  return rand();
}

// export num::range
std::vector<int> range(int start, int end) {
  std::vector<int> out;
  for (int i = start; i < end; i++)
    out.push_back(i);
  return out;
}
std::vector<int> range(int end) { return range(0, end); }
}
