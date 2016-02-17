# -*- coding: utf-8 -*-

import logging

from modules import IModule

from libs.core.structs import CommonData
from libs.core.models import IntegerField, StringField, SelectField

from .proc_raw_dump import action_proc_raw_dump
from .cmd_actions import parser_proc_raw_dump

log = logging.getLogger()


# ----------------------------------------------------------------------
class ModuleModel(CommonData):
	target = StringField(required=True)
	export_results = StringField(default="")
	import_results = StringField(default=None)
	db = StringField(default=None, label="only for Redis: database to use")
	broker_type = SelectField(default="redis", choices=[
		("redis", "Redis server"),
		("zmq", "ZeroMQ"),
		("amqp", "RabbitMQ broker")
	])


# ----------------------------------------------------------------------
class RemoteProcessModule(IModule):
	"""
	Try to extract information from remote processes
	"""
	__model__ = ModuleModel
	__submodules__ = {
		'raw-dump': dict(
			help="dump raw remote information process",
			cmd_args=parser_proc_raw_dump,
			action=action_proc_raw_dump
		),
	}

	name = "proc"
	description = "try to discover and handle processes in remote MQ/Brokers"

	# ----------------------------------------------------------------------
	def run(self, config):
		# --------------------------------------------------------------------------
		# Ver dirty monkey patch to avoid kombu write into screen
		# --------------------------------------------------------------------------
		try:
			import sys
			sys.stderr = open("/dev/null")
		except IOError:
			pass

		super(RemoteProcessModule, self).run(config)