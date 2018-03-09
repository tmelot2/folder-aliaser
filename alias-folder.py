import sublime_plugin
import functools

class AliasFolderCommand(sublime_plugin.WindowCommand):
	def run(self, *args, **kwargs):
		# TODO: Error if more than one selected
		selectedPath = kwargs['paths'][0]

		panel = self.window.show_input_panel(
			"New folder alias:",
			"currentMenuItem",
			functools.partial(self.on_done, selectedPath=str(selectedPath)),
			None,
			None
		)

	def on_done(self, alias, selectedPath):
		# print("alias = {}, selectedPath = {}".format(alias, selectedPath))
		projectData = self.window.project_data()

		# foundIndex = -1
		# for index, folder in enumerate(projectData['folders']):
		# 	if folder['path'] == selectedPath:
		# 		foundIndex = index
		# 		break
		foundIndex = (index for index, folder in enumerate(projectData['folders']) if folder['path'] == selectedPath)

		if foundIndex >= 0:
			print("found at index {}".format(foundIndex))
		else:
			print("not found!!!!!")
