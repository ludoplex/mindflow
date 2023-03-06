![Alt text](images/MindFlowHeader.png)

Inspired by the need for a more efficient and intelligent way to search code, conversations, and documentation we created MindFlow, the search engine powered by ChatGPT.

## What it MindFlow
MindFlow allows users to generate an index of documents using a powerful language models to provide insightful responses to questions you may have about your data. It offers a selection of models to play around with with the ability to configure each model.

## Getting Started

Pre-requisite: You need to create an OpenAI API account, you can do so [here](https://openai.com/blog/openai-api).

1. Run `pip install mindflow`, or you can clone this repo and run `pip install -e path/to/mindflow`.
2. Run `mf login {OPENAI_API_KEY}`, you can find your openAI API key [here](https://platform.openai.com/account/api-keys).
3. Now you're ready to start using MindFlow!

## Basic Usage

MindFlow allows you to directly interface with chatGPT from the command line. Try it with:
- Run `mf ask "Hey, How's it going?"`

You can also ask questions about source code repositories. You can either clone the mindflow repository and cd into it, or you can try it on one of your own code repositories:
1. `mf index ./` 
    - To index the entire repo, this will go through all files recursively and generate search indexes for them.
    - :warning: Beware! Large code repositories may take a while and have a decent cost. It shouldn't be too expensive for normal repos, try it on a smaller one first.
2. `mf query ./ "Please summarize this repository."`
    - This will take the index you generated in the above step and use it as context for your question!

## Examples
1. Query
    - Clone this repo and run `mf index mindflow` to index the repo.
    - Run `mf query mindflow "How can I add a new command to this CLI tool? Please show code."` to query the repo.
    - Output to clipboard:

```
To add a new command to this CLI tool, you need to follow these steps:

1. Define a new command in the `Command` enum class.
2. Create a new function that implements the logic for the new command.
3. Add a new argument parser function for the new command.
4. Add a new `get_parsed_cli_args` case for the new command.
5. Update the `cli` function to include the new command in the parser.
6. Call the new function in the `match` statement in the `cli` function.

Here is an example of how to add a new command called `mycommand`:

1. Define a new command in the `Command` enum class:

class Command(Enum):
    ...
    MYCOMMAND = "mycommand"

2. Create a new function that implements the logic for the new command:

def mycommand():
    print("This is my new command!")

3. Add a new argument parser function for the new command:

def mycommand_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="This is my new command.",
    )
    return parser.parse_args(sys.argv[2:])

4. Add a new `get_parsed_cli_args` case for the new command:

def get_parsed_cli_args(command: str) -> argparse.Namespace:
    ...
    case Command.MYCOMMAND.value:
        return mycommand_args()
    ...

5. Update the `cli` function to include the new command in the parser:

def cli():
    parser = set_parser()
    args = parser.parse_args()

    command = Command[args.command].value
    args = get_parsed_cli_args(command)

    ...
    parser.add_argument(
        "command",
        choices=Command.__members__,
        help="The command to execute",
    )
    ...

6. Call the new function in the `match` statement in the `cli` function:

def cli():
    ...
    match command:
        ...
        case Command.MYCOMMAND.value:
            mycommand()
        ...
```

2. Diff
    - Run `mf diff` to summarize the changes in the repo.
    - Output to clipboard:


```
`mindflow/commands/diff.py` changes:
- Added import statement for `List` and `Tuple` from the `typing` module.
- Added a function `parse_git_diff` that takes in the output of a `git diff` command and returns a list of tuples containing the file name and the diff content.
- Added a function `batch_git_diffs` that takes in the list of tuples returned by `parse_git_diff` and batches them into smaller chunks of diffs that are less than 3000 characters long.
- Modified the `diff` function to use the new `parse_git_diff` and `batch_git_diffs` functions to batch the diffs and send them to the GPT model for processing.

`mindflow/commands/inspect.py` changes:
- Removed the `print` statement that was used to output the result of a database query.The git diff shows changes in two files: `mindflow/commands/diff.py` and `mindflow/commands/inspect.py`.

`mindflow/commands/diff.py` changes:
- Added import statement for `List` and `Tuple` from the `typing` module.
- Added a function `parse_git_diff` that takes in the output of a `git diff` command and returns a list of tuples containing the file name and the diff content.
- Added a function `batch_git_diffs` that takes in the list of tuples returned by `parse_git_diff` and batches them into smaller chunks of diffs that are less than 3000 characters long.
- Modified the `diff` function to use the new `parse_git_diff` and `batch_git_diffs` functions to batch the diffs and send them to the GPT model for processing.

`mindflow/commands/inspect.py` changes:
- Removed the `print` statement that was used to output the result of a database query.
```

## Recommended Use
While this tool is in beta, it is recommended to use the base models, but more will be added in the future. The base models are:
- Query: GPT 3.5 Turbo
- Index: GPT 3.5 Turbo
- Embedding: Text Embedding Ada 001

By running MF config, you can change the models used for each of these tasks. You can also configure the soft token limit. The soft token limit truncated the text to be sent to the GPT apis. When using the index, this means that your index summaries will be created over smaller chunks of texts, which can be useful, because it allows the query mechanism to more selectively choose chunks of text to return. This will also result in longer indexing times, and it will be more expensive, because more requests must be made. The soft token limit can also be configure for the final prompt, which is the query prompt. Fitting more text into the prompt can allow for more context to be used to generate the response, however, sometimes to much context impacts the quality of the response negatively.

## Setup
- **Python:**
    - `pip install mindflow`
    - Binding: mf

**Authenticating with MindFlow:**

- **OpenAI Auth**
    - Create an OpenAI account (https://beta.openai.com/signup)
    - Create an API key (https://beta.openai.com/account/api-keys)

- Once you have an authorization token:
    - Python: `mf config`

## How does it work?
This tool allows you to build an index of text documents and search through them using GPT-based embeddings. The tool takes document paths as input, extracts the text, splits the documents into chunks, summarizes them, and builds a summarization tree. The tool then uses this tree to generate embeddings of the indexed documents and your query, and selects the top text chunks based on the cosine similarity between these embeddings. The generated index can be saved to a JSON file for later reuse, making subsequent searches faster and cheaper.

## What's next for MindFlow
In the future, MindFlow plans on becoming an even more integral part of the modern developer's toolkit. We plan on adding the ability to ditch traditional documentation and instead integrate directly with your private documents and communication channels, allowing for a more seamless and intuitive experience. With MindFlow, you can have a true "stream of consciousness" with your code, documentation, and communication channels, making it easier than ever to stay on top of your projects and collaborate with your team. We are excited to continue pushing the boundaries of what's possible with language models and revolutionize the way developers work.
