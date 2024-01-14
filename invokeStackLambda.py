import boto3
import json
import sys

AWS_ACCESS_KEY_ID="AKIATIENG4JLZKF4CWQU"
AWS_SECRET_ACCESS_KEY="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"

lambdaFunc = boto3.client('lambda',region_name='us-west-2',aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


def main(expHash,prefix,metaKey,stackKey):
    theDict = {}
    
    #prefix = downloadKey: where are the individual images located in s3
    #metaKey = full s3 key of metaDict.json 
    #stackKey = full s3 key of the stack image that is going to be created and placed in this location
    
    #create the event json
    theDict['expHash']=expHash
    theDict['prefix']=prefix
    theDict['metaKey']=metaKey
    theDict['stackKey']=stackKey
    
    #convert it to bytes to use in the boto3 client invoke
    dictToBytes = json.dumps(theDict).encode('utf-8')

    #invoke the lambda stacker
    lambdaFunc.invoke(FunctionName = 'arn:aws:lambda:us-west-2:223634448983:function:printName',
                    InvocationType='RequestResponse',
                    LogType = 'Tail',
                    Payload = dictToBytes,
                    )
   
    #print(Response)

if __name__=='__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
