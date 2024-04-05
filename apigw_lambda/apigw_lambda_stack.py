from aws_cdk import (
    Duration,
    Stack,
    RemovalPolicy,
    # aws_sqs as sqs,
)
# from aws_cdk import core
from constructs import Construct
from aws_cdk import aws_iam as iam
import aws_cdk.aws_lambda as _lambda
import aws_cdk.aws_apigateway as apigw
import aws_cdk.aws_apigatewayv2 as apigw2
import aws_cdk.aws_cloudwatch as cloudwatch
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as route53_targets
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_cloudfront_origins as origins
# from aws_cdk import core as cdk


class ApigwLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        not_my_money_net = route53.HostedZone.from_lookup(
            self, 'HostedZone',
            domain_name='not-my-money.net',

        )

        # acm
        certificate = acm.DnsValidatedCertificate(
            self, 'Certificate',
            certificate_name='not-my-money.net',
            domain_name=not_my_money_net.zone_name,
            hosted_zone=not_my_money_net,
            region='us-east-1',
            validation=acm.CertificateValidation.from_dns(
                not_my_money_net,               
                ), # records are added to the zone automatically
            cleanup_route53_records=True, # default is True
        )

        #To automate the creation of a record in Route53 for ACM using AWS CDK

        # route53.CnameRecord(
        #     self, 'CnameRecord',
        #     zone=not_my_money_net,
        #     domain_name=not_my_money_net.zone_name,
        #     record_name='not-my-money.net',
        #     ttl=Duration.seconds(300),
        # )

        # api domain name options, api mapping
        domain_name_options = apigw.DomainNameOptions(
            certificate=certificate,
            domain_name=not_my_money_net.zone_name,
            # base_path=base_path,
            endpoint_type=apigw.EndpointType.EDGE,
            security_policy=apigw.SecurityPolicy.TLS_1_2,
        )
        # create a lambda function for get method
        # The code will be automatically uploaded to Lambda by the CDK
        get_lambda = _lambda.Function(self, "get_lambda",
                                      function_name="get_method_lambda",
                                      runtime=_lambda.Runtime.PYTHON_3_12,
                                      code=_lambda.Code.from_asset("lambda"),
                                      handler="get_method.lambda_handler"
                                      )
        
        # create a lambda function for post method
        # You have to pass the value of the body to the lambda function, such as: key=value or {"key": "value"} pair
        post_lambda = _lambda.Function(self, "post_lambda",
                                      function_name="post_method_lambda",
                                      runtime=_lambda.Runtime.PYTHON_3_12,
                                      code=_lambda.Code.from_asset("lambda"),
                                      handler="post_method.lambda_handler"
                                      )
        
        #3. Create an API Gateway
        #3.1 Create a REST API
        api = apigw.RestApi(self, "api",
                            rest_api_name="rest_api",
                            description="This is a rest api",
                            deploy=True,
                            endpoint_types=[apigw.EndpointType.REGIONAL],
                            deploy_options=apigw.StageOptions(
                                stage_name="dev",
                                logging_level=apigw.MethodLoggingLevel.INFO,
                                data_trace_enabled=True,
                                metrics_enabled=True,
                                tracing_enabled=True
                            ),
                            retain_deployments=False,
                            default_cors_preflight_options=apigw.CorsOptions(
                                allow_origins=apigw.Cors.ALL_ORIGINS,
                                allow_methods=apigw.Cors.ALL_METHODS
                            ),
                            default_method_options=apigw.MethodOptions(
                                authorization_type=apigw.AuthorizationType.NONE
                            ),
                            cloud_watch_role=True,
                            cloud_watch_role_removal_policy=RemovalPolicy.DESTROY,
                            # policy=iam.PolicyDocument(
                            #     statements=[
                            #         iam.PolicyStatement(
                            #             effect=iam.Effect.ALLOW,
                            #             principals=[iam.AnyPrincipal()],
                            #             actions=["execute-api:Invoke"],
                            #             resources=["execute-api:/*/*/*"],
                            #             conditions={
                            #                 "IpAddress": {
                            #                     "aws:SourceIp": ["83.221.156.201"]
                            #                 }
                            #             }
                            #         )
                            #     ])
                            )

        # # get method
        get_method = api.root.add_method(
            "GET", 
            apigw.LambdaIntegration(get_lambda),
            api_key_required=False,
            # request_parameters={
            #     "method.request.header.Content-Type": True
            # }
            )
        # post method
        post_method = api.root.add_method(
            "POST", 
            apigw.LambdaIntegration(post_lambda),
            api_key_required=True,
            request_parameters={
                "method.request.header.Content-Type": True
            }
            )

        # create usage plan
        plan = api.add_usage_plan("UsagePlan",
                                  name="usage_plan",
                                  description="This is a usage plan",
                                  api_stages=[apigw.UsagePlanPerApiStage(
                                      api=api,
                                      stage=api.deployment_stage
                                  )]
                                  )

        key = api.add_api_key("ApiKey")
        # associate the API key with the usage plan
        plan.add_api_key(key)

        # add tags to api_key
        # cfn = cdk.CfnTags(self, "Tags")
        # cfn.add_tags(key.key_id, {
        #     'Name': 'api_key',
        #     'Environment': 'dev'
        # })

        # create a cloudfront distribution and associate it with the apigateway        

        # # cloudfront dribution 
        cloudfrnt = cloudfront.Distribution(self, "cf",
                                            default_behavior=cloudfront.BehaviorOptions(  
                                                origin=origins.HttpOrigin(f"{api.rest_api_id}.execute-api.{self.region}.amazonaws.com",
                                                                           origin_path="/dev",
                                                                           protocol_policy=cloudfront.OriginProtocolPolicy.HTTPS_ONLY),
                                                # edge_lambdas=[cloudfront.EdgeLambda(
                                                #     function_version=get_lambda.current_version,
                                                #     event_type=cloudfront.LambdaEdgeEventType.ORIGIN_REQUEST
                                                # )],                                           
                                                allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
                                                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.ALLOW_ALL,
                                                cache_policy=cloudfront.CachePolicy.CACHING_DISABLED,
                                                origin_request_policy=cloudfront.OriginRequestPolicy.ALL_VIEWER_EXCEPT_HOST_HEADER,
                                                compress=True,
                                            ),
                                            certificate=certificate,
                                            domain_names=[not_my_money_net.zone_name],
                                            enable_logging=False,
                                            log_file_prefix="my-cloudfront-logs",
                                            ssl_support_method=cloudfront.SSLMethod.SNI,
                                            enabled=True,
                                            # log_retention=logs.RetentionDays.ONE_WEEK,
                                            # web_acl_id=web_acl.web_acl_id,
                                            # geo_restriction=cloudfront.GeoRestriction.allowlist("US", "GB"),
                                            http_version=cloudfront.HttpVersion.HTTP2,
                                            minimum_protocol_version=cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
                                            )
        # # create a record in route53, record type is A
        route53.ARecord(self, "AliasRecord",
                        zone=not_my_money_net,
                        target=route53.RecordTarget.from_alias(route53_targets.CloudFrontTarget(cloudfrnt)),
                        record_name="not-my-money.net",
                        ttl=Duration.seconds(300),
                        )