#include <iostream>

#include <netdb.h>
#include <netinet/in.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#define null NULL

template <typename T> void print(T t) { std::cout << t << std::endl; }

template <typename T> void write(T t) { std::cout << t; }

size_t strlen(std::string s) { return s.length(); }

std::string repeat(std::string s, int n) {
  std::string out;
  for (int i = 0; i < n; i++)
    out += s;
  return out;
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