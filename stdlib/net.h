#pragma once
#include <iostream>

#include <netdb.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include "_string.h"

namespace net {
// export net::connect
int connect(std::string host, int port) {
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

// export net::send_str
bool send_str(int s, std::string data) {
  return send(s, data.c_str(), data.length(), 0) != -1;
}

// export net::receive
std::string receive(int s) {
  char buffer[65000];
  memset(buffer, 0, 65000);
  recv(s, buffer, 65000, 0);
  return buffer;
}

// export net::http_get
std::string http_get(std::string url) {
  if (string::contains(url, "://"))
    url = string::split(url, "://")[1];

  std::string path = "/";

  if (string::contains(url, "/")) {
    path = url.substr(url.find("/"));
    url = url.substr(0, url.find("/"));
  }
  std::string host = url;

  int sock = net::connect(host, 80);
  net::send_str(sock, "GET " + path + " HTTP/1.0\r\nHost: " + host + "\r\n\r\n");

  std::string out, chunk;
  do {
    chunk = net::receive(sock);
    out += chunk;
  } while (string::len(chunk) > 0);

  out.erase(0, out.find("\r\n\r\n")+4);

  return out;
}
}