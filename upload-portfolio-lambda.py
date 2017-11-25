import boto3, os
from botocore.client import Config
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):


    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-2:701127988230:portfolioTopic')

    location = {
        "bucketName": 'portfoliobuild.prototherian.com',
        "objectKey": 'portfoliobuild.zip'

    }

    try:
        job = event.get("CodePipeline.job")

        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "MyAppBuild":
                    location = artifact["location"]["s3Location"]

        print "Building portfolio from " + str(location)
        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
        #portfolio bucket
        p_bucket = s3.Bucket('portfolio.prototherian.com')
        #portfolio build bucket
        build_bucket = s3.Bucket(location['bucketName'])

        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj(location['objectKey'], portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                p_bucket.upload_fileobj(obj, nm,
                  ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                p_bucket.Object(nm).Acl().put(ACL='public-read')


        print "##Job Done"
        topic.publish(Subject="PortfolioUpdate", Message="Portfolio deployed successfully.")
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job['id'])
    except:
        topic.publish(Subject="PortfolioUpdate Failed", Message="The Portfolio was not deployed.")
        raise
    return 'Hello from Lambda'
