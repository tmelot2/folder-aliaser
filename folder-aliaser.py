import sublime_plugin
import sublime
import functools

class AliasFolderCommand(sublime_plugin.WindowCommand):

	def is_enabled(self, paths=[]):
		'''
			Returns true if there is exactly one selected path and it matches one of the top-level folders in the
			current project.
		'''
		return len(paths) == 1 and self.get_project_folder_index(paths[0]) >=0


	def run(self, *args, **kwargs):
		'''
			Called by Sublime when this command is run. Validates that you've only selected one folder and then opens
			a text input panel used to enter an alias for the selected folder.
		'''

		if len(kwargs['paths']) > 1:
			self.window.status_message("Can't alias multiple folders at once, please select just one folder to alias.")
			return
		else:
			selectedPath = kwargs['paths'][0]

		# Get current alias or name
		projectData = self.window.project_data()
		projectFolder = projectData['folders'][self.get_project_folder_index(selectedPath)]
		if 'name' in projectFolder:
			currentName = projectFolder['name']
		else:
			currentName = projectFolder['path'].split('/')[-1]

		# aah lots of barking! afk ... oh, just packages, bou was IN THE AIR haha
		panel = self.window.show_input_panel(
			"Alias this folder (enter nothing to clear an alias):",
			currentName,
			functools.partial(self.on_done, path=str(selectedPath)),
			None,
			None
		)


	def on_done(self, alias, path):
		'''
			TODO
		'''

		index = self.get_project_folder_index(path)
		projectData = self.window.project_data()

		# Clear alias if empty or the same as the last part of the path
		if alias == '' or alias == path.split('/')[-1]:
			if 'name' in projectData['folders'][index]:
				projectData['folders'][index].pop('name')
		else:
			projectData['folders'][index]['name'] = alias

		self.window.set_project_data(projectData)


	def get_project_folder_index(self, path):
		'''
			Searches the current project's folders list for an item with the given path, returns the index if found,
			otherwise -1.
		'''

		folders = self.window.project_data().get('folders')
		# Listcomp to get index of the folder with the given path.
		foundIndex = [index for index, folder in enumerate(folders) if folder['path'] == path]
		if len(foundIndex) > 0:
			return foundIndex[0]
		else:
			return -1
