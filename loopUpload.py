import PySimpleGUI as sg
import datetime
import time
import boto3
import os
import uuid
import glob
import pandas as pd
import json
from shutil import copyfile
import simrepsConfig

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

layout = [
            [sg.Frame(layout=[[sg.InputText('Set The Parent Directory'),sg.FolderBrowse(key='-FILE_LOCATION-')]],title='Parent Directory',title_color='orange')],
            [sg.Button('Start',button_color=('black','grey'),size=(10,2),font=("Courier",15, "bold italic"))],
            [sg.InputText('Button Will Appear Green When Finished')]
        ]

def uploadData(parentDirectory,subDirectories,upload):
    notUploaded=([])
    numberOfSubD = len(subDirectories)
    #print(numberOfSubD)
    uploadCount = 1
    howMany = 0
    
    for i in subDirectories:
        metaDataExists = os.path.exists(i+'metaDict.json')
        #print(i,metaDataExists)
        #print(metaDataExists)
        #open the metaData
        if metaDataExists:
            print ('the metaDict filePath is',i+'metaDict.json')
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

        #old route for getting theSubDirectory.  This produces an error if the parent directory string is found in the child directory
        #theSubDirectory = (i.split(os.path.basename(parentDirectory))[1].replace('\\','/').replace(' ',''))
        #print('the old sub directory route is',theSubDirectory)
#        return True
        #theSubDirectory = os.path.basename(os.path.normpath(i))
        #print(nCheck,cdCheck,icrCheck,fnCheck,clCheck)
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
            #print('the stackKey = ',metaDict['stackKey'])
            imgPathList = [f for f in glob.glob(i+'\\*.tif')]
            numImages = len(imgPathList)
            #potential route for stopping upload if "Capture is not the baseName"
            #captureCount = 0
            #for i in imgPathList:
            #    imageFileName = os.path.basename(i)
            #    baseNameTest = imageFileName.startswith('Capture')
            #    if baseNameTest:
            #        captureCount += 1
            #print(captureCount)
            #if(captureCount==0):
            #    print(theSubDirectory + ' of images does not have images that are named properly and will not be uploaded')
            #    break
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
                        s3.upload_file(Bucket=bucket,Key=imgUploadKey,Filename=imgPath)
            
            #upload the finalized metaData
            with open(i+'uploadMetaDict.json','w') as outFile:
                json.dump(metaDict,outFile,indent=4)
            metaKey = str(metaDict['collectionLocation']) + '/users/'+ str(metaDict['userName']) + '/rawData/' + str(metaDict['dateCollected']) + theSubDirectory +'metaDict.json'
            
            if upload==1:
                howMany+=1
                #upload uploadMetaDict.json this has the stackKey
                s3.upload_file(Bucket = bucket,Key=metaKey,Filename = i+'uploadMetaDict.json')
                
                #prep command to be sent to ec2 instance - the command run scripts for stacking, creating data container and updating dynamos
                downloadKey = str(metaDict['collectionLocation']) + '/users/'+ str(metaDict['userName']) + '/rawData/' + str(metaDict['dateCollected']) + theSubDirectory
                #stackKey = str(metaDict['collectionLocation']) + '/users/'+ str(metaDict['userName']) + '/rawData/' + str(metaDict['dateCollected']) + theSubDirectory + str(metaDict['fileName']+'.tif') 
                stackKey = metaDict['stackKey']
                print('the stack key is',stackKey)
                simrepsEnvCommand = 'source /home/ec2-user/venv/bin/activate'
                simrepsCommand = 'python3 createStack.py ' + " " + str(expUUID) + " " + '"' + downloadKey +'"' + " " + '"' + metaKey + '"' + " " + '"' + stackKey + '"'
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
    #when the loopUploader finishes we need to send email. This needs to be controlled from iam policy located on backend only
    #print(notUploaded)
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
    for i in notUploaded:
        print('The tool did not upload folder',i)
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
            
            #subDirectories = glob.glob(FL+'/*/')
            #for i in range(len(subDirectories)):
            #    subDirectories[i] = subDirectories[i].replace('/','\\')
            #print(subDirectories)
            subDirectories=([])
            parentDirectory=FL.replace('/','\\')
            #print(parentDirectory)
            for root, dirs, files in os.walk(parentDirectory):
                for file in files:
                    if file.endswith("metaDict.json"):
                        #print(os.path.join(root, file))
                        #print(root+'\\')
                        subDirectories.append(root+'\\')
            upload=1
            #print(subDirectories)
            uploadData(parentDirectory,subDirectories,upload)

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break


window.close()