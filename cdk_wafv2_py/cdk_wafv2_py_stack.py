from aws_cdk import core as cdk

import aws_cdk.aws_wafv2 as waf

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class CdkWafv2PyStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        
        acl = waf.CfnWebACL
        
        # BlockQueriesContainingSubString via query_string
        
        custom_rule = acl.RuleProperty(
            name='BlockQueriesContainingSubString',
            priority=1,
            action=acl.RuleActionProperty(block={}),
            statement=acl.StatementProperty(
                byte_match_statement=acl.ByteMatchStatementProperty(
                    search_string='blockme',
                    field_to_match=acl.FieldToMatchProperty(single_header={'Name':'Referer'}),
                    positional_constraint='EXACTLY',
                    text_transformations=[
                        acl.TextTransformationProperty(priority=0, type='NONE'),
                    ],
                )
            ),
            visibility_config=acl.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                sampled_requests_enabled=True,
                metric_name='custom_rule',
            )
        )
        
        custom_rule2 = acl.RuleProperty(
            name='BlockQueriesContainingSubString2',
            priority=1,
            action=acl.RuleActionProperty(block={}),
            statement=acl.StatementProperty(
                byte_match_statement=acl.ByteMatchStatementProperty(
                    search_string='blockme',
                    field_to_match=acl.FieldToMatchProperty(single_header={'Name':'User-Agent'}),
                    positional_constraint='EXACTLY',
                    text_transformations=[
                        acl.TextTransformationProperty(priority=0, type='NONE'),
                    ],
                )
            ),
            visibility_config=acl.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                sampled_requests_enabled=True,
                metric_name='custom_rule2',
            )
        )
        
        
        
        
        web_acl = waf.CfnWebACL(
            self, 'WebACL',
            default_action=acl.DefaultActionProperty(allow={}),
            scope='REGIONAL',  # or use CLOUDFRONT if protecting a distribution
            visibility_config=acl.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name='webACL',
                sampled_requests_enabled=True
            ),
            name=f'test-acl',
            rules=[
                custom_rule,
                custom_rule2,
            ]
        )
