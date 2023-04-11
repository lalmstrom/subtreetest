#!/usr/bin/python

import os
import argparse
import json
import subprocess as sp

def run(cmd):
    print(cmd)
    sp.run(cmd, check = True, shell = True)

class Subtree():

    def __init__(self, jsonpath):
        self.jsonpath = jsonpath
        if os.path.exists(jsonpath):
            with open(jsonpath, "r") as fd:
                self.trees = json.load(fd)
        else:
            self.trees = {}
            
    
    def list_raw(self):
        run("git log | grep git-subtree-dir | tr -d ' ' | cut -d ':' -f2 | sort | uniq")

    def list(self):
        for k in sorted(self.trees.keys()):
            print(f"{k}: {self.trees[k]['remote']} ({self.trees[k]['commit']})")

    def add(self, dest, remote, commit):
        self.trees[dest] = {"remote": remote, "commit": commit}
        run(f"git subtree -P {dest} add {remote} {commit} --squash")
        self.store_json()
        
    def store_json(self):
        with open(self.jsonpath, "w") as fd:
            json.dump(self.trees, fd)
        
def main():

    parser = argparse.ArgumentParser(
        description="Manage subtrees")
    parser.add_argument('command', choices=["add", "list", "list_raw", "update"])
    parser.add_argument('--subtree')
    parser.add_argument('--remote')
    parser.add_argument('--commit')
    parser.add_argument('--verbose', action="store_true")
    args = parser.parse_args()

    st = Subtree(".subtrees")
    if args.command == "list_raw":
        st.list_raw()
    elif args.command == "list":
        st.list()
    elif args.command == "add":
        st.add(args.subtree, args.remote, args.commit)

if __name__ == "__main__":
    main()
