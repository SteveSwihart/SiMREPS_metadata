# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 11:51:36 2020
@author: Steve (combining Clayton's 2 programs)
"""

UploadVer='3.1' # This is written to window name and is written in log file.

# Next Steps:
"""
Next:
    Use Tif tag dimension to figure out if a given Tif is stacked rather than using file size. 
Soon:
    Can we thread the moving/compressing so we only pay the penalty on first few files?        
Later:
    Copy some of the tif logic from meta tool and write to log
    
    Consider making lists of all folders, folders with or without metadata. Display if anything
      less than all folders have metadata.
"""

# Version History and change highlights (first line - summary, details indented below first line)
"""
  3.1, fixed message displayed when major ver OK, minor old - incorrectly said meta tool, now says uploader tool.
  3, 27-Aug-21, altered to have compression always happen, one way or another:
                 Check for type of compression. If != nothing, note type to log, don't compress...
                 types I check for: Packbits, LZW, Adobe Deflate.
                 if uncompressed or unknown (!= types I check for), turn on compression.
                 Removed compression check box.
     
  0002.1, 17-Aug-21, Added logging of current an minimum versions.
                      also corrected typo at end of version < minimum - still said metadata, not uploader.
  0002, 17-Aug-21, Added version checks for current and minimum. 
                      If running ver < current but >= minimum, you're notified
                      If running ver < minimum, notified, program stops.
  0001-4, 21-May-21 Finalized serverless upload Test both simreps and simreps dev.  Removed compression stats printouts from loop.  
  0001-3, 17-May-21 Added s3 upload of new file lambdaTrigger.txt, Which will be used to create s3 event to trigger Lambda function.
  0001-2, 13-May-21   All the below changes made because of Fargate serverless pipeline implemented for createStack.
                    Moved AWS credentials, region name, bucket name, dynamodb name to simrepsConfig.py.
                    In S3, 'simreps-dev' bucket has been created for development activiites. we can now configure this in one place - simrepsConfig.py.
                    Added downloadKey, metaKey to metaDict file. (since these two were passing directtly in ssm command)
                    All SSM commands has been removed.
                    s3 upload of uploadMetaDict.json is moved to last file to upload, 
                        In S3, event trigger has beed created to call lambda when uploadMetaDict.json is added, 
                        and that will execute Fargate ECS task with respect to uploadMetaDict.json 
                        CreateStack will now happen inside Fargate
                    Email code has been implemented locally.  Added userName variable to send as argument to sendEmail.py
  0001, 5-May-21    Added compression (Adobe deflate) with checkbox for on/off. If checkbox True:
                     For each file, compress, save as name which is re-used, 
                     check size close to expected, s.b. ~ 47% orig
                     ... if good upload using orig filename on destination
                     ... if bad, compress again.
                     at end of loop, delete the last temp image.
                     Also added a check for existence of metaLog.txt (in addition to metaDict.json)
  0000-10, 3-May-21, Added logging of end time, total time, time per image, upload rate.
  0000-9, 1-Apr-21, Added a S3 key msg on checking paths...
                     so that if user chooses a child folder (rather than a parent with children),
                     we can see what the key would be. Also, that'll display the key to the user
                     in the event they manually renamed a folder but didn't change metadata.
  0000-8, 1-Apr-21, Tweaked msg on check for metadata.
                     Note - check is for *any* metadata. If 1 folder out of 50 has metadata, upload will run.
                     Message displayed if no folders have metadata.
  0000-7, 01-Apr-21, Included boto3.dynamoDB resource creation to get a response for sfTable.  If the response is 
                      greater than 0, then the current directory that is about to be uploaded will be skipped
                      because it has already been uploaded once before.  This change will allow the end user
                      to re-run the tool against the parent directory, skipping all successfully uploaded directories.
                      A new print out appears in the terminal describing which folder paths were skipped.  
  0000-6, 19-Feb-21, changed instanceID and working directory locations to isolate uploads from analysis
  0000-5, 17-Feb-21, reverted to 0000-3 (removed serverless)
                      instanceID and working directory now variables
  0000-4, 27-Jan-21 - adds serverless stacking (not active)
                      this code was checked in 14-Jan, but with same ver #.
                      and no comments. To use serverless:
                          line 150 in uploadData, serverlessCheck = 1 will turn it on ...
                          and line 272 after upload section will then not see a 0 and it will move to the elif.
  0000-3, 8-Jan-21, rudimentary logging from upload tool
                    ...simple file with program version, date, time & location of upload
  0000-2, 7-Jan-20, uploads metaLog.txt to S3
                    ... Steve is an idiot and skipped 0000-1.
                    now uploads metaLog.txt
                    Changed name of meta dictionary json uploaded.
                      metaDict.json is created by meta tool on the computer capturing data
                      uploadmetaDict is created by uploader in same folder, and is same except
                      for lines added at end. expUUID, upload date, time, key
  0000, 18-Dec-20, combined haifaLoopUpload.py and loopUpload.py.
                     combined former haifa and loopUpload
                     added a version # to file and main window
"""


import PySimpleGUI as sg
import boto3
import os
import json
import datetime
import glob
import uuid
from datetime import datetime
from tifffile import imread, imsave
import simrepsConfig
import sendEmail
import math #needed for version check (converting float to maj + minor vers)
import sys #needed for version check (stopping the program if ver running < major ver)

# the bucket code from loopUpload.py
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
    ssm = boto3.client('ssm',
                   region_name=simrepsConfig.aws_region,
                   aws_access_key_id=simrepsConfig.aws_access_key_expanded,
                   #aws_access_key_id = AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=simrepsConfig.aws_secret_key_expanded
                   #aws_secret_access_key = AWS_SECRET_ACCESS_KEY
                )
    return
"""

# the bucket code from haifaLoopUpload.py
"""
    homeBucket = simrepsConfig.aws_bucket
    irelandBucket = simrepsConfig.aws_irelandBucket
    #limited access
    limited_AWS_ACCESS_KEY_ID=simrepsConfig.aws_access_key
    limited_AWS_SECRET_ACCESS_KEY=simrepsConfig.aws_secret_key
    #expanded access
    expanded_AWS_ACCESS_KEY_ID=simrepsConfig.aws_access_key_expanded
    expanded_AWS_SECRET_ACCESS_KEY=simrepsConfig.aws_secret_key_expanded
    #create s3 boto3 client
    s3 = boto3.client('s3',
                   region_name=simrepsConfig.aws_region,
                   aws_access_key_id=expanded_AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=expanded_AWS_SECRET_ACCESS_KEY
                )
    ssm = boto3.client('ssm',
                   region_name=simrepsConfig.aws_region,
                   aws_access_key_id = expanded_AWS_ACCESS_KEY_ID,
                   aws_secret_access_key = expanded_AWS_SECRET_ACCESS_KEY
                )
    return
"""

mainBucket=simrepsConfig.aws_bucket
irelandBucket=simrepsConfig.aws_irelandBucket
AWS_ACCESS_KEY_ID=simrepsConfig.aws_access_key
AWS_SECRET_ACCESS_KEY=simrepsConfig.aws_secret_key
instanceID='i-01c0b7f461672edbb'   #"i-0051f1752a1aad0da"
workingDirectory="/home/ec2-user/aihub/LSG/advancedDevelopmentRD/projects/simreps/simrepsApp"

s3_US=boto3.client('s3',
                   region_name=simrepsConfig.aws_region,
                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                  )

ssm_US = boto3.client('ssm',
               region_name=simrepsConfig.aws_region,
               aws_access_key_id=simrepsConfig.aws_access_key_expanded,
               #aws_access_key_id = AWS_ACCESS_KEY_ID,
               aws_secret_access_key=simrepsConfig.aws_secret_key_expanded
               #aws_secret_access_key = AWS_SECRET_ACCESS_KEY
            )

#limited access for Haifa
limited_AWS_ACCESS_KEY_ID=simrepsConfig.aws_access_key
limited_AWS_SECRET_ACCESS_KEY=simrepsConfig.aws_secret_key

#expanded access for Haira
expanded_AWS_ACCESS_KEY_ID=simrepsConfig.aws_access_key_expanded
expanded_AWS_SECRET_ACCESS_KEY=simrepsConfig.aws_secret_key_expanded

#create s3 boto3 client for Haifa
s3_Haifa = boto3.client('s3',
               region_name=simrepsConfig.aws_region,
               aws_access_key_id=expanded_AWS_ACCESS_KEY_ID,
               aws_secret_access_key=expanded_AWS_SECRET_ACCESS_KEY
            )

ssm_Haifa = boto3.client('ssm',
               region_name=simrepsConfig.aws_region,
               aws_access_key_id = expanded_AWS_ACCESS_KEY_ID,
               aws_secret_access_key = expanded_AWS_SECRET_ACCESS_KEY
            )

#create dynamodb boto3 resource so we can check if the directory of upload images can be skipped
dynamodb = boto3.resource('dynamodb',
                           region_name=simrepsConfig.aws_region,
                           aws_access_key_id=expanded_AWS_ACCESS_KEY_ID,
                           aws_secret_access_key=expanded_AWS_SECRET_ACCESS_KEY
                        )

sfTable = dynamodb.Table(simrepsConfig.aws_sfTable)

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
rdTable = dynamodb.Table(simrepsConfig.aws_sudTable)
response = rdTable.scan(AttributesToGet=['uploaderMinimumVersion','uploaderCurrentVersion'])
#preceding 2 lines are not in the code for meta tool as meta tool does those table steps already to be able to get UI field data.
minimumVersion = response['Items'][0]['uploaderMinimumVersion'] # added 11-Aug-21, check to see if new enough version is being used.
print('meta Tool minimum version (major.minor):',minimumVersion)
minVer=float(minimumVersion)
print('minVer',minVer)
minVerSeparated=math.modf(minVer)
print('minVerSeparated',minVerSeparated)
minVerMajor=int(minVerSeparated[1])
minVerMinor=round(10*(minVer-minVerMajor))
print('minimum major ver:',minVerMajor, ', minimum minor ver',minVerMinor)
thisVersion=float(UploadVer)
thisVerSeparated=math.modf(thisVersion)
print('version that is running:',thisVersion)
thisVerMajor=int(thisVerSeparated[1])
thisVerMinor=round(10*(thisVersion-thisVerMajor))
print('this major ver:',thisVerMajor, ', this minor ver',thisVerMinor)


currentVersion = response['Items'][0]['uploaderCurrentVersion'] # added 11-Aug-21, check to see what current is
print('uploader current version:', currentVersion)
currentVer=float(currentVersion)
currentVerSeparated=math.modf(currentVer)
currentVerMajor=int(currentVerSeparated[1])
currentVerMinor=round(10*(currentVer-currentVerMajor))
print('current version, minor =',currentVerMinor)

if thisVerMajor < minVerMajor:
    print('You are running version',thisVersion,'. Version',minVer,'is the minimum version. Version ',currentVersion,'is the current version.\nget new version via git pull.\nProgram will terminate.')
    # Use a PSG window to display the message....
    layoutOutOfDate=[
        [sg.T('Out of date uploader version used', text_color='OrangeRed2', font=('Any',13,'bold'))],
        [sg.T('You are running version'),sg.T(thisVersion, font=('Any',10,'italic'),pad=(0,0),text_color='orange')],
        [sg.T('Version'),sg.T(minVer, font=('Any',10,'italic'),pad=(0,0),text_color='orange'),sg.T('is required.')],
        [sg.T('   program will terminate.')],
        [sg.T('What to do:', font=('Any',11,'italic'))],
        [sg.T('  Do a git pull if possible.')],
        [sg.T('     In Spyder, !git pull. In Git Bash or Git CMD, git pull')],
        [sg.T('  If no git client is available:\n     delete all code in IDE, \n     view from web, \n     copy all, paste into IDE')],
        [sg.T('New version required before you can upload. \nSomething would break if you used this version.',font=('Any',13,'bold italic'),text_color='coral1')]
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
    sg.Popup('current uploader version is '+currentVersion+', you are running '+str(thisVersion)+'.\n\nVersion you are running will not break anything,\nbut upgrading is recommended.',title="Version information")

"""
End Version Checking Section
"""

def uploadData(parentDirectory,subDirectories,upload):
    notUploaded=([])
    numberOfSubD = len(subDirectories)
    uploadCount = 1
    howMany = 0
    # print('compression will be used ... '+compression)
    # compressionValue=1
    userName = 'undefined'
    #startTime = time.time()
    for i in subDirectories:
        metaDataExists = os.path.exists(i+'metaDict.json')
        if metaDataExists:
            #print ('the metaDict filePath is',i+'metaDict.json')
            with open (i+'metaDict.json') as jsonFile:
                metaDict = json.load(jsonFile)
            nCheck = metaDict['userName']
            if userName == 'undefined':
                userName = nCheck
            cdCheck = metaDict['dateCollected']
            icrCheck = metaDict['imageCollectionRate']
            fnCheck = metaDict['fileName']
            clCheck = metaDict['collectionLocation']
            if clCheck == "Hercules" or clCheck=="aLight":
                print('not Haifa')
                s3=s3_US
                ssm=ssm_US
                uploadBucket=mainBucket
                # can't add add the SSM command here because expUUID etc don't exist yet.
                
            elif clCheck=="Haifa":
                print('Haifa')
                s3=s3_Haifa
                ssm=ssm_Haifa
                uploadBucket=irelandBucket
                
                # ditto comment above 
                
        else:
            nCheck = "Undefined"
            cdCheck = "Undefined"
            icrCheck = "Undefined"
            fnCheck = "Undefined"
            clCheck = "Undefined"

        print('the parent directory path is',parentDirectory)
        print('the current child directory path (i) is', i)
        #print(i.split(parentDirectory))
        
        #new route for getting theSubDirectory.  This should stop a matching string in the string split 
        print('these images should load into a relative s3 subdirectory path of',i.split(parentDirectory)[1].replace('\\','/').replace(' ',''))
        theSubDirectory = (i.split(parentDirectory)[1].replace('\\','/').replace(' ',''))

        #old route for getting theSubDirectory
        #print(i.split(os.path.basename(parentDirectory)))
        #theSubDirectory = (i.split(os.path.basename(parentDirectory))[1].replace('\\','/').replace(' ',''))
        #print('the sub directory is',theSubDirectory)
        
        # Check that the required meta parameters exist and if so, upload.
        if nCheck!="Undefined" and cdCheck!="Undefined" and icrCheck !="Undefined" and fnCheck != "Undefined" and clCheck != "Undefined":
            
            #set upload dates
            theDateTime = datetime.now().strftime("%Y"+"%m"+"%d")+'/'+datetime.now().strftime("%H"+"%M"+"%S")
            date = str(theDateTime[0:8])
            theTime = str(theDateTime[-6:])
            startTime=datetime.now()
                        
            #define the exp uuid
            expUUID = uuid.uuid4()

            #append appropriate keys    
            metaDict['expUUID']=str(expUUID)
            metaDict['uploadDate']=str(date)
            metaDict['uploadTime']=str(theTime)
            metaDict['timeCollected']=str(date)+str(theTime)
            metaDict['stackKey'] = str(metaDict['collectionLocation']) + '/users/'+ str(metaDict['userName']) + '/rawData/' + str(metaDict['dateCollected'])  + theSubDirectory + str(metaDict['fileName']+'.tif')
            metaDict['fileKey'] = str(metaDict['collectionLocation']) + '/users/'+ str(metaDict['userName']) + '/rawData/' + str(metaDict['dateCollected'])  + theSubDirectory + str(metaDict['fileName']+'.tif')
            metaDict['downloadKey'] = str(metaDict['collectionLocation']) + '/users/'+ str(metaDict['userName']) + '/rawData/' + str(metaDict['dateCollected']) + theSubDirectory
            metaDict['metaKey'] = str(metaDict['collectionLocation']) + '/users/'+ str(metaDict['userName']) + '/rawData/' + str(metaDict['dateCollected']) + theSubDirectory +'uploadMetaDict.json'
            metaDict['fargateTriggerKey'] = str(metaDict['collectionLocation']) + '/users/'+ str(metaDict['userName']) + '/rawData/' + str(metaDict['dateCollected']) + theSubDirectory +'lambdaTriggerSimrepsUploadStackFargate.txt'
                       
            #run a check to determine if this directory of tifs has already been uploaded.
            #if the DB response is greater than zero, a stackKey exists for this set of images e.g. the directory has successfully been uploaded in past
            #with this particular stackKey.  If someon renames the fileName they want for the stack key, then the local directory would be considered
            #unique.
            response = sfTable.query(KeyConditionExpression = boto3.dynamodb.conditions.Key('stackKey').eq(metaDict['stackKey']))
            # response['Count']=0 # uncomment me to disable checking while coding/testing
            
            if(response['Count']!=0):
                print('It appears that you successfully uploaded the child directory "' + theSubDirectory + '" once before, so it is being skipped.')
                print('The S3 key is: '+metaDict["stackKey"])
            else:
                # get a list of files with paths
                imgPathList = [f for f in glob.glob(i+'\\*.tif')]
                print('\nimgPathList (just Tifs) for this folder: \n',imgPathList,'\n')
                numImages = len(imgPathList)
                numImagesUploaded=numImages
                
                # Now make a list of the tif files sans path so that we can find the lowest # after Capture_ from it
                imgFileList=[]
                for file in os.listdir(i):
                    if file.endswith(".tif"):                        
                        imgFileList.append(file)
                print('filename list: ', imgFileList)
                
                # Sort, oldest first
                sortedImgList=sorted(imgPathList,key=os.path.getctime)
                print('list of Tifs by time, oldest first',sortedImgList)
                
                # Get name of oldest Tif
                oldestTif=min(imgPathList,key=os.path.getctime)
                print('\nthe oldest of the Tifs is:',oldestTif)
                
                # If file exists, find out if it is compressed or not
                from PIL import Image
                img = Image.open(oldestTif)
                TagsInImage=img.tag_v2
                
                compressionValue=(TagsInImage[259])
                compression="True"
                compressionType="Unknown"
                if compressionValue==1:
                    compressionType="Uncompressed"
                    compression="True"
                    
                if compressionValue==5:
                    compressionType="LZW"
                    compression="False"
                    
                if compressionValue==8:
                    compressionType="Adobe Deflate"
                    compression="False"
                
                if compressionValue==32773:
                    compressionType="Packbits"
                    compression="False"
                print('Compression of files is:',compressionValue,' In English, that is: ',compressionType)                                
                
                
                totalBytes=0 #add to this with each uncompressed file
                totalCompressedBytes=0
                
                for count,imgPath in enumerate(imgPathList):
                    sg.OneLineProgressMeter('Uploading Sub Direc. ' + str(uploadCount) + ' of ' + str(numberOfSubD), count+1, numImages, 'key','Upload Metrics')
                    imageFileName = os.path.basename(imgPath)
                    fileSize = os.stat(imgPath)
                    tifSize=os.path.getsize(imgPath) #same as previous, different type
                    if ((fileSize.st_size/1e6) > 50):
                        print('I think ' + imageFileName +' is probably a stacked Image, so I am going to skip it')
                        numImagesUploaded=numImagesUploaded-1
                    else:
                        imgUploadKey = str(metaDict['collectionLocation']) + '/users/'+ str(metaDict['userName']) + '/rawData/' + str(metaDict['dateCollected']) + theSubDirectory + str(imageFileName)
                        #print(imgPath)                        
                        
                        if upload==1:                            
                            if compression=="True": # tifs are uncompressed now, need to compress
                                fileToCompress=imgPath
                                tifSize=os.path.getsize(fileToCompress)
                                #print('file size of', imgPath, 'is ',tifSize)
                                totalBytes+=tifSize # keeping track of total bytes uploaded to later calculate upload speed.
                                #print('total uncompressed bytes = ',totalBytes,'\n')
                                img = imread(fileToCompress)
                                # print('read the image')
                                # print('current subdir = ',i)
                                compressedImagePath=i+'temp.tiffImage' #+r'\\'
                                #print('compressed filename will be ',compressedImagePath)
                                imsave(compressedImagePath,img,compress=compressionValue)
                                compressedTifSize=os.path.getsize(compressedImagePath)
                                #print('compressed tif size = ', compressedTifSize)
                                if compressedTifSize < 0.37*tifSize: # just in case got a bad compression, though this only retries 1X
                                    #print('file < .37 of original, recompress')
                                    imsave(compressedImagePath,img,compress=compressionValue)
                                # if compressedTifSize > 0.57*tifSize:
                                #     imsave(compressedImagePath,img,compress=compressionValue)
                                totalCompressedBytes+=compressedTifSize
                                #print('total compressed bytes = ', totalCompressedBytes)
                                s3.upload_file(Bucket=uploadBucket,Key=imgUploadKey,Filename=compressedImagePath)
                            elif compression=="False":
                                #print('in compression false')
                                tifSize=os.path.getsize(imgPath)
                                #print('file size of', imgPath, 'is ',tifSize)
                                totalBytes+=tifSize # keeping track of total bytes uploaded to later calculate upload speed.
                                #print('total uncompressed bytes = ',totalBytes,'\n')
                                s3.upload_file(Bucket=uploadBucket,Key=imgUploadKey,Filename=imgPath)
                
                # get rid of placeholder compressed tif, if compression is being used
                if compression=="True":
                    if os.path.exists(compressedImagePath):
                        os.remove(compressedImagePath)
                            
                
                #upload the finalized metaData to the homeBucket.  It's important that the metaDict file does not go to ireland.
                with open(i+'uploadMetaDict.json','w') as outFile:
                    json.dump(metaDict,outFile,indent=4)
                metaKey = str(metaDict['collectionLocation']) + '/users/'+ str(metaDict['userName']) + '/rawData/' + str(metaDict['dateCollected']) + theSubDirectory +'uploadMetaDict.json'
                # this key is per-file. ATM it provides the name "metaDict.json", but the s3.upload line grabs uploadMetaDict.json. Could change to uploadMetaDict.json
                howMany+=1
                
                #upload meta tool log file
                metaLogKey = str(metaDict['collectionLocation']) + '/users/'+ str(metaDict['userName']) + '/rawData/' + str(metaDict['dateCollected']) + theSubDirectory +'metaLog.txt'
                s3.upload_file(Bucket = mainBucket,Key=metaLogKey,Filename = i+'metaLog.txt')
                
                # rudimentary logging for upload tool
                
                print('\nUpload Start time: ',theTime)
                stopDateTime = datetime.now()
                #print('stopDateTime',stopDateTime)
                stopDateTimeFixed = datetime.now().strftime("%Y"+"%m"+"%d")+'/'+datetime.now().strftime("%H"+"%M"+"%S")
                #print('stopDateTimeFixed',stopDateTimeFixed)
                #stopDateTimeStr=str(stopDateTime)
                stopDate = str(stopDateTimeFixed[0:8])
                stopTime = str(stopDateTimeFixed[-6:])                
                print('upload Stop time: ',stopTime)
                elapsedTime=stopDateTime-startTime
                elapsedSeconds=elapsedTime.total_seconds()
                print('seconds of upload (total): ',elapsedSeconds)
                print('\npath i = '+i)
                print('# of Tifs uploaded: ',numImages)
                print('seconds per image: ',elapsedSeconds/numImages)
                # secondsPerImage=elapsedSeconds/numImages
                # print('upload time per image: ',secondsPerImage)
                print('compression type of files: ',compressionType)
                print('uploader comressed?: ',compression)
    # print('\nnumber of Tifs = ',tifQuantity)
    # print('seconds per image = ',secondsPerImage)
    # print('total bytes before compression =',totalBytes)
    # print('average bytes/file uncompressed: ',totalBytes/tifQuantity)
                if compression=="True":
                    print('total compressed bytes uploaded = ',totalCompressedBytes)
                    print('average bytes/ compressed file = ',totalCompressedBytes/numImages)
                    bps=totalCompressedBytes*8/elapsedSeconds
                if compression=="False":
                    print('total bytes uploaded = ', totalBytes)
                    print('average bytes/file = ',totalBytes/numImages)
                    bps=totalBytes*8/elapsedSeconds
                # compressionRatio=100*(totalBytes-totalCompressedBytes)/totalBytes
    #print(f'compresseion ratio: {compressionRatio:.2f}'+"%")
                
                Mbps=bps/1000000
                print('data rate = ' + str(bps) + 'bps or ' +  str(Mbps) + 'Mbps')
                with open(i+'uploadLog.txt', 'w') as file:
                    file.write('upload Tool Version used: '+UploadVer+'\n')               
                    file.write('minimum version: '+str(minVer)+'\n')
                    file.write('current version: '+str(currentVer)+'\n')
                    #file.write('  Date of upload: '+datetime.datetime.now().strftime("%Y"+"%m"+"%d")+'\n')
                    #file.write('  Time upload was started: '+datetime.datetime.now().strftime("%H"+"%M")+'\n')
                    file.write('  Date of upload: '+date+'\n')
                    file.write('  Time upload was started: '+theTime+'\n')
                    file.write('  Date of upload finish: '+stopDate+'\n')
                    file.write('  Time upload was finished: '+stopTime+'\n')
                    file.write('  elapsed seconds: '+str(elapsedSeconds)+'\n\n')
                    file.write('  Compression type of files: '+compressionType+'\n')
                    file.write('  Uploader compressed files (only done if they were uncompressed)?: '+compression+'\n\n')
                    file.write('  # of Tifs found: '+str(numImages)+'\n')
                    file.write('  # of Tifs uploaded*: '+str(numImagesUploaded)+'\n')
                    file.write('  seconds per image: '+str(elapsedSeconds/numImages)+'\n')
                    file.write(f'  upload bit rate {bps:.2f} bps'+f' or {Mbps:.2f}'+ 'Mbps\n')
                    file.write('\n  Image Collection Location: '+clCheck+'\n')
                    file.write('  Path on uploading computer: '+i+'\n')
                    file.write('  Stack key: '+str(metaDict['stackKey']))
                    file.write('\n\n*images will not be uploaded if they are either not named according to\n the Capture_ convention or they are large enough to be stacked Tifs.')
                    # following commented lines are from meta tool's logging:
                    # file.write('\nFile information:\n')
                    # file.write('  Total # of files in folder = '+str(fileQty)+'\n')
                    # file.write('  # of Tif Files in folder = '+str(tifQty)+'\n')
                    # file.write('  # of bad Tifs (without Capture_) = '+str(badTifs)+'\n')
                    # file.write('\nMetaData:\n----------------\n')
                    # json.dump(values, file, indent=2)
    #                print('upload written to local file')
                uploadLogKey = str(metaDict['collectionLocation']) + '/users/'+ str(metaDict['userName']) + '/rawData/' + str(metaDict['dateCollected']) + theSubDirectory +'uploadLog.txt'
                s3.upload_file(Bucket = mainBucket,Key=uploadLogKey,Filename = i+'uploadLog.txt')   
                s3.upload_file(Bucket = mainBucket,Key=metaKey,Filename = i+'uploadMetaDict.json')         
                with open('lambdaTriggerSimrepsUploadStackFargate.txt', 'w') as file:
                    file.write('This file is created for triggering the Lambda funtion of Simreps-Upload-Stack-Fargate')   
                s3.upload_file(Bucket = mainBucket, Key = metaDict['fargateTriggerKey'], Filename = 'lambdaTriggerSimrepsUploadStackFargate.txt')         
                
                print('the stack key is',metaDict['stackKey'])

                # createStack/createHaifaStack is moved to Fargate. 
                # S3 will trigger Lambda and that will execute Fargate Create Stack
                # So SSM command has been removed.
                
        else: #the metaDataFile is missing or you did not define the four required meta data variables above
            notUploaded.append(theSubDirectory)
        uploadCount+=1
    if(howMany>0):
        sendEmail.main(userName)
        # Have to implement email code directly here instead of SSM command
    #endTime = time.time()
    #print('The upload to ' + bucket + ' required ' + str(round((endTime-startTime)/60, 2)) + ' minutes.')
    return
    
    

#The layout for the PySimpleGUI window
sg.theme('DarkGrey7')
layout = [
            [sg.Frame(layout=[[sg.InputText('Set The Parent Directory'),sg.FolderBrowse(key='-FILE_LOCATION-')]],title='Parent Directory',title_color='orange')],
            [sg.Button('Start',button_color=('black','grey'),size=(10,2),font=("Courier",15, "bold italic"))],
            [sg.InputText('Button Will Appear Green When Finished')]
        #,sg.T('                    Use compression?',text_color='orange'),sg.Checkbox('y/n',key='-COMPRESSION-')
        ]

# Create the RealTime Upload Window
window = sg.Window('SiMREPS Loop Upload v'+UploadVer, layout) 


#Start listening to the window
while True:             
    event, values = window.read()
    if event =='Start':      
        if values['-FILE_LOCATION-']=="":
            sg.Popup('You must select a parent directory')
        else:
            FL = values['-FILE_LOCATION-']
            subDirectories=([])
            parentDirectory=FL.replace('/','\\')
            jsonExists=0
            for root, dirs, files in os.walk(parentDirectory):
                for file in files:
                    if file.endswith("metaLog.txt"):
                        logExists=True
                    else: logExists=False
                    if file.endswith("metaLog.txt") and logExists==True:
                        subDirectories.append(root+'\\')
                        jsonExists=1
            if jsonExists==0:
                print('\nNo metadata and/or metadata log exists in any of the subfolders of the chosen parent.')
                sg.Popup('No metadata or log found in any subfolders.\nPlease use the metadata entry tool to place data in at least 1 subfolder.')
            upload=1
            
            #compression = str(values['-COMPRESSION-'])
            print('parent = ' + parentDirectory + ', subdirs = ' + str(subDirectories) + ', upload = ' + str(upload))
            
            uploadData(parentDirectory,subDirectories,upload)
            
            window.FindElement('Start').Update(button_color=('black', 'green'))
            window.refresh()

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break


window.close()