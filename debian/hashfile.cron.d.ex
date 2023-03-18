#
# Regular cron jobs for the hashfile package
#
0 4	* * *	root	[ -x /usr/bin/hashfile_maintenance ] && /usr/bin/hashfile_maintenance
