# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 14:41:38 2020
@author: Steve Swihart
"""

ProgVer='0014.2' # This is written to metaDict.json file and is in window name.

# Next Steps:
"""
  High priority:
    Figure out how to make collapsible sections on open be hidden or not depending on last setting
    Instrument-dependent HW field propagation (use table per instrument)
    
  Should we rearchitect uploader or:
    Check files in path for integers - make sure enough digits
    See if event == '-FILE_LOCATION-': in event loop and related function.
        
  Med priority:    
    Log file statistics.
    Evan: auto propagate conc from folder name, incl in checkbox that controls auto propagation.
    Date format check for mfg date.
    Font size - consider variable, adding + and - buttons to shrink them by adding an amount to the variable.
      Would help with scaled displays to make it fit, or high res small ones, to make it visible.
    Test each imported but not used. Comment/remove if not actually needed.
    Make choosing "Instrument Name" propagate the optical parameters automatically (except Inst serial #).

  Meh priority:
    Using sorted list of tif files, get time from oldest (lowest int), then don't need to capture time any more - just show.
    Consider multiline text input for Other Notes with visibility false, button turns it on. 
    Maybe another button to hide it.
    Try bind_return_key=True
      
"""

# Version History and change highlights (first line summary matches git, details in subsequent lines
# ... and those match the subsequent lines in Git notes.)
"""
  14.2, 2-Nov-21, Added chk for installed module, mostly to learn how.
                   Currently believe only PSG itself is not part of repo and not default anaconda.
                   Uses checkModule.py. Note the needed code to use that in subdir.
  14.1, 28-Oct-21, Removed chk for INT for assay concentration
  14.0, 27-Oct-21, Made "Movie Time" mandatory and put it in required section (was in imaging info)
                   Updated all popups in required section to have an appropriate window title
                     ... rather than the first characters of the message
                   Added checks for #s for movie time, collection time and assay conc - ints, # of digits, etc
                     ... movie time - just went for 2 or more digits (so 11-99 sec are valid)
  13.2, 2-Sep-21, UI tweak for db additions today of 6 additional analytes
                   file "DynamoDB_Changes to Sample Info - Standard PN + Cap Molecule, and Detection Molecule.txt" 
                     in supporting folder of git is updated with the additions.
                   tweaked height of Analyte field, hard-coded.
  13.1, 31-Aug-21, UI tweaks for updated dynamo list entries:
                   Standard PN list is taller and wider (width is auto, height set to go to bottom of window)
                   db tweaks are listed in "DynamoDB_Changes to Sample Info - Standard PN + Cap Molecule, and Detection Molecule.txt"
                   ... which is in the supporting folder in git and on sharepoint in AD, Adv Eng, simreps, metadataTool... (git structure)
  0013, 13-Aug-21, added check for new enough version #
                    works at startup, checks for minimum version and current version
                    if minimum ver not present, displays message, won't work
                    if current version not present but > min, display message, still works
                    ... added '(Herc-Haifa small FOV only)' to tooltip on illumination micrometer
  0012-6, 4-Jun-21, check for and replace / and \ in "Unique Tif Stack Name"
                    Tested characters in UI "Unique Tif Stack Name" = PSG key "-STACK_FILENAME-" = metadata field "filename" 
                      for failure during stacking ...
                          Don't break: " " and = + [ ] { } ( ) . # @ % ^ ? ! $ : *
                          Break: /  (stacks are created but in a subfolder on S3 called "/")
                                 \  (python throws "invalid control character")
                    ... replace either / or \ with -
  0012-5, 13-May-21, Moved AWS credentials, region name, bucket name, dynamodb name to simrepsConfig.py.
                     In S3, 'simreps-dev' bucket has been created for development activiites. 
                     we can now configure in one place - simrepsConfig.py.
  0012-4, 28-Apr-21, Fixed issue where single-character folder name threw an error checking for time collected...
                      and also moved time check into AutoProp is True loop 
                      (so don't check if not propatating from folder name)
  0012-3, 2-Apr-21, Made Imaging Info section collapsable.
                      ...super minor - symbol in title bar for tooltips corrected - is i was +
  0012-2, 1-Apr-21, Removed red asterisks from required section, because the whole section is required.
                     Moved Detection Molecule section from bottom of left column to above consumable, below required.
                     Made collection time and well # optional (not required) for aLight
  0012-1, 19-Feb-21. modified spacing for Sample matrix line, widths and heights of elements and dropdowns 
                       so as not to truncate lists width-wise and not need scrollbars vertically
  0012, 17-Feb-21,     UI, db, back end changes
                       see list in "MetaToolChangesAndStatus.txt", AD Sharepoint, simreps, MetaDataTool\supporting
          27-Jan-21,   modified Tweak's position to not be over left column - it's mostly off right edge. 
                         consequence of increased width with Tweak open 
                           - moved main window from centered to top of screen, left of center
                         Original logic: don't go outside the lines. 
                         New logic: now can't see that updates from Tweak were made in left column.
                       User/Customer Section:
                         User and Location now on top line together (added a line in Sample Info, wanted to keep window height)
                         Assay Conc no longer loads last value from saved on open, and now has a tooltip
                         Updated row # button to be 3x8 consumable graphic and format is lettNum, so a1, b8, etc
                         Analyte Target - was called Analyte ID ... plus element width changes to keep overall size same
                       New row of 3 buttons with tooltips: Save, Load and Clear, with floppy icon, folder open icon, red/white X clear icon
                         These save the contents of the Consumable, Sample and Detection frames (sample maker),
                         load them (microscope operator), and clear those 3 sections.
                       Consumable Info:
                         Added red/white "clear section" icon to ... clear the section ... uses "clearConsumable" function.
                         "Sample Mfg (site)" WAS "Sample Maker (who)" - along with dynamo chgs - loc instead of human names
                         db change 5-Feb-21 to add "Hercules 3x8" to Substrate Material list
                       Sample Info:
                         Cap Molecule a lot wider and on own line after decision to include additional info like where and date.
                         Added lot #, concentration and volume to cap molecule section on 2nd line - related json and dynamo changes
                         Added red/white clear button for Sample section
                         Blocking Reagent moved up from 2 below "Analyte Vol" to just under Cap Molecule section and now orange text
                         New Standard subsection/line with PN and lot #. Related dynamo and json changes.
                         Old "Sample Diluent" now "Sample Matrix".
                           Added Vendor and Lot # fields with related dynamo and json changes.
                         Buffer and Salt Conc now on smae line to save space, just above incubation
                         'Vol loaded/Well' = '-IMAGING_SOLUTION_VOLUME-', now on a line with 2 new calculated fields:
                            dil Factor: (dil+anal)/anal_vol
                            % matrix: (1/(dil Factor))*100
                       Detection Molecule:
                         Added red/white X button to clear section
                         Added Fluorophore list
                       Slightly shrunk Submit button due to added row of buttons to minimize overall height.
  0011-9, 25-Jan-21, Tweak has scrollbars if size > window
                      determined 46 is current max height in rows for Tweak UI
                      check length of list. If < 46, fine, else set Tweak window to 46 and scrollbars appear.
                      Reorganized notes - was separate summary and details.
  0011-8, 7-Jan-21, meta/cloud uses combined uploader
                      cloud button calls SiMREPS_Upload.py rather than "loopUpload.py"
  0011-7, 7-Jan-21, user list is taller - no scroll
                      with the addition of Karen M @ alight, name list requires scrolling for several users
                      - made it display the whole list without scrolling.
  0011-6, 15-Dec-20, additional logging
                      log additional info - total files, total tifs, bad tifs
                      those 3 things are declared globally within the fileNameCheck function
  0011-5, 14-Dec-20, name chk on folders is now a function
                      dealing with name checks for folder is now a function. 
                      Pulled code from the Tweak UI class and the if in events 
                      (was in 2 places with subtlely different names)
  0011-4, 14-Dec-20, put back savedValues.json write
                      Put back savedValues.json write at Submit - that's how we load last values on program open!
  0011-3, 14-Dec-20, added rudimentary logging
                      basic logging to metaLog.txt.
                      includes program version, date and time of meta capture, the metadata.
                      needs file info next.
                      removed writing savedValues.json to program file's folder.
  0011-2, 12-Dec-20, added well propagation to UI field
                      removed unused imports
                      get well # from folder incl. check for alpha 2nd char.
                      folder name has to include "well" (case insensitive).
                      Works for either a1 or 11 alphanumeric or int well naming
  0011-1, 9-Dec-20, fixed bug where 'Capture_' dialog comes up every time.
                      ... by moving namesOK into loop for first chars != 'Capture_'. It was out to allow checking of counted file quantities.
  0011, 5-Dec-20, Now checks tifs in folder for 'Capture_', added Cloud/upload button.
                      ... 5-Dec-20, Added Cloud icon near Submit button to open the uploader.
                          4-Dec-20, Added check for 'Capture_' at beginning of each tif file
                          whether chosen from folder browser or Tweak Location. Both call fileNameCheck function.
  0010-5, 3-Dec-20, Consumable UI returns int, it and Folder Tweak window on top.
                      ... Made consumable window always on top until you choose a well (so can't lose it behind main window)
                          Changed its output to send an integer rather than row/col.
                          Made Folder Tweak UI on top  (have to close folder tweak to get back to main UI)
  0010-4, 10-Nov-20, Small UI chgs. Chk for tifs in folder. Choice for auto propagate tif stk + coll time or not
                      list tweaks for Alex, Li, Evan. Chk for tifs in folder. Chkbox for auto propagate tif stk and coll time or not
                      Alex: Added "Pipette tip wells" to Substrate Material list (in dynamo)
                      Alex: Add "600" to salt conc list: list didn't exist in uploadDictionary - created there and used here
                      Alex: Change "CRISP" to "Autofocus" - verbiage only
                      Li/Evan - don't populate with saved 'unique tif stack name' because it'll change per experiment!
                      Check specified folder for existense of Tifs - display popup if none.
                      Group: Added checkbox in File Browse area to do/not do population of unique tif stack name 
                        and collection time from chosen folder name
                        ... because that way if you don't use the folder name or have pre-prepared, it won't over-write
  0010-3, 5-Nov-20, implemented chk for numbers in folder path time locations - if only #s and hours !>23 and minutes !>59, propagate coll time, if not, not.
                        see above. Uses isnumeric(), then chks for hours !>23 and min !>59. 
                        Puts '' in the field in case numbers were there previously, 
                        forcing user to enter time after hitting submit.
  0010-2, 4-Nov-20, autopopulate collection time and unique Tif stack name from folder path, added word 'Assay' b4 Analyte 'Conc.'
                        added auto-propagate of unique tif stack name from folder browse or tweak. Can still type in there.
                        added word "Assay" in front of "Conc" for assay in required box, and implemented 0 padding to keep size down
          2-Nov-20, de-Weaslified the folder UI, 
                     fixed date check, which was not using result of validate. 
                     Now copy result of validate to another var and if either it or first var are false, throws error. 
                     Finds both # of char and 202x v 2020.
  0010-1, 30-Oct-20, fixed folder tweak UI slash issue, made frequently changed items appear together, saved vertical space
                     Added 2 sec wait time after displaying "Metadict written" then go back to "user input".
                      Goal 1 was to fix \ issue with Tweak UI
                      Goal 2 was to move frequently used near eachother:
                       Collection Time to below Unique Tif Stack Name
                       Well # to just under that
                       Analyte Conc and ID under that
                     ....
                     combine protocol type and assay time into single row (saves vertical space)
                     combine incubation time into single row (saves vertical space)
                     well chooser visible on left side so if click out of it, can get back to it
                     made consumable window appear slightly to left of main window so it is easier to get to if click on main win while open
                     ditto Tweak UI, but off to right
  0010, 27-Oct-20, folder tweak UI
                     enabled folder tweak that passes info both ways. So far just into dev. Needs proper multiwindow treatment.
  0009-3, 27-Oct-20, removed auto populate of folder location from last saved.
  0009-2, 26-Oct-20, updated tooltips, removed punctuation from Well loc when chosen from UI.
                      removed "(", ")" and "'" from well field with simple replace command
                      organized tooltips - all have a str name, naming convention
  0009-1, 23-Oct-20, added check for Experiment Name - must enter.
  0009, 22-Oct-20, removed uploading of data (just by commenting it out), loads from last use automatically, graphic buttons,
        added Experiment Name required field, 1 collapsable section in each column for scaled displays, consumable well UI
  
  These starting with a v not necessarily on git, just used in Hercules for testing
   v0009 11, 22-Oct-20, added "Experiment Name" field to required entries and dynamo
   v0009 11, 15-Oct-20, (partially written, will be in v0010) chooser with list of sibling folders and multi-window for consumable and siblings.
   v0009 10, 13-Oct-20, Clayton fixed an issue allowing collection dates too long or short.
   v0009 9, 6-Oct-20, fixed the collapsable sections coming up default theme until collapsed/restored (moved sg.theme() above the section code).
   v0009 8, 6-Oct-20, In LHS, Sample info, and in RHS, Optical Info now collapsable.
   v0009 7, 6-Oct-20, added aLight/UM hardware via adding those to the dynamo lists and tweaking code here to use them.  
   v0009 7, 6-Oct-20, added removal of .tiff, .Tiff or .TIFF from the stack name if those are typed.    
   v0009 6, 5-Oct-20, added removal of .tif, .Tif or .TIF from the stack name if those are typed.    
   v0009 5, 5-Oct-20, Clayton added data checking for Collection Date. Steve copied to Mfg Date. Steve switched fr hardcoded name list to "users" dynamo list.
   v0009 4, 5-Oct-20, corrected json formatting errors
   v0009 3, 5-Oct-20, strip '"' from string before dict conversion for savedValDict correctly allows it to become a dict.
   v0009 2, 5-Oct-20, added a dict in error correct on load of json of saved values with "" for each key to prevent errors using savedValDict.
   v0009, 3-Oct-20, a few more value pairs using saved data, implemented function for graphic "today" button.
   v0009, 2-Oct-20, implemented loading value pairs from dict into UI for fields that need it (all but coll date and time, unique Tif stack name)
   v0009, 2-Oct-20, "today" button for MFG_DATE
   v0009, 2-Oct-20, implemented Text function with size (was just Text12, fixed at 12) and propagated through UI
   v0009, 1-Oct-20, proved could populate value (so long as it matches one in list)
   v0009, 30-Sep-20, implemented save out of values at end to text and json
   v0009, 29-Sep-20, implemented json using metaDict.json in that function, using names per Clayton    
  
  0008, 27-Sep-20, implemented all dynamo lists, added Status area 
                     (had issue, only works once)
                     implemented Status area in lower right.
                     25-Sep-20, implemented remaining dynamo lists (all but blocking reagent list, which was in 0007).
  0007, 18-Sep-20, first version sent to all the users.
                     Moved Analysis Start Time above Incubation Time and change keys related to it
                     updated Metadata.json to match those changes
                     changed key names going to table per above 2 lines, and added collectionTime key
        17-Sep-20, added lists to populate dropdowns and keep track of values used
                     data format check logic
                     Force input for some fields if empty (popups work now but hide button until ready?)
                     then don't need both Check and Submit    
  0006, 16-Sep-20, added imageCollectionRate, units for rest of item/value pairs, "Other" text entry
                     broke capture and analyte into 2 lines ea, with units added for conc. and vol.
                     also added units for Salt Conc, Incubation Time, 
                     removed "eg 50" from unit () for Det molecule, added (format) for Analysis Start time
                     added "Undefined" starting value for OtherText so if none is entered, won't crash
                     calculated imageCollectionRate (1/exposure time). We know it's slightly off
        15-Sep-20, added button which brings up OtherText entry field
  0005, 15-Sep-20, only Alex got this one, dynamo and S3 write of metadata and TIF files, but to temp location for testing,
                     fixed Movie Time 6 digit pre-populated field, added Alex and aLight users, more Haifans, 
                     restricted input to drop only for user and loc, popups for empty user, location, file location
                     any empty value is replaced by 'Undefined' unless location or user
                     Match Clayton's list of fields - add/change
                     add red asterisks for required fields, change tooltip symbol from * to +
        14-Sep-20, made UI do YYYYmmDD,HHMM, and then split into 2 pairs in uploaded metadata
                     Update name list per aLight & Haifa
                     date/time in YYYYMMDD format
                     Pull JSON write out as a function
                     replace empty fields "" with "Undefined" (used dict comprehension)
        11-Sep-20, added popups for empty fields (user, location, file location), 
                     and got working dir to write to if file location empty
        10-Sep-20, get rid of everything except date and fixed optical info (no pre-population)
                     don't allow user input for user and location (add readonly='true')
        9-Sep-20, fixed Movie Time 6 digit pre-populated field by adding , betw last 2 values!
  0004, 8-Sep-20, structured write of json. First version sent to Boaz/Itay. Had minor issue in Movie Time.
                     format the json formally
                     implement write with keys and values
                     fixed write issue (a matter of an additional \ at end of file location value)
  0003, 7-Sep-20, DOESN'T WORK without Py installed. fixed file location root cause
                     fix Metadata.json write - use selected path not location of executable for compiled version 
                     - it didn't actually write correctly, FWIW.
  0002, 7-Sep-20, added keys for all data, and Lens Temp to Optical Info, and movie time. Still writes to wherever .exe is.
                     implement PySimpleGUI keys (but they're not written to file yet)
  0000-2, 2-Sep-20: 0000 but writes version # ("0000-2") to top of file. Puts Metadata.json where the .exe is.
  0001, 2-Sep-20: DOESN'T WORK (compiled version won't write a file). This is the first version deployed 
    just to Hercules. It writes version # (line 8) at top of file, then writes metadata with indexes 
    being numerical (no keys_) with the exception of FileLocation, which is the first key implemented
    add version # to Metadata.json
  0000, 1-Sep-00: this version wrote a file in the location of the executable.
  Get file write to happen without close
  Store data in file
  Update per Bill
  2 columns - everything not inst in one, inst incl optical and imaging in the other
  Comments to tooltips to save H space b4 go to 2 columns
  Justification of boxes to an arbitrary h pos
  Short term with comments, (later use columns)
  H rules betw. major sections?
  Make location and maybe instrument name dropdowns
  sg.Frame - draw boxes around areas
"""


import sys
sys.path.insert(0, './supporting') # Need this to allow function to be in a subdir
import checkModule #which will check for a py module and install if not installed

#repeat next lines per module that isn't part of Anaconda default
moduleName='PySimpleGUI'
inst=checkModule.checkModuleInstalled(moduleName)
print('module ',moduleName,'is installed?',inst)

import PySimpleGUI as sg
# print('PSG Path = '+ sg) #print import name, which gives you path
# print('PSG Version = '+ sg.version)
import datetime
import time
import boto3
import subprocess
import simrepsConfig
# from os import path
from pathlib import Path #, PureWindowsPath
# from json import (load as jsonload, dump as jsondump)
import json
import ast #used in loading savedValues.json
import math # used for version # separation before and after decimal point



"""
# Set up S3 and Dynamo
"""
bucket = simrepsConfig.aws_bucket
AWS_ACCESS_KEY_ID=simrepsConfig.aws_access_key
AWS_SECRET_ACCESS_KEY=simrepsConfig.aws_secret_key

#create s3 boto3 client
s3 = boto3.client('s3',
                   region_name=simrepsConfig.aws_region,
                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                )

#create dynamodb boto3 resource
dynamodb = boto3.resource('dynamodb',
                           region_name=simrepsConfig.aws_region,
                           aws_access_key_id=AWS_ACCESS_KEY_ID,
                           aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                        )

sfTable = dynamodb.Table(simrepsConfig.aws_sfTable)
saTable = dynamodb.Table(simrepsConfig.aws_saTable)
rdTable = dynamodb.Table(simrepsConfig.aws_sudTable)
response = rdTable.scan(AttributesToGet=['users','collectionLocation','analyteID',
                                            'substrateFabricator','substrateMaterial','surfaceChemistry',
                                            'washProtocol','assay','capMoleculeID','blockingReagent','standardPartNumber','standardLotNumber',
                                            'sampleDiluent','sampleMatrixVendor','sampleMatrixLotNumber','buffer','saltConcentration',
                                            'analyteVolume','bufferOSS_Volume','imagingSolutionVolume',
                                            'detectionMoleculeID','detectionFluorophore',
                                            'instrumentName','CRISP_OnOff','oilBetwSampleAndLens','lensTemp','lensNA','lensMag','camera',
                                            'resolutionMax','resolutionUsed','binning',
                                            'metaMinimumVersion','metaCurrentVersion'])


# lists for dropdowns, pulled from dynamo
#   ... in order they appear in UI
#print(response['Items'])
userList = response['Items'][0]['users']
locationList = response['Items'][0]['collectionLocation']     # used 25-Sep-20
analyteIDList = response['Items'][0]['analyteID'] # used 25-Sep-20

detectIDList = response['Items'][0]['detectionMoleculeID'] # used 25-Sep-20
detectionFluorophoreList = response['Items'][0]['detectionFluorophore'] # added here and db 12-Feb-21

fabricatorList = response['Items'][0]['substrateFabricator']    # used 25-Sep-20
substateMatList = response['Items'][0]['substrateMaterial']     # used 25-Sep-20
surfaceChemistryList = response['Items'][0]['surfaceChemistry'] # used 25-Sep-20

washProtocolList = response['Items'][0]['washProtocol']  # used 25-Sep-20
assayList = response['Items'][0]['assay']  # used 25-Sep-20
capIDList = response['Items'][0]['capMoleculeID'] # used 25-Sep-20
# Cap Lot No - No list: a user-entered string
# Cap Conc - No list: a user-entered string
# Cap Vol - No list: a user-entered string
blockingReagentList = response['Items'][0]['blockingReagent'] #used in v0007
standardPartNumberList = response['Items'][0]['standardPartNumber'] # added 8-Feb-21
standardLotNumberList = response['Items'][0]['standardLotNumber'] # added 8-Feb-21
diluentList = response['Items'][0]['sampleDiluent'] # used 25-Sep-20. 8-Feb-21, now called "Sample Matrix" in UI
sampleMatrixVendorList = response['Items'][0]['sampleMatrixVendor'] # added 8-Feb-21
sampleMatrixLotNumberList = response['Items'][0]['sampleMatrixLotNumber'] # added 10-Feb-21
bufferList = response['Items'][0]['buffer'] # used, 25-Sep-20
saltConcentrationList = response['Items'][0]['saltConcentration'] #added 10-Nov-20
sampleVolumeList = response['Items'][0]['analyteVolume'] # Was simple string before 12-Feb-21, now a list
bufferOSS_VolumeList = response['Items'][0]['bufferOSS_Volume'] # Added 11-Feb-21 here and to dynamo
imagingSolutionVolumeList = response['Items'][0]['imagingSolutionVolume'] # Was hard coded at 55, 100, 200 b4 12-Feb-21, now a dynamo list

instrumentList = response['Items'][0]['instrumentName'] # used 25-Sep-20
# crispList = response['Items'][0]['CRISP_OnOff'] # Not implemented, modifies UI from hard coded 'y/n' to "True False".
# oilList = response['Items'][0]['oilBetwSampleAndLens'] # Not implemented, modifies UI from hard coded 'y/n' to "True False".
lensTempList = response['Items'][0]['lensTemp']  # added 6-Oct-20 to incorporate aLight/UM hardware
lensNAList = response['Items'][0]['lensNA']  # added 6-Oct-20 to incorporate aLight/UM hardware
lensMagList = response['Items'][0]['lensMag']  # added 6-Oct-20 to incorporate aLight/UM hardware
cameraList = response['Items'][0]['camera'] # implemented 27-Sep-20, though have to get Alex's camera info from e-mail, ditto resolution
resolutionMaxList =  response['Items'][0]['resolutionMax'] # added 6-Oct-20 to incorporate aLight/UM hardware
resolutionUsedList =  response['Items'][0]['resolutionUsed'] # added 6-Oct-20 to incorporate aLight/UM hardware
binningList = response['Items'][0]['binning'] # implemented 27-Sep-20



"""
VERSION CHECKING
  Minimum and Current vers are strings in dynamo. Turn them into major and minor versions,
  compare major and minor.

check that new enough ver is being used
  Anything that could break upload or processing is 'major' and will be a full int increase in ver. 
  Anything that won't break the universe is considered minor and will be after a decimal point.
  
  eg 0013.001 is on a computer. current version is 0013.5. Display message, will still operate.
     0013.001 is on a computer, current version is 0014.0. Display message, won't operate.
"""
minimumVersion = response['Items'][0]['metaMinimumVersion'] # added 11-Aug-21, check to see if new enough version is being used.
print('meta Tool minimum version (major.minor):',minimumVersion)
minVer=float(minimumVersion)
print('minVer',minVer)
minVerSeparated=math.modf(minVer)
print('minVerSeparated',minVerSeparated)
minVerMajor=int(minVerSeparated[1])
minVerMinor=round(10*(minVer-minVerMajor))
print('minimum major ver:',minVerMajor, ', minimum minor ver',minVerMinor)
thisVersion=float(ProgVer)
thisVerSeparated=math.modf(thisVersion)
print('version that is running:',thisVersion)
thisVerMajor=int(thisVerSeparated[1])
thisVerMinor=round(10*(thisVersion-thisVerMajor))
print('this major ver:',thisVerMajor, ', this minor ver',thisVerMinor)


currentVersion = response['Items'][0]['metaCurrentVersion'] # added 11-Aug-21, check to see what current is
print('meta Tool current version:', currentVersion)
currentVer=float(currentVersion)
currentVerSeparated=math.modf(currentVer)
currentVerMajor=int(currentVerSeparated[1])
currentVerMinor=round(10*(currentVer-currentVerMajor))
print('current version, minor =',currentVerMinor)

if thisVerMajor < minVerMajor:
    print('You are running version',thisVersion,'. Version',minVer,'is the minimum version. Version ',currentVersion,'is the current version.\nget new version via git pull.\nProgram will terminate.')
    # Use a PSG window to display the message....
    layoutOutOfDate=[
        [sg.T('Out of date version used', text_color='OrangeRed2', font=('Any',13,'bold'))],
        [sg.T('You are running version'),sg.T(thisVersion, font=('Any',10,'italic'),pad=(0,0),text_color='orange')],
        [sg.T('Version'),sg.T(minVer, font=('Any',10,'italic'),pad=(0,0),text_color='orange'),sg.T('is required.')],
        [sg.T('   program will terminate.')],
        [sg.T('What to do:', font=('Any',11,'italic'))],
        [sg.T('  Do a git pull if possible.')],
        [sg.T('     In Spyder, !git pull. In Git Bash or Git CMD, git pull')],
        [sg.T('  If no git client is available:\n     delete all code in IDE, \n     view from web, \n     copy all, paste into IDE')],
        [sg.T('New version required before metadata can be captured. \nSomething would break if you used this version.',font=('Any',13,'bold italic'),text_color='coral1')]
        ]
    winOutOfDate=sg.Window(title='Program Version Error',layout=layoutOutOfDate,modal=True)
    while True:
        event,values=winOutOfDate.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
             break
    sys.exit('Quit program due to version too old.')

elif thisVerMajor >= minVerMajor:
    print('major version >= minimum, moving on.')

# If runnin major ver was < minimum major ver, program stopped. Now, check against current version, and inform user if
#    non-fatally out of date.
if thisVerMajor >= minVerMajor and thisVerMinor < currentVerMinor:
    print('Current version minor is',currentVerMinor,'running ver minor is ',thisVerMinor)
    sg.Popup('current meta version is '+currentVersion+', you are running '+str(thisVersion)+'\nVersion you are running will not break anything,\nbut upgrading is recommended',title="Version information")

"""
End Version Checking Section
"""

# Check for last-used values and load if exist.
try:
    with open('savedValues.json','r') as f:
        savedValStr=f.read()
        print('savedValueStr string using f.read from savedValues.json:\n'+savedValStr)
        savedValStr=savedValStr.replace("Undefined",'')
        savedValStr=savedValStr.strip('"')
        print('savedValueStr string, replaced Undefined with blank:\n'+savedValStr)
        savedValDict=ast.literal_eval(savedValStr) 
        print('--------------------')
        print('savedVal(dict) sans Undefined: \n'+str(savedValDict))
except FileNotFoundError:
    print('aint got no savedValues.json file')
    savedValDict={"-USER-": "", "-COLLECTION_DATE-": "", "-COLLECTION_TIME-": "", "-LOCATION-": "", "-EXPOSURE_TIME(SEC)-": "", "-STACK_FILENAME-": "", "-SLIDE_ID-": "", "-MFG_DATE-": "", "-SAMPLE_MAKER-": "", "-SUBSTRATE_MATERIAL-": "", "-SURFACE_CHEMISTRY-": "", "-WELL_NUMBER-": "", "-PROTOCOL_TYPE-": "", "-ASSAY_TYPE-": "", "-CAPTURE_MOLECULE-": "", "-CAPTURE_MOLECULE_CONCENTRATION-": "", "-CAPTURE_MOLECULE_VOLUME-": "", "-ANALYTE_MOLECULE-": "", "-ANALYTE_CONCENTRATION-": "", "-ANALYTE_VOLUME-": "", "-BUFFER-": "", "-BLOCKING_REAGENT-": "", "-SAMPLE_DILUENT-": "", "-SALT_CONCENTRATION-": "", "-INCUBATION_START_TIME-": "", "-INCUBATION_TIME-": "", "-DETECTION_MOLECULE_ID-": "", "-DETECTION_MOLECULE_LOT_NUMBER(MFG_DATE)-": "", "-DETECTION_MOLECULE_CONCENTRATION-": "", "-LABEL_RATIO-": "", "-IMAGING_SOLUTION_VOLUME(uL)-": "", "-FILE_LOCATION-": "", "Browse": "", "-INSTRUMENT_NAME-": "", "-INSTRUMENT_SN/ID-": "", "-CRISP_ON-": True, "-OIL_BETWEEN_SAMPLE_AND_LENS-": True, "-LASER_POWER_SOURCE(mW)-": "", "-LASER_POWER_SAMPLE(mW)-": "", "-ILLUMINATION_MICROMETER-": "", "-LENS_TEMPERATURE-": "", "-LENS_NUMERICAL_APERTURE-": "", "-LENS_MAGNIFICATION-": "", "-CAMERA-": "", "-RESOLUTION_MAX-": "", "-RESOLUTION_USED-": "", "-BINNING-": "", "-MOVIE_TIME(SEC)-": "", "-CAMERA_OFFSET-": "", "-DARK_FRAME_VALUE-": "", "-CAMERA_GAIN-": ""}
    
"""
Functions, JSON write, validation of date, folder chooser, repeated UI functions
"""


def metadataJsonWrite():
    file = open (FL_Slash + "\metaDict.json","wt")  
    file.write('{'+'\n')
# Required Info UI Section
    file.write('  \"userName\": \"' + str(values['-USER-'])+'\",\n')
    file.write('  \"collectionLocation\": \"' + str(values['-LOCATION-'])+'\",\n')
    file.write('  \"dateCollected\": \"' + str(values['-COLLECTION_DATE-'])+'\",\n')
    file.write('  \"collectionTime\": \"' + str(values['-COLLECTION_TIME-'])+'\",\n')
    file.write('  \"exposureTime_sec\": \"' + str(values['-EXPOSURE_TIME(SEC)-'])+'\",\n')
    file.write('  \"imageCollectionRate\": \"'+ str(1/float(values['-EXPOSURE_TIME(SEC)-']))+'\",\n')
    file.write('  \"folderLocation\": \"'+ str(values['-FILE_LOCATION-'])+'\",\n')
    file.write('  \"experimentName\": \"'+ str(values['-EXPERIMENT_NAME-'])+'\",\n')
    file.write('  \"fileName\": \"' + str(values['-STACK_FILENAME-'])+'\",\n')
    file.write('  \"wellNumber\": \"' + str(values['-WELL_NUMBER-'])+'\",\n')
    file.write('  \"analyteID\": \"' + str(values['-ANALYTE_MOLECULE-'])+'\",\n')
    file.write('  \"analyteConcentration\": \"' + str(values['-ANALYTE_CONCENTRATION-'])+'\",\n')    

# Consumable Info UI Section
    file.write('  \"slideIDNumber\": \"' + str(values['-SLIDE_ID-'])+'\",\n')
    file.write('  \"consumableMfgDate\": \"' + str(values['-MFG_DATE-'])+'\",\n')
    file.write('  \"substrateFabricator\": \"' + str(values['-SAMPLE_MAKER-'])+'\",\n')   
    file.write('  \"substrateMaterial\": \"' + str(values['-SUBSTRATE_MATERIAL-'])+'\",\n')
    file.write('  \"surfaceChemistry\": \"' + str(values['-SURFACE_CHEMISTRY-'])+'\",\n')

# Sample Info UI Section
    file.write('  \"washProtocol\": \"' + str(values['-PROTOCOL_TYPE-'])+'\",\n')
    file.write('  \"assay\": \"' + str(values['-ASSAY_TYPE-'])+'\",\n')
    file.write('  \"capMoleculeID\": \"' + str(values['-CAPTURE_MOLECULE-'])+'\",\n')
    file.write('  \"capLotNumber\": \"' + str(values['-CAP_LOT_NUMBER-'])+'\",\n')
    file.write('  \"capMoleculeConcentration\": \"' + str(values['-CAPTURE_MOLECULE_CONCENTRATION-'])+'\",\n')
    file.write('  \"capMoleculeVolume\": \"' + str(values['-CAPTURE_MOLECULE_VOLUME-'])+'\",\n')
    file.write('  \"blockingReagent\": \"' + str(values['-BLOCKING_REAGENT-'])+'\",\n')
    file.write('  \"standardPN\": \"' + str(values['-STANDARD_PN-'])+'\",\n')
    file.write('  \"standard_LOT_NO\": \"' + str(values['-STANDARD_LOT_NO-'])+'\",\n')
    file.write('  \"sampleDiluent\": \"' + str(values['-SAMPLE_DILUENT-'])+'\",\n') # "Sample Matrix" in UI
    file.write('  \"sampleMatrixVendor\": \"' + str(values['-SAMPLE_DILUENT_VENDOR-'])+'\",\n') # "Sample Matrix Vendor" in UI
    file.write('  \"sampleMatrixLotNumber\": \"' + str(values['-SAMPLE_DILUENT_LOT_NO-'])+'\",\n') # "Sample Matrix Lot" in UI
    file.write('  \"buffer\": \"' + str(values['-BUFFER-'])+'\",\n')
    file.write('  \"saltConcentration\": \"' + str(values['-SALT_CONCENTRATION-'])+'\",\n')
    file.write('  \"analyteVolume\": \"' + str(values['-ANALYTE_VOLUME-'])+'\",\n') # "Sample Volume" in UI
    file.write('  \"bufferOSS_Volume\": \"' + str(values['-BUFFER_OSS_VOLUME(uL)-'])+'\",\n')
    file.write('  \"imagingSolutionVolume\": \"' + str(values['-IMAGING_SOLUTION_VOLUME(uL)-'])+'\",\n') #"Volume Loaded / Well (µL)" in UI
    file.write('  \"incubationStartTime\": \"' + str(values['-INCUBATION_START_TIME-'])+'\",\n')
    file.write('  \"incubationTime\": \"' + str(values['-INCUBATION_TIME-'])+'\",\n')

# Detection Molecule UI Section    
    file.write('  \"detectionMoleculeID\": \"' + str(values['-DETECTION_MOLECULE_ID-'])+'\",\n')
    file.write('  \"detectionMoleculeLotNumber\": \"' + str(values['-DETECTION_MOLECULE_LOT_NUMBER(MFG_DATE)-'])+'\",\n')
    file.write('  \"detectionMoleculeConcentration\": \"' + str(values['-DETECTION_MOLECULE_CONCENTRATION-'])+'\",\n')
    file.write('  \"labelRatio\": \"' + str(values['-LABEL_RATIO-'])+'\",\n')
    file.write('  \"detectionFluorophore\": \"' + str(values['-DETECTION_FLUOROPHORE-'])+'\",\n')

# Instrument Info UI Section       
    file.write('  \"instrumentName\": \"' + str(values['-INSTRUMENT_NAME-'])+'\",\n')
    file.write('  \"serialNumber-Identifier\": \"' + str(values['-INSTRUMENT_SN/ID-'])+'\",\n')
    file.write('  \"CRISP_OnOff\": \"' + str(values['-CRISP_ON-'])+'\",\n')

# Optical Info UI Subsection     
    file.write('  \"oilBetwSampleAndLens\": \"' + str(values['-OIL_BETWEEN_SAMPLE_AND_LENS-'])+'\",\n')
    file.write('  \"laserPowerSource_mW\": \"' + str(values['-LASER_POWER_SOURCE(mW)-'])+'\",\n')
    file.write('  \"laserPowerSample_mW\": \"' + str(values['-LASER_POWER_SAMPLE(mW)-'])+'\",\n')
    file.write('  \"illuminationMicrometer\": \"' + str(values['-ILLUMINATION_MICROMETER-'])+'\",\n')
    file.write('  \"lensTemp\": \"' + str(values['-LENS_TEMPERATURE-'])+'\",\n')
    file.write('  \"lensNA\": \"' + str(values['-LENS_NUMERICAL_APERTURE-'])+'\",\n')
    file.write('  \"lensMagnification\": \"' + str(values['-LENS_MAGNIFICATION-'])+'\",\n')
        
# Imaging Info UI Subsection    
    file.write('  \"camera\": \"' + str(values['-CAMERA-'])+'\",\n')
    file.write('  \"resolutionMax\": \"' + str(values['-RESOLUTION_MAX-'])+'\",\n')
    file.write('  \"resolutionUsed\": \"' + str(values['-RESOLUTION_USED-'])+'\",\n')    
    file.write('  \"binning\": \"' + str(values['-BINNING-'])+'\",\n')
    file.write('  \"movieTime_sec\": \"' + str(values['-MOVIE_TIME(SEC)-'])+'\",\n')
    file.write('  \"cameraOffset\": \"' + str(values['-CAMERA_OFFSET-'])+'\",\n')
    file.write('  \"darkFrameValue\": \"' + str(values['-DARK_FRAME_VALUE-'])+'\",\n')
    file.write('  \"cameraGain\": \"' + str(values['-CAMERA_GAIN-'])+'\",\n')        

# Other Info UI Box
    file.write('  \"experimentNotes\": \"'+ OtherText+ '\"\n')
    file.write('}'+'\n')
    file.close()
    return;


# 'Tweak' button: Fancy dir search sort routine (starts at "class ListboxWithSearch")
#    https://github.com/evan54/mysimplegui/blob/master/mysimplegui.py

def folderUI(values):
    import re
    import warnings
    import pandas as pd

# get chosen path, go one up, find paths below, make into a list    
    AutoProp=values['-AUTO_PROP_FROM_FOLDER-'] # True or false - checkbox on RHS
    oo=values['-FILE_LOCATION-'] # the path chosen by OS folder browserwhen select "Browse" on RHS
    p=str(values['-FILE_LOCATION-'])
    print('--------------------\nIn Tweak UI Section\n')
    print('Chosen path for images (p) is: '+p)
    p=p.replace('/','\\')
    print('p with slashes flipped:'+p)
    pt=Path(p)
    # print(pt)
    pp=pt.parent
#    pps=str(pp)
    print('Parent of p: '+str(pp))
#    sg.Popup('path one up =:',pp)
    lst=[x for x in pp.iterdir() if x.is_dir()]
    print('\n--------------------------\nLst of paths in parent as paths:\n',lst)
#    sg.Popup(lst)
    
    print('\nRemoving Path info to get at strings of paths:\n')
    item=0
    for item in range(len(lst)):
        print(''+str(lst[item]))
        lst[item]=str(lst[item])
    
    print('\n--------------------------\nLst of paths str:\n',lst)

    class ListboxWithSearch:
    
        def __init__(self, values, key='', select_mode='single',
                     size=(None, None), sort_fun=False, bind_return_key=False,
                     is_single_mode=True):
            if not is_single_mode:
                select_mode = 'extended'
                warnings.warn('Ev: is_single_mode is going to be deprecated use '
                              'select_mode instead', DeprecationWarning)
            print('\np str from within class: '+p)
            listp=p.split(sep=None)
            print('listp is a list of p: '+str(listp))
            print('Folder from Browse in main UI, oo: '+oo)
            self._key = key
            self._sort = sort_fun if sort_fun else lambda lst: list(lst)
            self._input_key = key + '_input'
            self._select_all_key = key + '_select_all'
            self._deselect_all_key = key + '_deselect_all'
            self._clear_search_key = key + '_clear_search'
            self._values = values
            self._selected = set()
            self._displayed_secret = values
            self._el = sg.Listbox(values=self._sort(self._displayed),
                                  size=self._initialise_size(size),
                                  key=key,
                                  select_mode=select_mode,
                                  default_values=[p],
                                  bind_return_key=bind_return_key, enable_events=True)
            #self._msg = sg.T('I DO NOT WORK YET.\nIf folder not chosen, i need to be initialized empty.\nI do not pass chosen value back. \nI do not pre-highlight last chosen.',text_color='OrangeRed2')
            self._i = sg.I(key=self._input_key, enable_events=True,
                           tooltip='''
            
    Start a string with = and everything after will be considered a regexp
    otherwise it will be a simple match:
    eg enter:
        =.*world$
    vs entering
        world''')
            buttons = []
            if select_mode != 'single':
                buttons.append(sg.B('Select all', key=self._select_all_key))
            buttons.append(sg.B('Deselect all', key=self._deselect_all_key))
            buttons.append(sg.B('Clear search', key=self._clear_search_key))
            self.layout = sg.Column([
                #[self._msg],
                [self._i],
                buttons,
                [self._el]])
    
        def frame_layout(self, name):
            return sg.Frame(name, layout=[[self.layout]])
    
        def _initialise_size(self, size):
            size = list(size)
            if size[0] is None and len(self._values) > 0:
                size[0] = max(len(lst) for lst in self._values) + 1
            if size[1] is None and len(self._values) > 0:
                size[1] = len(self._values) + 1
            return size
    
        @property
        def _displayed(self):
            return self._displayed_secret
    
        @property
        def selected(self):
            return tuple(self._selected)
    
        @_displayed.setter
        def _displayed(self, values):
            self._displayed_secret = (values if isinstance(values, dict)
                                      else set(values))
            self._el.Update(values=self._sort(self._displayed_secret),
                            set_to_index=0)
    
        def update(self, values):
    
            original_displayed = tuple(self._displayed)
            is_regexp = not(len(values[self._input_key]) > 0 and
                            values[self._input_key][0] == '=')
    
            if not is_regexp:
                search_string = values[self._input_key][1:]
            else:
                search_string = '.*' + re.escape(values[self._input_key]) + '.*'
            selected = values[self._key]
    
            def match_fun(s):
                try:
                    return re.match(search_string, s, re.I)
                except re.error:
                    return True
    
            # update displayed
            if isinstance(self._values, dict):
                self._displayed = {s: y for s, y in self._values.items()
                                   if match_fun(s)}
            else:
                self._displayed = [s for s in self._values if match_fun(s)]
    
            self._update_selection(selected, original_displayed)
    
        def _update_selection(self, selected, original_displayed):
            # update selection
            if self._el.SelectMode in ['multiple', 'extended']:
                self._selected = self._selected - set(original_displayed)
                self._selected.update(selected)
            elif self._el.SelectMode == 'single':
                if len(selected) > 0:
                    self._selected = set(selected)
            else:
                raise ValueError(self._el.SelectMode,
                                 'expected "single" or "multiple"')
            selected_and_displayed = self._selected.intersection(self._displayed)
    
            # self._el.Update(values=self._sort(self._displayed), set_to_index=0)
            self._el.SetValue(selected_and_displayed)
    
        def _select_all_displayed(self):
    
            self._selected.update(self._displayed)
            self._el.SetValue(self._sort(self._displayed))
    
        def _deselect_all_displayed(self):
    
            for el in self._displayed:
                self._selected.discard(el)
    
            self._el.SetValue([])
    
        def set_values(self, values, selected=None):
            self._values = values
            self._displayed = values
            if selected is None:
                self._selected = set()
                self._el.SetValue([])
            else:
                if isinstance(selected, str):
                    selected = [selected]
                self._selected = set(selected)
                self._el.SetValue(self._sort(selected))
    
        def _clear_search(self, values):
            selected = values[self._key]
            original_displayed = tuple(self._displayed)
            self._update_selection(selected, original_displayed)
            self._i.Update(value='')
            self.update({self._input_key: '',
                         self._key: tuple(self._selected)})
    
        def manage_events(self, event, values):
            if event == self._select_all_key:
                self._select_all_displayed()
            elif event == self._deselect_all_key:
                self._deselect_all_displayed()
            elif event == self._input_key:
                self.update(values)
            elif event == self._clear_search_key:
                self._clear_search(values)
            elif event is None:
                pass
            else:
                selected = values[self._key]
                original_displayed = tuple(self._displayed)
                self._update_selection(selected, original_displayed)
    
    
    def show_hidden_files_button(win):
        """
        To be used with layouts that include sg.FileBrowser, the purpose is to
        allow hidden files to not be shown. Inspired from:
            https://stackoverflow.com/a/54068050/1764089
            and
            https://github.com/PySimpleGUI/PySimpleGUI/issues/1830
        example usecase:
            import PySimpleGui as sg
            win = sg.Window('Test', layout=[[sg.FileBrowser('Load file'),
                                             sg.Button('ok')]])
            show_hidden_files_button(win)
            while True:
                event, values = win.Read()
                if event is None:
                    win.Close()
                    break
        """
        # set up TKroot
        win.Read(timeout=0)
    
        # from https://stackoverflow.com/a/54068050/1764089
        try:
            win.TKroot.tk.call('tk_getOpenFile', '-foobarbaz')
        except sg.tk.TclError:
            pass
        win.TKroot.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
        win.TKroot.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
    
    
    if __name__ == '__main__':
    
        values = lst #['hello', 'hello world', 'my world', 'your wold', 'god'] # the original list from Evan Scouros' routine
        numFolders=len(lst)
        if numFolders > 46:
            numFolders = 46
        listbox1 = ListboxWithSearch(values, 'mylistbox',size=(None,numFolders))
        layout = [ [listbox1.layout]
                  ]
        win = sg.Window('Sibling Folder Chooser', layout=layout, modal=True, resizable=True,location=locnadj)
        while True:
            event, values = win.Read()
            print('--------------------\n...In Tweak UI *Window* section')
            if event is None:
                break
            else:
                listbox1.manage_events(event, values)
            print(event, values)
            folderList=str(values['mylistbox']) #get list of folders
            windowUpdate(AutoProp, folderList)
            
    return fileQty

def windowUpdate(AutoProp,folderList):
    # propagate foldername and well # to UI fields if checkbox=true
    print('folderList:'+folderList)
    folderList=folderList.replace('[','').replace(']','') #nix [ and ]
    print('folderList without brackets:'+folderList)
    folderList=folderList.strip("'") # nix '
    print('folderList without beg and end single quotes:'+folderList)
    folderList=folderList.replace(r'\\','/') #swap \\ for /
    winMain['-FILE_LOCATION-'].update(folderList) #update path in file location field
    folderName=folderList.rsplit('/',2) # get everything past last slash (the folder)
    print('folder name sans path: '+str(folderName[-1]))
    folderNameOnly=folderName[-1] #same but different type
    print('folderNameOnly',folderNameOnly)
    
    if AutoProp==True: # then try to get stack name, well # and collection time from path
        winMain['-STACK_FILENAME-'].update(folderName[-1]) #update unique Tif stack name from folder name
        # get the well #
        folderNameOnlyLow=folderNameOnly.casefold() #gives the folder name in all lower
        print('foldername all lower case: ',folderNameOnlyLow)
        if "well" in folderNameOnlyLow:
            print('well is present in folder name')
            wellStartLoc=folderNameOnlyLow.find("well")
            print('pos of start of well loc: ',wellStartLoc)
            wellNumLong=folderNameOnly[wellStartLoc+4:wellStartLoc+6]
            print('2 digit well # - no letter check: ',wellNumLong)
            wellNum=wellNumLong
            wellNumLastChar=wellNumLong[-1]
            print('well # last char = ',wellNumLastChar)
            if wellNumLastChar.isnumeric() == False:
                wellNum=wellNum[0]
                print('last char != numeric, removed, well # =',wellNum)
            #update UI with well #
            winMain['-WELL_NUMBER-'].update(wellNum)                
        else:
            print('well is *not* present in folder name')
        
        hourColl=folderNameOnly[0:2] #get the hour from the folder name
        len_hourColl=len(hourColl)
        print('hour from folder name = ',hourColl, '... length of hourColl = ', len_hourColl)
        minuteColl=folderNameOnly[3:5] #get the minutes from the folder name
        len_minuteColl=len(minuteColl)
        print('minutes from folder name = ',minuteColl, '.. length of minuteColl = ', len_minuteColl)
        timeColl=hourColl+minuteColl #combine hours and minutes to get time
        print('timeColl combined hour and min = ',timeColl)
        gotNums=timeColl.isnumeric() #check 2C if have #s in timeColl
        if len_hourColl==2 and len_minuteColl==2 and gotNums==True:
            gotNumsLenOK=True
            print('hours and minutes length = 2 and are numeric')
        else:
            gotNumsLenOK=False
            print('hours or minutes too short or not numeric')
        print('timeColl is numbers b4 if loop? ',gotNums)
        if gotNumsLenOK==True: #check for whether #s make sense - hours>24, minutes>59 are invalid
            print('int of hourColl = ',int(hourColl))                
            if int(hourColl) > 23 or int(minuteColl)>59:
                print('type of hourColl =',type(hourColl),'\nvalue of hourColl',hourColl,'\ntype of timeColl =',type(timeColl))
                timeColl='' #since one or other of hours>24, minutes>59 are true, set timeColl to '', next if not true, winMain.update will send ''
                print('timeColl in if loop:',timeColl)
        print('timeColl is numbers? ',gotNums)
        print('time collected =',timeColl)
        if gotNumsLenOK==False: #if not all #s, set timeColl to '' so that winMain.update will clear the field
                            # user will then have to enter a time rather than possibly not updating.
            timeColl=''
            print('in gotNums loop, timecoll: ',timeColl)
        winMain['-COLLECTION_TIME-'].update(str(timeColl)) #update main window with time (or clear it if timeColl not numeric)
        
    if AutoProp==False: #don't clear well # - could be different FOV in same well
        winMain['-STACK_FILENAME-'].update('')
        winMain['-COLLECTION_TIME-'].update('')
               
    namesOK=fileNameCheck(folderList) #go to folder naming convention UI, get back 1 (good) or 0 (bad)


        
    return


def validate(theDate):
    try:
        datetime.datetime.strptime(theDate, "%Y-%m-%d")
    except ValueError:
        theCheck = 'false'
    else:
        theCheck = 'true'  
    return theCheck


def fileNameCheck(folderPath):
    pth=Path(folderPath)
    print('path from within fileNameCheck:'+str(pth))
    print('------------------------\nList of Files in path:')
    fileList=[]
    
    for file in pth.iterdir():
        print(file)
        fileList.append(file)
    global fileQty
    fileQty=len(fileList)
    print('# of files found:' , fileQty)
    
    captureOK=1
    namesOK=1 # 1=Good, 0=bad
    print('Status before reading tif list: captureOK: ',captureOK,' namesOK: ',namesOK)
    tifList=[]
    for file in pth.rglob('*.tif'):
        fileStr=str(file) #nix WindowsPath from each item
        tifList.append(fileStr)
    print('---------------------\nlist of tif files with baggage:\n'+str(tifList))
    tifListStr=str(tifList)
    tifListStr=tifListStr.replace('[','').replace(']','') #nix brackets
    tifListStr=tifListStr.strip("'") #nix single quotes
    tifListStr=tifListStr.replace(r'\\','/')
    print('---------------------\nlist of tif files:\n'+str(tifListStr))
    
    global tifQty
    tifQty=len(tifList)
    print('tifQty global var (len of tiflist) =',tifQty)
    
    nameList=[] #Create a list of just the filenames (without the paths)
    global badTifs
    badTifs=0
    for item in tifList:
        pathAndName=item.rsplit('\\',1)
        print('path and name, separated',pathAndName)
        name=pathAndName[-1]
        print('name: ',name)
        nameList.append(name)
        print('0-7 of name: ',name[0:8])
        if name[0:8] != 'Capture_':
            print('file',name,'does not start with Capture_')
            badTifs += 1
            namesOK=0
        
                
    print('-------------------------\nlist of names: ',nameList)

    #    if fileNameToCheck[0:7] != "Capture_":
    #        namesOK=0    
    notTifQty=fileQty-tifQty
    print('Status after reading tif list: captureOK: ',captureOK,' namesOK: ',namesOK)
    print('---------------------\n#files: ',fileQty,'#tifs: ', tifQty,'notTifs: ',notTifQty)    
    

    print('number of tif files:',len(tifList),tifQty)
    if len(tifList)==0:
        sg.Popup('No .tif files present.\nOK to save metadata.\n \nUploader will not process this folder without tifs.')
        
    # print('=====================\nfiles in the list:'+str(fileList))
        
    # fileList2=[e for e in pth.iterdir() if e.is_file()]
    # print('---------------------------------\nfiles via is_file:\n'+str(fileList2))
    
    nameCheckGood=1 # 0 = bad, 1 = good
    print('nameCheckStatus from within def: '+str(nameCheckGood))

    if namesOK==0:
        layoutFiles=[
            [sg.T('Warning', text_color='OrangeRed2', font=('Any',13,'bold'))],
            #[sg.T(str(badTifs)+' of '+str(tifQty)+' tif files in folder '+str(pth)+' do not conform to the naming convention:')],
            [sg.T(str(badTifs)+' of '+str(tifQty)+' tif files in folder'),
              sg.T(str(pth), font=('Any',10,'italic'),pad=(0,0),text_color='orange'),
              sg.T('do not conform to the naming convention:')],
            [sg.T('   files must start with "Capture_" and have an incrementing integer,')],
            [sg.T('   eg Capture_0001.tif, Capture0002.tif.\n')],
            [sg.T('Details:', font=('Any',11,'italic'))],
            [sg.T('  Beginning '+'"'+'Capture_'+'"'+': Not OK')],
            [sg.T('  Trailing Integers: Not yet checked\n')],
            [sg.T('Uploader checks for leading zeros. First digit of the integer must be 0 for all files. \nIf you only had 9 files, you could start with 00 and go through 09, but would fail at 10.')],
            [sg.T('with 3 digits you could have 99 files. 4 digits 999, etc.')],
            [sg.T('So, use a # of digits that is one larger than the decimal places needed.\n')],
            [sg.T('They must be renamed before using the upload tool.\nIn the future, I will offer to rename for you.',font=('Any',13,'bold italic'),text_color='coral1')]
            ]
        winFiles=sg.Window(title='File Naming Error',layout=layoutFiles,modal=True)

    # if nameCheckGood==0:
    #     layoutFiles=[
    #         [sg.T('Warning', text_color='OrangeRed2', font=('Any',13,'bold'))],
    #         [sg.T(str(notTifQty)+' of '+str(fileQty)+' files in folder'+str(pth)+' do not conform to the naming convention:')],
    #         [sg.T('   files must start with "Capture_" and have an incrementing integer,')],
    #         [sg.T('   eg Capture_0001.tif, Capture0002.tif.\n')],
    #         [sg.T('Details:', font=('Any',11,'italic'))],
    #         [sg.T('  Beginning '+'"'+'Capture_'+'"'+': OK')],
    #         [sg.T('  Trailing Integers: OK\n')],
    #         [sg.T('Uploader checks for leading zeros. If you only had 9 files, you could start with 00 and go through 09, but would fail at 10.')],
    #         [sg.T('with 3 digits you could have 99 files. 4 digits 999, etc.')],
    #         [sg.T('So, use a # of digits that is one larger than the decimal places needed.\n')],
    #         [sg.T('They must be renamed before using the upload tool.',font=('Any',13,'bold italic'),text_color='coral1')]
    #         ]
    #     winFiles=sg.Window(title='File Naming Error',layout=layoutFiles)
    
        while True:
            event,values=winFiles.read()
            if event in (sg.WIN_CLOSED, 'Cancel'):
                break
    
    return nameCheckGood

# def numberOfItems(values):
#     numInValDict=len(savedValDict)
#     numInValues=len(values)
#     print('\nNumber of items in savedValDict = ',numInValDict)
#     print('\nNumber of items in values = ',numInValues)
#     # Establish QTY empty next, return that too. Consider doing this
#     return numInValDict,numInValues

def clearConsumable():
    winMain['-SLIDE_ID-'].update("")
    winMain['-MFG_DATE-'].update("")
    winMain['-SAMPLE_MAKER-'].update("")
    winMain['-SUBSTRATE_MATERIAL-'].update("")
    winMain['-SURFACE_CHEMISTRY-'].update("")
    return

def clearSampleInfo():
    winMain['-PROTOCOL_TYPE-'].update("")
    winMain['-ASSAY_TYPE-'].update("")
    winMain['-CAPTURE_MOLECULE-'].update("")
    winMain['-CAP_LOT_NUMBER-'].update("")
    winMain['-CAPTURE_MOLECULE_CONCENTRATION-'].update("")
    winMain['-CAPTURE_MOLECULE_VOLUME-'].update("")
    winMain['-BLOCKING_REAGENT-'].update("")
    winMain['-STANDARD_PN-'].update("")
    winMain['-STANDARD_LOT_NO-'].update("")
    winMain['-SAMPLE_DILUENT-'].update("")
    winMain['-SAMPLE_DILUENT_VENDOR-'].update("")
    winMain['-SAMPLE_DILUENT_LOT_NO-'].update("")
    winMain['-BUFFER-'].update("")
    winMain['-SALT_CONCENTRATION-'].update("")
    winMain['-ANALYTE_VOLUME-'].update("")
    winMain['-BUFFER_OSS_VOLUME(uL)-'].update("")
    winMain['-IMAGING_SOLUTION_VOLUME(uL)-'].update("")
    winMain['-DIL_FACTOR-'].update("tbc_")
    winMain['-PERCENT_MATRIX-'].update("tbc")
    winMain['-INCUBATION_START_TIME-'].update("")
    winMain['-INCUBATION_TIME-'].update("")
    return

def clearDetectionMolecule():
    winMain['-DETECTION_MOLECULE_ID-'].update("")
    winMain['-DETECTION_MOLECULE_LOT_NUMBER(MFG_DATE)-'].update("")
    winMain['-DETECTION_MOLECULE_CONCENTRATION-'].update("")
    winMain['-LABEL_RATIO-'].update("")
    winMain['-DETECTION_FLUOROPHORE-'].update("")    
    return

def saveConsumableSampleDetection():
    temporaryDict=values
    keysToExtract=['-SLIDE_ID-','-MFG_DATE-','-SAMPLE_MAKER-','-SUBSTRATE_MATERIAL-','-SURFACE_CHEMISTRY-',
                   '-PROTOCOL_TYPE-','-ASSAY_TYPE-','-CAPTURE_MOLECULE-','-CAP_LOT_NUMBER-','-CAPTURE_MOLECULE_CONCENTRATION-','-CAPTURE_MOLECULE_VOLUME-','-BLOCKING_REAGENT-',
                   '-STANDARD_PN-','-STANDARD_LOT_NO-','-SAMPLE_DILUENT-','-SAMPLE_DILUENT_VENDOR-','-SAMPLE_DILUENT_LOT_NO-',
                   '-BUFFER-','-SALT_CONCENTRATION-','-ANALYTE_VOLUME-','-BUFFER_OSS_VOLUME(uL)-','-IMAGING_SOLUTION_VOLUME(uL)-',
                   '-INCUBATION_START_TIME-','-INCUBATION_TIME-',
                   '-DETECTION_MOLECULE_ID-','-DETECTION_MOLECULE_LOT_NUMBER(MFG_DATE)-','-DETECTION_MOLECULE_CONCENTRATION-','-LABEL_RATIO-','-DETECTION_FLUOROPHORE-']
    subsetValues={key: temporaryDict[key] for key in keysToExtract}
    # convert to string in order to remove { and } with replace if needed:
    #  subsetValuesStr=str(subsetValues)
    #  subsetValuesStr=subsetValuesStr.replace('{','').replace('}','')
    print('\n--------------------------\nIn saveConsumableSampleDetection...\nwhat will be extracted:\n',subsetValues)
    layoutSave=[
        [sg.T('Provide path and name for saved values')],
        [sg.I(key='-CONS_SAMPLE_DET_SAVE-',size=(65,1),enable_events=True),sg.SaveAs(target='-CONS_SAMPLE_DET_SAVE-',enable_events=True)]
        #sg.FolderBrowse(target='-FILE_LOCATION-',enable_events=True)
        ]
    winSave=sg.Window('File Save Dialog',layoutSave)
    while True: # Event Loop for getting save info
        event,vals3=winSave.Read()
        if event == '-CONS_SAMPLE_DET_SAVE-':
            print('in save of saveConsumableSampleDetection')
            saveTo=vals3['-CONS_SAMPLE_DET_SAVE-']
            
        if event is sg.WIN_CLOSED or event == None:
            break
    
    with open(saveTo,'wt') as sv:
        sv.write(str(subsetValues))
        sv.close()
    # sg.popup('file temptest.txt saved where the python program is.')
    return

def loadConsumableSampleDetection():    
    import ast
    layoutLoad=[
        [sg.T('Provide path and name for the file containing \nthe values you are loading')],
        [sg.I(key='-CONS_SAMPLE_DET_LOAD-',size=(65,1),enable_events=True),sg.FileBrowse(target='-CONS_SAMPLE_DET_LOAD-',enable_events=True)]
        #sg.FolderBrowse(target='-FILE_LOCATION-',enable_events=True)
        ]
    winLoad=sg.Window('File Load Dialog',layoutLoad)
    while True: # Event Loop for getting load file/path info
        event,vals4=winLoad.Read()
        if event == '-CONS_SAMPLE_DET_LOAD-':
            print('in load of saveConsumableSampleDetection')
            loadFrom=vals4['-CONS_SAMPLE_DET_LOAD-']
            
        if event is sg.WIN_CLOSED or event == None:
            break

    try:
        with open(loadFrom,'r') as bill:
            savedConsSampleDetStr=bill.read()
            
            # uncomment to get info on what's loaded from file - values and type
            #  print('savedConsSempleDetStr using f.read from temptest.txt:\n'+savedConsSampleDetStr+'\ntype: ',type(savedConsSampleDetStr))
            
            savedConsSampleDetDict=ast.literal_eval(savedConsSampleDetStr)
            # uncomment next 2 for debug purpose if have type issues
            #  print('\nsavedConsSampleDetDict type: ',type(savedConsSampleDetDict))
            #  print('value of sample ID: ',savedConsSampleDetDict.get('-SLIDE_ID-'))
            
            winMain['-SLIDE_ID-'].update(savedConsSampleDetDict.get('-SLIDE_ID-'))
            winMain['-MFG_DATE-'].update(savedConsSampleDetDict.get('-MFG_DATE-'))
            winMain['-SAMPLE_MAKER-'].update(savedConsSampleDetDict.get('-SAMPLE_MAKER-'))
            winMain['-SUBSTRATE_MATERIAL-'].update(savedConsSampleDetDict.get('-SUBSTRATE_MATERIAL-'))
            winMain['-SURFACE_CHEMISTRY-'].update(savedConsSampleDetDict.get('-SURFACE_CHEMISTRY-'))            
            
            winMain['-PROTOCOL_TYPE-'].update(savedConsSampleDetDict.get('-PROTOCOL_TYPE-'))
            winMain['-ASSAY_TYPE-'].update(savedConsSampleDetDict.get('-ASSAY_TYPE-'))
            winMain['-CAPTURE_MOLECULE-'].update(savedConsSampleDetDict.get('-CAPTURE_MOLECULE-'))
            winMain['-CAP_LOT_NUMBER-'].update(savedConsSampleDetDict.get('-CAP_LOT_NUMBER-'))
            winMain['-CAPTURE_MOLECULE_CONCENTRATION-'].update(savedConsSampleDetDict.get('-CAPTURE_MOLECULE_CONCENTRATION-'))
            winMain['-CAPTURE_MOLECULE_VOLUME-'].update(savedConsSampleDetDict.get('-CAPTURE_MOLECULE_VOLUME-'))
            winMain['-BLOCKING_REAGENT-'].update(savedConsSampleDetDict.get('-BLOCKING_REAGENT-'))
            winMain['-STANDARD_PN-'].update(savedConsSampleDetDict.get('-STANDARD_PN-'))
            winMain['-STANDARD_LOT_NO-'].update(savedConsSampleDetDict.get('-STANDARD_LOT_NO-'))
            winMain['-SAMPLE_DILUENT-'].update(savedConsSampleDetDict.get('-SAMPLE_DILUENT-'))
            winMain['-SAMPLE_DILUENT_VENDOR-'].update(savedConsSampleDetDict.get('-SAMPLE_DILUENT_VENDOR-'))
            winMain['-SAMPLE_DILUENT_LOT_NO-'].update(savedConsSampleDetDict.get('-SAMPLE_DILUENT_LOT_NO-'))
            winMain['-BUFFER-'].update(savedConsSampleDetDict.get('-BUFFER-'))
            winMain['-SALT_CONCENTRATION-'].update(savedConsSampleDetDict.get('-SALT_CONCENTRATION-'))
            winMain['-ANALYTE_VOLUME-'].update(savedConsSampleDetDict.get('-ANALYTE_VOLUME-'))
            winMain['-BUFFER_OSS_VOLUME(uL)-'].update(savedConsSampleDetDict.get('-BUFFER_OSS_VOLUME(uL)-'))
            if str(savedConsSampleDetDict['-ANALYTE_VOLUME-'])=="" or savedConsSampleDetDict['-ANALYTE_VOLUME-']=="Other" or str(savedConsSampleDetDict['-BUFFER_OSS_VOLUME(uL)-'])=="" or savedConsSampleDetDict['-BUFFER_OSS_VOLUME(uL)-']=="Other":
                winMain['-DIL_FACTOR-'].update('tbc')
                print('\n--------\nin loadConsumableSampleDetection\none of sample dil vol or buffer OSS vol is empty, setting dil factor to tbc')
                winMain['-PERCENT_MATRIX-'].update('tbc')
            if savedConsSampleDetDict['-ANALYTE_VOLUME-']!="" and str(savedConsSampleDetDict['-ANALYTE_VOLUME-'])!="Other" and savedConsSampleDetDict['-BUFFER_OSS_VOLUME(uL)-']!="" and savedConsSampleDetDict['-BUFFER_OSS_VOLUME(uL)-']!="Other":
                print('\n--------\nin loadConsumableSampleDetection\sample dil vol and buffer OSS vol not empty, calculating dil factor')
                winMain['-DIL_FACTOR-'].update((int(savedConsSampleDetDict['-ANALYTE_VOLUME-'])+int(savedConsSampleDetDict['-BUFFER_OSS_VOLUME(uL)-']))/int(savedConsSampleDetDict['-ANALYTE_VOLUME-']))
                dilFactor=float((int(savedConsSampleDetDict['-ANALYTE_VOLUME-'])+int(savedConsSampleDetDict['-BUFFER_OSS_VOLUME(uL)-']))/int(savedConsSampleDetDict['-ANALYTE_VOLUME-']))
                print('dilFactor = ',dilFactor)
                winMain['-PERCENT_MATRIX-'].update(100*(1/dilFactor))
            winMain['-IMAGING_SOLUTION_VOLUME(uL)-'].update(savedConsSampleDetDict.get('-IMAGING_SOLUTION_VOLUME(uL)-'))            
            winMain['-INCUBATION_START_TIME-'].update(savedConsSampleDetDict.get('-INCUBATION_START_TIME-'))
            winMain['-INCUBATION_TIME-'].update(savedConsSampleDetDict.get('-INCUBATION_TIME-'))

            winMain['-DETECTION_MOLECULE_ID-'].update(savedConsSampleDetDict.get('-DETECTION_MOLECULE_ID-'))
            winMain['-DETECTION_MOLECULE_LOT_NUMBER(MFG_DATE)-'].update(savedConsSampleDetDict.get('-DETECTION_MOLECULE_LOT_NUMBER(MFG_DATE)-'))
            winMain['-DETECTION_MOLECULE_CONCENTRATION-'].update(savedConsSampleDetDict.get('-DETECTION_MOLECULE_CONCENTRATION-'))
            winMain['-LABEL_RATIO-'].update(savedConsSampleDetDict.get('-LABEL_RATIO-'))
            winMain['-DETECTION_FLUOROPHORE-'].update(savedConsSampleDetDict.get('-DETECTION_FLUOROPHORE-'))            

        # sg.popup('loaded values into fields')

    except FileNotFoundError:
        print('aint got no file to load')
        sg.popup('did not find a file, nothing loaded')
    #    savedValDict={"-USER-": "", "-COLLECTION_DATE-": "", "-COLLECTION_TIME-": "", "-LOCATION-": "", "-EXPOSURE_TIME(SEC)-": "", "-STACK_FILENAME-": "", "-SLIDE_ID-": "", "-MFG_DATE-": "", "-SAMPLE_MAKER-": "", "-SUBSTRATE_MATERIAL-": "", "-SURFACE_CHEMISTRY-": "", "-WELL_NUMBER-": "", "-PROTOCOL_TYPE-": "", "-ASSAY_TYPE-": "", "-CAPTURE_MOLECULE-": "", "-CAPTURE_MOLECULE_CONCENTRATION-": "", "-CAPTURE_MOLECULE_VOLUME-": "", "-ANALYTE_MOLECULE-": "", "-ANALYTE_CONCENTRATION-": "", "-ANALYTE_VOLUME-": "", "-BUFFER-": "", "-BLOCKING_REAGENT-": "", "-SAMPLE_DILUENT-": "", "-SALT_CONCENTRATION-": "", "-INCUBATION_START_TIME-": "", "-INCUBATION_TIME-": "", "-DETECTION_MOLECULE_ID-": "", "-DETECTION_MOLECULE_LOT_NUMBER(MFG_DATE)-": "", "-DETECTION_MOLECULE_CONCENTRATION-": "", "-LABEL_RATIO-": "", "-IMAGING_SOLUTION_VOLUME(uL)-": "", "-FILE_LOCATION-": "", "Browse": "", "-INSTRUMENT_NAME-": "", "-INSTRUMENT_SN/ID-": "", "-CRISP_ON-": True, "-OIL_BETWEEN_SAMPLE_AND_LENS-": True, "-LASER_POWER_SOURCE(mW)-": "", "-LASER_POWER_SAMPLE(mW)-": "", "-ILLUMINATION_MICROMETER-": "", "-LENS_TEMPERATURE-": "", "-LENS_NUMERICAL_APERTURE-": "", "-LENS_MAGNIFICATION-": "", "-CAMERA-": "", "-RESOLUTION_MAX-": "", "-RESOLUTION_USED-": "", "-BINNING-": "", "-MOVIE_TIME(SEC)-": "", "-CAMERA_OFFSET-": "", "-DARK_FRAME_VALUE-": "", "-CAMERA_GAIN-": ""}
    return

# Functions for UI elements, esp. those that are re-used, like red * and green + and the "Today" button
def Text(text,Tsize):
    return sg.Text(text,size=(Tsize,1))

def ast(astSize):
    return sg.T('* ',size=(astSize,1),font=('Helvetica',12),text_color='red',pad=(0,0))

def plus():
    return sg.Text('i',text_color='chartreuse2')

def todayButton(key,target):
    return sg.B(button_text='',image_data=todayButtonGraphic,button_color=(sg.theme_background_color(),sg.theme_background_color()),
          border_width=0,key=key,target=target,enable_events=True)

todayButtonGraphic=b'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'
consumableButtonGraphic=b'iVBORw0KGgoAAAANSUhEUgAAABkAAAASCAYAAACuLnWgAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAB3RJTUUH5AoUEyIQcK9gMAAABGdJREFUOI2tlMtPVHcUxz937p07jA7IUxglDMxLC4oCBYuiYtGC+KgxbdN03bjsun9Ad023pqu6aKLVRDQVYxQVpIBFbVVEKPXFUzMOA8yLuXOfXUzBTEnTTc/y9znffE/OOb8jfDN0zVqYfYNpGBiaDoLA/xGCAILNxuatAaTXE8/RVY3pJ2Osz9+AJMuoqRQ2UUSUJFRFwbIsbDYb9pwctHQam82GaLejplIZJorIOTnvdHY7SiJJKhZHlCQkQRCIzMzR+dUp7A4Hj3v6UOIJTMPAHfQRbG7EMk20tMro7X4SC0tYpklJVQXvtXwAgJpSGO39heRiFMs0KfN78TfVcf30DwiiDSmdTOHMdeEqLKD3zFncAR/b2/ahKWme3LqDrqrUtLYw3HWFwk1uqvfvxtB0RnsHGOnpY2dHG8Nd3RR7yqlpbUFXVZ72DTLScwdnrgssC+HL099aK1UvL8XY3rYvq7dDFy6TV1yErqrs7GjLYsNd3Yh2CdnppPbg/izWe+YsoReT7Gj/ENvKYzwcobw6uGaAGysreH7/IZ4dNWtYmb+KFw8e4aldy0q9lUTfhhEl8Z2JJMskl2JrkpejMfJKiojPL6xhycUoecVFJBYW17JoFNnpxDTMjImualTUVjPeP5QlmHw0Smw+QtOJTiaG7hENhVfZ3B/PCE/N0Pzpx4z1DxELR1bZ7NgE8XAEd8CLrqlIAIamk1dcRHXrHh5eu0nu3zNQlxUajrbjzHVRe+gAIzf7cBUWYho6qXiChmPtuAry2XZgL49v3Ca3qBBD10knUzSdPMrgT11gkTFZic1bAqRiCf68ex/ZmUPj8cOZDQFKvR6UeIKndwaRZDv1Rz7CVZAPgDvgRYknGB/4FbtD5v3jHbgK8jFUDcuysk2Gu7oxdJ36zkMoiST3Ll8l2NyIp7aG367eYDkao66jDU1VeXz9Np4d2/A31nH/52uoyynqDh9EUxR+v9pDZd12HOvXZeYNIDsdzE08wzQMdn92YtXUHfAy3NUNgBJPsPeLT1bZpi1+hs5fynxUJc2ez0++0wV99P94gVg4QqmvMjN4mygSnpwhsKsha0Mc69ex0evhya1+gs2NWUyy2ymv3sJITx9bW3ZlMbvDQZm/itDLSSS7nDGxLAtBELAsi3+GZWZuk2mYa5hpmP/KLMtClKTMbQMwdQN3wMt4/92sxFg4wttXU9R3HmK8fyiriOVYnNmxCRqOtTPWN5ilSy5FCb2YYqPXg66qSFigqyobqzwsvgkxeP4SZb5K1GWF0Ksp6jra2FBawnIsxsC5i7j9XnRVI/Rykm0HWiiuKEdNKQycu0iZ34umpDOFHTnIgyvXMQ0D4dT331nTo+O4A14kWSb0coqFuTeIdolNQR+uwoJMNbLM/PQs89NzCDYBd8BHXknRKns7OU1k5jWiJOIO+sgtKmTy0Sg1rXsQvu4+Z82MjmPoOgCiZEeURCzLwtB1TMNYbcMKA9A17T+ZKEn4m+r5C89vEi5LXSUUAAAAAElFTkSuQmCC'
cloudButtonGraphic=b'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'
deleteButtonGraphic=b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAB3RJTUUH5QIFBgE7a94nFAAABEtJREFUOI2VlVuIVlUUx39r73P9LjPjzDcTjozYhUQyGIgcJ3RSk/BC5IhRYVnSQ1S+9KJCGATdxJewiz1EUJGFaDZMjQmmOaNGNSSRKZmSDZTRlM7tO983M+fs3cP55pb10ILFOZw/+8dae62zlpCaD6xrgGYDoQXF/zMrEEfQF8FBoE8AZ4HitRWhfrxGwPzHSZlO+Q89Bk6N2dMnxsx6DbSuDfQbN7uQAI6Aq0AZgyQG11E4gJYpdxRInKCtxXUUbkXPKmhUMvuHWPoVcGO1EmIEkdRNYnCNMLswh6SYgExpIkJcTihkaqjJVJOUp/QEIVRCHjNXAR6AAzgi6CTBFC1tz77Iw92nuLX5NsxQjJJUj6OYxiDPgx910r6/k9DLQinGEcEhLY4BrQBJUxS0sRgC2l56maXbt5G7fi7tnx5icUsrdjBmLBrnpqpaHuj4hPq2JcxbtpT1H3cSNMxBxUnKkLQaFbDgikAppqm1hZXbt00WxbmuntVdXSxZ3MrCsJoNnV3MWtY2qc+/azmLtjxBUjS4IjgpWBSAJgWHOY+rJ3o4vvXpmSWvrWF5Rwft3T1k7miZIZ0/sI8zu3aSy7vpdVQidpjoBBGsUthA6N31CrZcZtnuPVOEhnp0Q/0M6I8fvMfhRzehXIUf+ChrSSpaGrEoPFG4InhaU10b8P2rb3Js80bGB4eu6VlrDGdf383RRzYR+A5hGOAiuKJwRSETYAfwK2BXBF87ZB24fLSb0cHBfwVfPtaDHocw8CpQwRPBZap4OJWPvgiBUqiBEYL5C1l1rIfc3KZrwMpxuHPvXuY9tImkPyIU8CvnvWldgasEXwm+VjA0THJLM3cf+ozaG+ZdA50wx3NZ8e47FDY/RvmvIoFKoZ6aDkbSqyiVMc2LWPtFN4WmOTNA53Zs58s1K0lK0RRcYPXbb1H75BbscBFfqZkROyIEInjaoTEaJPytbwb0wnM7uLRzJ1cPf87p++4lHh6e1CSKaOz/ldBx8CtRqwmwJ4KvFJlMCL/8zLerVjDU+w0AF5/ZSt8Lz5Mv1FDdWMfwkSOc2XAPSRSRRBHfta9hoOMguao8vlL4Kp24DmA9UYRKYYyFqmqS4SEubt5I/vYW/tz/IVUNtRP/En5DgdLJHs7fvw4LlE/2kK8vgE0zF7GoChitIa8Vsa1M43wVtv8Phg/sI1tdM3P+WvBr6xg9dQKAXF0BrAWBQAmIZRSsA4ydK5VZkgupcz0MICIQ+sisKhBJx+LkqLdYC2RDLDaFWjup9Q4OUTIYB/jpQmncHL5yRdV4PjmtyCpNVmtyE0+tyWmFgzBiEkaShGLFR0zqUWIYGh/nbGkMA5cc4Ove2OyZVTZPNcWjBEqRUYqM0mSVkBFNViuySqGBorUUk4TIGCJjKBpDZA1lYxhIEo6Pmq8G4P2J/FxgdQ4WmPRdkmlr7p87bvr+0xVZwBThd6ALuPw3vFZ/kfpiZMMAAAAASUVORK5CYII='
saveIconGraphic=b'iVBORw0KGgoAAAANSUhEUgAAABIAAAATCAMAAACqTK3AAAADAFBMVEUAAAAAAFUAAKoAAP8AJAAAJFUAJKoAJP8ASQAASVUASaoASf8AbQAAbVUAbaoAbf8AkgAAklUAkqoAkv8AtgAAtlUAtqoAtv8A2wAA21UA26oA2/8A/wAA/1UA/6oA//8kAAAkAFUkAKokAP8kJAAkJFUkJKokJP8kSQAkSVUkSaokSf8kbQAkbVUkbaokbf8kkgAkklUkkqokkv8ktgAktlUktqoktv8k2wAk21Uk26ok2/8k/wAk/1Uk/6ok//9JAABJAFVJAKpJAP9JJABJJFVJJKpJJP9JSQBJSVVJSapJSf9JbQBJbVVJbapJbf9JkgBJklVJkqpJkv9JtgBJtlVJtqpJtv9J2wBJ21VJ26pJ2/9J/wBJ/1VJ/6pJ//9tAABtAFVtAKptAP9tJABtJFVtJKptJP9tSQBtSVVtSaptSf9tbQBtbVVtbaptbf9tkgBtklVtkqptkv9ttgBttlVttqpttv9t2wBt21Vt26pt2/9t/wBt/1Vt/6pt//+SAACSAFWSAKqSAP+SJACSJFWSJKqSJP+SSQCSSVWSSaqSSf+SbQCSbVWSbaqSbf+SkgCSklWSkqqSkv+StgCStlWStqqStv+S2wCS21WS26qS2/+S/wCS/1WS/6qS//+2AAC2AFW2AKq2AP+2JAC2JFW2JKq2JP+2SQC2SVW2Saq2Sf+2bQC2bVW2baq2bf+2kgC2klW2kqq2kv+2tgC2tlW2tqq2tv+22wC221W226q22/+2/wC2/1W2/6q2///bAADbAFXbAKrbAP/bJADbJFXbJKrbJP/bSQDbSVXbSarbSf/bbQDbbVXbbarbbf/bkgDbklXbkqrbkv/btgDbtlXbtqrbtv/b2wDb21Xb26rb2//b/wDb/1Xb/6rb////AAD/AFX/AKr/AP//JAD/JFX/JKr/JP//SQD/SVX/Sar/Sf//bQD/bVX/bar/bf//kgD/klX/kqr/kv//tgD/tlX/tqr/tv//2wD/21X/26r/2////wD//1X//6r////qm24uAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAB3RJTUUH5QIFBwETX6nl2QAAAJtJREFUGJVlj7sNwzAMRN2p0CgsNAgLFhqFo7BQ4UFcZLgLP0LswCIIAqfT0/HA6xxQiWnST9iWrKXUZKLLlraLTwjLn4sVjRvfLJgC0oUsXba/cl54g9Wd8etPuvhZMyTiZ8VDJRIaXjUTT3Yvo4Uf/teqAmily+82yVCs4ermKZLl6S+K3N6KftWO01NHct+jcgkWuyfaCv86Xy+lx/+Zmt8EAAAAAElFTkSuQmCC'
loadIconGraphic=b'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cmcvbGRmL3htcC8xLjAvIgogICAgeG1sbnM6R0lNUD0iaHR0cDovL3d3dy5naW1wLm9yZy94bXAvIgogICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iCiAgIHhtcE1NOkRvY3VtZW50SUQ9ImdpbXA6ZG9jaWQ6Z2ltcDo4MGU4NmIyMC0wNTM5LTQzMzEtYjhkMC00YjNkMjUxNmFiNmYiCiAgIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6YjhiODFjMDMtNTI4Yy00OWZkLTgxOGQtN2EzODNlYjU1YjgwIgogICB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6ZGI0MTA0ZDgtNDQyOS00MTkxLTk5ZDgtNmMyNDdiY2UyMDJhIgogICBHSU1QOkFQST0iMi4wIgogICBHSU1QOlBsYXRmb3JtPSJXaW5kb3dzIgogICBHSU1QOlRpbWVTdGFtcD0iMTYxMjUwOTYwNjAyOTgyMSIKICAgR0lNUDpWZXJzaW9uPSIyLjEwLjIyIgogICBkYzpGb3JtYXQ9ImltYWdlL3BuZyIKICAgdGlmZjpPcmllbnRhdGlvbj0iMSIKICAgeG1wOkNyZWF0b3JUb29sPSJHSU1QIDIuMTAiPgogICA8aXB0Y0V4dDpMb2NhdGlvbkNyZWF0ZWQ+CiAgICA8cmRmOkJhZy8+CiAgIDwvaXB0Y0V4dDpMb2NhdGlvbkNyZWF0ZWQ+CiAgIDxpcHRjRXh0OkxvY2F0aW9uU2hvd24+CiAgICA8cmRmOkJhZy8+CiAgIDwvaXB0Y0V4dDpMb2NhdGlvblNob3duPgogICA8aXB0Y0V4dDpBcnR3b3JrT3JPYmplY3Q+CiAgICA8cmRmOkJhZy8+CiAgIDwvaXB0Y0V4dDpBcnR3b3JrT3JPYmplY3Q+CiAgIDxpcHRjRXh0OlJlZ2lzdHJ5SWQ+CiAgICA8cmRmOkJhZy8+CiAgIDwvaXB0Y0V4dDpSZWdpc3RyeUlkPgogICA8eG1wTU06SGlzdG9yeT4KICAgIDxyZGY6U2VxPgogICAgIDxyZGY6bGkKICAgICAgc3RFdnQ6YWN0aW9uPSJzYXZlZCIKICAgICAgc3RFdnQ6Y2hhbmdlZD0iLyIKICAgICAgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDphNDAyNDNjZC01ZGUxLTRjZGMtYjI1NC1iYzdiMjk4NGZmZTciCiAgICAgIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkdpbXAgMi4xMCAoV2luZG93cykiCiAgICAgIHN0RXZ0OndoZW49IjIwMjEtMDItMDRUMjM6MjA6MDYiLz4KICAgIDwvcmRmOlNlcT4KICAgPC94bXBNTTpIaXN0b3J5PgogICA8cGx1czpJbWFnZVN1cHBsaWVyPgogICAgPHJkZjpTZXEvPgogICA8L3BsdXM6SW1hZ2VTdXBwbGllcj4KICAgPHBsdXM6SW1hZ2VDcmVhdG9yPgogICAgPHJkZjpTZXEvPgogICA8L3BsdXM6SW1hZ2VDcmVhdG9yPgogICA8cGx1czpDb3B5cmlnaHRPd25lcj4KICAgIDxyZGY6U2VxLz4KICAgPC9wbHVzOkNvcHlyaWdodE93bmVyPgogICA8cGx1czpMaWNlbnNvcj4KICAgIDxyZGY6U2VxLz4KICAgPC9wbHVzOkxpY2Vuc29yPgogIDwvcmRmOkRlc2NyaXB0aW9uPgogPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSJ3Ij8+reMI6AAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+UCBQcUBgXB5yYAAAJrSURBVEjHtZZNSFRRFMd/943TOONkMzomTRlREn1QbVrYoogWBgktIkxcRRQkJOFGhCJhQE2cRS0UAoNWSaG1ahH2gYQLFxEEtQhcKYJaEI2O4jjv32ZmGnWcMWfmDxfefe/c+zvnvHvPvUgykg5IeqrsGpF0lEIpAY1pa5qSFCwEtwS4DZTYEr+WlpiKRMCYdM/Y6/VSXVYGsA84BswUAlwDEI3FqG9tzWhUUxVgpLsHp2UB3JO0Apgs844bY1ZzgZtzeTc1/5Pfy8tUeTwA54GxHEO+SnoP9BtjJjcDF0MnE80H3MhkYCQJYGFlhbMtLZvO5POWMfCgE3dJbl93uVz4S0sBIsAZY8y3bUf8e2GR5vb2Ldn2hzqpC9ZgGbMTOA1sAFvFyHNbqItEIrMurqyyLIvhUMN/gZeoTN+SwXWF54cxJp4VPNTXx263mwq3O58EdCdaUh8ktWwKfhEOc9jvL8afuAB8zAh+GQ5Tm4DaEtORCI873qwpaNvRzVA9RyorAYIbwE+6uqj1+zFA3La5e32IyYn8w6ytg/3l5cmuvWZVH9xTzYlAAJOI9MvcXMGgvYONeJxOAAFNqQISi8dZlVIF4vPsLPfPvcsb6nDBs4krBP4t0FHgcirVTocDZ+J5Phqlt3E0xzmwNeijsUvp0LfAVWPMcipi0qB3Gl7xZ8bkHW14/CLHA4FkdxE4lTw0LOB58kvctnnY9rog0IExD4d8vmR3AWhMP6mMpB6gA2A6EmEuGiXffVPhchH0etnhcCRf3TLGDK6/+jRJiqs4siUNS3JnunMZSdckfS8w9JOkekmuTFn5C8SV0dHJYPpAAAAAAElFTkSuQmCC'

"""
  ***************************************************************************
  *                   End of functions, beginning of UI                     *
  ***************************************************************************
"""
# A note on text colors - RGB or Use this ref: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

SYMBOL_UP =    '▲'
SYMBOL_DOWN =  '▼'

#Long Text Strings - ToolTips and last one's the Status Message
LocTip='For now just Hercules, Haifa, aLight. Later betas, etc'
ExpNameTip='Overall experiment goal, can use for multiple FOVs, wells, etc'
UniqueTifTip='if a \\ or a / is entered, it will be replaced with a - to prevent errors'
WellTip='row x col (num x num), eg 1,1'
AssayConcTip='final concentration of target analyte in well'

MfgDateTip='Date consumable was made'
VolLoadedTip='Volume put into consumable well'
IncStartTip='Must use format listed'

DetLotNoTip='Mfg Date, YYYYmmDD'
LabRTip='Label to Ab, eg 1:1'

SampleVolTip='volume of the analyte/sample matrix added to the buffer/OSS diluent'
BufferOSS_Tip='Oxygen Scavenger System added to matrix'
# sampleVolume=0
# OSS_Vol=0
# sampleVol=1
# dilFactor=10000000

InstSNTip='Not yet - only when >1 of same inst'

TweakTip='This brings up a UI showing all children of parent\n     of last chosen folder, highlighting last used. \nUseful for long lists. \nAlso allows you to type a string and search'
AutoPopTip="If this is checked, ""'"+"Unique Tif Stack Name""'"+"\n and ""'"+"Collection Time""'"+" will populate \nfrom your chosen folder name"

LasPowSrcTip='Laser setting in software'
LasPowSampTip='Meas. with laser pointed straight up'
IllMicrometerTip='stand-in for TIR angle \n(Herc-Haifa small FOV only)'
LensTempTip='Hercules/Haifa: From ASI Software'
LensNATip='Hercules/Haifa: currently CFI160 from ASI, NA 1.49'
LensMagTip='Hercules/Haifa: currently CFI160 from ASI, 60X'

CamTip='ATM QHY 183 for Herc and Haifa, Photometrics et al aLight'
ResMaxTip='5472x3648 = recommended max in Sony spec'
OtherText="Undefined"

SubmitTip='You must do this to initiate store data about the experiment to save the data for posterity'
StatusMsg="User Input"
CloudTip='This will open the upload tool\n...used to upload tifs with metadata this program captures\n...which will be stacked for you and available in the analysis site.'

def collapse(layout, key):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key))

sg.theme('Dark')


# Optical Info section, collapsible, right column, 2nd sub section in Instrument Info section
# Tip:  button_color='yellow on green')
section1 = [
            [sg.Text('    Oil betw samp & lens?',size=(23,1)),sg.Checkbox('y/n',default=savedValDict['-OIL_BETWEEN_SAMPLE_AND_LENS-'],key='-OIL_BETWEEN_SAMPLE_AND_LENS-')],
            [sg.Text('    Laser Power (source (mW))',size=(23,1),tooltip=LasPowSrcTip),sg.InputText(default_text=savedValDict['-LASER_POWER_SOURCE(mW)-'],size=(25,1),tooltip=LasPowSrcTip,key='-LASER_POWER_SOURCE(mW)-'),plus()],
            [sg.Text('    Laser Power (sample (mW))',size=(23,1),tooltip=LasPowSampTip),sg.InputText(default_text=savedValDict['-LASER_POWER_SAMPLE(mW)-'],size=(25,1),tooltip=LasPowSampTip,key='-LASER_POWER_SAMPLE(mW)-'),plus()],
            [sg.Text('    Illumination Micrometer',size=(23,1),tooltip=IllMicrometerTip),sg.InputText(default_text=savedValDict['-ILLUMINATION_MICROMETER-'],size=(25,1),tooltip=IllMicrometerTip,key='-ILLUMINATION_MICROMETER-'),plus()],
            [sg.Text('    Lens Temp',size=(23,1),tooltip=LensTempTip),sg.InputCombo(lensTempList,default_value=savedValDict['-LENS_TEMPERATURE-'],size=(25,1),tooltip=LensTempTip,key='-LENS_TEMPERATURE-'),plus()],
            [sg.Text('    Lens NA',size=(23,1),tooltip=LensNATip),sg.InputCombo(lensNAList,default_value=savedValDict['-LENS_NUMERICAL_APERTURE-'],size=(25,1),tooltip=LensNATip,key='-LENS_NUMERICAL_APERTURE-'),plus()], #1.49 Herc/Haifa ASI
            [sg.Text('    Lens Magnification',size=(23,1),tooltip=LensMagTip),sg.InputCombo(lensMagList,default_value=savedValDict['-LENS_MAGNIFICATION-'],size=(25,1),tooltip=LensMagTip,key='-LENS_MAGNIFICATION-'),plus()], # 60X Herc/Haifa ASI
           ]

            # Note physical FOV = pixel #px*(px size/mag) for x and y. With 183 that's 110.88 µm or .11088 mm

# Sample Info section - collapsible, left column, 3rd subsection
section2 = [[sg.Frame(layout=[
             
             [Text(' Protocol Type',12),sg.InputCombo((washProtocolList),default_value=savedValDict['-PROTOCOL_TYPE-'],size=(13,1),key='-PROTOCOL_TYPE-'),
              Text('  Assay Type',11),sg.InputCombo((assayList),default_value=savedValDict['-ASSAY_TYPE-'],size=(11,1),key='-ASSAY_TYPE-')],
             [sg.Text(' Cap Molecule:',font=("Helvetica",10,'italic'),text_color='burlywood1'),sg.T("ID"),
               sg.InputCombo((capIDList),default_value=savedValDict['-CAPTURE_MOLECULE-'],size=(None,15),expand_x=True,key='-CAPTURE_MOLECULE-'),
               sg.T('       '),sg.B('',key='-CLEAR_SAMPLE_INFO-',image_data=deleteButtonGraphic,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,tooltip="Clear the Sample Info box's fields")],
             [sg.T('      Lot #'),sg.I(size=(8,1),key='-CAP_LOT_NUMBER-'),sg.Text('Conc (nM)'),
              sg.InputText(default_text=savedValDict['-CAPTURE_MOLECULE_CONCENTRATION-'],size=(7,1),key='-CAPTURE_MOLECULE_CONCENTRATION-'),
              sg.T('Volume (\u03BCL)'),sg.InputText(default_text=savedValDict['-CAPTURE_MOLECULE_VOLUME-'],size=(7,1),key='-CAPTURE_MOLECULE_VOLUME-')],
             [sg.Text(' Blocking Reagent',font=("Helvetica",10,'italic'),text_color='burlywood1'),
              sg.InputCombo((blockingReagentList),default_value='None',size=(15,1),key='-BLOCKING_REAGENT-')],   
             [sg.Text('  Standard:',font=("Helvetica",10,'italic'),text_color='burlywood1',pad=(0,0)),              
               sg.T('PN'), sg.InputCombo(standardPartNumberList,key='-STANDARD_PN-',size=(None,12),auto_size_text=True,expand_x=True),sg.T('Lot #'),
               sg.InputCombo(standardLotNumberList,auto_size_text=True,key='-STANDARD_LOT_NO-')],
             [sg.T('  Sample Matrix',font=("Helvetica",10,'italic'),text_color='burlywood1',pad=(0,0)),
              sg.InputCombo((diluentList),default_value=savedValDict['-SAMPLE_DILUENT-'],size=(12,1),key='-SAMPLE_DILUENT-'),
              sg.T('Vendor'),sg.InputCombo(sampleMatrixVendorList,size=(9,1),key='-SAMPLE_DILUENT_VENDOR-',pad=(0,0)),
              sg.T('Lot'),sg.InputCombo(sampleMatrixLotNumberList,size=(9,20),key='-SAMPLE_DILUENT_LOT_NO-',pad=(0,0))],
             [Text(' Buffer',7),sg.InputCombo((bufferList),default_value=savedValDict['-BUFFER-'],size=(13,1),key='-BUFFER-'),Text('     Salt Conc (mM)',14),
              sg.InputCombo((saltConcentrationList),default_value=savedValDict['-SALT_CONCENTRATION-'],size=(6,1),key='-SALT_CONCENTRATION-')],
             [sg.T('  Sample Vol',font=("Helvetica",10,'italic'),text_color='burlywood1',pad=(0,0)),
              sg.InputCombo(sampleVolumeList,default_value=savedValDict['-ANALYTE_VOLUME-'],tooltip=SampleVolTip,key='-ANALYTE_VOLUME-',enable_events=True),
              sg.T('  Buffer/OSS Vol (\u03BCL)',tooltip=BufferOSS_Tip),
              sg.InputCombo(bufferOSS_VolumeList,key='-BUFFER_OSS_VOLUME(uL)-',enable_events=True,tooltip=BufferOSS_Tip),plus()],
             [sg.Text('   Vol loaded/Well',tooltip=VolLoadedTip),
              sg.InputCombo(imagingSolutionVolumeList,default_value=savedValDict['-IMAGING_SOLUTION_VOLUME(uL)-'],size=(5,1),key='-IMAGING_SOLUTION_VOLUME(uL)-',tooltip=VolLoadedTip),
              plus(),sg.T('    dil Factor'),sg.T('tbc_',key='-DIL_FACTOR-',text_color='green'),sg.T('% matrix'),sg.T('tbc',key='-PERCENT_MATRIX-',text_color='green')],
             [sg.Text(' Incubation:',font=("Helvetica",10,'italic'),text_color='burlywood1'),
              sg.Text('Start (hhMM)',size=(10,1),tooltip=IncStartTip),
              sg.InputText(default_text=savedValDict['-INCUBATION_START_TIME-'],size=(10,1),tooltip=IncStartTip,key='-INCUBATION_START_TIME-'),plus(),
              Text('  Time (min)',9),sg.InputText(default_text=savedValDict['-INCUBATION_TIME-'],size=(7,1),key='-INCUBATION_TIME-')],             
            ],title=""),
           ]
          ]

# Imaging Info Section - collapsible, right column, below optical info
section3 = [
             #[sg.Text("    Imaging Info",text_color='orange')],
             [sg.Text('      Camera',size=(23,1),tooltip=CamTip),sg.InputCombo(cameraList,default_value=savedValDict['-CAMERA-'],size=(25,1),tooltip=CamTip,key='-CAMERA-'),plus()],
             [sg.Text('      Resolution (max)',size=(23,1),tooltip=ResMaxTip),sg.InputCombo(resolutionMaxList, default_value=savedValDict['-RESOLUTION_MAX-'],size=(25,1),tooltip=ResMaxTip,key='-RESOLUTION_MAX-'),plus()], # IMX183 = '5472 x 3648'
             [sg.Text('      Resolution Used (ROI)',size=(23,1)),sg.InputCombo(resolutionUsedList,default_value=savedValDict['-RESOLUTION_USED-'],size=(25,1),key='-RESOLUTION_USED-')], # Herc/Haifa using '2772x2772'
             [sg.Text('          Phsyical FOV of Herc/Haifa = .11 x .11 mm (110.88x110.88 \u03BCm)',font=("Helvetica",8,'italic'))],
             [sg.Text('      Binning',size=(23,1)),sg.InputCombo(binningList,default_value=savedValDict['-BINNING-'],size=(25,1),key='-BINNING-')],        
             #[sg.Text('      Movie Time (sec)',size=(23,1)),sg.InputCombo(('120','150','600'),default_value=savedValDict['-MOVIE_TIME(SEC)-'],size=(25,1),key='-MOVIE_TIME(SEC)-')],
             [sg.Text('      Camera Offset',size=(23,1)),sg.InputText(default_text=savedValDict['-CAMERA_OFFSET-'],size=(25,1),key='-CAMERA_OFFSET-')],
             [sg.Text('      Dark Frame Value',size=(23,1),tooltip='average pixel value of dark frame'),sg.InputText(default_text=savedValDict['-DARK_FRAME_VALUE-'],size=(25,1),tooltip='average pixel value of dark frame',key='-DARK_FRAME_VALUE-')],
             [sg.Text('      Gain',size=(23,1)),sg.InputText(default_text=savedValDict['-CAMERA_GAIN-'],size=(25,1),key='-CAMERA_GAIN-')]
            ]        
         

#----Column Definition----#   #[sg.Frame(layout=[
LeftCol=sg.Column([
    # User/Customer (Required) Box
    [sg.Frame(layout=[
        [Text('  User',5),sg.Combo((userList),default_value=savedValDict['-USER-'],readonly='true',size=(17,20),key='-USER-',enable_events=True),
         sg.Text('  Location',size=(7,1),tooltip=LocTip),sg.InputCombo((locationList),default_value=savedValDict['-LOCATION-'],readonly='true',tooltip=LocTip,size=(15,1),key='-LOCATION-'),plus()],
        [Text('  Collection Date',12),sg.Text(' (YYYYmmDD)',font=('Helvetica',8),size=(16,1)),sg.InputText(size=(17,1),key='-COLLECTION_DATE-'),todayButton('-TODAY-','-COLLECTION_DATE-')],
        [Text('  Exposure Time (sec)',16),sg.InputText(default_text=savedValDict['-EXPOSURE_TIME(SEC)-'],size=(4,1),key='-EXPOSURE_TIME(SEC)-'),
        sg.Text('              Movie Time (sec)',size=(19,1)),sg.InputCombo(('120','150','600'),default_value=savedValDict['-MOVIE_TIME(SEC)-'],size=(5,1),key='-MOVIE_TIME(SEC)-')],
        [sg.Text('  Experiment Name/Intent',size=(26,1),tooltip=ExpNameTip),sg.InputText(size=(25,1),tooltip=ExpNameTip,key='-EXPERIMENT_NAME-'),plus()],
        [Text('  Unique Tif Stack Name',26),sg.InputText(size=(25,1),key='-STACK_FILENAME-',enable_events=True,tooltip=UniqueTifTip),plus()],        
        [Text('  Collection Time',12),sg.Text('(HHMM)',font=('Helvetica',8),size=(16,1)),sg.InputText(size=(18,1),key='-COLLECTION_TIME-'),sg.B(button_text='now',key='-NOW-',target='-COLLECTION_TIME-',enable_events=True)],
        [sg.Text('  Well # (Row,col)',size=(26,1),tooltip=WellTip),sg.InputText(size=(20,1),tooltip=WellTip,key='-WELL_NUMBER-'),
         sg.B(key='-CONS_BUTTON-',target='-WELL_NUMBER-',button_text='',image_data=consumableButtonGraphic,button_color=(sg.theme_background_color(),sg.theme_background_color())),plus()],
        [sg.Text(' Analyte:',font=("Helvetica",10,'italic'),text_color='burlywood1',pad=(0,0)),
         sg.T("Target"),sg.InputCombo((analyteIDList),default_value=savedValDict['-ANALYTE_MOLECULE-'],size=(8,16),auto_size_text=True,expand_y=True,key='-ANALYTE_MOLECULE-'),
         sg.Text(' Assay Conc',pad=(0,0),tooltip=AssayConcTip), sg.T('(DNA: fM, protein: pg/mL)',font=('Any',9),pad=(0,0),tooltip=AssayConcTip),
         sg.InputText(size=(3,1),tooltip=AssayConcTip,key='-ANALYTE_CONCENTRATION-'),plus()] # to add me to make me load from saved: default_text=savedValDict['-ANALYTE_CONCENTRATION-'],
        ],title='User/Customer Info + Exp Time (Required Entries)',title_color='coral1')],
     # End Frame of User/Customer Info
    
    # Row of buttons for save, load, clear Consumable, Sample Info and Detection Molecule
    [sg.T('                                                                                     '),
     sg.B(image_data=saveIconGraphic,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='-SAVE-',
          tooltip="saves contents of Consumable, Sample Info and Detection Molecule box\n for loading by person capturing image data"),
     sg.B(image_data=loadIconGraphic,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,key='-LOAD-',
          tooltip="load a file to populate Consumable, Sample and Detection Molecule boxes"),
     sg.B('',key='-CLEAR_CONSUMABLE_SAMPLE_DETECTION-',image_data=deleteButtonGraphic,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,tooltip="Clear the Consumable, Sample Info and Detection Molecule box's fields")
     ],

    # Detection Molecule Box
    [sg.Frame(title='Detection Molecule',title_color='orange',
      layout=[
              [sg.Text('   ID'),sg.InputCombo((detectIDList),default_value=savedValDict['-DETECTION_MOLECULE_ID-'],size=(None,40),expand_x=True,key='-DETECTION_MOLECULE_ID-'),
               sg.Text('Lot #',tooltip=DetLotNoTip),plus(),sg.InputText(default_text=savedValDict['-DETECTION_MOLECULE_LOT_NUMBER(MFG_DATE)-'],size=(8,1),tooltip=DetLotNoTip,key='-DETECTION_MOLECULE_LOT_NUMBER(MFG_DATE)-'),
               sg.T('   '),sg.B('',key='-CLEAR_DETECTION-',image_data=deleteButtonGraphic,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,tooltip="Clear the Detection Molecule box's fields")],
              [sg.Text('   Conc (nM)'),sg.InputText(default_text=savedValDict['-DETECTION_MOLECULE_CONCENTRATION-'],size=(5,1),key='-DETECTION_MOLECULE_CONCENTRATION-'),
               sg.Text('   Label Ratio',tooltip=LabRTip),sg.InputText(default_text=savedValDict['-LABEL_RATIO-'],size=(5,1),tooltip=LabRTip,key='-LABEL_RATIO-'),plus(),
               sg.T('Fluor'),sg.InputCombo(detectionFluorophoreList,size=(11,1),key='-DETECTION_FLUOROPHORE-')
               ]
             ]),
    ], # End Frame of Detection Molecule Info
    
    # Consumable Box
    [sg.Frame(layout=[
        [Text('   Slide ID #',23),sg.InputText(default_text=savedValDict['-SLIDE_ID-'],size=(25,1),key='-SLIDE_ID-'),
         sg.T('   '),sg.B('',key='-CLEAR_CONSUMABLE-',image_data=deleteButtonGraphic,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0,tooltip="Clear the Consumable box's fields")],
        [sg.Text('   Mfg Date',size=(23,1),tooltip=MfgDateTip),sg.InputText(default_text=savedValDict['-MFG_DATE-'],size=(19,1),tooltip=MfgDateTip,key='-MFG_DATE-'),todayButton('-TODAY_M-','-MFG_DATE-'),plus()],
        [Text('   Sample Mfg (site)',23),sg.InputCombo((fabricatorList),default_value=savedValDict['-SAMPLE_MAKER-'],size=(25,1),key='-SAMPLE_MAKER-')],
        [Text('   Substrate Material',23),sg.InputCombo((substateMatList),default_value=savedValDict['-SUBSTRATE_MATERIAL-'],size=(25,1),key='-SUBSTRATE_MATERIAL-')],
        [Text('   Surface Chemistry',23),sg.InputCombo((surfaceChemistryList),default_value=savedValDict['-SURFACE_CHEMISTRY-'],size=(25,1),key='-SURFACE_CHEMISTRY-')]            
        ],title='Consumable Info',title_color='orange'),
    ], # End Frame of Consumable Info
 
    # Collapsable Sample Box
    [sg.T(SYMBOL_DOWN, enable_events=True, k='-OPEN SEC2-', text_color='yellow'),
     sg.T('Sample Info', enable_events=True, text_color='orange', k='-OPEN SEC2-TEXT'),    
      ],
    [collapse(section2, '-SEC2-')],

   ]) # End Column 1

RightCol=sg.Column([
     [sg.Frame(layout=[
        [sg.Text('Individual (unstacked) files). No stacked Tifs.',background_color='DodgerBlue3'),
            sg.T('* ',size=(3,1),font=('Helvetica',12),text_color='red',background_color='DodgerBlue4',pad=(0,0))],
            [sg.InputText(size=(51,1),key='-FILE_LOCATION-',enable_events=True),sg.FolderBrowse(target='-FILE_LOCATION-',enable_events=True)], #initial_folder=savedValDict['-FILE_LOCATION-'],
            [sg.B('Tweak Location', key='-TWEAK-',tooltip=TweakTip),
             sg.T('   Autopopulate tif name & coll time from folder?',background_color='DodgerBlue4',tooltip=AutoPopTip),
             sg.Checkbox('',background_color='DodgerBlue4',default=True,key='-AUTO_PROP_FROM_FOLDER-',tooltip=AutoPopTip)]

        ],title='Child Tif Folder Location',title_color='orange',relief=sg.RELIEF_RAISED,background_color='DodgerBlue4'), #, enable_events=True
         ],
    [sg.Frame(layout=[ # Frame on Instrument Info, with 3 sub-areas - Inst, Optical, Imaging
        [sg.Text('  Instrument Name',size=(23,1)),sg.InputCombo((instrumentList),default_value=savedValDict['-INSTRUMENT_NAME-'],size=(25,1),key='-INSTRUMENT_NAME-')],
        [sg.Text('  Serial #/Identifier',size=(23,1),tooltip=InstSNTip),sg.InputText(default_text=savedValDict['-INSTRUMENT_SN/ID-'],size=(25,1),tooltip=InstSNTip,key='-INSTRUMENT_SN/ID-'),plus()],
        [sg.Text('  Autofocus on?',size=(23,1)),sg.Checkbox('y/n',default=savedValDict['-CRISP_ON-'],key='-CRISP_ON-')],
        
        [sg.Text('_' * 56,text_color='#bbbbee')], # HR betw Instrument and Optical subsection
        
        # Begin collapsable section for Optical Info
        [sg.T(SYMBOL_DOWN, enable_events=True, k='-OPEN SEC1-', text_color='yellow'), 
         sg.T('Optical Info',text_color='orange', enable_events=True, k='-OPEN SEC1-TEXT')],
        [collapse(section1, '-SEC1-')],        
        
        [sg.Text('_' * 56,text_color='#bbbbee')], # HR betw Optical and Imaging subsection
        
        # Imaging Info Section - Old, not collapsable
    #     [sg.Text("    Imaging Info",text_color='orange')],
    #     [sg.Text('      Camera',size=(23,1),tooltip=CamTip),sg.InputCombo(cameraList,default_value=savedValDict['-CAMERA-'],size=(25,1),tooltip=CamTip,key='-CAMERA-'),plus()],
    #     [sg.Text('      Resolution (max)',size=(23,1),tooltip=ResMaxTip),sg.InputCombo(resolutionMaxList, default_value=savedValDict['-RESOLUTION_MAX-'],size=(25,1),tooltip=ResMaxTip,key='-RESOLUTION_MAX-'),plus()], # IMX183 = '5472 x 3648'
    #     [sg.Text('      Resolution Used (ROI)',size=(23,1)),sg.InputCombo(resolutionUsedList,default_value=savedValDict['-RESOLUTION_USED-'],size=(25,1),key='-RESOLUTION_USED-')], # Herc/Haifa using '2772x2772'
    #     [sg.Text('          Phsyical FOV of Herc/Haifa = .11 x .11 mm (110.88x110.88 \u03BCm)',font=("Helvetica",8,'italic'))],
    #     [sg.Text('      Binning',size=(23,1)),sg.InputCombo(binningList,default_value=savedValDict['-BINNING-'],size=(25,1),key='-BINNING-')],        
    #     [sg.Text('      Movie Time (sec)',size=(23,1)),sg.InputCombo(('120','150','600'),default_value=savedValDict['-MOVIE_TIME(SEC)-'],size=(25,1),key='-MOVIE_TIME(SEC)-')],
    #     [sg.Text('      Camera Offset',size=(23,1)),sg.InputText(default_text=savedValDict['-CAMERA_OFFSET-'],size=(25,1),key='-CAMERA_OFFSET-')],
    #     [sg.Text('      Dark Frame Value',size=(23,1),tooltip='average pixel value of dark frame'),sg.InputText(default_text=savedValDict['-DARK_FRAME_VALUE-'],size=(25,1),tooltip='average pixel value of dark frame',key='-DARK_FRAME_VALUE-')],
    #     [sg.Text('      Gain',size=(23,1)),sg.InputText(default_text=savedValDict['-CAMERA_GAIN-'],size=(25,1),key='-CAMERA_GAIN-')]

        # Imaging Info Section - Collapsible
        [sg.T(SYMBOL_DOWN, enable_events=True, k='-OPEN SEC3-', text_color='yellow'), 
         sg.T('Imaging Info',text_color='orange', enable_events=True, k='-OPEN SEC3-TEXT')],
        [collapse(section3, '-SEC3-')],    


         ],title='Instrument Info',title_color='orange'),
     ], # End Frame of Instrument Parameters
    
    # Other Box
    [sg.Frame(layout=[     
        [sg.Button(button_text='Click to type notes/new items',key='-OTHER_TEXT-')]
        ],title='Other Info',title_color='orange'),
    ], # End Frame of Other Info Box
    
#    [sg.Text(' ')], #add lines while col shorter than left
    ])

layout = [ [LeftCol,sg.VSeperator(color='MediumPurple1'),RightCol],
       
           [ sg.B('Submit',tooltip=SubmitTip,button_color=('gold','green'),size=(10,1),border_width="9",auto_size_button=True,font=("Courier",14, "bold italic")),
            sg.Frame(layout=[[
                sg.Text(StatusMsg,size=(34,1),key='-STATUS-',text_color='grey38',background_color='gainsboro',font=('bold'))]],title='Status',title_color='DodgerBlue2',relief=sg.RELIEF_RAISED,background_color='PeachPuff2',font=('bold')),
            sg.B(key="Upload_Tool",tooltip=CloudTip,button_text='',image_data=cloudButtonGraphic,button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0, enable_events=True), #,button_color=(sg.theme_background_color()),sg.theme_background_color()            
           ] # sg.B('Upload Tool')
        ]       
# see lines below - swap depending on where you want the button to be.

""" 
For Submit same line as File Storage, copy next 2 lines to after previous comment.
        ],title='File Storage',title_color='orange',relief=sg.RELIEF_SUNKEN,background_color='DodgerBlue4'),sg.Submit(button_color=('gold','green'),size=(10,2),font=("Courier",15, "bold italic"),tooltip=SubmitTip)],
        ]
