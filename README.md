
# cms-playground

## Installation
Instructions to install the project can be found in the INSTALL.md file

## Code flow / explanation of the version_history app

The code in this app is a proof of concept / prototype and is not and is never intended to be production level code. It has been used to further my knowledge.

### cms_toolbars.py
This file contains a toolbar with a history button. The button opens a model.

### views.py
The views contain two methods:

#### Method: view_versions
The view_versions method takes car of populating a template (history_list) in a model which lists all of the versions available for the current page.
There is currently an issue where the list is only available for the page when in edit mode. This can be rectified and is a minor caveat.

#### Method: rewind
Rewind is currently not implemented due to a shortage of time and is still a WIP. The plan was to deserialize the version and update all of the draft Page, Title, Placeholders and Plugins.
The function would need to take care of removing / adding any plugins that exist in the current version but not in the version that is being changed to. A combination of removing / updating is one option although it may be more stable to remove all and rebuild which is how a page is published.
It would be good to tie the code into using the same method of creation as the page publish works. This should be the most stable method but could mean a major refactor of page publish to accommodate.

### signals.py
Contains a listener to the publish signal. This file is responsible for creating a version entry when a page is successfully published.

### external_utils.py
This file contains snippets and methods from Django CMS and Django CMS History due to the difficulty serializing plugins and accessing the plugin pool.