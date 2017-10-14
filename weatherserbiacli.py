# -*- coding: utf-8 -*-
#==============================================================================
# WeatherSerbiaCLI - display current weather conditions for Serbia
#
#  Copyright (C) 2010,2017 Ljubomir Kurij <kurijlj@gmail.com>
#
# This file is part of WeatherSerbiaCLI.
#
# WeatherSerbiaCLI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WeatherSerbiaCLI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WeatherSerbiaCLI.  If not, see <http://www.gnu.org/licenses/>.
#
#==============================================================================

#==============================================================================
#
# WeatherSerbiaCLI is a CLI application designed to display current weather
# conditions for all major cities in Serbia. Application uses data published by
# Republic Hydrometeorological Service of Serbia on page
# http://www.hidmet.gov.rs/eng/osmotreni/index.rss.
#
# 2017-09-30 Ljubomir Kurij <kurijlj@gmail.com>
#
# * weatherserbiacli.py: created.
#
# 2010-11-08 Ljubomir Kurij <kurijlj@gmail.com>
#
# * svreme.py: created.
#
#==============================================================================


import argparse


#==============================================================================
# Utility classes and functions
#==============================================================================

class ProgramAction(object):
	"""Abstract base class for all program actions, that provides execute.

	The execute method contains code that will actually be executed after
	arguments parsing is finished. The method is called from within method
	run of the CommandLineApp instance.
	"""

	def __init__(self, exitf):
		self._exit_app = exitf

	def execute(self):
		pass


def _format_epilog(epilogAddition, bugMail):
	"""Formatter for generating help epilogue text. Help epilogue text is an
	additional description of the program that is displayed after the
	description of the arguments. Usually it consists only of line informing
	to which email address to report bugs to, or it can be completely
	omitted.

	Depending on provided parameters function will properly format epilogue
	text and return string containing formatted text. If none of the
	parameters are supplied the function will return None which is default
	value for epilog parameter when constructing parser object.
	"""

	fmtAdition = None
	fmtMail = None
	fmtEpilog = None

	if None == epilogAddition and None == bugMail:
		return None

	if None != bugMail:
		fmtMail = 'Report bugs to <{bugMail}>.'\
			.format(bugMail = bugMail)
	else:
		fmtMail = None

	if None == epilogAddition:
		fmtEpilog = fmtMail

	elif None == fmtMail:
		fmtEpilog = epilogAddition

	else:
		fmtEpilog = '{addition}\n\n{mail}'\
			.format(addition = epilogAddition, mail = fmtMail)

	return fmtEpilog


def _formulate_action(Action, **kwargs):
	"""Factory method to create and return proper action object.
	"""

	return Action(**kwargs)


#==============================================================================
# Command line app class
#==============================================================================

class CommandLineApp(object):
	"""Actual command line app object containing all relevant application
	information (NAME, VERSION, DESCRIPTION, ...) and which instantiates
	action that will be executed depending on the user input from
	command line.
	"""

	def __init__(self,
		programName=None,
		programDescription=None,
		programLicense=None,
		versionString=None,
		yearString=None,
		authorName=None,
		authorMail=None,
		epilog=None):

		self.programLicense = programLicense
		self.versionString = versionString
		self.yearString = yearString
		self.authorName = authorName
		self.authorMail = authorMail

		fmtEpilog = _format_epilog(epilog, authorMail)

		self._parser = argparse.ArgumentParser(
			prog = programName,
			description = programDescription,
			epilog = fmtEpilog,
			formatter_class=argparse.RawDescriptionHelpFormatter
			)

		# Since we add argument options to groups by calling group
		# method add_argument, we have to sore all that group objects
		# somewhere before adding arguments. Since we want to store all
		# application relevant data in our application object we use
		# this list for that purpose.
		self._argumentGroups = []


	@property
	def programName(self):
		"""Utility function that makes accessing program name attribute
		neat and hides implementation details.
		"""
		return self._parser.prog


	@property
	def programDescription(self):
		"""Utility function that makes accessing program description
		attribute neat and hides implementation details.
		"""
		return self._parser.description


	def add_argument_group(self, title=None, description=None):
		"""Adds an argument group to application object.
		At least group title must be provided or method will rise
		NameError exception. This is to prevent creation of titleless
		and descriptionless argument groups. Although this is allowed bu
		argparse module I don't see any use of a such utility."""

		if None == title:
			raise NameError('Missing arguments group title.')

		group = self._parser.add_argument_group(title, description)
		self._argumentGroups.append(group)

		return group


	def _group_by_title(self, title):
		group = None

		for item in self._argumentGroups:
			if title == item.title:
				group = item
				break

		return group


	def add_argument(self, *args, **kwargs):
		"""Wrapper for add_argument methods of argparse module. If
		parameter group is supplied with valid group name, argument will
		be added to that group. If group parameter is omitted argument
		will be added to parser object. In a case of invalid group name
		it rises ValueError exception.
		"""

		if 'group' not in kwargs or None == kwargs['group']:
			self._parser.add_argument(*args, **kwargs)

		else:
			group = self._group_by_title(kwargs['group'])

			if None == group:
				raise ValueError(
				'Trying to reference nonexisten argument group.'
				)

			else:
				kwargsr = {k:kwargs[k] for k in list(kwargs.keys()) \
					if 'group' != k}
				group.add_argument( *args, **kwargsr)


	def parse_args(self, args=None, namespace=None):
		"""Wrapper for parse_args method of a parser object. It also
		instantiates action object that will be executed based on a
		input from command line.
		"""

		arguments = self._parser.parse_args(args, namespace)

		if arguments.usage:
			self._action = _formulate_action(
				ProgramUsageAction,
				parser=self._parser,
				exitf=self._parser.exit)

		elif arguments.version:
			self._action = _formulate_action(
				ShowVersionAction,
				prog=self._parser.prog,
				ver=self.versionString,
				year=self.yearString,
				author=self.authorName,
				license=self.programLicense,
				exitf=self._parser.exit)

		elif arguments.list_stations:
			self._action = _formulate_action(
				FetchData,
				prog=self._parser.prog,
				station='all',
				exitf=self._parser.exit)

		elif arguments.station:
			self._action = _formulate_action(
				FetchData,
				prog=self._parser.prog,
				station=arguments.station[0],
				exitf=self._parser.exit)

		else:
			self._action = _formulate_action(
				ProgramUsageAction,
				parser=self._parser,
				exitf=self._parser.exit)


	def run(self):
		"""This method executes action code.
		"""

		self._action.execute()


