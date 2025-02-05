from typing import Optional, Any, Callable, Literal
from openai.types import Completion

from adalflow.components.model_client.openai_client import OpenAIClient

BASE_URL = "https://api.x.ai/v1"


class XAIClient(OpenAIClient):
    __doc__ = r"""xAI's client is similar to OpenAIClient. It inherits OpenAIClient,
    and there is no overriding of methods necessary.

    References:
    - To get the API key, sign up at https://x.ai/
    - See https://docs.x.ai/docs/api-reference#list-models
    for more.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        chat_completion_parser: Callable[[Completion], Any] = None,
        input_type: Literal["text", "messages"] = "messages",
        base_url: str = BASE_URL,
        env_api_key_name: str = "XAI_API_KEY",
    ):
        super().__init__(
            api_key=api_key,
            chat_completion_parser=chat_completion_parser,
            input_type=input_type,
            base_url=base_url,
            env_api_key_name=env_api_key_name,
        )


if __name__ == "__main__":
    from adalflow.core import Generator
    from adalflow.utils import setup_env, get_logger

    get_logger(enable_file=False)

    setup_env()

    client = XAIClient()

    generator = Generator(
        model_client=client,
        model_kwargs={"model": "grok-2-latest", "temperature": 0, "stream": False},
    )

    prompt_kwargs = {
        "input": [
            {"role": "system", "content": "You are a test assistant."},
            {
                "role": "user",
                "content": "Testing. Just say hi and hello world and nothing else.",
            },
        ]
    }

    response = generator(prompt_kwargs)

    if response.error:
        print(f"[xAI] Generator Error: {response.error}")
    else:
        print(f"[xAI] Response: {response.data}")
