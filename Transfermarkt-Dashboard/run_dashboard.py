import streamlit as st
import subprocess

def main():
    cmd = ['streamlit', 'run', '⚽_Transfermarkt.py']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline().decode().strip()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output)

if __name__ == '__main__':
    main()
