#include <iostream>
#include <vector>
#include <sstream>

#include <netdb.h>
#include <netinet/in.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#define null NULL

size_t string__len(std::string s) { return s.length(); }

std::string string__repeat(std::string s, int n) {
  std::string out;
  for (int i = 0; i < n; i++)
    out += s;
  return out;
}

std::vector<std::string> string__split(std::string s, std::string delim) {
  std::vector<std::string> out;
  size_t pos = 0;
  std::string token;
  while ((pos = s.find(delim)) != std::string::npos) {
    token = s.substr(0, pos);
    out.push_back(token);
    s.erase(0, pos + delim.length());
  }
  out.push_back(s);
  return out;
}

std::string string__join(std::vector<std::string> v, std::string delim) {
  std::string out;
  for (int i = 0; i < v.size(); i++) {
    out += v[i];
    if (i + 1 != v.size())
      out += delim;
  }
  return out;
}

template <typename T> void fmt__write(T t) { std::cout << t; }
template <typename T> void fmt__write(std::vector<T> t) {
  std::cout << "[" << string__join(t, " ") << "]";
}

template <typename T> void fmt__print(T t) {
  fmt__write(t);
  std::cout << std::endl;
}

template <typename T> std::string fmt__tostring(T t) {
  std::stringstream s;
  s << t;
  return s.str();
}

int net__connect(std::string host, int port) {
  int s;
  if ((s = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    return -1;

  struct hostent *lh = gethostbyname(host.c_str());
  if (!lh)
    return -1;

  struct sockaddr_in sa;
  memset(&sa, 0, sizeof(sa));
  sa.sin_family = AF_INET;
  sa.sin_port = htons(port);
  memcpy(&sa.sin_addr.s_addr, lh->h_addr, lh->h_length);

  if (connect(s, (struct sockaddr *)&sa, sizeof(sa)) < 0)
    return -1;

  return s;
}

bool net__send(int s, std::string data) {
  return send(s, data.c_str(), data.length(), 0) != -1;
}

std::string net__receive(int s) {
  char buffer[65000];
  memset(buffer, 0, 65000);
  recv(s, buffer, 65000, 0);
  return buffer;
}