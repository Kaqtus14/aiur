#!/usr/bin/env python3
import argparse
import subprocess
import os

from ctx import Context
from lexer import Lexer
from parser import Parser
from codegen import CodeGenerator


def compile(ctx):
    lexer = Lexer(ctx)
    tokens = lexer.scan_tokens()

    parser = Parser(ctx, tokens)
    statements = parser.parse()

    interpreter = CodeGenerator(ctx)
    return interpreter.compile(statements)


def compile_file(args):
    include_path = os.path.join(os.path.dirname(__file__), "..", "stdlib")

    with open(args.path) as f:
        ctx = Context(args.path, f.read(), include_path)
    out = compile(ctx)

    with open(args.build_path, "w+") as f:
        f.write(out)

    if os.system(f"g++ -I {include_path} -o {args.out_path} {args.build_path}"):
        exit(1)

    if args.run:
        os.system(args.out_path if args.out_path.startswith(
            "/") else "./"+args.out_path)


def run_tests(args):
    aiur_path = os.path.join(os.path.dirname(__file__), "..")
    for file in os.listdir(aiur_path+"/examples"):
        proc = subprocess.Popen(f"{aiur_path}/aiur c -r {aiur_path}/examples/{file}",
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        proc.wait()
        if proc.returncode == 0:
            print(f"✅ {file} {b''.join(proc.communicate())[:100]}")
        else:
            print(b"\n".join(proc.communicate()).decode().strip())
            print(f"❌ {file}")
            exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog="aiur", usage="%(prog)s <mode>", description="Aiur compiler")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    compile_parser = subparsers.add_parser("compile", aliases=["c"])
    compile_parser.add_argument(
        "-r", dest="run", action="store_true", help="Run executable after compiling")
    compile_parser.add_argument(
        "-b", dest="build_path", default="/tmp/aiur_build.cpp", help="Specify the build path (default: /tmp/aiur_build.cpp)")
    compile_parser.add_argument(
        "-o", dest="out_path", default="output.exe", help="Specify the out path (default: output.exe)")
    compile_parser.add_argument("path")
    compile_parser.set_defaults(func=compile_file)

    test_parser = subparsers.add_parser("test")
    test_parser.set_defaults(func=run_tests)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
