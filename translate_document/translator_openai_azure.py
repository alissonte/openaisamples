import requests
from bs4 import BeautifulSoup
from langchain_openai.chat_models.azure import AzureChatOpenAI

client = AzureChatOpenAI(
    azure_endpoint = "https://oai-dio-bootcamp-dev-eastus-ali.openai.azure.com/",
    api_key = "<secret>",
    api_version = "2024-02-15-preview",
    deployment_name = "gpt-4o-mini",
    max_retries = 0
)

def extract_text_from_url(url):
  response = requests.get(url)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    for script_or_style in soup(["script", "style"]):
      script_or_style.decompose()
    text = soup.get_text(separator=' ')
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
  else:
    raise Exception(f"Failed to fetch the URL. Status code: {response.status_code}")

  return text

def translate_article(text, lang):
  message = [
      ("system", "Voce atua como tradutor de textos"),
      ("user", f"Traduza o {text} para o idioma {lang} e responda em markdown")
  ]

  response = client.invoke(message)
  print(response.content)
  return response.content

translate_article("Let's see if the deployment was successed", "portugues")
extract_text_from_url("https://dev.to/bhagvank/open-ai-codex-playground-3l6e")