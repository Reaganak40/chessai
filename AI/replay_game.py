import os
import subprocess
from pathlib import Path

def replay_game():
    path_to_exe = Path(os.path.dirname(os.path.abspath(__file__))).absolute().parent.joinpath('Chess').joinpath('bin').joinpath('Debug').joinpath('net6.0').joinpath('Chess.exe')
    
    if not path_to_exe.exists():
        raise FileNotFoundError(path_to_exe)
    
    subprocess.call(str(path_to_exe))

if __name__ == '__main__':
    replay_game()