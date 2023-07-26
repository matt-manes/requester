# requester

Just a little command line `Requests` client.

## Installation

Install with:

<pre>
pip install git+https://github.com/matt-manes/requester
</pre>



## Usage

<pre>
>req -h
usage: req [-h] [-H [HEADERS ...]] [-p [PARAMS ...]] [-d [DATA ...]] [-sr] [-st] [-sb] [-dp] url [{delete,get,head,options,patch,post,put}]

positional arguments:
  url
  {delete,get,head,options,patch,post,put}
                        Request method, default is 'get'.

options:
  -h, --help            show this help message and exit
  -H [HEADERS ...], --headers [HEADERS ...]
                        By default, the only header is 'User-Agent' and the value is randomized. Use this to provide additional or override headers. Separate key and value with ':', i.e. 'Referer:https://somesite.com'
  -p [PARAMS ...], --params [PARAMS ...]
                        List of parameter key-value pairs. Separate key and value with ':'.
  -d [DATA ...], --data [DATA ...]
                        List of request body data key-value pairs. Separate key and value with ':'.
  -sr, --save_response  Save response to a .json file in the cwd.
  -st, --save_text      Save response text to an HTML file in the cwd.
  -sb, --save_bytes     Save response content as bytes to a file in the cwd.
  -dp, --dont_print     Don't print response to the terminal.
</pre>
