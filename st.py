#!/usr/bin/python

import os
import argparse
import yaml
import subprocess as sp

def run(cmd):
    print(cmd)
    sp.run(cmd, check = True, shell = True)

class Subtree():

    def __init__(self, confpath):
        self.confpath = confpath
        if os.path.exists(confpath):
            with open(confpath, "r") as fd:
                self.trees = yaml.safe_load(fd)
        else:
            self.trees = {}
            
    
    def list(self):
        for k in sorted(self.trees.keys()):
            print(f"{k}: {self.trees[k]['remote']} ({self.trees[k]['commit']})")
        

    def add(self, dest):
        remote = self.trees[dest]["remote"]
        commit = self.trees[dest]["commit"]
        run(f"git subtree -P {dest} add {remote} {commit} --squash")
        
    def update(self, dest):
        remote = self.trees[dest]["remote"]
        commit = self.trees[dest]["commit"]
        run(f"git subtree -P {dest} pull {remote} {commit} --squash")

    def sync(self):
        for st in self.trees.keys():
            if os.path.exists(st):
                self.update(st)
            else:
                self.add(st)
        
def main():

    parser = argparse.ArgumentParser(
        description="Manage subtrees")
    parser.add_argument('command', choices=["list", "sync"])
    parser.add_argument('--verbose', action="store_true")
    args = parser.parse_args()

    st = Subtree(".subtrees")
    if args.command == "list":
        st.list()
    elif args.command == "sync":
        st.sync()

if __name__ == "__main__":
    main()
