from danoan.word_guru.cli.commands import copywriter, dictionary, translate, setup
from danoan.word_guru.cli import config

import argparse


def extend_parser(subcommand_action=None):
    command_name = "word-guru"
    description = "word-guru: your language expert"
    help = description

    if subcommand_action:
        parser = subcommand_action.add_parser(
            command_name,
            help=help,
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    else:
        parser = argparse.ArgumentParser(description)

    parser.add_argument(
        "--openai-key",
        help="The OpenAI key id used to authenticate requests to OpenAI API.",
    )
    parser.add_argument(
        "--cache-path",
        help="If specified, use this folder as cache. Otherwise, it uses the folder specified in the configuration file",
    )

    subparser_action = parser.add_subparsers()

    list_of_commands = [copywriter, dictionary, translate, setup]
    for command in list_of_commands:
        command.extend_parser(subparser_action)

    return parser


def main():
    config_file_params = {}
    try:
        configuration_file = config.get_configuration()
        config_file_params = configuration_file.__dict__
    except:
        pass

    parser = extend_parser()
    args = parser.parse_args()

    input_params = vars(args)
    for key, value in config_file_params.items():
        if key not in input_params:
            input_params[key] = value
        elif input_params[key] is None:
            input_params[key] = value

    if "func" in args:
        args.func(**input_params)
    elif "subcommand_help" in args:
        args.subcommand_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
