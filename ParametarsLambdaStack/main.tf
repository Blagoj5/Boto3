provider "aws" {
  region = "${var.region}"
}

resource "aws_s3_bucket" "b" {
  bucket = "buckettesparametars"
  acl    = "public-read"
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}
data "archive_file" "init" {
  type        = "zip"
  source_file = "./LambdaFunction.py"
  output_path = "./LambdaFunction.zip"
}

resource "aws_lambda_function" "test_lambda" {
  filename      = "LambdaFunction.zip"
  function_name = "${var.FunctionName}"
  role          = "${aws_iam_role.iam_for_lambda.arn}"
  handler       = "LambdaFunction.LambdaFunction"
  timeout       = "90"
  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  source_code_hash = "${data.archive_file.init.output_base64sha256}"
  runtime = "python3.7"
  # depends_on = ["aws_iam_role_policy_attachment.Attach", "aws_cloudwatch_log_group.lambdalogs"]
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.test_lambda.function_name}"
  principal     = "s3.amazonaws.com"  
  source_arn    = "${aws_s3_bucket.b.arn}"
}

resource "aws_iam_policy" "policy" {
  name        = "AllowS3toLambda"
  path        = "/"
  description = "PolicyForLambdaToAllowS3andLogging"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:*"
      ],
      "Effect": "Allow",
      "Resource": [
        "${aws_s3_bucket.b.arn}",
        "${aws_s3_bucket.b.arn}/*"
      ]
    },
     {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:us-east-1:*:*",
      "Effect": "Allow"
    },
     {
            "Effect": "Allow",
            "Action": [
                "cloudformation:CreateStack",
                "cloudformation:ValidateTemplate",
                "cloudformation:DeleteStack",
                "cloudformation:DescribeStacks",
                "cloudformation:ListStacks"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
              "ec2:*"
            ],
            "Resource": [
                "*"
            ]
        }
  ]
}
EOF
}


resource "aws_iam_role_policy_attachment" "Attach" {
  role       = "${aws_iam_role.iam_for_lambda.name}"
  policy_arn = "${aws_iam_policy.policy.arn}"
}

resource "aws_cloudwatch_log_group" "lambdalogs" {
  name = "/aws/lambda/${var.FunctionName}"
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = "${aws_s3_bucket.b.id}"

  lambda_function {
    lambda_function_arn = "${aws_lambda_function.test_lambda.arn}"
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".json"
  }
  depends_on  = ["aws_lambda_permission.allow_s3"]
}

