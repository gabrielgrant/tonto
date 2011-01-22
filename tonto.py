"""Tonto - A poor Apache imitation

Tonto is a single-file, configuration-free testing webserver that imitates (at a very basic level) the behaviour of Apache+mod_php: when run, it serves files below the current working directory, and executes any php scripts it encounters using php-cgi.

Like Apache, it will return an index file when directories are requested, and show a basic index listing if there is no index file present.


This file also contains a patched version of Python's CGIHTTPServer.py because the original implementation is very un-modular, and therefore essentially impossible to override.

"""


import os.path
from subprocess import Popen, PIPE, STDOUT
import CGIHTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler, test

if not CGIHTTPServer.__version__.endswith('tonto'):
	raise RuntimeError('Tonto say him require patch version of CGIHTTPServer')

class PHPHandler(CGIHTTPRequestHandler):
	interpreter = 'php-cgi'
	
	def is_cgi(self):
		if os.path.splitext(self.path)[-1].startswith('.php'):
			self.cgi_info = os.path.split(self.path)
			return True
		else:
			return False
			
	def is_python(self):
		"""Sure, we're python...whatever you say :)"""
		return True
	
	def build_cgi_env(self, scriptname, *args, **kwargs):
		"""
		Adds SCRIPT_FILENAME to the env created by CGIHTTPRequestHandler
		
		CGIHTTPServer doesn't set the 'SCRIPT_FILENAME' environment
		variable, which causes php-cgi (on Ubuntu, at least) to fail
		with "No input file specified."
		
		Details:
		http://community.activestate.com/faq/cgi-debugging-no-input-fi
		"""
		env = CGIHTTPRequestHandler.build_cgi_env(self, scriptname, *args, **kwargs)
		env['SCRIPT_FILENAME'] = self.translate_path(scriptname)
		return env
	
	def parse_request_path(self):
		scriptname, scriptfile, script, rest, query = CGIHTTPRequestHandler.parse_request_path(self)
		php = Popen(["which", "php-cgi"], stdout=PIPE).communicate()[0].strip()
		return scriptname, php, scriptfile, rest, query
		
	def path_sanity_checks(self, *args, **kwargs):
		pass

	def output_script(self, php, scriptfile, query):
		"""Execute a PHP script."""
		CGIHTTPRequestHandler.output_script(self, php, 'php-cgi', scriptfile)

if __name__ == '__main__':
	test(HandlerClass=PHPHandler)
