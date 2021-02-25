from hotimport import importer

"""
Create importer class
=====================
The importer class contains the methods for loading functions
You can check its following attributes:
importer.cogs : returns the currently loaded cogs
importer.fags : returns flags, WIP
"""
imp = importer()

"""
Load cogs
=========
The function to load the cogs works in the following way:
load_cogs(self, path)
The path variable must be the path to the config containing settings for
the importer. It must be in the following formart:
{
	"name":"Cogs",
	"version":"0.0.1",
	"locations":["cogs/test.json"],
	"status":"rolling"
}
"""
imp.load_cogs("cogs.json")

"""
Check cog info
==============
This function allows you to get cog information during the execution.
The function requires the cog name, for now there are no limitations to what 
a cog name can be. Example output:

=== Test Cog ===
version: 1
function: test
variables: x
depends: testlib
"""
imp.read_cog("Test Cog")

"""
Run cog
=======
The function 'execute' allows running the command. The inner workings are
quite intricate while also quite simple. A library called 'importlib' is 
used to import the file/library that the user wants, and the function works
in the following manner:

self.return_code = 2
dep = importlib.import_module(cog[4])
method = getattr(dep, cog[2])
return_code = method(var)
self.return_code = return_code  

The return code does not correlate with the functions output code and is only 
used for checking the states of the importer.
The dep is the module from which the function is then executed, the function is 
aquired by using getattr. 
"""
print("\nCog with a variable in action:")
imp.execute("Test Cog",var='a')

"""
Hot loading a cog
=================
This function is similar to 'load_cogs' except it does not use a configuration
file and loads the cog straight from the path provided. 

The function works in the following way:
cogTemp = ezconfig()
cogTemp.read(path)
cog = [cogTemp.get("name"),cogTemp.get("version"),cogTemp.get("function")cogTemp.get("variables"),cogTemp.get("depends")]
self.cogs.append(cog)

You might have noticed that 'ezconfig' is a class used through out the library,
it is another library that is used to read json, all in all its a prettified 
and simplified wrapper of the normal python json library with better errors
and sugestions.

Once ezconfig reads the configuration file for a cog, the cog is appended to the
'importer.cogs' list. Using a list is not great and will be later replaced with
a dictionary so that you can unload cogs faster.
"""
imp.hot_cog("hotcog.json")

"""
Running the hot cog
=================
Running the hot cog can be done the same way as a normal cog, if you want to
completely reset the cog once its done executing you can use the 'hot' flag.
this can be done in the following manner:

importer.execute("Hot Cog",hot=True)
"""
print("\nHot cog in action:")
imp.execute("Hot Cog")