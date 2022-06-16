from dataclasses import dataclass


@dataclass
class Context:
    file: str
    src: str
    include_path: str


def error(msg, ctx, pos=None):
    pos_str = ctx.file

    if pos is not None:
        pos_str += f":{pos[0]}:{pos[1]}"

        line = ctx.src.split("\n")[pos[0]-1]
        print("\033[31m"+pos_str+":\033[0m "+line)

        pad_length = len(pos_str) + 2 + pos[1]
        print(" "*pad_length + "^--- " + msg)
    else:
        print("\033[31m"+pos_str+":\033[0m "+msg)

    exit(1)
