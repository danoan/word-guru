from danoan.word_guru.core import api, exception

import argparse
import logging
from pathlib import Path
import sys
from typing import Optional

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setStream(sys.stderr)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


def get_usage_examples(
    openai_key: str,
    cache_folder: Optional[str],
    word: str,
    language: str,
    *args,
    **kwargs,
):
    """
    Get common examples using the given word in the given language.
    """
    if cache_folder:
        cache_folder_path = Path(cache_folder)
        if not cache_folder_path.exists():
            logger.error(
                "The given cache folder does not exist. Create one before proceeding."
            )
            exit(1)

    try:
        print(api.get_usage_examples(openai_key, cache_folder_path, word, language))
    except exception.OpenAIEmptyResponse:
        logger.error("OpeanAI returned an empty response.")


def extend_parser(subcommand_action=None):
    command_name = "get-usage-examples"
    description = get_usage_examples.__doc__
    help = description.split(".")[0] if description else ""

    if subcommand_action:
        parser = subcommand_action.add_parser(
            command_name,
            help=help,
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    else:
        parser = argparse.ArgumentParser(
            command_name,
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

    parser.add_argument("word", help="The word you ask for usage examples.")
    parser.add_argument(
        "language", help="The IETF 639-3 code of the language. E.g. eng"
    )

    parser.set_defaults(func=get_usage_examples, subcommand_help=parser.print_help)

    return parser


def main():
    parser = extend_parser()

    args = parser.parse_args()
    if "func" in args:
        args.func(**vars(args))
    elif "subcommand_help" in args:
        args.subcommand_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