#==============================================================================
# App action classes
#==============================================================================

class ProgramUsageAction(ProgramAction):
	"""Program action that formats and displays usage message to the stdout.
	"""
	
	def __init__(self, parser, exitf):
		self._usageMessage = \
		'{usage}Try \'{prog} --help\' for more information.'\
		.format(usage=parser.format_usage(), prog=parser.prog)
		self._exit_app = exitf
	
	def execute(self):
		print(self._usageMessage)
		self._exit_app()
	
	
class ShowVersionAction(ProgramAction):
	"""Program action that formats and displays program version information
	to the stdout.
	"""
	
	def __init__(self, prog, ver, year, author, license, exitf):
		self._versionMessage = \
		'{0} {1} Copyright (C) {2} {3}\n{4}'\
		.format(prog, ver, year, author, license)
		self._exit_app = exitf
	
	def execute(self):
		print(self._versionMessage)
		self._exit_app()
	
	
class FetchData(ProgramAction):
	"""Program action to fetch data from RSS feed and display it to stdout.
	"""
	
	def __init__(self, prog, station, exitf):
		self._programName = prog
		self._station = station
		self._exit_app = exitf

	def execute(self):
		
		# We need to import library file.
		import weatherserbiafeed as wsf
		
		# Now we can create feed object.
		feed = wsf.WeatherSerbiaFeed()
		
		# Try to fetch data from server.
		feed.parse()
		
		# Check status.
		if 0 != feed.status:
			print('{0}: Error {1}\n'.format(self._programName, feed.status))
			self._exit_app()

		# Everything is fine.
		else:
			
			# Print list of stations if needed.
			if 'all' == self._station:
				for station in sorted(feed.stations()):
					print (station)
				print ('\n')
	
			# Print weather data.
			else:
				data = feed.observed_data_by_station(self._station)

				if None == data:
					print ('{0}: Station \"{1}\" not available.'\
					.format(self._programName, self._station))
					print ('Weather stations available for:')
					for station in sorted(feed.stations()):
						print (station)
	
				else:
					data.display_data()
	
				print ('\n')
	
		self._exit_app()


#==============================================================================
# Script main body
#==============================================================================

if __name__ == '__main__':
	program = CommandLineApp(
		programDescription='WeatherSerbia is a CLI application designed to \
			display current weather\n\
			conditions for all major cities in Serbia. Application uses data \
			published by\n\
			Republic Hydrometeorological Service of Serbia on page\n\
			http://www.hidmet.gov.rs/eng/osmotreni/index.rss.'\
			.replace('\t',''),
		programLicense='License GPLv3+: GNU GPL version 3 or later \
			<http://gnu.org/licenses/gpl.html>\n\
			This is free software: you are free to change and \
			redistribute it.\n\
			There is NO WARRANTY, to the extent permitted by law.'\
			.replace('\t',''),
		versionString='2.1',
		yearString='2017',
		authorName='Ljubomir Kurij',
		authorMail='kurijlj@gmail.com',
		epilog=None)

	program.add_argument_group('general options')
	program.add_argument(
		'-V', '--version',
		action='store_true',
		help='print program version',
		group='general options')
	program.add_argument(
		'--list-stations',
		action='store_true',
		help='list weather stations',
		group='general options')
	program.add_argument(
		'-S', '--station',
		action='store',
		nargs=1,
		default=None,
		type=str,
		required=False,
		help='show weather conditions for STATION',
		metavar='STATION',
		group='general options')
	program.add_argument(
			'--usage',
			action='store_true',
			help='give a short usage message')

	program.parse_args()
	program.run()
