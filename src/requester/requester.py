import argparse
from pathier import Pathier
import requests
from whosyouragent import get_agent
import re
import time
import json

root = Pathier(__file__).parent


def to_dict(items: list[str]) -> dict:
    """Convert a list of strings to a dictionary.

    Key-value pairs must be delimited with a `:`."""
    return {item[: item.find(":")]: item[item.find(":") + 1 :] for item in items}


def url_to_filestem(url: str) -> str:
    """Convert a url to a valid file stem with a timestamp."""
    return "_".join(
        chunk
        for chunk in (
            re.sub(r"[^a-zA-Z0-9]", "_", url) + "_" + str(int(time.time()))
        ).split("_")
        if chunk != ""
    )


def response_to_dict(response: requests.Response) -> dict:
    """Convert a `Response` object to a dictionary."""
    return {
        "Request": {
            "url": response.request.url,
            "full_url": response.request.url.strip("/") + response.request.path_url,
            "method": response.request.method,
            "headers": {
                header: value for header, value in response.request.headers.items()
            },
            "body": response.request.body,
        },
        "Response": {
            "url": response.url,
            "status_code": response.status_code,
            "reason": response.reason,
            "headers": {header: value for header, value in response.headers.items()},
            "text": response.text,
        },
    }


def dump_response(response: requests.Response) -> str:
    """Convert a `Response` object to a string."""
    return "\n".join(
        [
            "REQUEST:",
            f"Url: {response.request.url}",
            "",
            f"Full Url: {response.request.url.strip('/')}{response.request.path_url}",
            "",
            f"Method: {response.request.method}",
            "",
            "Headers:",
            "\n".join(
                f"{header}: {response.request.headers[header]}"
                for header in response.request.headers
            ),
            "",
            "Body:",
            f"{response.request.body}",
            "",
            "",
            "RESPONSE:",
            f"Url: {response.url}",
            "",
            f"Status Code: {response.status_code}",
            "",
            f"Reason: {response.reason}",
            "",
            "Headers:",
            "\n".join(
                f"{header}: {response.headers[header]}" for header in response.headers
            ),
            "",
            "text:",
            response.text,
        ]
    )


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("url", type=str)
    parser.add_argument(
        "method",
        nargs="?",
        default="get",
        type=str,
        choices=["delete", "get", "head", "options", "patch", "post", "put"],
        help=""" Request method, default is 'get'. """,
    )
    parser.add_argument(
        "-H",
        "--headers",
        nargs="*",
        type=str,
        default=[],
        help=""" By default, the only header is 'User-Agent' and the value is randomized.
        Use this to provide additional or override headers.
        Separate key and value with ':', i.e. 'Referer:https://somesite.com'""",
    )
    parser.add_argument(
        "-p",
        "--params",
        nargs="*",
        type=str,
        default=[],
        help=""" List of parameter key-value pairs. Separate key and value with ':'. """,
    )
    parser.add_argument(
        "-d",
        "--data",
        nargs="*",
        type=str,
        default=[],
        help=""" List of request body data key-value pairs. Separate key and value with ':'. """,
    )
    parser.add_argument(
        "-sr",
        "--save_response",
        action="store_true",
        help=""" Save response to a .json file in the cwd.""",
    )
    parser.add_argument(
        "-st",
        "--save_text",
        action="store_true",
        help=""" Save response text to an HTML file in the cwd. """,
    )
    parser.add_argument(
        "-sb",
        "--save_bytes",
        action="store_true",
        help=""" Save response content as bytes to a file in the cwd. """,
    )
    parser.add_argument(
        "-dp",
        "--dont_print",
        action="store_true",
        help=""" Don't print response to the terminal. """,
    )
    args = parser.parse_args()

    return args


def main(args: argparse.Namespace | None = None):
    if not args:
        args = get_args()
    for arg in ["headers", "params", "data"]:
        setattr(args, arg, to_dict(getattr(args, arg)))
    args.headers = get_agent(True) | args.headers
    try:
        response = requests.request(
            args.method,
            args.url,
            headers=args.headers,
            params=args.params,
            data=args.data,
        )
    except Exception as e:
        print("Failed to send request.")
        if input("Print traceback? (y/n) ") == "y":
            print(e)
    else:
        print(f"Status code: {response.status_code} - {response.reason}")
        print()
        # data = dump_response(response)
        data = response_to_dict(response)
        stem = url_to_filestem(
            response.request.url.strip("/") + response.request.path_url
        )
        if args.save_response:
            try:
                Pathier(f"{stem}.json").dumps(data, indent=2, encoding="utf-8")
            except Exception as e:
                print("Error saving .json file.")
                print(e)
        if args.save_text:
            try:
                Pathier(f"{stem}.html").write_text(response.text, encoding="utf-8")
            except Exception as e:
                print("Error saving .html file.")
                print(e)
        if args.save_bytes:
            try:
                Pathier(f"{stem}.bytes").write_bytes(response.content)
            except Exception as e:
                print("Error saving .bytes file.")
                print(e)
        if not args.dont_print:
            print(json.dumps(data, indent=1))
            print()
            print(f"Status code: {response.status_code} - {response.reason}")


if __name__ == "__main__":
    main(get_args())
