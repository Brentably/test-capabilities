from capabilities import llm
from typing import List, Tuple
import test
import json 
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows CORS for this specific origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
import uvicorn

@app.post("/")
async def get_results(request: Request):
  body = (await request.json())["data"]
  print(body)

  @llm
  def fuzzy_classifier(input: str, classifier_instructions: str, example_inputs: List[str] = [], example_labels: List[bool] = [], chain_of_thought: str = "") -> bool:
      """
      Classify the input according to the `classifier instructions`, the `example_inputs`, `example_labels`, and the `chain_of_thought` (if not empty).
      """
      ...

  def chain_of_thought(input: str, classifier_instructions: str) -> str:
    """
      You are ultimately tasked with classifying the `input` according to the `classifier_instructions`. First, write a bullet-pointed list of reasons why the `input` should be classified one way or the other according to the `classifier_instructions`.
    """
    return ""
  # with open('test.json') as test:
  # file = json.load(data)
  CLASSIFICATION_EXAMPLES: List[Tuple[str, any]] = body['cases']


  # if __name__ == "__main__":
  from concurrent.futures import ThreadPoolExecutor
  from concurrent import futures

  info = []
  labels_and_predictions: List[Tuple[any, any]] = []
  fs = []

  def _work(input, classifier_instructions, label):
    cot = chain_of_thought(input, classifier_instructions)
    return label, fuzzy_classifier(input=input, classifier_instructions=classifier_instructions, chain_of_thought=cot)
  with ThreadPoolExecutor(4) as pool:
    for example in CLASSIFICATION_EXAMPLES:
      fs.append(pool.submit(_work, input=example[0], classifier_instructions=body['prompt'], label=example[1]))
    from tqdm import tqdm
    for f_done in tqdm(futures.as_completed(fs), total=len(CLASSIFICATION_EXAMPLES)):
      label, prediction = f_done.result()
      labels_and_predictions.append((label, prediction))
      info.append({label: label, prediction: prediction, })
  print(labels_and_predictions)
  pass_rate = len([None for label, prediction in labels_and_predictions if label == prediction])/len(labels_and_predictions)

  print("PASS RATE: ", pass_rate)
  return [labels_and_predictions, pass_rate]
    # import json
    # print("LABELS AND PREDICTIONS: ", json.dumps(labels_and_predictions, indent=2))

    # print(fuzzy_classifier(input="Burn the jews.", classifier_instructions="Determine whether the message is toxic. Return `true` if the message is toxic and `false` otherwise."))