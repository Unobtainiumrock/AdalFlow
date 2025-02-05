from typing import Optional, Any, Callable, Literal
from openai.types import Completion
from adalflow.components.model_client.openai_client import OpenAIClient

BASE_URL = "https://api.mistral.ai/v1"


class MistralClient(OpenAIClient):
    __doc__ = r"""
    A minimal Mistral client that inherits from OpenAIClient.

    - Defaults to base_url=https://api.mistral.ai/v1
    - Pulls API key from MISTRAL_API_KEY if not supplied directly
    - Expects 'messages' or 'text' input format
    - Let the AdalFlow Generator specify actual model parameters
      (model, temperature, max_tokens, etc.) in one place.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = BASE_URL,
        input_type: Literal["text", "messages"] = "messages",
        env_api_key_name: str = "MISTRAL_API_KEY",
        chat_completion_parser: Callable[[Completion], Any] = None,
    ):
        """
        :param api_key: Mistral API key. If None, reads from env var MISTRAL_API_KEY.
        :param base_url: URL for Mistral’s endpoint.
                         Defaults to https://api.mistral.ai/v1
        :param input_type: Whether your input is 'text' or 'messages'.
        :param env_api_key_name: Name of environment variable for the Mistral API key.
        :param chat_completion_parser: Optional function to parse Mistral's responses.
        """

        super().__init__(
            api_key=api_key,
            chat_completion_parser=chat_completion_parser,
            input_type=input_type,
            base_url=base_url,
            env_api_key_name=env_api_key_name,
        )


if __name__ == "__main__":
    import os
    from adalflow.core import Generator
    from adalflow.utils import setup_env, get_logger

    get_logger(enable_file=False)
    setup_env()

    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"), input_type="messages")

    generator = Generator(
        model_client=client,
        model_kwargs={
            "model": "mistral-large-latest",
            "temperature": 0.7,
            "max_tokens": 2000,
        },
    )

    prompt_kwargs = {"input_str": "Explain the concept of machine learning."}

    response = generator(prompt_kwargs)

    if response.error:
        print(f"[Mistral] Generator Error: {response.error}")
    else:
        print(f"[Mistral] Response: {response.data}")
