# This script will setup stuff in order to
# use a remote server as a git server

repo=$(basename $(pwd))

echo "Server:"
read -e server
barerepospath="bare-repos"

echo "Setting up the remote repo"
# if $repo exist in remote then mkdir $repo will fail, and stop the following commands
ssh $server "cd bare-repos && mkdir $repo && cd $repo && git init --bare" >> /dev/null 2>&1

echo "Registering repo ${repo} on server ${server}"
git remote add origin $server:$barerepospath/$repo
git push --all origin

echo "If to be clone locally on the server:"
echo "   git clone file:///full/path/to/repo"
echo "   git pull --all"
