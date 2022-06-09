#pragma once
#include <iostream>
#include <vector>

namespace string {
// export string::alphabet
std::string alphabet = "abcdefghijklmnopqrstuvwxyz";

// export string::len
size_t len(std::string s) { return s.length(); }

// export string::repeat
std::string repeat(std::string s, int n) {
  std::string out;
  for (int i = 0; i < n; i++)
    out += s;
  return out;
}

// export string::split
std::vector<std::string> split(std::string s, std::string delim) {
  std::vector<std::string> out;
  size_t pos;
  while ((pos = s.find(delim)) != std::string::npos) {
    out.push_back(s.substr(0, pos));
    s.erase(0, pos + delim.length());
  }
  out.push_back(s);
  return out;
}

// export string::join
std::string join(std::vector<std::string> v, std::string delim) {
  std::string out;
  for (int i = 0; i < v.size(); i++) {
    out += v[i];
    if (i + 1 != v.size())
      out += delim;
  }
  return out;
}
}