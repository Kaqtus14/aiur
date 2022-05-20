#include <iostream>
#define null NULL

template <typename T> void print(T t) { std::cout << t << std::endl; }

template <typename T> void write(T t) { std::cout << t; }

std::string repeat(std::string s, int n) {
  std::string out;
  for (int i = 0; i < n; i++)
    out += s;
  return out;
}