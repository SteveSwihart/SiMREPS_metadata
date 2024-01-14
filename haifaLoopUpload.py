import PySimpleGUI as sg
import datetime
import time
import boto3
import os
import uuid
import glob
import pandas as pd
import json
import simrepsConfig
from shutil import copyfile

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

layout = [
            [sg.Frame(layout=[[sg.InputText('Set The Parent Directory'),sg.FolderBrowse(key='-FILE_LOCATION-')]],title='Parent Directory',title_color='orange')],
            [sg.Button('Start',button_color=('black','grey'),size=(10,2),font=("Courier",15, "bold italic"))],
            [sg.InputText('Button Will Appear Green When Finished')]
        ]

def uploadData(parentDirectory,subDirectories,upload):
    notUploaded=([])
    numberOfSubD = len(subDirectories)
    uploadCount = 1
    howMany = 0
    #startTime = time.time()
    for i in subDirectories:
        metaDataExists = os.path.exists(i+'metaDict.json')
        if metaDataExists:
            #print ('the metaDict filePath is',i+'metaDict.json')
            with open (i+'metaDict.json') as jsonFile:
                metaDict = json.load(jsonFile)
            nCheck = metaDict['userName']
            cdCheck = metaDict['dateCollected']
            icrCheck = metaDict['imageCollectionRate']
            fnCheck = metaDict['fileName']
            clCheck = metaDict['collectionLocation']
        else:
            nCheck = "Undefined"
            cdCheck = "Undefined"
            icrCheck = "Undefined"
            fnCheck = "Undefined"
            clCheck = "Undefined"

        print('the parent directory path is',parentDirectory)
        print('the current child directory path is', i)
        #print(i.split(parentDirectory))
        
        #new route for getting theSubDirectory.  This should stop a matching string in the string split 
        print('these images should load into a relative s3 subdirectory path of',i.split(parentDirectory)[1].replace('\\','/').replace(' ',''))
        theSubDirectory = (i.split(parentDirectory)[1].replace('\\','/').replace(' ',''))

        #old route for getting theSubDirectory
        #print(i.split(os.path.basename(parentDirectory)))
        #theSubDirectory = (i.split(os.path.basename(parentDirectory))[1].replace('\\','/').replace(' ',''))
        #print('the sub directory is',theSubDirectory)
        if nCheck!="Undefined" and cdCheck!="Undefined" and icrCheck !="Undefined" and fnCheck != "Undefined" and clCheck != "Undefined":
            #set upload dates
            theDateTime = datetime.datetime.now().strftime("%Y"+"%m"+"%d")+'/'+datetime.datetime.now().strftime("%H"+"%M")
            date = str(theDateTime[0:8])
            theTime = str(theDateTime[-4:])
            
            #define the exp uuid
            expUUID = uuid.uuid4()

            #append appropriate keys    
            metaDict['expUUID']=str(expUUID)
            metaDict['uploadDate']=str(date)
            metaDict['uploadTime']=str(theTime)
            metaDict['timeCollected']=str(date)+str(theTime)
            metaDict['stackKey'] = str(metaDict['collectionLocation']) + '/users/'+ str(metaDict['userName']) + '/rawData/' + str(metaDict['dateCollected'])  + theSubDirectory + str(metaDict['fileName']+'.tif')
            metaDict['fileKey'] = str(metaDict['collectionLocation']) + '/users/'+ str(metaDict['userName']) + '/rawData/' + str(metaDict['dateCollected'])  + theSubDirectory + str(metaDict['fileName']+'.tif')
            
            imgPathList = [f for f in glob.glob(i+'\\*.tif')]
            numImages = len(imgPathList)                
            for count,imgPath in enumerate(imgPathList):
                sg.OneLineProgressMeter('Uploading Sub Direc. ' + str(uploadCount) + ' of ' + str(numberOfSubD), count+1, numImages, 'key','Upload Metrics')
                imageFileName = os.path.basename(imgPath)
                fileSize = os.stat(imgPath)
                if ((fileSize.st_size/1e6) > 50):
                    print('I think ' + imageFileName +' is probably a stacked Image, so I am going to skip it')
                else:
                    imgUploadKey = str(metaDict['collectionLocation']) + '/users/'+ str(metaDict['userName']) + '/rawData/' + str(metaDict['dateCollected']) + theSubDirectory + str(imageFileName)
                    print(imgPath)
                    if upload==1:
                        s3.upload_file(Bucket=irelandBucket,Key=imgUploadKey,Filename=imgPath)              
            
            #upload the finalized metaData to the homeBucket.  It's important that the metaDict file does not go to ireland.
            with open(i+'uploadMetaDict.json','w') as outFile:
                json.dump(metaDict,outFile,indent=4)
            metaKey = str(metaDict['collectionLocation']) + '/users/'+ str(metaDict['userName']) + '/rawData/' + str(metaDict['dateCollected']) + theSubDirectory +'metaDict.json'    
            howMany+=1
            s3.upload_file(Bucket = homeBucket,Key=metaKey,Filename = i+'uploadMetaDict.json')

            #send a command to home ec2 to pull data from ireland then stack it.
            #create argument variables for the key to the data location adn the what the user wants the stackKey to be named
            downloadKey = str(metaDict['collectionLocation']) + '/users/'+ str(metaDict['userName']) + '/rawData/' + str(metaDict['dateCollected']) + theSubDirectory
            stackKey = metaDict['stackKey']
            print('the stack key is',stackKey)
            simrepsEnvCommand = 'source /home/ec2-user/venv/bin/activate'
            simrepsCommand = 'python3 createHaifaStack.py ' + " " + str(expUUID) + " " + '"' + downloadKey +'"' + " " + '"' + metaKey + '"' + " " + '"' + stackKey + '"'
            simrepsWorkingDirectory = '/home/ec2-user/aihub/LSG/advancedDevelopmentRD/projects/simreps/simrepsApp'
            ssm.send_command(
                                InstanceIds=['i-01c0b7f461672edbb'],
                                DocumentName='AWS-RunShellScript',
                                Parameters = {
                                    'commands':[simrepsEnvCommand,simrepsCommand],
                                    'workingDirectory':[simrepsWorkingDirectory]
                                },
                                CloudWatchOutputConfig={
                                    'CloudWatchLogGroupName':'SSMLogs',
                                    'CloudWatchOutputEnabled':True
                                }
                            )
            
        else: #the metaDataFile is missing or you did not define the four required meta data variables above
            notUploaded.append(theSubDirectory)
        uploadCount+=1
    if(howMany>0):
        print('just sent email command')
        simrepsEnvCommand = 'source /home/ec2-user/venv/bin/activate'
        simrepsCommand = 'python3 sendEmail.py ' + " " + '"' + str(metaDict['userName']) + '"' + " " + str(howMany)
        simrepsWorkingDirectory = '/home/ec2-user/aihub/LSG/advancedDevelopmentRD/projects/simreps/simrepsApp'
        ssm.send_command(
                            InstanceIds=['i-01c0b7f461672edbb'],
                            DocumentName='AWS-RunShellScript',
                            Parameters = {
                                'commands':[simrepsEnvCommand,simrepsCommand],
                                'workingDirectory':[simrepsWorkingDirectory]
                            },
                            CloudWatchOutputConfig={
                                'CloudWatchLogGroupName':'SSMLogs',
                                'CloudWatchOutputEnabled':True
                            }
                        )
    #endTime = time.time()
    #print('The upload to ' + bucket + ' required ' + str(round((endTime-startTime)/60, 2)) + ' minutes.')
    
    window.FindElement('Start').Update(button_color=('black', 'green'))

# Create the RealTime Upload Window
window = sg.Window('SiMREPS Loop Upload', layout) 

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
            for root, dirs, files in os.walk(parentDirectory):
                for file in files:
                    if file.endswith("metaDict.json"):
                        subDirectories.append(root+'\\')
            upload=1
            uploadData(parentDirectory,subDirectories,upload)

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break


window.close()