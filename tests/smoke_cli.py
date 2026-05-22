import subprocess
import sys


def run(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=60,
    )

    print(f"\n$ {command}")
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main():
    run("python main.py --status")
    run("python main.py --queue-clear --yes")
    run("python main.py --queue-add 'Smoke parent task'")
    run("python main.py --queue-add 'Smoke child task' --depends-on task-1")
    run("python main.py --queue-list")
    run("python main.py --queue-validate")
    run("python main.py --queue-status")


if __name__ == '__main__':
    main()
