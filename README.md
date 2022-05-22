# aiur

My programming language

## Features
- [x] Compiles to C++
- [x] No dependencies
- [x] Cross-platform

## Syntax
```cpp
func fib(n) {
    if n <= 1
        return n

    return fib(n-2) + fib(n-1)
}

func main() {
    for i in range(20) {
        $ fmt::print(fib(i))
    }
}
```

## Credits
* [Crafting Interpreters](http://www.craftinginterpreters.com/)