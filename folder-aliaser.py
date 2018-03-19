import sublime_plugin
import sublime
import functools

# ___  __      __   __
#  |  /  \    |  \ /  \ .
#  |  \__/    |__/ \__/ .
#
#	[ ] Persist ProjectFolders instance in AliasFolderCommand
#	[ ] Not great that __getitem__() constantly reloads
#	[ ] Project Folders expand collapse state clears after an edit
#	[ ] Remove reload(), don't need it, make comment that object inits before each thing is run, so
#		it's ok if it looks like it could be in a bad state.

class ProjectFolders:

	def __init__(self, window):
		'''
			TODO
		'''
		# Save a reference to the window, used for refreshing the project folders.
		self._window = window
		#self._reload()
		self._folders = self._window.project_data().get("folders")

	def __getitem__(self, index):
		'''
			Returns project folder at given index.
		'''
		#self._reload()
		return self._folders[index]

	def __setitem__(self, index, value):
		self._folders[index] = value

	#def _reload(self):
		'''
			Reloads the current project file and thus loads any updated folders.

			TODO: _reload() the right format?
		'''
		#self._folders = self._window.project_data().get("folders")

	def get_folders(self):
		'''
			Returns a copy of the list of folders.
		'''
		return list(self._folders)

	def has_folder(self, path):
		return self.get_index(path) >= 0

	def get_index(self, path):
		'''
			Returns index of the project folder that has a path matching the given path. Returns -1 if not found.
		'''
		#self._reload()
		for index, folder in enumerate(self._folders):
			if folder['path'] == path:
				return index

		# Not found
		return -1

	def get_display_name(self, path):
		'''
			Returns the display name for the project folder whose path matches the given path. Display name is
			determined in this order:

				1) Folder alias - If the folder has the 'name' property, that's an alias so use that.
				2) Folder name - If no alias, use the folder name i.e. the last part of the path i.e. the 'c' in
				   '/a/b/c/'
				3) No match - No folders in the project match the given path, return None
		'''
		#self._reload()
		for folder in self._folders:
			if folder['path'] == path:
				if 'name' in folder:
					return folder['name']
				else:
					# Return the last part of the path
					return folder['path'].split('/')[-1]

		return None

	def save(self, folders):
		'''
			Saves the given folders list to the current project 'folders' entry.
		'''
		projectData = self._window.project_data()
		projectData['folders'] = folders
		self._window.set_project_data(projectData)

		# Update the local version
		self._folders = folders


class AliasFolderCommand(sublime_plugin.WindowCommand):

	def is_enabled(self, paths=[]):
		'''
			Called by Sublime when it needs to know if the Alias Folder menu option is active when right-clicking on a
			Side Bar Folder. It should be active when a single, top-level folder is selected.
		'''
		projectFolders = ProjectFolders(self.window)
		# There should be only one selection and the selection must exist in the current project's folders.
		return len(paths) == 1 and projectFolders.has_folder(paths[0])


	def run(self, *args, **kwargs):
		'''
			Called by Sublime when this command is run. Gets the appropriate data and opens a Sublime text input panel
			where user enters an alias. A callback is passed to the input panel to handle submission.
		'''
		# Get the selected folder's path.
		selectedPath = kwargs['paths'][0]

		# Get current alias or folder name
		pathDisplayName = ProjectFolders(self.window).get_display_name(selectedPath)

		# Show input panel where user types in alias name
		#
		panel = self.window.show_input_panel(
			"Alias this folder (enter nothing to clear an alias):",
			pathDisplayName,
			functools.partial(self.on_input_panel_submit, path=selectedPath),
			None,
			None
		)


	def on_input_panel_submit(self, alias, path):
		'''
			TODO
		'''
		# Get project folders and index of the folder with given path

		projectFolders = ProjectFolders(self.window)
		index = projectFolders.get_index(path)

		# Get a copy of the project folders list to operate on
		folders = projectFolders.get_folders()

		# Save reference so code is cleaner
		targetFolder = folders[index]

		# Clear alias if empty or the same as the last part of the path
		#
		if alias == '' or alias == path.split('/')[-1]:
			if 'name' in targetFolder:
				targetFolder.pop('name')
		else:
			targetFolder['name'] = alias

		# Save
		projectFolders.save(folders)
