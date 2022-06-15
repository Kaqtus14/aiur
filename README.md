# aiur

My programming language

## Features
- Compiles to C++
- Rust-like syntax
- No semicolons
- No dependencies
- Cross-platform

## Syntax
```go
func fib(n) {
    if n <= 1
        return n

    return fib(n-2) + fib(n-1)
}

func main() {
    defer {
        fmt::print("Finished!")
    }

    for i in num::range(20) {
        fmt::print(fib(i))
    }
}
```

## Credits
* [Crafting Interpreters](http://www.craftinginterpreters.com/)
