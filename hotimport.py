
# EZCONF
import os
import json
import re

try:
  import merrors
  merrors=merrors.merror()
  mer = True
except:
  print("For better error checking and functionability please install merrors")
  mer = False

class ezconfig:

  def __init__(self):
    self.filename = ""
    self.datajson = None

  def read(self,filename):
    """
    Reads the config file and saves the values
    :return: 
    """
    with open(str(filename),"r") as f:
      data = f.read()
      #check if the loaded file is json
      try:
        datajson = json.loads(data)
      except Exception as e:
        if mer == True:
          merrors.error('could not load '+str(filename)+', add a basic entry to the config like {"name":"Example"}. Python error: '+str(e))
          quit()
        else:
          print("could not load "+str(filename)+". Python error: "+str(e))
          quit()
      self.datajson = datajson
      self.filename = filename
      f.close()

  def get(self,var,*args):
    """
    Return a variable
    :param var: variable to get
    :return var_val:
    """
    #update datajson
    self.read(self.filename)
    try:
      var_val = self.datajson[str(var)]
      if bool(args)!=False:
        p = re.compile('(?<!\\\\)\'')
        var_val = p.sub('\"', str(var_val))
        return json.loads(str(var_val))[str(args[0])]
    except Exception as e:
      if mer == True:
        merrors.error("[1] could not get variable ["+str(var)+"] does it exist in config.json?\nPython error: "+str(e))
        quit()
      else:
        print(e)
    if var_val == None:
      merrors.error("[2] could not get variable ["+str(var)+"]. It equals to None, is there a python problem?")
      quit()
    else:
      return var_val
  
  def update(self,var,*args):
    """
    Update a variable
    :param var: variable to update
    """
    #update datajson
    self.read(self.filename)
    try:
      self.datajson[str(var)] = str(args[0])
    except Exception as e:
      merrors.error("could not update variable, does it exist? Did you parse a new value? Python error: "+str(e))
    jsonFile = open(str(self.filename), "w+")
    jsonFile.write(json.dumps(self.datajson))
    jsonFile.close()

  def pretty(self):
    """
    Return pretty print
    :return prettyprint:
    """
    #update datajson
    self.read(self.filename)
    try:
      return json.dumps(self.datajson, indent=4, sort_keys=True)
    except Exception as e:
      merrors.error("could not pretty print, did you load the config? Python error: "+str(e))
      quit()

  def nested(self,main,name,var):
    self.read(self.filename)
    tmp = []
    try:
      old_nested = self.get(str(main))
    except Exception as e:
      merrors.error("could not create a nested value, does the main value exist? Python error: "+str(e))
      quit()
    for elem in old_nested:
      tmp.append(elem)
    tmp.append({str(name):str(var)})
    self.datajson[str(main)] = tmp
    file = open(str(self.filename), "w")
    json.dump(self.datajson,file)
    file.close()

  def add(self,name,var):
    file = open(str(self.filename), "w")
    self.datajson[str(name)] = str(var)
    json.dump(self.datajson,file)
    file.close()


# IMPORTER
import importlib
class importer:

  def __init__(self):
    self.flags = []
    self.return_code = 0
    self.cogs = []

  def read_cog(self,cog_name):
    for cog in self.cogs:
      if cog[0] == cog_name:
        print("===",cog_name,"===")
        print("version:",cog[1])
        print("function:",cog[2])
        print("variables:",cog[3])
        print("depends:",cog[4])
  
  def execute(self,cog_name,var=None,hot=False):
    for cog in self.cogs:
      if cog[0] == cog_name:
        #print("Running execute for",command,"from",dep,"with variable",var)
        self.return_code = 2
        dep = importlib.import_module(cog[4])
        method = getattr(dep, cog[2])
        return_code = method(var)
        if hot:
          return_code = 3
          dep = ""
          method = ""
        self.return_code = return_code

  def hot_cog(self,path):
    cogTemp = ezconfig()
    cogTemp.read(path)

    cog = [cogTemp.get("name"),cogTemp.get("version"),cogTemp.get("function"),cogTemp.get("variables"),cogTemp.get("depends")]

    self.cogs.append(cog)

  def load_cogs(self,path):
    config = ezconfig()
    config.read(path)
    
    # Load each cog
    locations = config.get("locations")
    
    for cog in locations:
        #print(cog)
        cogTemp = ezconfig()
        cogTemp.read(cog)
    
        # Check output
        #print(cogTemp.pretty())
    
        # create the list with the cog components
        cog = [cogTemp.get("name"),cogTemp.get("version"),cogTemp.get("function"),cogTemp.get("variables"),cogTemp.get("depends")]
    
        self.cogs.append(cog)

