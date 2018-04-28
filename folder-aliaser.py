import sublime_plugin
import functools

class ProjectFolders:
	'''
		A simple class used to interact with the current project's folders.
	'''

	def __init__(self, window):
		# Save a reference to the window, used to read / write project data.
		self._window = window
		# Save the current project's folders.
		self._folders = self._window.project_data().get("folders")

	def get_folders(self):
		'''
			Returns a copy of the list of folders.
		'''
		return list(self._folders)

	def has_folder(self, path):
		'''
			Returns true if project has folder with given path.
		'''
		return self.get_index(path) >= 0

	def get_index(self, path):
		'''
			Returns index of the project folder that has a path matching the given path. Returns -1 if not found.
		'''
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
		for folder in self._folders:
			if folder['path'] == path:
				# Return the alias, or if none given return the name of the folder itself
				return folder.get('name', folder['path'].split('/')[-1])
		return None

	def save(self, folders):
		'''
			Saves the given folders list to the current project 'folders' entry.
		'''
		self._window.set_project_data({**self._window.project_data(), 'folders': folders})

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

		# Get the display name (will be the alias or the folder name itself)
		pathDisplayName = ProjectFolders(self.window).get_display_name(selectedPath)

		# Show input panel where user types in the folder alias
		panel = self.window.show_input_panel(
			"Alias this folder (enter nothing to clear an alias):",
			pathDisplayName,
			functools.partial(self.on_input_panel_submit, path=selectedPath),
			None,
			None
		)


	def on_input_panel_submit(self, alias, path):
		'''
			Called by Sublime when user submits the alias input. Saves the alias into the project
			file. Clears alias if user entered nothing or the folder name.
		'''
		projectFolders = ProjectFolders(self.window)
		index = projectFolders.get_index(path)

		# If path is in project
		if index > -1:
			folders = projectFolders.get_folders()
			# Save reference so below code is cleaner
			targetFolder = folders[index]

			# Clear alias if empty or the same as the folder name (last part of the path)
			#
			if alias in ('', path.split('/')[-1]):
				if 'name' in targetFolder:
					targetFolder.pop('name')
			else:
				targetFolder['name'] = alias

			# Save
			projectFolders.save(folders)
