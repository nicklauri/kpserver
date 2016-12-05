
import os;
import platform;

class KPS:
    version = '1.4';
    class framework:
        name = "KPF";
        fullname = "KProj Python Framework";
        version = '1.0';
        description = ""
    class python:
        version = platform.python_version();
        compiler = platform.python_compiler();
        implementation = platform.python_implementation();
    if os.name == "nt":
        class system:
            name = "Windows"
            cmd_version = platform.win32_ver()[1]
            win_version = platform.win32_ver()[0]
    elif os.name == "linux":
        class system:
            name = "Linux";
            win_version = "Not supported"
    else:
        class system:
            name = "Other OS";
            cmd_version = "not-supported";
            win_version = "not-supported";
