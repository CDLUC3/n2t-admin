if [ -f ~/.bashrc ] ; then
	source ~/.bashrc
fi

# Customize this possibly shared (eg, role) account startup files based on who
# is actually logged into it. Determine the user's <username> and source any
# file you find called ~/.profile.d/<username>.

whoami=`who -m | awk '{ print $1 }'`

if [ -f ~/.profile.d/$whoami ] ; then
	source ~/.profile.d/$whoami
fi
