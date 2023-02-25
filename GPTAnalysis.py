#Import open AI OS and System Modules
import openai,os,sys

api_key = "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"

prompt = "Summarize the following reviews into top 3 positive and negative qualities:\n"
openai.api_key = api_key

completions = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)

message = completions.choices[0].text
print(message)