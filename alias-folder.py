import sublime_plugin
import functools

class AliasFolderCommand(sublime_plugin.WindowCommand):
	def run(self, *args, **kwargs):
		'''
			Called by Sublime when this command is run. Validates that you've only selected one folder and then opens
			a text input panel used to enter the folder alias.
		'''

		# TODO: Error if more than one selected
		selectedPath = kwargs['paths'][0]

		# aah lots of barking! afk ... oh, just packages, bou was IN THE AIR haha
		panel = self.window.show_input_panel(
			"New folder alias:",
			"currentMenuItem",
			functools.partial(self.on_done, selectedPath=str(selectedPath)),
			None,
			None
		)

	def on_done(self, alias, selectedPath):
		'''

		'''

		# print("alias = {}, selectedPath = {}".format(alias, selectedPath))
		projectData = self.window.project_data()

		# Genexp to get index of the folder from the current project file. next() to get the first value from the
		# genexp object.
		foundIndex = next((index for index, folder in enumerate(projectData['folders']) if folder['path'] == selectedPath))

		if foundIndex >= 0:
			print("found at index {}".format(foundIndex))
		else:
			print("not found!!!!!")
