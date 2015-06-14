"""
A simple job scheduler that uses the at utility, SSH, logging and a POSIX interface.

Written by Bud Peters
"""

import argparse
import cPickle as pickle
import logging
import os.path

from fabric.api import local, run, env

class ScheduleManager:
	def __init__(self):
		self.job_count = 0
		self.job_queue = {}

	def add_job(self, cmd, time, address=None, username=None, password=None):
		self.job_count += 1
		job = Job(self.job_count, cmd, time, address, username, password)
		self.job_queue[self.job_count] = job
		local('echo "sh run_job.sh ' + str(job.id_) + '" | sudo at ' + time)
		logging.info('Job ' + str(self.job_count) + ' successfully scheduled')

	def remove_job(self, job_id):
		local('at -r ' + job_id)
		del self.job_queue[job_id]
		logging.info('Job ' + str(job_id) + ' removed')

	def view_jobs(self):
		for job_id in self.job_queue:
			print self.job_queue[job_id]

class Job:
	'''Common base class for all jobs'''
	def __init__(self, id_, cmd, time, address, username, password_):
		self.id_ = id_
		self.cmd = cmd
		self.time = time
		self.address = address
		self.username = username
		self.password_ = password_

	def __str__(self):
		return '--- \nJobID: ' + str(self.id_) + '\n' 'Time: ' + str(self.time)

	def execute(self):
		if self.address is None:
			local(self.cmd)
		else:
			env.host = self.username + '@' + self.address
			env.password = self.password_
			run(self.cmd)

def main():

	logging.basicConfig(filename='job_history.log',
						format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
						datefmt='%m-%d %H:%M.%S', 
						level=logging.DEBUG)

	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--method', help='add, edit, remove, or view')
	parser.add_argument('-o', '--host', help='address and port for the remote system')
	parser.add_argument('-u', '--user', help='username for the remote system')
	parser.add_argument('-p', '--password', help='password for the remote system')
	parser.add_argument('-f', '--filepath', help='filepath to directory where the job is the be run')
	parser.add_argument('-t', '--time', help='time when the job is to be run (in crontab format)')
	parser.add_argument('-j', '--job_id', help='jobId of the job to be modified')
	parser.add_argument('-c', '--command', help='command indicating the job to be run')

	args = parser.parse_args()

	if os.path.isfile('sched.pk'):
		manager = pickle.load(open ('sched.pk', 'rb') )
	else:
		manager = ScheduleManager()

	if args.job_id and not args.method:
		logging.info('Beginning execution of scheduled job_id: %s', args.job_id)
		daemon_job = manager.job_queue[int(args.job_id)]
		daemon_job.execute()
		logging.info('Successfully completed execution of job_id: %s', args.job_id)
		if args.filepath:
			logging.info('Output files have been stored to the %s directory', args.filepath)
	else:
		if args.filepath:
			env.deploy_source = args.filepath
		if args.method == 'add':
			manager.add_job(args.command, args.time, args.host, args.user, args.password)
		elif args.method == 'remove':
			manager.remove_job()
		elif args.method == 'view':
			manager.view_jobs()

	with open('sched.pk', 'wb') as output:
		pickle.dump(manager, output, -1)


if __name__ == '__main__':
	main()