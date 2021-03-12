# Customize this shared (eg, role) account user's startup files based on
# who is actually logged into it. Determine the user and source any file
# that you find for that user named ~/.profile.d/<username>.

if [ -f ~/.bashrc ] ; then
	source ~/.bashrc
fi

whoami=`who -m | awk '{ print $1 }'`

if [ -f ~/.profile.d/$whoami ] ; then
	source ~/.profile.d/$whoami
fi
