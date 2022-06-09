#include <functional>

// export null
#define null 0

class ScopeGuard {
public:
  ScopeGuard(std::function<void()> callback)
      : m_callback(std::move(callback)) {}

  ~ScopeGuard() { m_callback(); }

private:
  std::function<void()> m_callback;
};
