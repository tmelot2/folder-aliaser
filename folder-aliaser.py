import sublime_plugin
import sublime
import functools

class AliasFolderCommand(sublime_plugin.WindowCommand):

	def is_enabled(self, paths=[]):
		'''
			Called by Sublime when it needs to know if the Alias Folder menu option is active when right-clicking on an
			item in the Side Bar Folders. It should be active when a single, top-level folder is selected.
		'''
		# There should be only one selection and the selection must exist in the current project's folders.
		return len(paths) == 1 and self._project_has_folder(paths[0])


	def run(self, *args, **kwargs):
		'''
			Called by Sublime when this command is run. Gets the appropriate data and opens a Sublime text input panel
			where user enters an alias. A callback is passed to the input panel to handle submission.
		'''

		# Get the selected folder's path.
		selectedPath = kwargs['paths'][0]

		# Get current alias or folder name
		#
		folders = self._get_project_folders()
		selectedFolder = folders[self._get_project_folder_index(selectedPath)]
		if 'name' in selectedFolder:
			currentName = selectedFolder['name']
		else:
			currentName = selectedFolder['path'].split('/')[-1]

		# Show input panel where user types in alias name
		#
		panel = self.window.show_input_panel(
			"Alias this folder (enter nothing to clear an alias):",
			currentName,
			functools.partial(self.on_input_panel_submit, path=selectedPath),
			None,
			None
		)


	def on_input_panel_submit(self, alias, path):
		'''
			TODO
		'''

		index = self._get_project_folder_index(path)
		folders = self._get_project_folders()
		targetFolder = folders[index]

		# Clear alias if empty or the same as the last part of the path
		#
		if alias == '' or alias == path.split('/')[-1]:
			if 'name' in targetFolder:
				targetFolder.pop('name')
		else:
			targetFolder['name'] = alias

		# Save
		self._save_project_folders(folders)


	def _get_project_folders(self):
		'''
			Returns a list of the 'folders' array in the current project's sublime-project file.
		'''
		print(type(self.window.project_data().get('folders')))
		return self.window.project_data().get('folders')


	def _save_project_folders(self, folders):
		'''
			Saves the given list of folders into the 'folders' property in the current
			sublime-project.
		'''
		projectData = self.window.project_data()
		projectData['folders'] = folders
		self.window.set_project_data(projectData)


	def _project_has_folder(self, path):
		'''
			Returns true if the current project has the given path as a project folder.
		'''
		return self._get_project_folder_index(path) >= 0


	def _get_project_folder_index(self, path):
		'''
			Searches the current project's folders list for an item with the given path, returns the index if found,
			otherwise -1. Simple linear search.
		'''

		folders = self._get_project_folders()
		# Listcomp to get index of the folder with the given path.
		foundIndex = [index for index, folder in enumerate(folders) if folder['path'] == path]
		if len(foundIndex) > 0:
			return foundIndex[0]
		else:
			return -1
