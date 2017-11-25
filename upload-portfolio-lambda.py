import boto3, os
from botocore.client import Config
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):


    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-2:701127988230:portfolioTopic')
    try:
        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
        #portfolio bucket
        p_bucket = s3.Bucket('portfolio.prototherian.com')
        #portfolio build bucket
        build_bucket = s3.Bucket('portfoliobuild.prototherian.com')

        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                p_bucket.upload_fileobj(obj, nm,
                  ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                p_bucket.Object(nm).Acl().put(ACL='public-read')


        print "##Job Done"
        topic.publish(Subject="PortfolioUpdate", Message="Portfolio deployed successfully.")
    except:
        topic.publish(Subject="PortfolioUpdate Failed", Message="The Portfolio was not deployed.")
        raise
    return 'Hello from Lambda'
