#Git Repo Syncer

This is just a tool to have my git projects on my AWS servers stay up to date. Just add projects to this and then have a script which runs the sync command to pull in all the remote changes. 

Here is the help page:


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
1) Run 'git config --global credential.helper store' and then enter your creds. It will then be stored so that this script can use them
2) Use SSH keys
3) Provide the urls like https://username:password@github.com/path/to/repo.git

Examples:
gitreposyncer --new --dir /home/username/Ubuntu --url https://github.com/sindresorhus/awesome
gitreposyncer --list
gitreposyncer --sync

