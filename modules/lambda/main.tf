data "aws_iam_role" "lab_role" {
  name = "LabRole"
}

resource "aws_lambda_layer_version" "this" {
    layer_name          = "api_layer"
    compatible_runtimes = ["python3.12"]
    filename            = "${var.api_folder}/api_layer.zip"
    source_code_hash    = filebase64sha256("${var.api_folder}/api_layer.zip")
}

resource "aws_lambda_function" "this" {
    function_name    = var.name
    role             = data.aws_iam_role.lab_role.arn
    handler          = var.handler
    runtime          = "python3.12"
    filename         = "${var.api_folder}/${var.name}.zip"
    source_code_hash = filebase64sha256("${var.api_folder}/${var.name}.zip")
    layers           = [aws_lambda_layer_version.this.arn]

    environment {
        variables = var.env_vars
    }
}