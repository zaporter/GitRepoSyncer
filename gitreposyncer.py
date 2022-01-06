#!/bin/python

import json
import os
import subprocess
import sys
import getopt

dir_path = os.path.dirname(os.path.realpath(__file__))
repos_file = dir_path+"/repos.json"

helpString = """
Welcome to the GitRepoSyncer. This tool is designed to make it easier to manage large numbers of git repos on multiple servers where you want to easily run git pull on each repo.

Main arguments:

-h, --help: Displays this message

-n, --new: Indicates that you wish to create a new synced repo (you must then use the -d and -u options)

-r, --remove: Indicates that you wish to remove a synced repo (you must then use one of the -d option to specify which repo you wish to remove)

-s, --sync: Indicates you wish to sync all of the repos (If -d or -u is passed then just that repo is updated)

-d, --dir [absolute path]: Specifies the local absolute path of the repo you're interested in

-u, --url [URL to git repo]: Specifies URL of git repo you want to sync from

-l, --list: Show all current synced repos

Authentication:
You have three main options for authentication. 
1) Run \'git config --global credential.helper store\' and then enter your creds. It will then be stored so that this script can use them
2) Use SSH keys
3) Provide the urls like https://username:password@github.com/path/to/repo.git

Examples:
gitreposyncer --new --dir /home/username/Ubuntu --url https://github.com/sindresorhus/awesome
gitreposyncer --list
gitreposyncer --sync


"""

def createReposIfNotPresent():
    if not os.path.exists(repos_file):
        saveRepos([])

def loadRepos():
    reposFile = open(repos_file,'r')
    reposString = reposFile.read()
    repos = json.loads(reposString)
    return repos

def addRepo(repos, path, url):
    repo = {
        "path":path,
        "url":url
    }
    repos.append(repo)
    return repos

def saveRepos(repos):
    reposFile = open(repos_file,'w')
    reposFile.write(json.dumps(repos))

def delRepo(repos, path):
    reposCopy = []
    for i in repos:
        if not (i["path"] == path):
            reposCopy.append(i)
    return reposCopy

def runLine(cmd):
    result = subprocess.run(cmd)
    return result.returncode==0

createReposIfNotPresent()
repos = loadRepos()


url = ""
path = ""
username = ""
password = ""
mode = "HELP"
argumentList = sys.argv[1:]
options = "nrsU:P:hd:u:l"
longOptions = ["new","remove","sync","username","password","help", "dir","url","list"]
try:
    arguments, values = getopt.getopt(argumentList,options,longOptions)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-n","--new" ):
            mode="NEW"
        elif currentArgument in ("-d","--dir" ):
            path=os.path.abspath(currentValue)
        elif currentArgument in ("-u","--url" ):
            url=currentValue
        elif currentArgument in ("-r","--remove"):
            mode="REMOVE"
        elif currentArgument in ("-s","--sync"):
            mode="SYNC"
        elif currentArgument in ("-l","--list"):
            mode="LIST"
        elif currentArgument in ("-h","--help"):
            mode="HELP"
except getopt.error as err:
    print(str(err))

success=True
if mode=="HELP":
    print(helpString)
elif mode=="NEW":
    if path and url:
        repos=addRepo(repos,path,url)
        if not runLine(['git','clone',url,path]):
            success=False
    else:
        print("You must specify both the directory and the url with the -d and -u options in order to use --new")
elif mode=="REMOVE":
    if path:
        repos=delRepo(repos,path)
    else:
        print("You must specify the directory -d option in order to use --remove")
elif mode=="SYNC":
    for entry in repos:
        if os.path.isdir(entry["path"]):
            shouldPull=False
            if url:
                if url==entry["url"]:
                    shouldPull=True
            elif path:
                if path==entry["path"]:
                    shouldPull=True
            else:
                shouldPull=True

            if shouldPull:
                if not runLine(['git','-C',entry['path'],'pull']):
                    success=False
        else:
            if not runLine(['git','clone',entry['url'],entry['path']]):
                success=False
elif mode=="LIST":
    for entry in repos:
        print(f"{entry['url']} -> {entry['path']}")
if success:
    saveRepos(repos);
else:
    print("Git Repo Syncer failed.")
