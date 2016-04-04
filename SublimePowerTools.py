import sublime_api, sublime, sublime_plugin, re
import functools

# internals
# TODO: add:
#			fold
#			unfold
#			toggle log result regex
#			toggle log input?
#			toggle hex/UTF8
class NewScratchViewCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.new_file().set_scratch(True)

class ToggleScratchCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.set_scratch(not self.view.is_scratch())

class ToggleReadOnlyCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.set_read_only(not self.view.is_read_only())

# TODO: somehow detect current logging status, rather than just assuming current is False.
class ToggleCommandLogCommand(sublime_plugin.ApplicationCommand):
	logging = False

	def run(self):
		self.logging = not self.logging
		sublime.log_commands(self.logging)
		print("setting logging to: ", self.logging)

# This is completely unnecessary because view already has a "revert" command.
# class RevertWrapperCommand(sublime_plugin.TextCommand):
# 	def run(self, edit):
# 		self.view.run_command("revert")

class ToggleEncodingHexUtf8Command(sublime_plugin.TextCommand):
	def run(self, edit):
		encoding = self.view.encoding()

		if encoding == "Hexadecimal":
			encoding = "utf-8"
		else:
			encoding = "Hexadecimal"

		if self.view.is_dirty():
			sublime.status_message("Cannot toggle encoding of dirty file.")
		else:
			sublime.set_timeout((lambda : self.view.run_command("reopen", {"encoding": encoding})), 0)