For Submit to be on its own line, copy these 2 lines (repl what's there).
        ],title='File Storage',title_color='orange',relief=sg.RELIEF_SUNKEN,background_color='DodgerBlue4')],
        [sg.Submit(button_color=('gold','green'),size=(10,2),font=("Courier",15, "bold italic"),tooltip=FileTooltip)]]
 
"""  
     

#] #End the overall frame


# Create the Window
winMain = sg.Window('SiMREPS Metadata Entry, v'+ProgVer+'.   i = item has a tooltip', layout, location=(200,0)) #,location=(-880,50) xy loc is for multimonitor setups so it doesn't appear behind in-focus window on main monitor

winWellPick_active=False # this is for the consumable well picker diagram window

opened1, opened2, opened3 = True, True, True # for the collapsible sections

# Event Loop to process "events"
while True:             
    event, values = winMain.read()
    
    # put anything new after the break/cancel to avoid NoneType.
    
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    print('----------------------\nvalues from read before check/submit:\n'+str(values))
    
    # Window location info passed to consumable window and Tweak to allow them to be positioned relative to main windowl
    locn=winMain.CurrentLocation()
    locDelta=(900,8)
    locnadj=(locn[0]+locDelta[0],locn[1]+locDelta[1]) # a smarter way of doing this
                                                      # would be to get window size, 
                                                      # then half of each would be center, then add to go up and over
    print('\nwindow location:'+str(locn))
    print('proposed loc for sibling (Tweak) window:'+str(locnadj))
    
    # Calculating Dilution Factor and $ matrix, after checking for "" or "Other", upon which one can't do math
    print('\nSample Dil Vol = '+values['-ANALYTE_VOLUME-'])
    if str(values['-ANALYTE_VOLUME-'])=="" or values['-ANALYTE_VOLUME-']=="Other" or values['-BUFFER_OSS_VOLUME(uL)-']=="" or values['-BUFFER_OSS_VOLUME(uL)-']=="Other":
        winMain['-DIL_FACTOR-'].update('tbc')
        print('\n--------\nNear top of event loop\none of sample dil vol or buffer OSS vol is empty, setting dil factor to tbc')
        winMain['-PERCENT_MATRIX-'].update('tbc')
    if values['-ANALYTE_VOLUME-']!="" and values['-ANALYTE_VOLUME-']!="Other" and values['-BUFFER_OSS_VOLUME(uL)-']!="" and values['-BUFFER_OSS_VOLUME(uL)-']!="Other":  
        print('\n--------\nNear top of event loop\sample dil vol and buffer OSS vol not empty, calculating dil factor')
        winMain['-DIL_FACTOR-'].update((int(values['-ANALYTE_VOLUME-'])+int(values['-BUFFER_OSS_VOLUME(uL)-']))/int(values['-ANALYTE_VOLUME-']))
        dilFactor=float((int(values['-ANALYTE_VOLUME-'])+int(values['-BUFFER_OSS_VOLUME(uL)-']))/int(values['-ANALYTE_VOLUME-']))
        print('dilFactor = ',dilFactor)
        winMain['-PERCENT_MATRIX-'].update(100*(1/dilFactor)) #1/(int(values['-DIL_FACTOR-'])
        

    # Collapsible section controls
    if event.startswith('-OPEN SEC1-'): #Optical Info, Right Column: collapse or not
        opened1 = not opened1
        winMain['-OPEN SEC1-'].update(SYMBOL_DOWN if opened1 else SYMBOL_UP)
        winMain['-SEC1-'].update(visible=opened1)

    if event.startswith('-OPEN SEC2-'): # Sample Info, Left Column: collapse or not
        opened2 = not opened2
        winMain['-OPEN SEC2-'].update(SYMBOL_DOWN if opened2 else SYMBOL_UP)
        winMain['-SEC2-'].update(visible=opened2)

    if event.startswith('-OPEN SEC3-'): # Imaging Info: collapse or not
        opened3 = not opened3
        winMain['-OPEN SEC3-'].update(SYMBOL_DOWN if opened3 else SYMBOL_UP)
        winMain['-SEC3-'].update(visible=opened3)
        
    # following 3 ifs get "today" or "now" for collection date, time, and mfg date
    if event =='-TODAY-':
        print('in today loop')
        winMain.FindElement('-COLLECTION_DATE-').Update(datetime.datetime.now().strftime("%Y"+"%m"+"%d")) #   https://docs.python.org/2.0/ref/strings.html
        print('----------------------\nvalues after Today pressed: \n'+str(values))

    if event =='-NOW-':
        print('in now loop')
        winMain.FindElement('-COLLECTION_TIME-').Update(datetime.datetime.now().strftime("%H"+"%M"))
        
    if event =='-TODAY_M-':
        print('----------------------\nin today_M loop')
        winMain.FindElement('-MFG_DATE-').Update(datetime.datetime.now().strftime("%Y"+"%m"+"%d")) #   https://docs.python.org/2.0/ref/strings.html
        print('----------------------\nvalues after Today pressed: '+str(values))
        
    # Following 2 ifs check that the date is formatted correctly, see the function
    #I have figured out how to get this function to validate the date is correctly YYYYMMDD
    # But the this check needs to  return 'true' if it is    

    if str(values['-COLLECTION_DATE-'])!="":
        testDate = values['-COLLECTION_DATE-']
        secondCheck = testDate    
        testDate = testDate[:4]+'-'+testDate[4:6]+'-'+testDate[6:]
        
        theCollectDateCheck = validate(testDate)
        theCollDateCheck=theCollectDateCheck
        print('just back from validate fn:'+theCollectDateCheck)
        #print(len(secondCheck))
        if(len(secondCheck)>8):
            #print('in greater')
            theCollectDateCheck='false'
        elif(len(secondCheck)<8):
            #print('in less')
            theCollectDateCheck='false'
        else:
            #print('in goldilocks')
            theCollectDateCheck='true'
        #print('theDate check =',theDateCheck)
  
    #if str(values['-MFG_DATE-'])!="":
    #    testDate = values['-MFG_DATE-']    
    #    testDate = testDate[:4]+'-'+testDate[4:6]+'-'+testDate[6:]
    #    theMFGDateCheck = validate(testDate)

    # This if removes .tif, .Tif or .TIF if those are put into the "Unique stack name" field
    if str(values['-STACK_FILENAME-']).endswith('.tif') or str(values['-STACK_FILENAME-']).endswith('.Tif') or str(values['-STACK_FILENAME-']).endswith('.TIF'):
        print('---\nStack filename provided had .tif or .Tif or .TIF in it\n   is:'+str(values['-STACK_FILENAME-']))
        strStkFilename=str(values['-STACK_FILENAME-'])
        strStkFilename=strStkFilename[:-4]
        print('... changing it to:' + strStkFilename)
        values['-STACK_FILENAME-']=strStkFilename

    # and this if removes .Tiff, .tiff ...
    if str(values['-STACK_FILENAME-']).endswith('.tiff') or str(values['-STACK_FILENAME-']).endswith('.Tiff') or str(values['-STACK_FILENAME-']).endswith('.TIFF'):
        print('---\nStack filename provided had .tiff or .Tiff in it\n   is:'+str(values['-STACK_FILENAME-']))
        strStkFilename=str(values['-STACK_FILENAME-'])
        strStkFilename=strStkFilename[:-5]
        print('... changing it to:' + strStkFilename)
        values['-STACK_FILENAME-']=strStkFilename
    
    # If / or \ are entered into "Unique Tif Stack Name", replace with -
    if str(values['-STACK_FILENAME-']).find('\\') !=-1:
        slashChars=str(values['-STACK_FILENAME-']).replace("\\","-")
        values['-STACK_FILENAME-']=slashChars
        fred=r"removed \\"
        print (fred)
        winMain.FindElement('-STACK_FILENAME-').Update(values['-STACK_FILENAME-'])
    
    if str(values['-STACK_FILENAME-']).find('/') !=-1:
        slashChars=str(values['-STACK_FILENAME-']).replace("/","-")
        values['-STACK_FILENAME-']=slashChars
        fred=r"removed /"
        print (fred)
        winMain.FindElement('-STACK_FILENAME-').Update(values['-STACK_FILENAME-'])
    
    
    # Folder tweak (showing all children of last-selected folder's parent)
    if event =='-TWEAK-':
        folderUI(values)

    # Checking that tif files conform to naming convention
    if event == '-FILE_LOCATION-':
        print('got to if in events for file location')
        # sg.Popup('in if for file location')
        folderPath = values['-FILE_LOCATION-']
        #folderName=folderPath.rsplit('/',2) #split into 2 pcs at last /
        folderList=folderPath
        AutoProp=values['-AUTO_PROP_FROM_FOLDER-']
        windowUpdate(AutoProp,folderList)


    
    # This pops up for "Other_Text" if you want to put something there.    
    if event =='-OTHER_TEXT-':
        print('got into if of -OTHER_TEXT-')
        # sg.Popup('enter other info here')
        OtherText=sg.popup_get_text(title='Enter other info here',message='... perhaps a new chemistry or value, or comments on the weather',size=(60,2))


    # This listens for WellChooser button. If happens, make that window active    
    if event=='-CONS_BUTTON-' and not winWellPick_active:
        cols=8
        locnow=winMain.CurrentLocation()
        locDeltaC=(-90,300)
        locnAdjCons=(locnow[0]+locDeltaC[0],locnow[1]+locDeltaC[1]) # a smarter way of doing this
                                                      # would be to get window size, 
                                                      # then half of each would be center, then add to go up and over
        sg.theme('BluePurple')
        winWellPick_active=True
        layoutCons=[
          [sg.B('\u20DD',size=(6,2),button_color=('orange','#223344'),key=(1,f'{i+1}'),pad=(0,0)) for i in range(cols)],
          [sg.B('\u20DD',size=(6,2),button_color=('orange','#223344'),key=(2,f'{i+1}'),pad=(0,0)) for i in range(cols)],
          [sg.B('\u20DD',size=(6,2),button_color=('orange','#223344'),key=(3,f'{i+1}'),pad=(0,0)) for i in range(cols)]
          # [sg.B('Done',size=(8,2),font=('Any',13),button_color=('gold','green4'),key='-DONE-')]
        ]
        winWellPick=sg.Window('',no_titlebar=True,alpha_channel=.9,modal=True,grab_anywhere=True,element_justification='c',location=locnAdjCons).Layout(layoutCons)

    if winWellPick_active:
        ev2, vals2 = winWellPick.Read()
        #vals2txt=str(vals2)
        #print('vals2: '+vals2txt)
        chosenWell=str(ev2)
        print(chosenWell)
        chosenWell=chosenWell.replace('(','').replace(')','').replace("'",'') # the chooser ui returns (1,'3), for row 1, col 3. Get rid of the puncutation
        print('chosenWell after removing parenthesis, quotes: ',chosenWell)
        wellRow=int(chosenWell[0])
        print('row =',wellRow)
        if wellRow==1:
            wellRowAlpha='a'
        elif wellRow==2:
            wellRowAlpha='b'
        elif wellRow==3:
            wellRowAlpha='c'
        print('rowAlpha = '+wellRowAlpha)
        wellCol=int(chosenWell[-1])
        wellColStr=str(wellCol)
        print('str of wellCol = '+wellColStr)
        print('col =',wellCol)
        # use for numeric: wellNum=cols*(wellRow-1)+wellCol
        wellNum=wellRowAlpha+wellColStr
        print('wellNum =',wellNum)
        winMain['-WELL_NUMBER-'].update(wellNum)
        if ev2 is None or ev2 == 'Exit':
            winWellPick.Close()
            winWellPick_active = False
        print('chosenWell after winMain update: ',chosenWell)
        winWellPick_active = False
        sg.theme('Dark')
        winWellPick.close()
        

    # Clear the Consumable section on button press    
    if event == "-CLEAR_CONSUMABLE-":
        clearConsumable() # Go to function to clear all fields in consumable, 
                          # re-used in clear consumable+sample+detection and clear all

    # Clear the Sample Info section on button press    
    if event == "-CLEAR_SAMPLE_INFO-":
        clearSampleInfo()
        
    # Clear the Detection Molecule section on button press    
    if event == "-CLEAR_DETECTION-":
        clearDetectionMolecule()
    
    # Clear the Detection Molecule section on button press    
    if event == "-CLEAR_CONSUMABLE_SAMPLE_DETECTION-":
        clearConsumable()
        clearSampleInfo()
        clearDetectionMolecule()       
    
    # Save button
    if event == "-SAVE-":
        saveConsumableSampleDetection()

    # Load button
    if event == "-LOAD-":
        loadConsumableSampleDetection()
    
    # Spawn the uploader on cloud button press
    if event == "Upload_Tool":
        sg.PopupNoBorder('The uploader will open. \nUse only if you are done entering metadata for all experiments.\n\nAlso, this window can get behind the main window.\nIf the cloud button does not work, look behind main window or...\n  mouse over the white program icon on the task bar\n  which will show 2 window images.',background_color='DodgerBlue4')
        subprocess.Popen(['python','SiMREPS_Upload.py'])


    if event =='Submit':
        #print(theCollectDateCheck)
        if values['-USER-'] == "":
            sg.Popup('You must select a user', title='Missing info')
        elif values['-COLLECTION_DATE-']=="":
            sg.Popup('You must enter a Collection Date with correct format', title='Missing info')
        elif theCollectDateCheck=='false' or theCollDateCheck=='false':
            sg.Popup('The date format you entered is not allowed', title='Data format error')
        elif values['-LOCATION-']=="":
            sg.Popup('You must enter you Collection Location', title='Missing info')
        elif values['-EXPOSURE_TIME(SEC)-']=="":
            sg.Popup('You must enter an Exposure Time in seconds', title='Missing info')
        elif values['-MOVIE_TIME(SEC)-']=="":
            sg.Popup('You must enter a Movie Time in seconds', title='Missing info')
        elif str(values['-MOVIE_TIME(SEC)-']).isnumeric()==False:
            sg.Popup('Movie Time must be an integer',title='Data format error')
        elif str(values['-MOVIE_TIME(SEC)-']).isnumeric()==True and len(str(values['-MOVIE_TIME(SEC)-']))<2:
            sg.Popup('Movie time must be at least 2 digits long',title='Wrong # of digits')
        elif values['-EXPERIMENT_NAME-']=="":
            sg.Popup('You must enter an Experiment Name which can be common across experiments', title='Missing info')
        elif values['-STACK_FILENAME-']=="":
            sg.Popup('You must enter a Tif Stack Name which is unique to this set of Tifs', title='Missing info')
        # aLight gets a Papal dispensation on collection time
        elif values['-COLLECTION_TIME-']=="" and values['-LOCATION-']=="Hercules":
            sg.Popup('You must enter a Collection Time with correct format', title='Missing info')
        elif values['-COLLECTION_TIME-']=="" and values['-LOCATION-']=="Haifa":
            sg.Popup('You must enter a Collection Time with correct format', title='Missing info')
        elif str(values['-COLLECTION_TIME-']).isnumeric()==False:
            sg.Popup('collection time must be a 4-digit integer \nin the format hhmm',title='Data format error')
        elif str(values['-COLLECTION_TIME-']).isnumeric()==True and len(str(values['-COLLECTION_TIME-']))!=4:
            sg.Popup('collection time must be a 4-digit integer',title='Wrong # of digits')
        elif values['-WELL_NUMBER-']=="" and values['-LOCATION-']=="Hercules":
            sg.Popup('You must enter a Well #, row,col', title='Missing info')
        elif values['-WELL_NUMBER-']=="" and values['-LOCATION-']=="Haifa":
            sg.Popup('You must enter a Well #, row,col', title='Missing info')
        elif values['-ANALYTE_MOLECULE-']=="":
            sg.Popup('You must enter an analyte ID', title='Missing info')
        elif values['-ANALYTE_CONCENTRATION-']=="":
            sg.Popup('You must enter an analyte concentration', title='Missing info')
#        elif str(values['-ANALYTE_CONCENTRATION-']).isnumeric()==False:
#            sg.Popup('Assay (analyte) concentration must be an integer',title='Data format error')
        elif values['-FILE_LOCATION-']=="":
            sg.Popup('You must select a folder that contains your experiment tifs', title='Missing info')
        else:
            FL=values['-FILE_LOCATION-']
            FL_Slash=FL.replace('/','\\')
            origValues=values # use this for the saved version so "" is really "". Or do it with string.replace after read
            values={k:('Undefined' if v=="" else v) for (k,v) in values.items()} # Comprehension to change all "" to 'Undefined'
            print('you created metadata')
            #print('Values after comprehension to replace empty with Undefined: '+str(values))
            StatusMsg='writing metaDict.json'
            time.sleep(1)
            print('before find element writing metadata')
            winMain.FindElement('-STATUS-').Update(StatusMsg)
            winMain.refresh()
            time.sleep(1)
            print('before writing metadata')
            metadataJsonWrite()
            print('back from json write')
            StatusMsg='metaDict.json written'
            print('status msg updated')
            winMain.FindElement('-STATUS-').Update(StatusMsg)
            winMain.refresh()
            print('values at end = '+str(values))

            # saving values to json in folder of py for population on next program open            
            singleQuoteValues=str(values)
            dblQuoteValues=singleQuoteValues.replace("'",'"')
            
            with open('savedValues.json', 'w') as f:
                json.dump(str(values), f)

            # writing log file which is later uploaded to S3 by uploader
            with open(FL_Slash+"\metaLog.txt", 'w') as file:
                file.write('Meta Tool Program Version: '+ProgVer+'\n')
                file.write('Minimum Meta Tool Version:'+str(minVer)+'\n')
                file.write('Current Meta Tool Version:'+currentVersion+'\n')
                file.write('  Date metadata was captured: '+datetime.datetime.now().strftime("%Y"+"%m"+"%d")+'\n')
                file.write('  Time metadata was captured: '+datetime.datetime.now().strftime("%H"+"%M")+'\n')
                file.write('\nFile information:\n')
                file.write('  Total # of files in folder = '+str(fileQty)+'\n')
                file.write('  # of Tif Files in folder = '+str(tifQty)+'\n')
                file.write('  # of bad Tifs (without Capture_) = '+str(badTifs)+'\n')
                file.write('\nMetaData:\n----------------\n')
                json.dump(values, file, indent=2)
                print('metadata written to local file, info + json dump')
                
                
            time.sleep(2)
            StatusMsg='User Input'
            winMain.FindElement('-STATUS-').Update(StatusMsg)
            
winMain.close()